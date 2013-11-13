import ply.lex as lex
import sys, collections
from panda3d.core import PandaNode, NodePath, Filename, DecalEffect, TextNode, SceneGraphReducer, FontPool
from panda3d.core import LVector3f, LVector4f
from direct.showbase import Loader
import math
tokens = [
  'FLOAT',
  'INTEGER',
  'UNQUOTED_STRING',
  'QUOTED_STRING'
]
reserved = {
  'store_suit_point' : 'STORE_SUIT_POINT',
  'group' : 'GROUP',
  'visgroup' : 'VISGROUP',
  'vis' : 'VIS',
  'STREET_POINT' : 'STREET_POINT',
  'FRONT_DOOR_POINT' : 'FRONT_DOOR_POINT',
  'SIDE_DOOR_POINT' : 'SIDE_DOOR_POINT',
  'COGHQ_IN_POINT' : 'COGHQ_IN_POINT',
  'COGHQ_OUT_POINT' : 'COGHQ_OUT_POINT',
  'suit_edge' : 'SUIT_EDGE',
  'battle_cell' : 'BATTLE_CELL',
  'prop' : 'PROP',
  'pos' : 'POS',
  'hpr' : 'HPR',
  'scale' : 'SCALE',
  'code' : 'CODE',
  'color' : 'COLOR',
  'model' : 'MODEL',
  'store_node' : 'STORE_NODE',
  'sign' : 'SIGN',
  'baseline' : 'BASELINE',
  'width' : 'WIDTH',
  'height' : 'HEIGHT',
  'stomp' : 'STOMP',
  'stumble' : 'STUMBLE',
  'indent' : 'INDENT',
  'wiggle' : 'WIGGLE',
  'kern' : 'KERN',
  'text' : 'TEXT',
  'letters' : 'LETTERS',
  'store_font' : 'STORE_FONT',
  'flat_building' : 'FLAT_BUILDING',
  'wall' : 'WALL',
}
tokens += reserved.values()
t_ignore = ' \t'

literals = '[],'

def t_ignore_COMMENT(t):
    r'[/]{2,2}.*'

def t_ignore_ML_COMMENT(t):
    r'\/\*([^*]|[\r\n])*\*/'

def t_QUOTED_STRING(t):
    r'["][^"]*["]'
    t.value = t.value[1:-1]
    return t

def t_FLOAT(t):
    r'[+-]?\d+[.]\d*'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'[+-]?\d+'
    t.value = int(t.value)
    return t

def t_UNQUOTED_STRING(t):
    r'[^ \t\n\r\[\],"]+'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print 'Illegal character %s' % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()#TODO: set optimize=1 in preperation for mirai's shanenagens

def wl(file, ilevel, string):
    file.write('\t'*ilevel + string + '\n')

