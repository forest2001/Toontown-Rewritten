# 2013.08.22 22:14:30 Pacific Daylight Time
# Embedded file name: direct.showbase.BufferViewer
__all__ = ['BufferViewer']
from pandac.PandaModules import *
from direct.task import Task
from direct.directnotify.DirectNotifyGlobal import *
from direct.showbase.DirectObject import DirectObject
import math

class BufferViewer(DirectObject):
    __module__ = __name__
    notify = directNotify.newCategory('BufferViewer')

    def __init__(self):
        self.enabled = 0
        self.sizex = 0
        self.sizey = 0
        self.position = 'lrcorner'
        self.layout = 'hline'
        self.include = 'all'
        self.exclude = 'none'
        self.cullbin = 'fixed'
        self.cullsort = 10000
        self.renderParent = render2d
        self.cards = []
        self.cardindex = 0
        self.cardmaker = CardMaker('cubemaker')
        self.cardmaker.setFrame(-1, 1, -1, 1)
        self.task = 0
        self.window = 0
        self.dirty = 1
        self.accept('render-texture-targets-changed', self.refreshReadout)
        if ConfigVariableBool('show-buffers', 0).getValue():
            self.enable(1)

    def refreshReadout(self):
        self.dirty = 1
        self.enable(self.enabled)

    def isValidTextureSet(self, x):
        if isinstance(x, list):
            for elt in x:
                if self.isValidTextureSet(elt) == 0:
                    return 0

        else:
            return x == 'all' or isinstance(x, Texture) or isinstance(x, GraphicsOutput)

    def isEnabled(self):
        return self.enabled

    def enable(self, x):
        if x != 0 and x != 1:
            BufferViewer.notify.error('invalid parameter to BufferViewer.enable')
            return
        self.enabled = x
        self.dirty = 1
        if x and self.task == 0:
            self.task = taskMgr.add(self.maintainReadout, 'buffer-viewer-maintain-readout', priority=1)

    def toggleEnable(self):
        self.enable(1 - self.enabled)

    def setCardSize(self, x, y):
        if x < 0 or y < 0:
            BufferViewer.notify.error('invalid parameter to BufferViewer.setCardSize')
            return
        self.sizex = x
        self.sizey = y
        self.dirty = 1

    def setPosition(self, pos):
        valid = ['llcorner',
         'lrcorner',
         'ulcorner',
         'urcorner',
         'window']
        if valid.count(pos) == 0:
            BufferViewer.notify.error('invalid parameter to BufferViewer.setPosition')
            BufferViewer.notify.error('valid parameters are: llcorner, lrcorner, ulcorner, urcorner, window')
            return
        if pos == 'window':
            BufferViewer.notify.error('BufferViewer.setPosition - "window" mode not implemented yet.')
            return
        self.position = pos
        self.dirty = 1

    def setLayout(self, lay):
        valid = ['vline',
         'hline',
         'vgrid',
         'hgrid',
         'cycle']
        if valid.count(lay) == 0:
            BufferViewer.notify.error('invalid parameter to BufferViewer.setLayout')
            BufferViewer.notify.error('valid parameters are: vline, hline, vgrid, hgrid, cycle')
            return
        self.layout = lay
        self.dirty = 1

    def selectCard(self, i):
        self.cardindex = i
        self.dirty = 1

    def advanceCard(self):
        self.cardindex += 1
        self.dirty = 1

    def setInclude(self, x):
        if self.isValidTextureSet(x) == 0:
            BufferViewer.notify.error('setInclude: must be list of textures and buffers, or "all"')
            return
        self.include = x
        self.dirty = 1

    def setExclude(self, x):
        if self.isValidTextureSet(x) == 0:
            BufferViewer.notify.error('setExclude: must be list of textures and buffers')
            return
        self.exclude = x
        self.dirty = 1

    def setSort(self, bin, sort):
        self.cullbin = bin
        self.cullsort = sort
        self.dirty = 1

    def setRenderParent(self, renderParent):
        self.renderParent = renderParent
        self.dirty = 1

    def analyzeTextureSet(self, x, set):
        if isinstance(x, list):
            for elt in x:
                self.analyzeTextureSet(elt, set)

        elif isinstance(x, Texture):
            set[x] = 1
        elif isinstance(x, GraphicsOutput):
            for itex in range(x.countTextures()):
                tex = x.getTexture(itex)
                set[tex] = 1

        elif isinstance(x, GraphicsEngine):
            for iwin in range(x.getNumWindows()):
                win = x.getWindow(iwin)
                self.analyzeTextureSet(win, set)

        elif x == 'all':
            self.analyzeTextureSet(base.graphicsEngine, set)
        else:
            return

    def makeFrame(self, sizex, sizey):
        format = GeomVertexFormat.getV3cp()
        vdata = GeomVertexData('card-frame', format, Geom.UHDynamic)
        vwriter = GeomVertexWriter(vdata, 'vertex')
        cwriter = GeomVertexWriter(vdata, 'color')
        ringoffset = [0,
         1,
         1,
         2]
        ringbright = [0,
         0,
         1,
         1]
        for ring in range(4):
            offsetx = ringoffset[ring] * 2.0 / float(sizex)
            offsety = ringoffset[ring] * 2.0 / float(sizey)
            bright = ringbright[ring]
            vwriter.addData3f(-1 - offsetx, 0, -1 - offsety)
            vwriter.addData3f(1 + offsetx, 0, -1 - offsety)
            vwriter.addData3f(1 + offsetx, 0, 1 + offsety)
            vwriter.addData3f(-1 - offsetx, 0, 1 + offsety)
            cwriter.addData3f(bright, bright, bright)
            cwriter.addData3f(bright, bright, bright)
            cwriter.addData3f(bright, bright, bright)
            cwriter.addData3f(bright, bright, bright)

        triangles = GeomTriangles(Geom.UHStatic)
        for i in range(2):
            delta = i * 8
            triangles.addVertices(0 + delta, 4 + delta, 1 + delta)
            triangles.addVertices(1 + delta, 4 + delta, 5 + delta)
            triangles.addVertices(1 + delta, 5 + delta, 2 + delta)
            triangles.addVertices(2 + delta, 5 + delta, 6 + delta)
            triangles.addVertices(2 + delta, 6 + delta, 3 + delta)
            triangles.addVertices(3 + delta, 6 + delta, 7 + delta)
            triangles.addVertices(3 + delta, 7 + delta, 0 + delta)
            triangles.addVertices(0 + delta, 7 + delta, 4 + delta)

        triangles.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(triangles)
        geomnode = GeomNode('card-frame')
        geomnode.addGeom(geom)
        return NodePath(geomnode)

    def maintainReadout(self, task):
        if self.dirty == 0:
            return Task.cont
        self.dirty = 0
        for card in self.cards:
            card.removeNode()

        self.cards = []
        if self.enabled == 0:
            self.task = 0
            return Task.done
        exclude = {}
        include = {}
        self.analyzeTextureSet(self.exclude, exclude)
        self.analyzeTextureSet(self.include, include)
        cards = []
        wins = []
        for iwin in range(base.graphicsEngine.getNumWindows()):
            win = base.graphicsEngine.getWindow(iwin)
            for itex in range(win.countTextures()):
                tex = win.getTexture(itex)
                if tex in include and tex not in exclude:
                    if tex.getTextureType() == Texture.TTCubeMap:
                        for face in range(6):
                            self.cardmaker.setUvRangeCube(face)
                            card = NodePath(self.cardmaker.generate())
                            card.setTexture(tex)
                            cards.append(card)

                    else:
                        card = win.getTextureCard()
                        card.setTexture(tex)
                        cards.append(card)
                    wins.append(win)
                    exclude[tex] = 1

        self.cards = cards
        if len(cards) == 0:
            self.task = 0
            return Task.done
        ncards = len(cards)
        if self.layout == 'hline':
            rows = 1
            cols = ncards
        elif self.layout == 'vline':
            rows = ncards
            cols = 1
        elif self.layout == 'hgrid':
            rows = int(math.sqrt(ncards))
            cols = rows
            if rows * cols < ncards:
                cols += 1
            if rows * cols < ncards:
                rows += 1
        elif self.layout == 'vgrid':
            rows = int(math.sqrt(ncards))
            cols = rows
            if rows * cols < ncards:
                rows += 1
            if rows * cols < ncards:
                cols += 1
        elif self.layout == 'cycle':
            rows = 1
            cols = 1
        else:
            BufferViewer.notify.error('shouldnt ever get here in BufferViewer.maintainReadout')
        aspectx = wins[0].getXSize()
        aspecty = wins[0].getYSize()
        for win in wins:
            if win.getXSize() * aspecty != win.getYSize() * aspectx:
                aspectx = 1
                aspecty = 1

        bordersize = 4.0
        if float(self.sizex) == 0.0 and float(self.sizey) == 0.0:
            sizey = int(0.4266666667 * base.win.getYSize())
            sizex = sizey * aspectx // aspecty
            v_sizey = (base.win.getYSize() - (rows - 1) - rows * 2) // rows
            v_sizex = v_sizey * aspectx // aspecty
            if v_sizey < sizey or v_sizex < sizex:
                sizey = v_sizey
                sizex = v_sizex
            adjustment = 2
            h_sizex = float(base.win.getXSize() - adjustment) / float(cols)
            h_sizex -= bordersize
            if h_sizex < 1.0:
                h_sizex = 1.0
            h_sizey = h_sizex * aspecty // aspectx
            if h_sizey < sizey or h_sizex < sizex:
                sizey = h_sizey
                sizex = h_sizex
        else:
            sizex = int(self.sizex * 0.5 * base.win.getXSize())
            sizey = int(self.sizey * 0.5 * base.win.getYSize())
            if sizex == 0:
                sizex = sizey * aspectx // aspecty
            if sizey == 0:
                sizey = sizex * aspecty // aspectx
        fsizex = 2.0 * sizex / float(base.win.getXSize())
        fsizey = 2.0 * sizey / float(base.win.getYSize())
        fpixelx = 2.0 / float(base.win.getXSize())
        fpixely = 2.0 / float(base.win.getYSize())
        if self.position == 'llcorner':
            dirx = -1.0
            diry = -1.0
        elif self.position == 'lrcorner':
            dirx = 1.0
            diry = -1.0
        elif self.position == 'ulcorner':
            dirx = -1.0
            diry = 1.0
        elif self.position == 'urcorner':
            dirx = 1.0
            diry = 1.0
        else:
            BufferViewer.notify.error('window mode not implemented yet')
        frame = self.makeFrame(sizex, sizey)
        for r in range(rows):
            for c in range(cols):
                index = c + r * cols
                if index < ncards:
                    index = (index + self.cardindex) % len(cards)
                    posx = dirx * (1.0 - (c + 0.5) * (fsizex + fpixelx * bordersize)) - fpixelx * dirx
                    posy = diry * (1.0 - (r + 0.5) * (fsizey + fpixely * bordersize)) - fpixely * diry
                    placer = NodePath('card-structure')
                    placer.setPos(posx, 0, posy)
                    placer.setScale(fsizex * 0.5, 1.0, fsizey * 0.5)
                    placer.setBin(self.cullbin, self.cullsort)
                    placer.reparentTo(self.renderParent)
                    frame.instanceTo(placer)
                    cards[index].reparentTo(placer)
                    cards[index] = placer

        return Task.cont
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\BufferViewer.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:31 Pacific Daylight Time
