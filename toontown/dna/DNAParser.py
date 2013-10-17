import ply.lex as lex
import sys, collections
from panda3d.core import PandaNode, NodePath
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
}
tokens += reserved.values()
t_QUOTED_STRING = r'["][^"]*["]'
t_ignore = ' \t'

literals = '[],'

def t_ignore_COMMENT(t):
    r'[/]{2,2}.*'

def t_ignore_ML_COMMENT(t):
    r'\/\*([^*]|[\r\n])*\*/'

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
    def ls(self):
        print 'DNASuitPoints:'
        for suitPoint in self.suitPoints:
            print '\t', suitPoint

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
        nodePath.attachNewNode(node, 0)
        for child in self.children:
            child.traverse(nodePath, dnaStorage, storeInStorage)

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
        parser.parse(stream.read())

class DNALoader:
    def __init__(self):
        node = PandaNode('dna')
        self.nodePath = NodePath(node)
        self.data = DNAData("loader_data")
    def buildGraph(self):
        '''Traverses the DNAGroup tree and builds a NodePath'''
        self.data.traverse(self.nodePath, self.data.getDnaStorage())
    def getData(self):
        return self.data
    

import ply.yacc as yacc

def p_dna(p):
    '''dna : dna object
            | object'''

def p_object(p):
    '''object : suitpoint
                | group'''
    p[0] = p[1]

def p_number(p):
    '''number : FLOAT
                | INTEGER'''
    p[0] = p[1]

def p_lpoint3f(p):
    '''lpoint3f : number number number'''
    p[0] = (p[1], p[2], p[3])

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
    '''visgroup : visgroupdef "[" vis subgroup_list "]"'''
    p[0] = p[1]
    p.parser.parentGroup = p[0].getParent()

def p_vis(p):
    '''vis : VIS "[" string "]"'''
    p.parser.parentGroup.addVisible(p[3])

def p_empty(p):
    '''empty : '''

def p_group(p):
    '''group : dnagroup
             | visgroup'''
    p[0] = p[1]

def p_suitedge(p):
    '''suitedge : SUIT_EDGE "[" number number "]"'''
    zoneId = p.parser.parentGroup.getName()
    p.parser.dnaStore.storeSuitEdge(p[2], p[3], zoneId)

def p_subgroup_opt(p):
    '''subgroup_list : subgroup_list group
                     | subgroup_list suitedge
                     | empty'''
    p[0] = p[1]
    if len(p) == 3:
        if isinstance(p[2], DNAGroup):
            p[0] += [p[2]]
    else:
        p[0] = []