class DNAStorage:
    def __init__(self):
        self.suitPoints = []
        self.suitPointMap = {}
        self.DNAGroups = {}
        self.suitEdges = {}# stored as {startIndex : [edges]}
        self.battleCells = []
        self.nodes = {}
        self.fonts = {}
    def storeSuitPoint(self, suitPoint):
        if not isinstance(suitPoint, DNASuitPoint):
            raise TypeError("suit_point must be an instance of DNASuitPoint")
        self.suitPoints += [suitPoint]
        self.suitPointMap[suitPoint.getIndex()] = suitPoint
    def getSuitPointAtIndex(self, index):
        if index in self.suitPoints:
            return self.suitPoints[index]
        return None
    def getSuitPointWithIndex(self, index):
        if index in self.suitPointMap:
            return self.suitPointMap[index]
        return None
    def resetSuitPoints(self):
        self.suitPoints = []
        self.suitPointMap = {}
        self.suitEdges = {}
    def findDNAGroup(self, node):
        return DNAGroups[node]
    def removeDNAGroup(self, dnagroup):
        for node, group in self.DNAGroups.items():
            if group == dnagroup:
                del self.DNAGroups[node]
    def resetDNAGroups(self):
        self.DNAGroups = {}
    def storeSuitEdge(self, startIndex, endIndex, zoneId):
        startPoint = self.getSuitPointWithIndex(startIndex)
        endPoint = self.getSuitPointWithIndex(endIndex)
        if startPoint is None or endPoint is None:
            return
        if not startIndex in self.suitEdges:
            self.suitEdges[startIndex] = []
        self.suitEdges[startIndex] += [DNASuitEdge(startPoint, endPoint, zoneId)]
    def getSuitEdge(self, startIndex, endIndex):
        if not startIndex in self.suitEdges:
            return None
        for edge in self.suitEdges[startIndex]:
            if edge.getEndPoint().getIndex() == endIndex:
                return edge
        return None
    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)
    def storeBattleCell(self, cell):
        self.battleCells += [cell]
    def resetBattleCells(self):
        self.battleCells = []
    def findNode(self, code):
        if code in self.nodes:
            return self.nodes[code]
        return None
    def resetNodes(self):
        self.nodes = []
    def storeNode(self, node, code):
        self.nodes[code] = node
    def findFont(self, code):
        if code in self.fonts:
            return self.fonts[code]
        return None
    def resetFonts(self):
        self.fonts = {}
    def storeFont(self, font, code):
        self.fonts[code] = font
    def ls(self):
        print 'DNASuitPoints:'
        for suitPoint in self.suitPoints:
            print '\t', suitPoint
        print 'DNABattleCells:'
        for cell in self.battleCells:
            print '\t', cell

class DNASuitPoint:
    pointTypeMap = {
      'STREET_POINT' : 0,
      'FRONT_DOOR_POINT' : 1,
      'SIDE_DOOR_POINT' : 2,
      'COGHQ_IN_POINT' : 3,
      'COGHQ_OUT_POINT' : 4
    }
    ivPointTypeMap = {v: k for k, v in pointTypeMap.items()}
    def __init__(self, index, pointType, pos, landmarkBuildingIndex = -1):
        self.index = index
        self.pointType = pointType
        self.pos = pos
        self.graphId = 0
        self.landmarkBuildingIndex = landmarkBuildingIndex
    def __str__(self):
        pointTypeStr = ''#bring it into scope
        for k, v in DNASuitPoint.pointTypeMap.items():
            if v == self.pointType:
                pointTypeStr = k
        return 'DNASuitPoint index: ' + str(self.index) + ', pointType: ' + pointTypeStr + ', pos: ' + str(self.pos)
    def getIndex(self):
        return self.index
    def getGraphId(self):
        return self.graphId
    def getLandmarkBuildingIndex(self):
        return self.landmarkBuildingIndex
    def getPos(self):
        return self.pos
    def isTerminal(self):
        return self.pointType <= 2
    def setGraphId(self, id):
        self.graphId = id
    def setIndex(self, index):
        self.index = index
    def setLandmarkBuildingIndex(self, index):
        self.landmarkBuildingIndex = index
    def setPointType(self, type):
        if isinstance(type, int):
            if type in DNASuitPoint.ivPointTypeMap:
                self.pointType = type
            else:
                raise TypeError('%i is not a valid DNASuitPointType' % type)
        elif isinstance(type, str):
            if type in DNASuitPoint.pointTypeMap:
                self.pointType = DNASuitPoint.pointTypeMap[type]
            else:
                raise TypeError('%s is not a valid DNASuitPointType' % type)
    def setPos(self, pos):
        self.pos = pos

class DNABattleCell:
    def __init__(self, width, height, pos):
        self.width = width
        self.height = height
        self.pos = pos
    def __str__(self):
        return 'DNABattleCell width: ' + str(self.width) + ' height: ' + str(self.height) + ' pos: ' + str(self.pos)
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getPos(self):
        return self.pos
    def setWidthHeight(width, height):
        self.width = width
        self.height = height

