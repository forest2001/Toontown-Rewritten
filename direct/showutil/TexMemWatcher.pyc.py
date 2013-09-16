# 2013.08.22 22:14:50 Pacific Daylight Time
# Embedded file name: direct.showutil.TexMemWatcher
from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import math
import copy

class TexMemWatcher(DirectObject):
    __module__ = __name__
    NextIndex = 1
    StatusHeight = 20

    def __init__(self, gsg = None, limit = None):
        DirectObject.__init__(self)
        self.name = 'tex-mem%s' % TexMemWatcher.NextIndex
        TexMemWatcher.NextIndex += 1
        self.cleanedUp = False
        self.top = 1.0
        self.quantize = 1
        self.maxHeight = base.config.GetInt('tex-mem-max-height', 300)
        self.totalSize = 0
        self.placedSize = 0
        self.placedQSize = 0
        if gsg is None:
            gsg = base.win.getGsg()
        elif isinstance(gsg, GraphicsOutput):
            gsg = gsg.getGsg()
        self.gsg = gsg
        size = ConfigVariableInt('tex-mem-win-size', '300 300')
        origin = ConfigVariableInt('tex-mem-win-origin', '100 100')
        self.winSize = (size[0], size[1])
        name = 'Texture Memory'
        props = WindowProperties()
        props.setOrigin(origin[0], origin[1])
        props.setSize(*self.winSize)
        props.setTitle(name)
        props.setFullscreen(False)
        props.setUndecorated(False)
        fbprops = FrameBufferProperties.getDefault()
        flags = GraphicsPipe.BFFbPropsOptional | GraphicsPipe.BFRequireWindow
        self.pipe = None
        moduleName = base.config.GetString('tex-mem-pipe', '')
        if moduleName:
            self.pipe = base.makeModulePipe(moduleName)
        if not self.pipe:
            self.pipe = base.pipe
        self.win = base.graphicsEngine.makeOutput(self.pipe, name, 0, fbprops, props, flags)
        self.win.setSort(10000)
        self.win.setClearColorActive(False)
        self.win.setClearDepthActive(False)
        eventName = '%s-window' % self.name
        self.win.setWindowEvent(eventName)
        self.accept(eventName, self.windowEvent)
        self.accept('graphics_memory_limit_changed', self.graphicsMemoryLimitChanged)
        self.mouse = base.dataRoot.attachNewNode(MouseAndKeyboard(self.win, 0, '%s-mouse' % self.name))
        bt = ButtonThrower('%s-thrower' % self.name)
        self.mouse.attachNewNode(bt)
        bt.setPrefix('button-%s-' % self.name)
        self.accept('button-%s-mouse1' % self.name, self.mouseClick)
        self.setupGui()
        self.setupCanvas()
        self.background = None
        self.nextTexRecordKey = 0
        self.rollover = None
        self.isolate = None
        self.isolated = None
        self.needsRepack = False
        updateInterval = base.config.GetDouble('tex-mem-update-interval', 0.5)
        self.task = taskMgr.doMethodLater(updateInterval, self.updateTextures, 'TexMemWatcher')
        self.setLimit(limit)
        return

    def setupGui(self):
        self.render2d = NodePath('render2d')
        self.render2d.setDepthTest(False)
        self.render2d.setDepthWrite(False)
        self.render2d.setTwoSided(True)
        self.render2d.setBin('unsorted', 0)
        dr = self.win.makeDisplayRegion()
        cam = Camera('cam2d')
        self.lens = OrthographicLens()
        self.lens.setNearFar(-1000, 1000)
        self.lens.setFilmSize(2, 2)
        cam.setLens(self.lens)
        np = self.render2d.attachNewNode(cam)
        dr.setCamera(np)
        self.aspect2d = self.render2d.attachNewNode('aspect2d')
        cm = CardMaker('statusBackground')
        cm.setColor(0.85, 0.85, 0.85, 1)
        cm.setFrame(0, 2, 0, 2)
        self.statusBackground = self.render2d.attachNewNode(cm.generate(), -1)
        self.statusBackground.setPos(-1, 0, -1)
        self.status = self.aspect2d.attachNewNode('status')
        self.statusText = TextNode('statusText')
        self.statusText.setTextColor(0, 0, 0, 1)
        self.statusTextNP = self.status.attachNewNode(self.statusText)
        self.statusTextNP.setScale(1.5)
        self.sizeText = TextNode('sizeText')
        self.sizeText.setTextColor(0, 0, 0, 1)
        self.sizeText.setAlign(TextNode.ARight)
        self.sizeText.setCardAsMargin(0.25, 0, 0, -0.25)
        self.sizeText.setCardColor(0.85, 0.85, 0.85, 1)
        self.sizeTextNP = self.status.attachNewNode(self.sizeText)
        self.sizeTextNP.setScale(1.5)

    def setupCanvas(self):
        self.canvasRoot = NodePath('canvasRoot')
        self.canvasRoot.setDepthTest(False)
        self.canvasRoot.setDepthWrite(False)
        self.canvasRoot.setTwoSided(True)
        self.canvasRoot.setBin('unsorted', 0)
        self.canvas = self.canvasRoot.attachNewNode('canvas')
        self.canvasDR = self.win.makeDisplayRegion()
        self.canvasDR.setSort(-10)
        cam = Camera('cam2d')
        self.canvasLens = OrthographicLens()
        self.canvasLens.setNearFar(-1000, 1000)
        cam.setLens(self.canvasLens)
        np = self.canvasRoot.attachNewNode(cam)
        self.canvasDR.setCamera(np)
        self.mw = MouseWatcher('%s-watcher' % self.name)
        self.mw.setDisplayRegion(self.canvasDR)
        mwnp = self.mouse.attachNewNode(self.mw)
        eventName = '%s-enter' % self.name
        self.mw.setEnterPattern(eventName)
        self.accept(eventName, self.enterRegion)
        eventName = '%s-leave' % self.name
        self.mw.setLeavePattern(eventName)
        self.accept(eventName, self.leaveRegion)
        p = PNMImage(2, 2, 1)
        p.setGray(0, 0, 0.4)
        p.setGray(1, 1, 0.4)
        p.setGray(0, 1, 0.75)
        p.setGray(1, 0, 0.75)
        self.checkTex = Texture('checkTex')
        self.checkTex.load(p)
        self.checkTex.setMagfilter(Texture.FTNearest)
        self.canvasBackground = None
        self.makeCanvasBackground()
        return

    def makeCanvasBackground(self):
        if self.canvasBackground:
            self.canvasBackground.removeNode()
        self.canvasBackground = self.canvasRoot.attachNewNode('canvasBackground', -100)
        cm = CardMaker('background')
        cm.setFrame(0, 1, 0, 1)
        cm.setUvRange((0, 0), (1, 1))
        self.canvasBackground.attachNewNode(cm.generate())
        cm.setFrame(0, 1, 1, self.top)
        cm.setUvRange((0, 1), (1, self.top))
        bad = self.canvasBackground.attachNewNode(cm.generate())
        bad.setColor((0.8, 0.2, 0.2, 1))
        self.canvasBackground.setTexture(self.checkTex)

    def setLimit(self, limit = None):
        self.__doSetLimit(limit)
        self.reconfigureWindow()

    def __doSetLimit(self, limit):
        self.limit = limit
        self.lruLimit = False
        self.dynamicLimit = False
        if not limit:
            lruSize = self.gsg.getPreparedObjects().getGraphicsMemoryLimit()
            if lruSize and lruSize < 2 ** 32 - 1:
                self.limit = lruSize
                self.lruLimit = True
            else:
                self.dynamicLimit = True
        if self.dynamicLimit:
            self.limit = Texture.upToPower2(self.totalSize)
        self.win.getGsg().getPreparedObjects().setGraphicsMemoryLimit(self.limit)
        top = 1.25
        if self.dynamicLimit:
            top = 1
        if top != self.top:
            self.top = top
            self.makeCanvasBackground()
        self.canvasLens.setFilmSize(1, self.top)
        self.canvasLens.setFilmOffset(0.5, self.top / 2.0)

    def cleanup(self):
        if not self.cleanedUp:
            self.cleanedUp = True
            base.graphicsEngine.removeWindow(self.win)
            self.win = None
            self.gsg = None
            self.pipe = None
            self.mouse.detachNode()
            taskMgr.remove(self.task)
            self.ignoreAll()
            self.canvas.getChildren().detach()
            self.texRecordsByTex = {}
            self.texRecordsByKey = {}
            self.texPlacements = {}
        return

    def graphicsMemoryLimitChanged(self):
        if self.dynamicLimit or self.lruLimit:
            self.__doSetLimit(None)
            self.reconfigureWindow()
        return

    def windowEvent(self, win):
        if win == self.win:
            props = win.getProperties()
            if not props.getOpen():
                self.cleanup()
                return
            size = (props.getXSize(), props.getYSize())
            if size != self.winSize:
                self.winSize = size
                self.reconfigureWindow()

    def enterRegion(self, region, buttonName):
        key, pi = map(int, region.getName().split(':'))
        tr = self.texRecordsByKey.get(key)
        if not tr:
            return
        self.setRollover(tr, pi)

    def leaveRegion(self, region, buttonName):
        key, pi = map(int, region.getName().split(':'))
        tr = self.texRecordsByKey.get(key)
        if tr != self.rollover:
            return
        self.setRollover(None, None)
        return

    def mouseClick(self):
        if self.isolate:
            self.isolateTexture(None)
            return
        if self.rollover:
            self.isolateTexture(self.rollover)
        return

    def setRollover(self, tr, pi):
        self.rollover = tr
        if self.rollover:
            self.statusText.setText(tr.tex.getName())
        else:
            self.statusText.setText('')

    def isolateTexture(self, tr):
        if self.isolate:
            self.isolate.removeNode()
            self.isolate = None
        self.isolated = tr
        self.canvas.show()
        self.canvasBackground.clearColor()
        self.win.getGsg().setTextureQualityOverride(Texture.QLDefault)
        if hasattr(self.gsg, 'clearFlashTexture'):
            self.gsg.clearFlashTexture()
        if not tr:
            return
        self.canvas.hide()
        self.canvasBackground.setColor(1, 1, 1, 1, 1)
        self.win.getGsg().setTextureQualityOverride(Texture.QLBest)
        if hasattr(self.gsg, 'setFlashTexture'):
            self.gsg.setFlashTexture(tr.tex)
        self.isolate = self.render2d.attachNewNode('isolate')
        wx, wy = self.winSize
        tn = TextNode('tn')
        tn.setText('%s\n%s x %s\n%s' % (tr.tex.getName(),
         tr.tex.getXSize(),
         tr.tex.getYSize(),
         self.formatSize(tr.size)))
        tn.setAlign(tn.ACenter)
        tn.setCardAsMargin(100.0, 100.0, 0.1, 0.1)
        tn.setCardColor(0.1, 0.2, 0.4, 1)
        tnp = self.isolate.attachNewNode(tn)
        scale = 30.0 / wy
        tnp.setScale(scale * wy / wx, scale, scale)
        tnp.setPos(render2d, 0, 0, -1 - tn.getBottom() * scale)
        labelTop = tn.getHeight() * scale
        tw = tr.tex.getXSize()
        th = tr.tex.getYSize()
        wx = float(wx)
        wy = float(wy) * (2.0 - labelTop) * 0.5
        w = min(tw, wx)
        h = min(th, wy)
        sx = w / tw
        sy = h / th
        s = min(sx, sy)
        w = tw * s / float(self.winSize[0])
        h = th * s / float(self.winSize[1])
        cx = 0.0
        cy = 1.0 - (2.0 - labelTop) * 0.5
        l = cx - w
        r = cx + w
        b = cy - h
        t = cy + h
        cm = CardMaker('card')
        cm.setFrame(l, r, b, t)
        c = self.isolate.attachNewNode(cm.generate())
        c.setTexture(tr.tex)
        c.setTransparency(TransparencyAttrib.MAlpha)
        ls = LineSegs('frame')
        ls.setColor(0, 0, 0, 1)
        ls.moveTo(l, 0, b)
        ls.drawTo(r, 0, b)
        ls.drawTo(r, 0, t)
        ls.drawTo(l, 0, t)
        ls.drawTo(l, 0, b)
        self.isolate.attachNewNode(ls.create())
        return

    def reconfigureWindow(self):
        wx, wy = self.winSize
        if wx <= 0 or wy <= 0:
            return
        self.aspect2d.setScale(float(wy) / float(wx), 1, 1)
        statusScale = float(self.StatusHeight) / float(wy)
        self.statusBackground.setScale(1, 1, statusScale)
        self.status.setScale(statusScale)
        self.statusTextNP.setPos(self.statusBackground, 0, 0, 0.5)
        self.sizeTextNP.setPos(self.statusBackground, 2, 0, 0.5)
        self.canvasDR.setDimensions(0, 1, statusScale, 1)
        w = self.canvasDR.getPixelWidth()
        h = self.canvasDR.getPixelHeight()
        self.canvasBackground.setTexScale(TextureStage.getDefault(), w / 20.0, h / (20.0 * self.top))
        if self.isolate:
            self.needsRepack = True
            self.isolateTexture(self.isolated)
        else:
            self.repack()

    def updateTextures(self, task):
        if self.isolate:
            return task.again
        if self.needsRepack:
            self.needsRepack = False
            self.repack()
            return task.again
        pgo = self.gsg.getPreparedObjects()
        totalSize = 0
        texRecords = []
        neverVisited = copy.copy(self.texRecordsByTex)
        for tex in self.gsg.getPreparedTextures():
            if tex in neverVisited:
                del neverVisited[tex]
            size = 0
            if tex.getResident(pgo):
                size = tex.getDataSizeBytes(pgo)
            tr = self.texRecordsByTex.get(tex, None)
            if size:
                totalSize += size
                active = tex.getActive(pgo)
                if not tr:
                    key = self.nextTexRecordKey
                    self.nextTexRecordKey += 1
                    tr = TexRecord(key, tex, size, active)
                    texRecords.append(tr)
                else:
                    tr.setActive(active)
                    if tr.size != size or not tr.placements:
                        tr.setSize(size)
                        self.unplaceTexture(tr)
                        texRecords.append(tr)
            elif tr:
                self.unplaceTexture(tr)

        for tex, tr in neverVisited.items():
            self.unplaceTexture(tr)
            del self.texRecordsByTex[tex]
            del self.texRecordsByKey[tr.key]

        self.totalSize = totalSize
        self.sizeText.setText(self.formatSize(self.totalSize))
        if totalSize > self.limit and self.dynamicLimit:
            self.repack()
        else:
            overflowCount = sum(map(lambda tp: tp.overflowed, self.texPlacements.keys()))
            if totalSize <= self.limit and overflowCount:
                self.repack()
            else:
                texRecords.sort(key=lambda tr: (tr.tw, tr.th), reverse=True)
                for tr in texRecords:
                    self.placeTexture(tr)
                    self.texRecordsByTex[tr.tex] = tr
                    self.texRecordsByKey[tr.key] = tr

        return task.again

    def repack(self):
        self.canvas.getChildren().detach()
        self.texRecordsByTex = {}
        self.texRecordsByKey = {}
        self.texPlacements = {}
        self.bitmasks = []
        self.mw.clearRegions()
        self.setRollover(None, None)
        self.w = 1
        self.h = 1
        self.placedSize = 0
        self.placedQSize = 0
        pgo = self.gsg.getPreparedObjects()
        totalSize = 0
        for tex in self.gsg.getPreparedTextures():
            if tex.getResident(pgo):
                size = tex.getDataSizeBytes(pgo)
                if size:
                    active = tex.getActive(pgo)
                    key = self.nextTexRecordKey
                    self.nextTexRecordKey += 1
                    tr = TexRecord(key, tex, size, active)
                    self.texRecordsByTex[tr.tex] = tr
                    self.texRecordsByKey[tr.key] = tr
                    totalSize += size

        self.totalSize = totalSize
        self.sizeText.setText(self.formatSize(self.totalSize))
        if not self.totalSize:
            return
        if self.dynamicLimit or self.lruLimit:
            self.__doSetLimit(None)
        x, y = self.winSize
        y /= self.top
        r = float(y) / float(x)
        w = math.sqrt(self.limit) / math.sqrt(r)
        h = w * r
        if h > self.maxHeight:
            self.quantize = int(math.ceil(h / self.maxHeight))
        else:
            self.quantize = 1
        w = max(int(w / self.quantize + 0.5), 1)
        h = max(int(h / self.quantize + 0.5), 1)
        self.w = w
        self.h = h
        self.area = self.w * self.h
        self.bitmasks = []
        for i in range(self.h):
            self.bitmasks.append(BitArray())

        self.canvas.setScale(1.0 / w, 1.0, 1.0 / h)
        self.mw.setFrame(0, w, 0, h * self.top)
        texRecords = self.texRecordsByTex.values()
        texRecords.sort(key=lambda tr: (tr.tw, tr.th), reverse=True)
        for tr in texRecords:
            self.placeTexture(tr)

        return

    def formatSize(self, size):
        if size < 1000:
            return '%s bytes' % size
        size /= 1024.0
        if size < 1000:
            return '%0.1f kb' % size
        size /= 1024.0
        if size < 1000:
            return '%0.1f MB' % size
        size /= 1024.0
        return '%0.1f GB' % size

    def unplaceTexture(self, tr):
        if tr.placements:
            for tp in tr.placements:
                tp.clearBitmasks(self.bitmasks)
                if not tp.overflowed:
                    self.placedQSize -= tp.area
                del self.texPlacements[tp]

            tr.placements = []
            tr.clearCard(self)
            if not tr.overflowed:
                self.placedSize -= tr.size
        tr.overflowed = 0

    def placeTexture(self, tr):
        tr.computePlacementSize(self)
        tr.overflowed = 0
        shouldFit = False
        availableSize = self.limit - self.placedSize
        if availableSize >= tr.size:
            shouldFit = True
            availableQSize = self.area - self.placedQSize
            if availableQSize < tr.area:
                tr.area = availableQSize
        if shouldFit:
            tp = self.findHole(tr.area, tr.w, tr.h)
            if tp:
                texCmp = cmp(tr.w, tr.h)
                holeCmp = cmp(tp.p[1] - tp.p[0], tp.p[3] - tp.p[2])
                if texCmp != 0 and holeCmp != 0 and texCmp != holeCmp:
                    tp.rotated = True
                tr.placements = [tp]
                tr.makeCard(self)
                tp.setBitmasks(self.bitmasks)
                self.placedQSize += tp.area
                self.texPlacements[tp] = tr
                self.placedSize += tr.size
                return
            tpList = self.findHolePieces(tr.area)
            if tpList:
                texCmp = cmp(tr.w, tr.h)
                tr.placements = tpList
                for tp in tpList:
                    holeCmp = cmp(tp.p[1] - tp.p[0], tp.p[3] - tp.p[2])
                    if texCmp != 0 and holeCmp != 0 and texCmp != holeCmp:
                        tp.rotated = True
                    tp.setBitmasks(self.bitmasks)
                    self.placedQSize += tp.area
                    self.texPlacements[tp] = tr

                self.placedSize += tr.size
                tr.makeCard(self)
                return
        tr.overflowed = 1
        tp = self.findOverflowHole(tr.area, tr.w, tr.h)
        tp.overflowed = 1
        while len(self.bitmasks) <= tp.p[3]:
            self.bitmasks.append(BitArray())

        tr.placements = [tp]
        tr.makeCard(self)
        tp.setBitmasks(self.bitmasks)
        self.texPlacements[tp] = tr

    def findHole(self, area, w, h):
        if area == 0:
            tp = TexPlacement(0, 0, 0, 0)
            return tp
        w, h = max(w, h), min(w, h)
        aspect = float(w) / float(h)
        holes = self.findAvailableHoles(area, w, h)
        matches = []
        for tarea, tp in holes:
            l, r, b, t = tp.p
            tw = r - l
            th = t - b
            if tw < w:
                nh = min(area / tw, th)
                th = nh
            elif th < h:
                nw = min(area / th, tw)
                tw = nw
            else:
                tw = w
                th = h
            tp = TexPlacement(l, l + tw, b, b + th)
            ta = float(max(tw, th)) / float(min(tw, th))
            if ta == aspect:
                return tp
            match = min(ta, aspect) / max(ta, aspect)
            matches.append((match, tp))

        if matches:
            return max(matches)[1]
        return None

    def findHolePieces(self, area):
        savedTexPlacements = copy.copy(self.texPlacements)
        savedBitmasks = []
        for ba in self.bitmasks:
            savedBitmasks.append(BitArray(ba))

        result = []
        while area > 0:
            tp = self.findLargestHole()
            if not tp:
                break
            l, r, b, t = tp.p
            tpArea = (r - l) * (t - b)
            if tpArea >= area:
                shorten = (tpArea - area) / (r - l)
                t -= shorten
                tp.p = (l,
                 r,
                 b,
                 t)
                tp.area = (r - l) * (t - b)
                result.append(tp)
                self.texPlacements = savedTexPlacements
                self.bitmasks = savedBitmasks
                return result
            area -= tpArea
            result.append(tp)
            tp.setBitmasks(self.bitmasks)
            self.texPlacements[tp] = None

        self.texPlacements = savedTexPlacements
        self.bitmasks = savedBitmasks
        return

    def findLargestHole(self):
        holes = self.findAvailableHoles(0)
        if holes:
            return max(holes)[1]
        return None

    def findAvailableHoles(self, area, w = None, h = None):
        holes = []
        lastTuples = set()
        lastBitmask = None
        b = 0
        while b < self.h:
            bm = self.bitmasks[b]
            if bm == lastBitmask:
                b += 1
                continue
            lastBitmask = bm
            tuples = self.findEmptyRuns(bm)
            newTuples = tuples.difference(lastTuples)
            for l, r in newTuples:
                mask = BitArray.range(l, r - l)
                t = b + 1
                while t < self.h and (self.bitmasks[t] & mask).isZero():
                    t += 1

                tpw = r - l
                tph = t - b
                tarea = tpw * tph
                if tarea >= area:
                    tp = TexPlacement(l, r, b, t)
                    if w and h and (tpw >= w and tph >= h or tph >= w and tpw >= h):
                        return [(tarea, tp)]
                    holes.append((tarea, tp))

            lastTuples = tuples
            b += 1

        return holes

    def findOverflowHole(self, area, w, h):
        if w > self.w:
            b = len(self.bitmasks)
            while b > self.h and self.bitmasks[b - 1].isZero():
                b -= 1

            tp = TexPlacement(0, w, b, b + h)
            return tp
        lastTuples = set()
        lastBitmask = None
        b = self.h
        while True:
            if b >= len(self.bitmasks):
                tp = TexPlacement(0, w, b, b + h)
                return tp
            bm = self.bitmasks[b]
            if bm == lastBitmask:
                b += 1
                continue
            lastBitmask = bm
            tuples = self.findEmptyRuns(bm)
            newTuples = tuples.difference(lastTuples)
            for l, r in newTuples:
                if r - l < w:
                    continue
                r = l + w
                mask = BitArray.range(l, r - l)
                t = b + 1
                while t < b + h and (t >= len(self.bitmasks) or (self.bitmasks[t] & mask).isZero()):
                    t += 1

                if t < b + h:
                    continue
                tp = TexPlacement(l, r, b, t)
                return tp

            lastTuples = tuples
            b += 1

        return

    def findEmptyRuns(self, bm):
        tuples = set()
        l = bm.getLowestOffBit()
        if l < self.w:
            r = bm.getNextHigherDifferentBit(l)
            if r == l or r >= self.w:
                r = self.w
            tuples.add((l, r))
            l = bm.getNextHigherDifferentBit(r)
            while l != r and l < self.w:
                r = bm.getNextHigherDifferentBit(l)
                if r == l or r >= self.w:
                    r = self.w
                tuples.add((l, r))
                l = bm.getNextHigherDifferentBit(r)

        return tuples