class DNASuitEdge:
    def __init__(self, startpt, endpt, zoneId):
        self.startpt = startpt
        self.endpt = endpt
        self.zoneId = zoneId
    def getEndPoint(self):
        return self.endpt
    def getStartPoint(self):
        return seld.startpt
    def getZoneId(self):
        return self.zoneId
    def setZoneId(self, zoneId):
        self.zoneId = zoneId

class DNAGroup:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
    def add(self, child):
        self.children += [child]
    def at(self, index):
        return self.children[index]
    def clearParent(self):
        self.parent = None
    def getNumChildren(self):
        return len(self.children)
    def getParent(self):
        return self.parent
    def remove(self, child):
        self.children.remove(child)
    def setParent(self, parent):
        self.parent = parent
    def getName(self):
        return self.name
    def traverse(self, nodePath, dnaStorage):
        node = PandaNode(self.name)
        nodePath = nodePath.attachNewNode(node, 0)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNAVisGroup(DNAGroup):
    def __init__(self, name):
        DNAGroup.__init__(self,name)
        self.visibles = []
        self.suitEdges = []
        self.battleCells = []
    def addBattleCell(self, cell):
        self.battleCells += [cell]
    def addSuitEdge(self, edge):
        self.suitEdges += [edge]
    def addVisible(self, visible):
        self.visibles += [visible]
    def getBattleCell(self, index):
        return self.battleCells[index]
    def getNumBattleCells(self):
        return len(self.battleCells)
    def getNumSuitEdges(self):
        return len(self.suitEdges)
    def getNumVisibles(self):
        return len(self.visibles)
    def getSuitEdge(self, index):
        return self.suitEdges[index]
    def getVisibleName(self, index):
        return self.visibles[index]
    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)
    def removeSuitEdge(self, edge):
        self.suitEdges.remove(edge)
    def removeVisible(self, visible):
        self.visibles.remove(visible)

class DNAData(DNAGroup):
    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.coordSystem = 0
        self.dnaFilename = ''
        self.dnaStorage = None
    def getCoordSystem(self):
        return self.coordSystem
    def getDnaFilename(self):
        return self.dnaFilename
    def getDnaStorage(self):
        if self.dnaStorage is None:
            self.dnaStorage = DNAStorage()
        return self.dnaStorage
    def setCoordSystem(self, system):
        self.coordSystem = system
    def setDnaFilename(self, filename):
        self.dnaFilename = filename
    def setDnaStorage(self, storage):
        self.dnaStorage = storage
    def read(self, stream):
        parser = yacc.yacc(debug=1)#TODO: optimize->1 debug->0
        parser.dnaData = self
        parser.parentGroup = parser.dnaData
        parser.dnaStore = self.getDnaStorage()
        parser.nodePath = None
        parser.parse(stream.read())

class DNANode(DNAGroup):
    def __init__(self, name):
        DNAGroup.__init__(self, name)
        self.pos = LVector3f()
        self.hpr = LVector3f()
        self.scale = LVector3f(1,1,1)
    def getPos(self):
        return self.pos
    def getHpr(self):
        return self.hpr
    def getScale(self):
        return self.scale
    def setPos(self, pos):
        self.pos = pos
    def setHpr(self, hpr):
        self.hpr = hpr
    def setScale(self, scale):
        self.scale = scale
    def traverse(self, nodePath, dnaStorage):
        node = PandaNode(self.name)
        nodePath = nodePath.attachNewNode(node, 0).setPosHprScale(self.pos, self.hpr, self.scale)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNAProp(DNANode):
    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
    def setCode(self, code):
        self.code = code
    def setColor(self, color):
        self.color = color
    def getCode(self):
        return self.code
    def getColor(self):
        return self.color
    def traverse(self, nodePath, dnaStorage):
        if self.code == 'DCS':
            raise NotImplemented
        node = dnaStorage.findNode(self.code)
        if not node is None:
            nodePath = node.copyTo(nodePath, 0)
            nodePath.setPosHprScale(self.pos, self.hpr, self.scale)
            nodePath.setName(self.name)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNASign(DNANode):
    def __init__(self):
        DNANode.__init__(self, '')
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
    def setCode(self, code):
        self.code = code
    def setColor(self, color):
        self.color = color
    def getCode(self):
        return self.code
    def getColor(self):
        return self.color
    def traverse(self, nodePath, dnaStorage):
        decNode = nodePath.find('**/sign_decal')
        if decNode.isEmpty():
            decNode = nodePath.find('**/*_front')
        if decNode.isEmpty():
            decNode = nodePath.find('**/+GeomNode')
        decEffect = DecalEffect.make()
        decNode.setEffect(decEffect)
        node = None
        if self.code != '':
            node = dnaStorage.findNode(self.code)
            node = node.copyTo(decNode, 0)
            node.setName('sign')
        else:
            node = ModelNode('sign')
            node = decNode.attachNewNode(node, 0)
        node.setDepthWrite(False, 0)
        origin = nodePath.find('**/*sign_origin')
        node.setPosHprScale(origin, self.pos, self.hpr, self.scale)
        for child in self.children:
            child.traverse(node, dnaStorage)
        sgr = SceneGraphReducer()
        sgr.flatten(node.getNode(0), -1)

class DNASignBaseline(DNANode):
    def __init__(self):
        DNANode.__init__(self, '')
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)
        self.font = None
        self.height = 0.0
        self.counter = 0
        self.indent = 1.0
        self.kern = 1.0
        self.wiggle = 1.0
        self.stumble = 1.0
        self.stomp = 1.0
        self.width = 0
        self.height = 0
        self.angle = 0
        self.f104 = 0
    def getNextPosHprScale(self, pos, hpr, scale):
        wiggle = self.wiggle
        stomp = self.stomp
        if self.counter % 2 == 0:
            wiggle *= -1
            stomp *= -1
        sx, sy, sz = scale
        h, p, r = hpr
        x, y, z = pos
        sx *= self.scale[0]
        sy *= self.scale[1] 
        sz *= self.scale[2]
        #someone else can figure this shit out
        return ((x,y,z), (h,p,r), (sx, sy, sz))
    def setCode(self, code):
        self.code = code
    def setColor(self, color):
        self.color = color
    def getCode(self):
        return self.code
    def getColor(self):
        return self.color
    def getCurrentKern(self):
        return self.kern*self.counter
    def getCurrentStomp(self):
        return self.stomp*self.counter
    def getCurrentStumble(self):
        return self.stumble*self.counter
    def getCurrentWiggle(self):
        return self.wiggle*self.counter
    def getFont(self):
        return self.font
    def getHeight(self):
        return self.height
    def getIndent(self):
        return self.indent
    def getKern(self):
        return self.kern
    def getStomp(self):
        return self.stomp
    def getStumble(self):
        return self.stumble
    def getWidth(self):
        return self.width
    def getWiggle(self):
        return self.wiggle
    def incCounter(self):
        self.counter += 1
    def reset(self):
        self.counter = 0
    def resetCounter(self):
        self.counter = 0
    def setFont(self, font):
        self.font = font
    def setHeight(self, height):
        self.height = height
    def setIndent(self, indent):
        self.indent = indent
    def setKern(self, kern):
        self.kern = kern
    def setStomp(self, stomp):
        self.stomp = stomp
    def setStumble(self, stumble):
        self.stumble = stumble
    def setWidth(self, width):
        self.width = width
    def setWiggle(self, wiggle):
        self.wiggle = wiggle
    def traverse(self, nodePath, dnaStorage):
        nodePath = nodePath.attachNewNode('baseline', 0)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNASignText(DNANode):
    def __init__(self):
        DNANode.__init__(self, '')
        self.letters = ''
    def setLetters(self, letters):
        self.letters = letters
    def traverse(self, nodePath, dnaStorage):
        tn = TextNode('sign')
        tn.setText(self.letters)
        baseline = self.getParent()
        tn.setTextColor(baseline.getColor())
        tn.setTextScale(baseline.getScale()[0])
        tn.setFont(dnaStorage.findFont(baseline.getCode()))
        nodePath = nodePath.attachNewNode(tn.generate(), 0)
        pos, hpr, scale = baseline.getNextPosHprScale(self.pos, self.hpr, self.scale)
        nodePath.setPosHprScale(nodePath.getParent(), pos, hpr, scale)