class TexRecord():
    __module__ = __name__

    def __init__(self, key, tex, size, active):
        self.key = key
        self.tex = tex
        self.active = active
        self.root = None
        self.regions = []
        self.placements = []
        self.overflowed = 0
        self.setSize(size)
        return

    def setSize(self, size):
        self.size = size
        x = self.tex.getXSize()
        y = self.tex.getYSize()
        r = float(y) / float(x)
        self.tw = math.sqrt(self.size) / math.sqrt(r)
        self.th = self.tw * r

    def computePlacementSize(self, tmw):
        self.w = max(int(self.tw / tmw.quantize + 0.5), 1)
        self.h = max(int(self.th / tmw.quantize + 0.5), 1)
        self.area = self.w * self.h

    def setActive(self, flag):
        self.active = flag
        if self.active:
            self.backing.clearColor()
            self.matte.clearColor()
            self.card.clearColor()
        else:
            self.backing.setColor((0.2, 0.2, 0.2, 1), 2)
            self.matte.setColor((0.2, 0.2, 0.2, 1), 2)
            self.card.setColor((0.4, 0.4, 0.4, 1), 2)

    def clearCard(self, tmw):
        if self.root:
            self.root.detachNode()
            self.root = None
        for r in self.regions:
            tmw.mw.removeRegion(r)

        self.regions = []
        return

    def makeCard(self, tmw):
        self.clearCard(tmw)
        root = NodePath('root')
        matte = root.attachNewNode('matte', 0)
        backing = root.attachNewNode('backing', 10)
        card = root.attachNewNode('card', 20)
        frame = root.attachNewNode('frame', 30)
        for p in self.placements:
            l, r, b, t = p.p
            cx = (l + r) * 0.5
            cy = (b + t) * 0.5
            shrinkMat = Mat4.translateMat(-cx, 0, -cy) * Mat4.scaleMat(0.9) * Mat4.translateMat(cx, 0, cy)
            cm = CardMaker('backing')
            cm.setFrame(l, r, b, t)
            cm.setColor(0.1, 0.3, 0.5, 1)
            c = backing.attachNewNode(cm.generate())
            c.setMat(shrinkMat)
            cm = CardMaker('card')
            cm.setFrame(l, r, b, t)
            if p.rotated:
                cm.setUvRange((0, 1), (0, 0), (1, 0), (1, 1))
            c = card.attachNewNode(cm.generate())
            c.setMat(shrinkMat)
            cm = CardMaker('matte')
            cm.setFrame(l, r, b, t)
            matte.attachNewNode(cm.generate())
            ls = LineSegs('frame')
            ls.setColor(0, 0, 0, 1)
            ls.moveTo(l, 0, b)
            ls.drawTo(r, 0, b)
            ls.drawTo(r, 0, t)
            ls.drawTo(l, 0, t)
            ls.drawTo(l, 0, b)
            f1 = frame.attachNewNode(ls.create())
            f2 = f1.copyTo(frame)
            f2.setMat(shrinkMat)

        self.matte = matte
        self.backing = backing
        card.setTransparency(TransparencyAttrib.MAlpha)
        card.setTexture(self.tex)
        self.card = card
        self.frame = frame
        root.reparentTo(tmw.canvas)
        self.root = root
        for pi in range(len(self.placements)):
            p = self.placements[pi]
            r = MouseWatcherRegion(('%s:%s' % (self.key, pi)), *p.p)
            tmw.mw.addRegion(r)
            self.regions.append(r)


class TexPlacement():
    __module__ = __name__

    def __init__(self, l, r, b, t):
        self.p = (l,
         r,
         b,
         t)
        self.area = (r - l) * (t - b)
        self.rotated = False
        self.overflowed = 0

    def intersects(self, other):
        ml, mr, mb, mt = self.p
        tl, tr, tb, tt = other.p
        return tl < mr and tr > ml and tb < mt and tt > mb

    def setBitmasks(self, bitmasks):
        l, r, b, t = self.p
        mask = BitArray.range(l, r - l)
        for yi in range(b, t):
            bitmasks[yi] |= mask

    def clearBitmasks(self, bitmasks):
        l, r, b, t = self.p
        mask = ~BitArray.range(l, r - l)
        for yi in range(b, t):
            bitmasks[yi] &= mask

    def hasOverlap(self, bitmasks):
        l, r, b, t = self.p
        mask = BitArray.range(l, r - l)
        for yi in range(b, t):
            if not (bitmasks[yi] & mask).isZero():
                return True

        return False
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showutil\TexMemWatcher.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:52 Pacific Daylight Time