class DNAFlatBuilding(DNANode): #TODO: finish me
    currentWallHeight = 0
    def __init__(self, name):
        DNANode.__init__(self, name)
    def getWidth(self):
        return self.width
    def setWidth(self, width):
        self.width = width
    def traverse(self, nodePath, dnaStorage):
        currentWallHeight = 0
        nodePath = nodePath.attachNewNode(self.name, 0)
        nodePath.attachNewNode(self.name + '-internal', 0)
        nodePath.setScale(self.scale)
        nodePath.setPosHpr(self.pos, self.hpr)
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNAWall(DNANode):
    def __init__(self, name):
        DNANode.__init__(self, name)
        self.code = ''
        self.height = 10
        self.color = LVector4f(1, 1, 1, 1)
    def getCode(self):
        return self.code
    def getColor(self):
        return self.color
    def getHeight(self):
        return self.height
    def setCode(self, code):
        self.code = code
    def setColor(self, color):
        self.color = color
    def setHeight(self, height):
        self.height = height
    def traverse(self, nodePath, dnaStorage):
        node = dnaStorage.findNode(self.code)
        if not node is None:
            nodePath = node.copyTo(nodePath, 0)
            self.pos.setZ(DNAFlatBuilding.currentWallHeight)
            self.scale.setZ(self.height)
            nodePath.setPosHprScale(self.pos, self.hpr, self.scale)
            nodePath.setColor(self.color)
        else:
            raise KeyError('DNAWall code ' + self.code + ' not found in DNAStorage')#Should this be a keyerror or something else?
        for child in self.children:
            child.traverse(nodePath, dnaStorage)

class DNALoader:
    def __init__(self):
        node = PandaNode('dna')
        self.nodePath = NodePath(node)
        self.data = DNAData("loader_data")
    def buildGraph(self):
        '''Traverses the DNAGroup tree and builds a NodePath'''
        self.data.traverse(self.nodePath, self.data.getDnaStorage())
        return self.nodePath.getChild(0).getChild(0)
    def getData(self):
        return self.data
    

import ply.yacc as yacc

def p_dna(p):
    '''dna : dna object
            | object'''

def p_object(p):
    '''object : suitpoint
              | group
              | model
              | font'''
    p[0] = p[1]

def p_number(p):
    '''number : FLOAT
                | INTEGER'''
    p[0] = p[1]

def p_lpoint3f(p):
    '''lpoint3f : number number number'''
    p[0] = LVector3f(p[1], p[2], p[3])

def p_suitpoint(p):
    '''suitpoint : STORE_SUIT_POINT "[" number "," suitpointtype "," lpoint3f "]"'''
    p.parser.dnaStore.storeSuitPoint(DNASuitPoint(p[3], p[5], p[7]))

def p_suitpointtype(p):
    '''suitpointtype : STREET_POINT
                      | FRONT_DOOR_POINT
                      | SIDE_DOOR_POINT
                      | COGHQ_IN_POINT
                      | COGHQ_OUT_POINT'''
    p[0] = DNASuitPoint.pointTypeMap[p[1]]

def p_string(p):
    '''string : QUOTED_STRING
                | UNQUOTED_STRING'''
    p[0] = p[1]

def p_dnagroupdef(p):
    '''dnagroupdef : GROUP string'''
    print "New group: ", p[2]
    p[0] = DNAGroup(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_visgroupdef(p):
    '''visgroupdef : VISGROUP string'''
    print "New visgroup: ", p[2]
    p[0] = DNAVisGroup(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_dnagroup(p):
    '''dnagroup : dnagroupdef "[" subgroup_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_visgroup(p):
    '''visgroup : visgroupdef "[" subvisgroup_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_vis(p):
    '''vis : VIS "[" string "]"'''
    p.parser.parentGroup.addVisible(p[3])

def p_empty(p):
    '''empty : '''

def p_group(p):
    '''group : dnagroup
             | visgroup
             | dnanode'''
    p[0] = p[1]

def p_dnanode(p):
    '''dnanode : prop
               | sign
               | signbaseline
               | signtext
               | flatbuilding
               | wall'''
    p[0] = p[1]

def p_sign(p):
    '''sign : signdef "[" subprop_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_prop(p):
    '''prop : propdef "[" subprop_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_signbaseline(p):
    '''signbaseline : baselinedef "[" subbaseline_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_signtest(p):
    '''signtext : signtextdef "[" subtext_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()
    
def p_flatbuilding(p):
    '''flatbuilding : flatbuildingdef "[" subflatbuilding_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_wall(p):
    '''wall : walldef "[" subwall_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_propdef(p):
    '''propdef : PROP string'''
    print "New prop: ", p[2]
    p[0] = DNAProp(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_flatbuildingdef(p):
    '''flatbuildingdef : FLAT_BUILDING string'''
    print "New DNAFlatBuilding: ", p[2]
    p[0] = DNAFlatBuilding(p[2])
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_walldef(p):
    '''walldef : WALL'''
    print 'New DNAWall'
    p[0] = DNAWall('')
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_signdef(p):
    '''signdef : SIGN'''
    print 'New DNASign'
    p[0] = DNASign()
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_baselinedef(p):
    '''baselinedef : BASELINE'''
    print 'New DNASignBaseline'
    p[0] = DNASignBaseline()
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_signtextdef(p):
    '''signtextdef : TEXT'''
    print 'New DNASignText'
    p[0] = DNASignText()
    p.parser.parentGroup.add(p[0])
    p[0].setParent(p.parser.parentGroup)
    p.parser.parentGroup = p[0]

def p_suitedge(p):
    '''suitedge : SUIT_EDGE "[" number number "]"'''
    zoneId = p.parser.parentGroup.getName()
    p.parser.dnaStore.storeSuitEdge(p[2], p[3], zoneId)

def p_battlecell(p):
    '''battlecell : BATTLE_CELL "[" number number lpoint3f "]"'''
    p[0] = DNABattleCell(p[3], p[4], p[5])
    p.parser.dnaStore.storeBattleCell(p[0])
    p.parser.parentGroup.addBattleCell(p[0])

def p_subgroup_list(p):
    '''subgroup_list : subgroup_list group
                     | empty'''
    p[0] = p[1]
    if len(p) == 3:
        p[0] += [p[2]]
    else:
        p[0] = []

def p_subvisgroup_list(p):
    '''subvisgroup_list : subvisgroup_list group
                     | subvisgroup_list suitedge
                     | subvisgroup_list battlecell
                     | subvisgroup_list vis
                     | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []

def p_pos(p):
    '''pos : POS "[" lpoint3f "]"'''
    p.parser.parentGroup.setPos(p[3])

def p_hpr(p):
    '''hpr : HPR "[" lpoint3f "]"'''
    p.parser.parentGroup.setHpr(p[3])

def p_scale(p):
    '''scale : SCALE "[" lpoint3f "]"'''
    p.parser.parentGroup.setScale(p[3])

def p_dnanode_subs(p):
    '''dnanode_sub : group
                   | pos
                   | hpr
                   | scale'''
    p[0] = p[1]

def p_dnaprop_sub(p):
    '''dnaprop_sub : code
                   | color'''
    p[0] = p[1]

def p_baseline_sub(p):
    '''baseline_sub : code
                | color
                | width
                | height
                | indent
                | kern
                | stomp
                | stumble
                | wiggle'''
    p[0] = p[1]

def p_text_sub(p):
    '''text_sub : letters'''
    p[0] = p[1]

def p_flatbuilding_sub(p):
    '''flatbuilding_sub : width'''
    p[0] = p[1]

def p_wall_sub(p):
    '''wall_sub : height
                | code
                | color'''
    p[0] = p[1]

def p_letters(p):
    '''letters : LETTERS "[" string "]"'''
    p.parser.parentGroup.setLetters(p[3])

def p_width(p):
    '''width : WIDTH "[" number "]"'''
    p.parser.parentGroup.setWidth(p[3])

def p_height(p):
    '''height : HEIGHT "[" number "]"'''
    p.parser.parentGroup.setHeight(p[3])

def p_stomp(p):
    '''stomp : STOMP "[" number "]"'''
    p.parser.parentGroup.setStomp(p[3])

def p_indent(p):
    '''indent : INDENT "[" number "]"'''
    p.parser.parentGroup.setIndent(p[3])

def p_kern(p):
    '''kern : KERN "[" number "]"'''
    p.parser.parentGroup.setKern(p[3])

def p_stumble(p):
    '''stumble : STUMBLE "[" number "]"'''
    p.parser.parentGroup.setStumble(p[3])

def p_wiggle(p):
    '''wiggle : WIGGLE "[" number "]"'''
    p.parser.parentGroup.setWiggle(p[3])

def p_code(p):
    '''code : CODE "[" string "]"'''
    p.parser.parentGroup.setCode(p[3])

def p_color(p):
    '''color : COLOR "[" number number number number "]"'''
    p.parser.parentGroup.setColor((p[3],p[4],p[5],p[6]))

def p_subprop_list(p):
    '''subprop_list : subprop_list dnanode_sub
                    | subprop_list dnaprop_sub
                    | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []

def p_subbaseline_list(p):
    '''subbaseline_list : subbaseline_list dnanode_sub
                        | subbaseline_list baseline_sub
                        | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []

def p_subtext_list(p):
    '''subtext_list : subtext_list dnanode_sub
                    | subtext_list text_sub
                    | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []


def p_subflatbuilding_list(p):
    '''subflatbuilding_list : subflatbuilding_list dnanode_sub
                            | subflatbuilding_list flatbuilding_sub
                            | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []

def p_subwall_list(p):
    '''subwall_list : subwall_list dnanode_sub
                    | subwall_list wall_sub
                    | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []

def p_modeldef(p):
    '''modeldef : MODEL string'''
    filename = Filename(p[2])
    filename.setExtension('bam')
    loader = Loader.Loader(None)
    p.parser.nodePath = loader.loadModel(filename)

def p_model(p):
    '''model : modeldef "[" modelnode_list "]"'''

def p_modelnode_list(p):
    '''modelnode_list : modelnode_list node
                      | empty'''

def p_node(p):
    '''node : STORE_NODE "[" string string "]"
            | STORE_NODE "[" string string string "]"'''
    nodePath = None
    if len(p) == 6:
        nodePath = p.parser.nodePath.find('**/' + p[4])
    else:
        nodePath = p.parser.nodePath.find('**/' + p[5])
    nodePath.setTag('DNACode', p[4])
    nodePath.setTag('DNARoot', p[3])
    p.parser.dnaStore.storeNode(nodePath, p[4])

def p_font(p):
    '''font : STORE_FONT "[" string string string "]"'''
    filename = Filename(p[5])
    filename.setExtension('bam')
    p.parser.dnaStore.storeFont(FontPool.loadFont(filename.cStr()), p[4])