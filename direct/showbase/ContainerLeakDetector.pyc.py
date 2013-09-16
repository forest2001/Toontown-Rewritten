# 2013.08.22 22:14:31 Pacific Daylight Time
# Embedded file name: direct.showbase.ContainerLeakDetector
from pandac.PandaModules import PStatCollector
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import Queue, invertDictLossless, makeFlywheelGen
from direct.showbase.PythonUtil import itype, serialNum, safeRepr, fastRepr
from direct.showbase.Job import Job
import types, weakref, random, __builtin__

def _createContainerLeak():

    def leakContainer(task = None):
        base = getBase()
        if not hasattr(base, 'leakContainer'):
            base.leakContainer = {}

        class LeakKey():
            __module__ = __name__

        base.leakContainer[LeakKey()] = {}
        if random.random() < 0.01:
            key = random.choice(base.leakContainer.keys())
            ContainerLeakDetector.notify.debug('removing reference to leakContainer key %s so it will be garbage-collected' % safeRepr(key))
            del base.leakContainer[key]
        taskMgr.doMethodLater(10, leakContainer, 'leakContainer-%s' % serialNum())
        if task:
            return task.done

    leakContainer()
    return


def _createTaskLeak():
    leakTaskName = uniqueName('leakedTask')
    leakDoLaterName = uniqueName('leakedDoLater')

    def nullTask(task = None):
        return task.cont

    def nullDoLater(task = None):
        return task.done

    def leakTask(task = None, leakTaskName = leakTaskName):
        base = getBase()
        taskMgr.add(nullTask, uniqueName(leakTaskName))
        taskMgr.doMethodLater(1 << 31, nullDoLater, uniqueName(leakDoLaterName))
        taskMgr.doMethodLater(10, leakTask, 'doLeakTask-%s' % serialNum())
        if task:
            return task.done

    leakTask()
    return


class NoDictKey():
    __module__ = __name__


class Indirection():
    __module__ = __name__

    def __init__(self, evalStr = None, dictKey = NoDictKey):
        self.evalStr = evalStr
        self.dictKey = NoDictKey
        self._isWeakRef = False
        self._refCount = 0
        if dictKey is not NoDictKey:
            keyRepr = safeRepr(dictKey)
            useEval = False
            try:
                keyEval = eval(keyRepr)
                useEval = True
            except:
                pass

            if useEval:
                if hash(keyEval) != hash(dictKey):
                    useEval = False
            if useEval:
                self.evalStr = '[%s]' % keyRepr
            else:
                try:
                    self.dictKey = weakref.ref(dictKey)
                    self._isWeakRef = True
                except TypeError as e:
                    ContainerLeakDetector.notify.debug('could not weakref dict key %s' % keyRepr)
                    self.dictKey = dictKey
                    self._isWeakRef = False

    def destroy(self):
        self.dictKey = NoDictKey

    def acquire(self):
        self._refCount += 1

    def release(self):
        self._refCount -= 1
        if self._refCount == 0:
            self.destroy()

    def isDictKey(self):
        return self.dictKey is not NoDictKey

    def _getNonWeakDictKey(self):
        if not self._isWeakRef:
            return self.dictKey
        else:
            key = self.dictKey()
            if key is None:
                return '<garbage-collected dict key>'
            return key
        return

    def dereferenceDictKey(self, parentDict):
        key = self._getNonWeakDictKey()
        if parentDict is None:
            return key
        return parentDict[key]

    def getString(self, prevIndirection = None, nextIndirection = None):
        instanceDictStr = '.__dict__'
        if self.evalStr is not None:
            if nextIndirection is not None and self.evalStr[-len(instanceDictStr):] == instanceDictStr:
                return self.evalStr[:-len(instanceDictStr)]
            if prevIndirection is not None and prevIndirection.evalStr is not None:
                if prevIndirection.evalStr[-len(instanceDictStr):] == instanceDictStr:
                    return '.%s' % self.evalStr[2:-2]
            return self.evalStr
        keyRepr = safeRepr(self._getNonWeakDictKey())
        if prevIndirection is not None and prevIndirection.evalStr is not None:
            if prevIndirection.evalStr[-len(instanceDictStr):] == instanceDictStr:
                return '.%s' % keyRepr
        return '[%s]' % keyRepr

    def __repr__(self):
        return self.getString()


class ObjectRef():
    __module__ = __name__
    notify = directNotify.newCategory('ObjectRef')

    class FailedEval(Exception):
        __module__ = __name__

    def __init__(self, indirection, objId, other = None):
        self._indirections = []
        if other is not None:
            for ind in other._indirections:
                self._indirections.append(ind)

        self._indirections.append(indirection)
        for ind in self._indirections:
            ind.acquire()

        self.notify.debug(repr(self))
        return

    def destroy(self):
        for indirection in self._indirections:
            indirection.release()

        del self._indirections

    def getNumIndirections(self):
        return len(self._indirections)

    def goesThroughGen--- This code section failed: ---

0	LOAD_FAST         'obj'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	JUMP_IF_FALSE     '15'

12	JUMP_FORWARD      '27'

15	LOAD_GLOBAL       'id'
18	LOAD_FAST         'obj'
21	CALL_FUNCTION_1   None
24	STORE_FAST        'objId'
27_0	COME_FROM         '12'

27	LOAD_CONST        None
30	STORE_FAST        'o'

33	LOAD_CONST        ''
36	STORE_FAST        'evalStr'

39	LOAD_CONST        None
42	STORE_FAST        'curObj'

45	LOAD_FAST         'self'
48	LOAD_ATTR         '_indirections'
51	STORE_FAST        'indirections'

54	SETUP_LOOP        '85'
57	LOAD_FAST         'indirections'
60	GET_ITER          None
61	FOR_ITER          '84'
64	STORE_FAST        'indirection'

67	LOAD_CONST        None
70	YIELD_VALUE       None

71	LOAD_FAST         'indirection'
74	LOAD_ATTR         'acquire'
77	CALL_FUNCTION_0   None
80	POP_TOP           None
81	JUMP_BACK         '61'
84	POP_BLOCK         None
85_0	COME_FROM         '54'

85	SETUP_LOOP        '253'
88	LOAD_FAST         'indirections'
91	GET_ITER          None
92	FOR_ITER          '252'
95	STORE_FAST        'indirection'

98	LOAD_CONST        None
101	YIELD_VALUE       None

102	LOAD_FAST         'indirection'
105	LOAD_ATTR         'isDictKey'
108	CALL_FUNCTION_0   None
111	JUMP_IF_TRUE      '133'

114	LOAD_FAST         'evalStr'
117	LOAD_FAST         'indirection'
120	LOAD_ATTR         'getString'
123	CALL_FUNCTION_0   None
126	INPLACE_ADD       None
127	STORE_FAST        'evalStr'
130	JUMP_FORWARD      '202'

133	LOAD_FAST         'self'
136	LOAD_ATTR         '_getContainerByEval'
139	LOAD_FAST         'evalStr'
142	LOAD_CONST        'curObj'
145	LOAD_FAST         'curObj'
148	CALL_FUNCTION_257 None
151	STORE_FAST        'curObj'

154	LOAD_FAST         'curObj'
157	LOAD_CONST        None
160	COMPARE_OP        'is'
163	JUMP_IF_FALSE     '181'

166	LOAD_GLOBAL       'FailedEval'
169	LOAD_FAST         'evalStr'
172	CALL_FUNCTION_1   None
175	RAISE_VARARGS_1   None
178	JUMP_FORWARD      '181'
181_0	COME_FROM         '178'

181	LOAD_FAST         'indirection'
184	LOAD_ATTR         'dereferenceDictKey'
187	LOAD_FAST         'curObj'
190	CALL_FUNCTION_1   None
193	STORE_FAST        'curObj'

196	LOAD_CONST        ''
199	STORE_FAST        'evalStr'
202_0	COME_FROM         '130'

202	LOAD_CONST        None
205	YIELD_VALUE       None

206	LOAD_FAST         'self'
209	LOAD_ATTR         '_getContainerByEval'
212	LOAD_FAST         'evalStr'
215	LOAD_CONST        'curObj'
218	LOAD_FAST         'curObj'
221	CALL_FUNCTION_257 None
224	STORE_FAST        'o'

227	LOAD_GLOBAL       'id'
230	LOAD_FAST         'o'
233	CALL_FUNCTION_1   None
236	LOAD_FAST         'objId'
239	COMPARE_OP        '=='
242	JUMP_IF_FALSE     '249'

245	BREAK_LOOP        None
246	JUMP_BACK         '92'
249	JUMP_BACK         '92'
252	POP_BLOCK         None
253_0	COME_FROM         '85'

253	SETUP_LOOP        '284'
256	LOAD_FAST         'indirections'
259	GET_ITER          None
260	FOR_ITER          '283'
263	STORE_FAST        'indirection'

266	LOAD_CONST        None
269	YIELD_VALUE       None

270	LOAD_FAST         'indirection'
273	LOAD_ATTR         'release'
276	CALL_FUNCTION_0   None
279	POP_TOP           None
280	JUMP_BACK         '260'
283	POP_BLOCK         None
284_0	COME_FROM         '253'

284	LOAD_GLOBAL       'id'
287	LOAD_FAST         'o'
290	CALL_FUNCTION_1   None
293	LOAD_FAST         'objId'
296	COMPARE_OP        '=='
299	YIELD_VALUE       None
300	LOAD_CONST        None
303	RETURN_VALUE      None

Syntax error at or near `POP_TOP' token at offset 80

    def goesThrough(self, obj = None, objId = None):
        for goesThrough in self.goesThroughGen(obj=obj, objId=objId):
            pass

        return goesThrough

    def _getContainerByEval(self, evalStr, curObj = None):
        if curObj is not None:
            evalStr = 'curObj%s' % evalStr
        else:
            bis = '__builtin__'
            if evalStr[:len(bis)] != bis:
                evalStr = '%s.%s' % (bis, evalStr)
        try:
            container = eval(evalStr)
        except NameError as ne:
            return
        except AttributeError as ae:
            return
        except KeyError as ke:
            return

        return container

    def getContainerGen--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'evalStr'

6	LOAD_CONST        None
9	STORE_FAST        'curObj'

12	LOAD_FAST         'self'
15	LOAD_ATTR         '_indirections'
18	STORE_FAST        'indirections'

21	SETUP_LOOP        '48'
24	LOAD_FAST         'indirections'
27	GET_ITER          None
28	FOR_ITER          '47'
31	STORE_FAST        'indirection'

34	LOAD_FAST         'indirection'
37	LOAD_ATTR         'acquire'
40	CALL_FUNCTION_0   None
43	POP_TOP           None
44	JUMP_BACK         '28'
47	POP_BLOCK         None
48_0	COME_FROM         '21'

48	SETUP_LOOP        '169'
51	LOAD_FAST         'indirections'
54	GET_ITER          None
55	FOR_ITER          '168'
58	STORE_FAST        'indirection'

61	LOAD_CONST        None
64	YIELD_VALUE       None

65	LOAD_FAST         'indirection'
68	LOAD_ATTR         'isDictKey'
71	CALL_FUNCTION_0   None
74	JUMP_IF_TRUE      '96'

77	LOAD_FAST         'evalStr'
80	LOAD_FAST         'indirection'
83	LOAD_ATTR         'getString'
86	CALL_FUNCTION_0   None
89	INPLACE_ADD       None
90	STORE_FAST        'evalStr'
93	JUMP_BACK         '55'

96	LOAD_FAST         'self'
99	LOAD_ATTR         '_getContainerByEval'
102	LOAD_FAST         'evalStr'
105	LOAD_CONST        'curObj'
108	LOAD_FAST         'curObj'
111	CALL_FUNCTION_257 None
114	STORE_FAST        'curObj'

117	LOAD_FAST         'curObj'
120	LOAD_CONST        None
123	COMPARE_OP        'is'
126	JUMP_IF_FALSE     '144'

129	LOAD_GLOBAL       'FailedEval'
132	LOAD_FAST         'evalStr'
135	CALL_FUNCTION_1   None
138	RAISE_VARARGS_1   None
141	JUMP_FORWARD      '144'
144_0	COME_FROM         '141'

144	LOAD_FAST         'indirection'
147	LOAD_ATTR         'dereferenceDictKey'
150	LOAD_FAST         'curObj'
153	CALL_FUNCTION_1   None
156	STORE_FAST        'curObj'

159	LOAD_CONST        ''
162	STORE_FAST        'evalStr'
165	JUMP_BACK         '55'
168	POP_BLOCK         None
169_0	COME_FROM         '48'

169	SETUP_LOOP        '200'
172	LOAD_FAST         'indirections'
175	GET_ITER          None
176	FOR_ITER          '199'
179	STORE_FAST        'indirection'

182	LOAD_CONST        None
185	YIELD_VALUE       None

186	LOAD_FAST         'indirection'
189	LOAD_ATTR         'release'
192	CALL_FUNCTION_0   None
195	POP_TOP           None
196	JUMP_BACK         '176'
199	POP_BLOCK         None
200_0	COME_FROM         '169'

200	LOAD_FAST         'getInstance'
203	JUMP_IF_FALSE     '252'

206	LOAD_GLOBAL       'len'
209	LOAD_CONST        '.__dict__'
212	CALL_FUNCTION_1   None
215	STORE_FAST        'lenDict'

218	LOAD_FAST         'evalStr'
221	LOAD_FAST         'lenDict'
224	UNARY_NEGATIVE    None
225	SLICE+1           None
226	LOAD_CONST        '.__dict__'
229	COMPARE_OP        '=='
232	JUMP_IF_FALSE     '249'

235	LOAD_FAST         'evalStr'
238	LOAD_FAST         'lenDict'
241	UNARY_NEGATIVE    None
242	SLICE+2           None
243	STORE_FAST        'evalStr'
246	JUMP_ABSOLUTE     '252'
249	JUMP_FORWARD      '252'
252_0	COME_FROM         '249'

252	LOAD_FAST         'self'
255	LOAD_ATTR         '_getContainerByEval'
258	LOAD_FAST         'evalStr'
261	LOAD_CONST        'curObj'
264	LOAD_FAST         'curObj'
267	CALL_FUNCTION_257 None
270	YIELD_VALUE       None
271	LOAD_CONST        None
274	RETURN_VALUE      None

Syntax error at or near `INPLACE_ADD' token at offset 89

    def getEvalStrGen--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'str'

6	LOAD_CONST        None
9	STORE_FAST        'prevIndirection'

12	LOAD_CONST        None
15	STORE_FAST        'curIndirection'

18	LOAD_CONST        None
21	STORE_FAST        'nextIndirection'

24	LOAD_FAST         'self'
27	LOAD_ATTR         '_indirections'
30	STORE_FAST        'indirections'

33	SETUP_LOOP        '60'
36	LOAD_FAST         'indirections'
39	GET_ITER          None
40	FOR_ITER          '59'
43	STORE_FAST        'indirection'

46	LOAD_FAST         'indirection'
49	LOAD_ATTR         'acquire'
52	CALL_FUNCTION_0   None
55	POP_TOP           None
56	JUMP_BACK         '40'
59	POP_BLOCK         None
60_0	COME_FROM         '33'

60	SETUP_LOOP        '211'
63	LOAD_GLOBAL       'xrange'
66	LOAD_GLOBAL       'len'
69	LOAD_FAST         'indirections'
72	CALL_FUNCTION_1   None
75	CALL_FUNCTION_1   None
78	GET_ITER          None
79	FOR_ITER          '210'
82	STORE_FAST        'i'

85	LOAD_CONST        None
88	YIELD_VALUE       None

89	LOAD_FAST         'i'
92	LOAD_CONST        0
95	COMPARE_OP        '>'
98	JUMP_IF_FALSE     '118'

101	LOAD_FAST         'indirections'
104	LOAD_FAST         'i'
107	LOAD_CONST        1
110	BINARY_SUBTRACT   None
111	BINARY_SUBSCR     None
112	STORE_FAST        'prevIndirection'
115	JUMP_FORWARD      '124'

118	LOAD_CONST        None
121	STORE_FAST        'prevIndirection'
124_0	COME_FROM         '115'

124	LOAD_FAST         'indirections'
127	LOAD_FAST         'i'
130	BINARY_SUBSCR     None
131	STORE_FAST        'curIndirection'

134	LOAD_FAST         'i'
137	LOAD_GLOBAL       'len'
140	LOAD_FAST         'indirections'
143	CALL_FUNCTION_1   None
146	LOAD_CONST        1
149	BINARY_SUBTRACT   None
150	COMPARE_OP        '<'
153	JUMP_IF_FALSE     '173'

156	LOAD_FAST         'indirections'
159	LOAD_FAST         'i'
162	LOAD_CONST        1
165	BINARY_ADD        None
166	BINARY_SUBSCR     None
167	STORE_FAST        'nextIndirection'
170	JUMP_FORWARD      '179'

173	LOAD_CONST        None
176	STORE_FAST        'nextIndirection'
179_0	COME_FROM         '170'

179	LOAD_FAST         'str'
182	LOAD_FAST         'curIndirection'
185	LOAD_ATTR         'getString'
188	LOAD_CONST        'prevIndirection'
191	LOAD_FAST         'prevIndirection'

194	LOAD_CONST        'nextIndirection'
197	LOAD_FAST         'nextIndirection'
200	CALL_FUNCTION_512 None
203	INPLACE_ADD       None
204	STORE_FAST        'str'
207	JUMP_BACK         '79'
210	POP_BLOCK         None
211_0	COME_FROM         '60'

211	LOAD_FAST         'getInstance'
214	JUMP_IF_FALSE     '263'

217	LOAD_GLOBAL       'len'
220	LOAD_CONST        '.__dict__'
223	CALL_FUNCTION_1   None
226	STORE_FAST        'lenDict'

229	LOAD_FAST         'str'
232	LOAD_FAST         'lenDict'
235	UNARY_NEGATIVE    None
236	SLICE+1           None
237	LOAD_CONST        '.__dict__'
240	COMPARE_OP        '=='
243	JUMP_IF_FALSE     '260'

246	LOAD_FAST         'str'
249	LOAD_FAST         'lenDict'
252	UNARY_NEGATIVE    None
253	SLICE+2           None
254	STORE_FAST        'str'
257	JUMP_ABSOLUTE     '263'
260	JUMP_FORWARD      '263'
263_0	COME_FROM         '260'

263	SETUP_LOOP        '294'
266	LOAD_FAST         'indirections'
269	GET_ITER          None
270	FOR_ITER          '293'
273	STORE_FAST        'indirection'

276	LOAD_CONST        None
279	YIELD_VALUE       None

280	LOAD_FAST         'indirection'
283	LOAD_ATTR         'release'
286	CALL_FUNCTION_0   None
289	POP_TOP           None
290	JUMP_BACK         '270'
293	POP_BLOCK         None
294_0	COME_FROM         '263'

294	LOAD_FAST         'str'
297	YIELD_VALUE       None
298	LOAD_CONST        None
301	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 112

    def getFinalIndirectionStr(self):
        prevIndirection = None
        if len(self._indirections) > 1:
            prevIndirection = self._indirections[-2]
        return self._indirections[-1].getString(prevIndirection=prevIndirection)

    def __repr__(self):
        for result in self.getEvalStrGen():
            pass

        return result


class FindContainers(Job):
    __module__ = __name__

    def __init__(self, name, leakDetector):
        Job.__init__(self, name)
        self._leakDetector = leakDetector
        self._id2ref = self._leakDetector._id2ref
        self._id2baseStartRef = {}
        self._id2discoveredStartRef = {}
        self._baseStartRefWorkingList = ScratchPad(refGen=nullGen(), source=self._id2baseStartRef)
        self._discoveredStartRefWorkingList = ScratchPad(refGen=nullGen(), source=self._id2discoveredStartRef)
        self.notify = self._leakDetector.notify
        ContainerLeakDetector.addPrivateObj(self.__dict__)
        ref = ObjectRef(Indirection(evalStr='__builtin__.__dict__'), id(__builtin__.__dict__))
        self._id2baseStartRef[id(__builtin__.__dict__)] = ref
        if not hasattr(__builtin__, 'leakDetectors'):
            __builtin__.leakDetectors = {}
        ref = ObjectRef(Indirection(evalStr='leakDetectors'), id(leakDetectors))
        self._id2baseStartRef[id(leakDetectors)] = ref
        for i in self._addContainerGen(__builtin__.__dict__, ref):
            pass

        try:
            base
        except:
            pass
        else:
            ref = ObjectRef(Indirection(evalStr='base.__dict__'), id(base.__dict__))
            self._id2baseStartRef[id(base.__dict__)] = ref
            for i in self._addContainerGen(base.__dict__, ref):
                pass

        try:
            simbase
        except:
            pass
        else:
            ref = ObjectRef(Indirection(evalStr='simbase.__dict__'), id(simbase.__dict__))
            self._id2baseStartRef[id(simbase.__dict__)] = ref
            for i in self._addContainerGen(simbase.__dict__, ref):
                pass

    def destroy(self):
        ContainerLeakDetector.removePrivateObj(self.__dict__)
        Job.destroy(self)

    def getPriority(self):
        return Job.Priorities.Low

    @staticmethod
    def getStartObjAffinity(startObj):
        try:
            return len(startObj)
        except:
            return 1

    def _isDeadEnd(self, obj, objName = None):
        if type(obj) in (types.BooleanType,
         types.BuiltinFunctionType,
         types.BuiltinMethodType,
         types.ComplexType,
         types.FloatType,
         types.IntType,
         types.LongType,
         types.NoneType,
         types.NotImplementedType,
         types.TypeType,
         types.CodeType,
         types.FunctionType,
         types.StringType,
         types.UnicodeType,
         types.TupleType):
            return True
        if id(obj) in ContainerLeakDetector.PrivateIds:
            return True
        if type(objName) == types.StringType and objName in ('im_self', 'im_class'):
            return True
        try:
            className = obj.__class__.__name__
        except:
            pass
        else:
            if className == 'method-wrapper':
                return True

        return False

    def _hasLength(self, obj):
        return hasattr(obj, '__len__')

    def _addContainerGen--- This code section failed: ---

0	LOAD_GLOBAL       'id'
3	LOAD_FAST         'cont'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'contId'

12	LOAD_FAST         'contId'
15	LOAD_FAST         'self'
18	LOAD_ATTR         '_id2ref'
21	COMPARE_OP        'in'
24	JUMP_IF_FALSE     '91'

27	SETUP_LOOP        '61'
30	LOAD_FAST         'self'
33	LOAD_ATTR         '_id2ref'
36	LOAD_FAST         'contId'
39	BINARY_SUBSCR     None
40	LOAD_ATTR         'getEvalStrGen'
43	CALL_FUNCTION_0   None
46	GET_ITER          None
47	FOR_ITER          '60'
50	STORE_FAST        'existingRepr'

53	LOAD_CONST        None
56	YIELD_VALUE       None
57	JUMP_BACK         '47'
60	POP_BLOCK         None
61_0	COME_FROM         '27'

61	SETUP_LOOP        '91'
64	LOAD_FAST         'objRef'
67	LOAD_ATTR         'getEvalStrGen'
70	CALL_FUNCTION_0   None
73	GET_ITER          None
74	FOR_ITER          '87'
77	STORE_FAST        'newRepr'

80	LOAD_CONST        None
83	YIELD_VALUE       None
84	JUMP_BACK         '74'
87	POP_BLOCK         None
88_0	COME_FROM         '61'
88	JUMP_FORWARD      '91'
91_0	COME_FROM         '88'

91	LOAD_FAST         'contId'
94	LOAD_FAST         'self'
97	LOAD_ATTR         '_id2ref'
100	COMPARE_OP        'not in'
103	JUMP_IF_TRUE      '130'
106	LOAD_GLOBAL       'len'
109	LOAD_FAST         'newRepr'
112	CALL_FUNCTION_1   None
115	LOAD_GLOBAL       'len'
118	LOAD_FAST         'existingRepr'
121	CALL_FUNCTION_1   None
124	COMPARE_OP        '<'
127_0	COME_FROM         '103'
127	JUMP_IF_FALSE     '180'

130	LOAD_FAST         'contId'
133	LOAD_FAST         'self'
136	LOAD_ATTR         '_id2ref'
139	COMPARE_OP        'in'
142	JUMP_IF_FALSE     '164'

145	LOAD_FAST         'self'
148	LOAD_ATTR         '_leakDetector'
151	LOAD_ATTR         'removeContainerById'
154	LOAD_FAST         'contId'
157	CALL_FUNCTION_1   None
160	POP_TOP           None
161	JUMP_FORWARD      '164'
164_0	COME_FROM         '161'

164	LOAD_FAST         'objRef'
167	LOAD_FAST         'self'
170	LOAD_ATTR         '_id2ref'
173	LOAD_FAST         'contId'
176	STORE_SUBSCR      None
177	JUMP_FORWARD      '180'
180_0	COME_FROM         '177'
180	LOAD_CONST        None
183	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 60

    def _addDiscoveredStartRef(self, obj, ref):
        objId = id(obj)
        if objId in self._id2discoveredStartRef:
            existingRef = self._id2discoveredStartRef[objId]
            if type(existingRef) not in (types.IntType, types.LongType):
                if existingRef.getNumIndirections() >= ref.getNumIndirections():
                    return
        if objId in self._id2ref:
            if self._id2ref[objId].getNumIndirections() >= ref.getNumIndirections():
                return
        storedItem = ref
        if objId in self._id2ref:
            storedItem = objId
        self._id2discoveredStartRef[objId] = storedItem

    def run--- This code section failed: ---

0	SETUP_EXCEPT      '1770'

3	LOAD_GLOBAL       'nullGen'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'workingListSelector'

12	LOAD_CONST        None
15	STORE_FAST        'curObjRef'

18	SETUP_LOOP        '1766'
21	LOAD_GLOBAL       'True'
24	JUMP_IF_FALSE     '1765'

27	LOAD_CONST        None
30	YIELD_VALUE       None

31	LOAD_FAST         'curObjRef'
34	LOAD_CONST        None
37	COMPARE_OP        'is'
40	JUMP_IF_FALSE     '506'

43	SETUP_EXCEPT      '62'

46	LOAD_FAST         'workingListSelector'
49	LOAD_ATTR         'next'
52	CALL_FUNCTION_0   None
55	STORE_FAST        'startRefWorkingList'
58	POP_BLOCK         None
59	JUMP_FORWARD      '203'
62_0	COME_FROM         '43'

62	DUP_TOP           None
63	LOAD_GLOBAL       'StopIteration'
66	COMPARE_OP        'exception match'
69	JUMP_IF_FALSE     '202'
72	POP_TOP           None
73	POP_TOP           None
74	POP_TOP           None

75	LOAD_GLOBAL       'len'
78	LOAD_DEREF        'self'
81	LOAD_ATTR         '_baseStartRefWorkingList'
84	LOAD_ATTR         'source'
87	CALL_FUNCTION_1   None
90	STORE_FAST        'baseLen'

93	LOAD_GLOBAL       'len'
96	LOAD_DEREF        'self'
99	LOAD_ATTR         '_discoveredStartRefWorkingList'
102	LOAD_ATTR         'source'
105	CALL_FUNCTION_1   None
108	STORE_FAST        'discLen'

111	LOAD_GLOBAL       'float'
114	LOAD_GLOBAL       'max'
117	LOAD_CONST        1
120	LOAD_GLOBAL       'min'
123	LOAD_FAST         'baseLen'
126	LOAD_FAST         'discLen'
129	CALL_FUNCTION_2   None
132	CALL_FUNCTION_2   None
135	CALL_FUNCTION_1   None
138	STORE_FAST        'minLen'

141	LOAD_FAST         'minLen'
144	LOAD_CONST        3.0
147	INPLACE_MULTIPLY  None
148	STORE_FAST        'minLen'

151	LOAD_GLOBAL       'flywheel'
154	LOAD_DEREF        'self'
157	LOAD_ATTR         '_baseStartRefWorkingList'
160	LOAD_DEREF        'self'
163	LOAD_ATTR         '_discoveredStartRefWorkingList'
166	BUILD_LIST_2      None

169	LOAD_FAST         'baseLen'
172	LOAD_FAST         'minLen'
175	BINARY_DIVIDE     None
176	LOAD_FAST         'discLen'
179	LOAD_FAST         'minLen'
182	BINARY_DIVIDE     None
183	BUILD_LIST_2      None
186	CALL_FUNCTION_2   None
189	STORE_FAST        'workingListSelector'

192	LOAD_CONST        None
195	YIELD_VALUE       None

196	CONTINUE          '21'
199	JUMP_FORWARD      '203'
202	END_FINALLY       None
203_0	COME_FROM         '59'
203_1	COME_FROM         '202'

203	SETUP_LOOP        '348'
206	LOAD_GLOBAL       'True'
209	JUMP_IF_FALSE     '347'

212	LOAD_CONST        None
215	YIELD_VALUE       None

216	SETUP_EXCEPT      '239'

219	LOAD_FAST         'startRefWorkingList'
222	LOAD_ATTR         'refGen'
225	LOAD_ATTR         'next'
228	CALL_FUNCTION_0   None
231	STORE_FAST        'curObjRef'

234	BREAK_LOOP        None
235	POP_BLOCK         None
236	JUMP_BACK         '206'
239_0	COME_FROM         '216'

239	DUP_TOP           None
240	LOAD_GLOBAL       'StopIteration'
243	COMPARE_OP        'exception match'
246	JUMP_IF_FALSE     '343'
249	POP_TOP           None
250	POP_TOP           None
251	POP_TOP           None

252	LOAD_GLOBAL       'len'
255	LOAD_FAST         'startRefWorkingList'
258	LOAD_ATTR         'source'
261	CALL_FUNCTION_1   None
264	LOAD_CONST        0
267	COMPARE_OP        '=='
270	JUMP_IF_FALSE     '277'

273	BREAK_LOOP        None
274	JUMP_FORWARD      '277'
277_0	COME_FROM         '274'

277	SETUP_LOOP        '331'
280	LOAD_GLOBAL       'makeFlywheelGen'
283	LOAD_FAST         'startRefWorkingList'
286	LOAD_ATTR         'source'
289	LOAD_ATTR         'values'
292	CALL_FUNCTION_0   None

295	LOAD_CONST        'countFunc'
298	LOAD_CLOSURE      'self'
301	LOAD_LAMBDA       '<code_object <lambda>>'
304	MAKE_CLOSURE_0    None

307	LOAD_CONST        'scale'
310	LOAD_CONST        0.05
313	CALL_FUNCTION_513 None
316	GET_ITER          None
317	FOR_ITER          '330'
320	STORE_FAST        'fw'

323	LOAD_CONST        None
326	YIELD_VALUE       None
327	JUMP_BACK         '317'
330	POP_BLOCK         None
331_0	COME_FROM         '277'

331	LOAD_FAST         'fw'
334	LOAD_FAST         'startRefWorkingList'
337	STORE_ATTR        'refGen'
340	JUMP_BACK         '206'
343	END_FINALLY       None
344_0	COME_FROM         '343'
344	JUMP_BACK         '206'
347	POP_BLOCK         None
348_0	COME_FROM         '203'

348	LOAD_FAST         'curObjRef'
351	LOAD_CONST        None
354	COMPARE_OP        'is'
357	JUMP_IF_FALSE     '366'

360	CONTINUE          '21'
363	JUMP_FORWARD      '366'
366_0	COME_FROM         '363'

366	LOAD_GLOBAL       'type'
369	LOAD_FAST         'curObjRef'
372	CALL_FUNCTION_1   None
375	LOAD_GLOBAL       'types'
378	LOAD_ATTR         'IntType'
381	LOAD_GLOBAL       'types'
384	LOAD_ATTR         'LongType'
387	BUILD_TUPLE_2     None
390	COMPARE_OP        'in'
393	JUMP_IF_FALSE     '503'

396	LOAD_FAST         'curObjRef'
399	STORE_FAST        'startId'

402	LOAD_CONST        None
405	STORE_FAST        'curObjRef'

408	SETUP_EXCEPT      '448'

411	SETUP_LOOP        '444'
414	LOAD_DEREF        'self'
417	LOAD_ATTR         '_leakDetector'
420	LOAD_ATTR         'getContainerByIdGen'
423	LOAD_FAST         'startId'
426	CALL_FUNCTION_1   None
429	GET_ITER          None
430	FOR_ITER          '443'
433	STORE_FAST        'containerRef'

436	LOAD_CONST        None
439	YIELD_VALUE       None
440	JUMP_BACK         '430'
443	POP_BLOCK         None
444_0	COME_FROM         '411'
444	POP_BLOCK         None
445	JUMP_FORWARD      '494'
448_0	COME_FROM         '408'

448	POP_TOP           None
449	POP_TOP           None
450	POP_TOP           None

451	LOAD_DEREF        'self'
454	LOAD_ATTR         'notify'
457	LOAD_ATTR         'debug'
460	LOAD_CONST        'invalid startRef, stored as id %s'
463	LOAD_FAST         'startId'
466	BINARY_MODULO     None
467	CALL_FUNCTION_1   None
470	POP_TOP           None

471	LOAD_DEREF        'self'
474	LOAD_ATTR         '_leakDetector'
477	LOAD_ATTR         'removeContainerById'
480	LOAD_FAST         'startId'
483	CALL_FUNCTION_1   None
486	POP_TOP           None

487	CONTINUE          '21'
490	JUMP_FORWARD      '494'
493	END_FINALLY       None
494_0	COME_FROM         '445'
494_1	COME_FROM         '493'

494	LOAD_FAST         'containerRef'
497	STORE_FAST        'curObjRef'
500	JUMP_ABSOLUTE     '506'
503	JUMP_FORWARD      '506'
506_0	COME_FROM         '503'

506	SETUP_EXCEPT      '540'

509	SETUP_LOOP        '536'
512	LOAD_FAST         'curObjRef'
515	LOAD_ATTR         'getContainerGen'
518	CALL_FUNCTION_0   None
521	GET_ITER          None
522	FOR_ITER          '535'
525	STORE_FAST        'curObj'

528	LOAD_CONST        None
531	YIELD_VALUE       None
532	JUMP_BACK         '522'
535	POP_BLOCK         None
536_0	COME_FROM         '509'
536	POP_BLOCK         None
537	JUMP_FORWARD      '572'
540_0	COME_FROM         '506'

540	POP_TOP           None
541	POP_TOP           None
542	POP_TOP           None

543	LOAD_DEREF        'self'
546	LOAD_ATTR         'notify'
549	LOAD_ATTR         'debug'
552	LOAD_CONST        'lost current container, ref.getContainerGen() failed'
555	CALL_FUNCTION_1   None
558	POP_TOP           None

559	LOAD_CONST        None
562	STORE_FAST        'curObjRef'

565	CONTINUE          '21'
568	JUMP_FORWARD      '572'
571	END_FINALLY       None
572_0	COME_FROM         '537'
572_1	COME_FROM         '571'

572	LOAD_DEREF        'self'
575	LOAD_ATTR         'notify'
578	LOAD_ATTR         'debug'
581	LOAD_CONST        '--> %s'
584	LOAD_FAST         'curObjRef'
587	BINARY_MODULO     None
588	CALL_FUNCTION_1   None
591	POP_TOP           None

592	LOAD_FAST         'curObjRef'
595	STORE_FAST        'parentObjRef'

598	LOAD_CONST        None
601	STORE_FAST        'curObjRef'

604	LOAD_GLOBAL       'hasattr'
607	LOAD_FAST         'curObj'
610	LOAD_CONST        '__dict__'
613	CALL_FUNCTION_2   None
616	JUMP_IF_FALSE     '825'

619	LOAD_FAST         'curObj'
622	LOAD_ATTR         '__dict__'
625	STORE_FAST        'child'

628	LOAD_DEREF        'self'
631	LOAD_ATTR         '_hasLength'
634	LOAD_FAST         'child'
637	CALL_FUNCTION_1   None
640	STORE_FAST        'hasLength'

643	LOAD_DEREF        'self'
646	LOAD_ATTR         '_isDeadEnd'
649	LOAD_FAST         'child'
652	CALL_FUNCTION_1   None
655	UNARY_NOT         None
656	STORE_FAST        'notDeadEnd'

659	LOAD_FAST         'hasLength'
662	JUMP_IF_TRUE      '671'
665	LOAD_FAST         'notDeadEnd'
668_0	COME_FROM         '662'
668	JUMP_IF_FALSE     '819'

671	SETUP_LOOP        '697'
674	LOAD_FAST         'parentObjRef'
677	LOAD_ATTR         'goesThroughGen'
680	LOAD_FAST         'child'
683	CALL_FUNCTION_1   None
686	GET_ITER          None
687	FOR_ITER          '696'
690	STORE_FAST        'goesThrough'

693	JUMP_BACK         '687'
696	POP_BLOCK         None
697_0	COME_FROM         '671'

697	LOAD_FAST         'goesThrough'
700	JUMP_IF_TRUE      '816'

703	LOAD_GLOBAL       'ObjectRef'
706	LOAD_GLOBAL       'Indirection'
709	LOAD_CONST        'evalStr'
712	LOAD_CONST        '.__dict__'
715	CALL_FUNCTION_256 None

718	LOAD_GLOBAL       'id'
721	LOAD_FAST         'child'
724	CALL_FUNCTION_1   None
727	LOAD_FAST         'parentObjRef'
730	CALL_FUNCTION_3   None
733	STORE_FAST        'objRef'

736	LOAD_CONST        None
739	YIELD_VALUE       None

740	LOAD_FAST         'hasLength'
743	JUMP_IF_FALSE     '782'

746	SETUP_LOOP        '782'
749	LOAD_DEREF        'self'
752	LOAD_ATTR         '_addContainerGen'
755	LOAD_FAST         'child'
758	LOAD_FAST         'objRef'
761	CALL_FUNCTION_2   None
764	GET_ITER          None
765	FOR_ITER          '778'
768	STORE_FAST        'i'

771	LOAD_CONST        None
774	YIELD_VALUE       None
775	JUMP_BACK         '765'
778	POP_BLOCK         None
779_0	COME_FROM         '746'
779	JUMP_FORWARD      '782'
782_0	COME_FROM         '779'

782	LOAD_FAST         'notDeadEnd'
785	JUMP_IF_FALSE     '813'

788	LOAD_DEREF        'self'
791	LOAD_ATTR         '_addDiscoveredStartRef'
794	LOAD_FAST         'child'
797	LOAD_FAST         'objRef'
800	CALL_FUNCTION_2   None
803	POP_TOP           None

804	LOAD_FAST         'objRef'
807	STORE_FAST        'curObjRef'
810	JUMP_ABSOLUTE     '816'
813	JUMP_ABSOLUTE     '819'
816	JUMP_BACK         '21'

819	CONTINUE          '21'
822	JUMP_FORWARD      '825'
825_0	COME_FROM         '822'

825	LOAD_GLOBAL       'type'
828	LOAD_FAST         'curObj'
831	CALL_FUNCTION_1   None
834	LOAD_GLOBAL       'types'
837	LOAD_ATTR         'DictType'
840	COMPARE_OP        'is'
843	JUMP_IF_FALSE     '1762'

846	LOAD_CONST        None
849	STORE_FAST        'key'

852	LOAD_CONST        None
855	STORE_FAST        'attr'

858	LOAD_FAST         'curObj'
861	LOAD_ATTR         'keys'
864	CALL_FUNCTION_0   None
867	STORE_FAST        'keys'

870	LOAD_GLOBAL       'len'
873	LOAD_FAST         'keys'
876	CALL_FUNCTION_1   None
879	LOAD_CONST        1
882	BINARY_ADD        None
883	STORE_FAST        'numKeysLeft'

886	SETUP_LOOP        '1303'
889	LOAD_FAST         'keys'
892	GET_ITER          None
893	FOR_ITER          '1302'
896	STORE_FAST        'key'

899	LOAD_CONST        None
902	YIELD_VALUE       None

903	LOAD_FAST         'numKeysLeft'
906	LOAD_CONST        1
909	INPLACE_SUBTRACT  None
910	STORE_FAST        'numKeysLeft'

913	SETUP_EXCEPT      '930'

916	LOAD_FAST         'curObj'
919	LOAD_FAST         'key'
922	BINARY_SUBSCR     None
923	STORE_FAST        'attr'
926	POP_BLOCK         None
927	JUMP_FORWARD      '984'
930_0	COME_FROM         '913'

930	DUP_TOP           None
931	LOAD_GLOBAL       'KeyError'
934	COMPARE_OP        'exception match'
937	JUMP_IF_FALSE     '983'
940	POP_TOP           None
941	STORE_FAST        'e'
944	POP_TOP           None

945	LOAD_DEREF        'self'
948	LOAD_ATTR         'notify'
951	LOAD_ATTR         'debug'
954	LOAD_CONST        'could not index into %s with key %s'
957	LOAD_FAST         'parentObjRef'
960	LOAD_GLOBAL       'safeRepr'
963	LOAD_FAST         'key'
966	CALL_FUNCTION_1   None
969	BUILD_TUPLE_2     None
972	BINARY_MODULO     None
973	CALL_FUNCTION_1   None
976	POP_TOP           None

977	CONTINUE          '893'
980	JUMP_FORWARD      '984'
983	END_FINALLY       None
984_0	COME_FROM         '927'
984_1	COME_FROM         '983'

984	LOAD_DEREF        'self'
987	LOAD_ATTR         '_hasLength'
990	LOAD_FAST         'attr'
993	CALL_FUNCTION_1   None
996	STORE_FAST        'hasLength'

999	LOAD_GLOBAL       'False'
1002	STORE_FAST        'notDeadEnd'

1005	LOAD_FAST         'curObjRef'
1008	LOAD_CONST        None
1011	COMPARE_OP        'is'
1014	JUMP_IF_FALSE     '1039'

1017	LOAD_DEREF        'self'
1020	LOAD_ATTR         '_isDeadEnd'
1023	LOAD_FAST         'attr'
1026	LOAD_FAST         'key'
1029	CALL_FUNCTION_2   None
1032	UNARY_NOT         None
1033	STORE_FAST        'notDeadEnd'
1036	JUMP_FORWARD      '1039'
1039_0	COME_FROM         '1036'

1039	LOAD_FAST         'hasLength'
1042	JUMP_IF_TRUE      '1051'
1045	LOAD_FAST         'notDeadEnd'
1048_0	COME_FROM         '1042'
1048	JUMP_IF_FALSE     '1299'

1051	SETUP_LOOP        '1081'
1054	LOAD_FAST         'parentObjRef'
1057	LOAD_ATTR         'goesThroughGen'
1060	LOAD_FAST         'curObj'
1063	LOAD_FAST         'key'
1066	BINARY_SUBSCR     None
1067	CALL_FUNCTION_1   None
1070	GET_ITER          None
1071	FOR_ITER          '1080'
1074	STORE_FAST        'goesThrough'

1077	JUMP_BACK         '1071'
1080	POP_BLOCK         None
1081_0	COME_FROM         '1051'

1081	LOAD_FAST         'goesThrough'
1084	JUMP_IF_TRUE      '1296'

1087	LOAD_FAST         'curObj'
1090	LOAD_GLOBAL       '__builtin__'
1093	LOAD_ATTR         '__dict__'
1096	COMPARE_OP        'is'
1099	JUMP_IF_FALSE     '1143'

1102	LOAD_GLOBAL       'ObjectRef'
1105	LOAD_GLOBAL       'Indirection'
1108	LOAD_CONST        'evalStr'
1111	LOAD_CONST        '%s'
1114	LOAD_FAST         'key'
1117	BINARY_MODULO     None
1118	CALL_FUNCTION_256 None

1121	LOAD_GLOBAL       'id'
1124	LOAD_FAST         'curObj'
1127	LOAD_FAST         'key'
1130	BINARY_SUBSCR     None
1131	CALL_FUNCTION_1   None
1134	CALL_FUNCTION_2   None
1137	STORE_FAST        'objRef'
1140	JUMP_FORWARD      '1180'

1143	LOAD_GLOBAL       'ObjectRef'
1146	LOAD_GLOBAL       'Indirection'
1149	LOAD_CONST        'dictKey'
1152	LOAD_FAST         'key'
1155	CALL_FUNCTION_256 None

1158	LOAD_GLOBAL       'id'
1161	LOAD_FAST         'curObj'
1164	LOAD_FAST         'key'
1167	BINARY_SUBSCR     None
1168	CALL_FUNCTION_1   None
1171	LOAD_FAST         'parentObjRef'
1174	CALL_FUNCTION_3   None
1177	STORE_FAST        'objRef'
1180_0	COME_FROM         '1140'

1180	LOAD_CONST        None
1183	YIELD_VALUE       None

1184	LOAD_FAST         'hasLength'
1187	JUMP_IF_FALSE     '1226'

1190	SETUP_LOOP        '1226'
1193	LOAD_DEREF        'self'
1196	LOAD_ATTR         '_addContainerGen'
1199	LOAD_FAST         'attr'
1202	LOAD_FAST         'objRef'
1205	CALL_FUNCTION_2   None
1208	GET_ITER          None
1209	FOR_ITER          '1222'
1212	STORE_FAST        'i'

1215	LOAD_CONST        None
1218	YIELD_VALUE       None
1219	JUMP_BACK         '1209'
1222	POP_BLOCK         None
1223_0	COME_FROM         '1190'
1223	JUMP_FORWARD      '1226'
1226_0	COME_FROM         '1223'

1226	LOAD_FAST         'notDeadEnd'
1229	JUMP_IF_FALSE     '1293'

1232	LOAD_DEREF        'self'
1235	LOAD_ATTR         '_addDiscoveredStartRef'
1238	LOAD_FAST         'attr'
1241	LOAD_FAST         'objRef'
1244	CALL_FUNCTION_2   None
1247	POP_TOP           None

1248	LOAD_FAST         'curObjRef'
1251	LOAD_CONST        None
1254	COMPARE_OP        'is'
1257	JUMP_IF_FALSE     '1290'
1260	LOAD_GLOBAL       'random'
1263	LOAD_ATTR         'randrange'
1266	LOAD_FAST         'numKeysLeft'
1269	CALL_FUNCTION_1   None
1272	LOAD_CONST        0
1275	COMPARE_OP        '=='
1278_0	COME_FROM         '1257'
1278	JUMP_IF_FALSE     '1290'

1281	LOAD_FAST         'objRef'
1284	STORE_FAST        'curObjRef'
1287	JUMP_ABSOLUTE     '1293'
1290	JUMP_ABSOLUTE     '1296'
1293	JUMP_ABSOLUTE     '1299'
1296	JUMP_BACK         '893'
1299	JUMP_BACK         '893'
1302	POP_BLOCK         None
1303_0	COME_FROM         '886'

1303	DELETE_FAST       'key'

1306	DELETE_FAST       'attr'

1309	CONTINUE          '21'

1312	SETUP_EXCEPT      '1331'

1315	LOAD_GLOBAL       'dir'
1318	LOAD_FAST         'curObj'
1321	CALL_FUNCTION_1   None
1324	STORE_FAST        'childNames'
1327	POP_BLOCK         None
1328	JUMP_FORWARD      '1338'
1331_0	COME_FROM         '1312'

1331	POP_TOP           None
1332	POP_TOP           None
1333	POP_TOP           None

1334	JUMP_ABSOLUTE     '1762'
1337	END_FINALLY       None
1338_0	COME_FROM         '1328'

1338	SETUP_EXCEPT      '1734'

1341	LOAD_CONST        -1
1344	STORE_FAST        'index'

1347	BUILD_LIST_0      None
1350	STORE_FAST        'attrs'

1353	SETUP_LOOP        '1410'

1356	LOAD_CONST        None
1359	YIELD_VALUE       None

1360	SETUP_EXCEPT      '1379'

1363	LOAD_FAST         'itr'
1366	LOAD_ATTR         'next'
1369	CALL_FUNCTION_0   None
1372	STORE_FAST        'attr'
1375	POP_BLOCK         None
1376	JUMP_FORWARD      '1393'
1379_0	COME_FROM         '1360'

1379	POP_TOP           None
1380	POP_TOP           None
1381	POP_TOP           None

1382	LOAD_CONST        None
1385	STORE_FAST        'attr'

1388	BREAK_LOOP        None
1389	JUMP_FORWARD      '1393'
1392	END_FINALLY       None
1393_0	COME_FROM         '1376'
1393_1	COME_FROM         '1392'

1393	LOAD_FAST         'attrs'
1396	LOAD_ATTR         'append'
1399	LOAD_FAST         'attr'
1402	CALL_FUNCTION_1   None
1405	POP_TOP           None
1406	JUMP_BACK         '1356'
1409	POP_BLOCK         None
1410_0	COME_FROM         '1353'

1410	LOAD_GLOBAL       'len'
1413	LOAD_FAST         'attrs'
1416	CALL_FUNCTION_1   None
1419	LOAD_CONST        1
1422	BINARY_ADD        None
1423	STORE_FAST        'numAttrsLeft'

1426	SETUP_LOOP        '1727'
1429	LOAD_FAST         'attrs'
1432	GET_ITER          None
1433	FOR_ITER          '1726'
1436	STORE_FAST        'attr'

1439	LOAD_CONST        None
1442	YIELD_VALUE       None

1443	LOAD_FAST         'index'
1446	LOAD_CONST        1
1449	INPLACE_ADD       None
1450	STORE_FAST        'index'

1453	LOAD_FAST         'numAttrsLeft'
1456	LOAD_CONST        1
1459	INPLACE_SUBTRACT  None
1460	STORE_FAST        'numAttrsLeft'

1463	LOAD_DEREF        'self'
1466	LOAD_ATTR         '_hasLength'
1469	LOAD_FAST         'attr'
1472	CALL_FUNCTION_1   None
1475	STORE_FAST        'hasLength'

1478	LOAD_GLOBAL       'False'
1481	STORE_FAST        'notDeadEnd'

1484	LOAD_FAST         'curObjRef'
1487	LOAD_CONST        None
1490	COMPARE_OP        'is'
1493	JUMP_IF_FALSE     '1515'

1496	LOAD_DEREF        'self'
1499	LOAD_ATTR         '_isDeadEnd'
1502	LOAD_FAST         'attr'
1505	CALL_FUNCTION_1   None
1508	UNARY_NOT         None
1509	STORE_FAST        'notDeadEnd'
1512	JUMP_FORWARD      '1515'
1515_0	COME_FROM         '1512'

1515	LOAD_FAST         'hasLength'
1518	JUMP_IF_TRUE      '1527'
1521	LOAD_FAST         'notDeadEnd'
1524_0	COME_FROM         '1518'
1524	JUMP_IF_FALSE     '1723'

1527	SETUP_LOOP        '1557'
1530	LOAD_FAST         'parentObjRef'
1533	LOAD_ATTR         'goesThrough'
1536	LOAD_FAST         'curObj'
1539	LOAD_FAST         'index'
1542	BINARY_SUBSCR     None
1543	CALL_FUNCTION_1   None
1546	GET_ITER          None
1547	FOR_ITER          '1556'
1550	STORE_FAST        'goesThrough'

1553	JUMP_BACK         '1547'
1556	POP_BLOCK         None
1557_0	COME_FROM         '1527'

1557	LOAD_FAST         'goesThrough'
1560	JUMP_IF_TRUE      '1720'

1563	LOAD_GLOBAL       'ObjectRef'
1566	LOAD_GLOBAL       'Indirection'
1569	LOAD_CONST        'evalStr'
1572	LOAD_CONST        '[%s]'
1575	LOAD_FAST         'index'
1578	BINARY_MODULO     None
1579	CALL_FUNCTION_256 None

1582	LOAD_GLOBAL       'id'
1585	LOAD_FAST         'curObj'
1588	LOAD_FAST         'index'
1591	BINARY_SUBSCR     None
1592	CALL_FUNCTION_1   None
1595	LOAD_FAST         'parentObjRef'
1598	CALL_FUNCTION_3   None
1601	STORE_FAST        'objRef'

1604	LOAD_CONST        None
1607	YIELD_VALUE       None

1608	LOAD_FAST         'hasLength'
1611	JUMP_IF_FALSE     '1650'

1614	SETUP_LOOP        '1650'
1617	LOAD_DEREF        'self'
1620	LOAD_ATTR         '_addContainerGen'
1623	LOAD_FAST         'attr'
1626	LOAD_FAST         'objRef'
1629	CALL_FUNCTION_2   None
1632	GET_ITER          None
1633	FOR_ITER          '1646'
1636	STORE_FAST        'i'

1639	LOAD_CONST        None
1642	YIELD_VALUE       None
1643	JUMP_BACK         '1633'
1646	POP_BLOCK         None
1647_0	COME_FROM         '1614'
1647	JUMP_FORWARD      '1650'
1650_0	COME_FROM         '1647'

1650	LOAD_FAST         'notDeadEnd'
1653	JUMP_IF_FALSE     '1717'

1656	LOAD_DEREF        'self'
1659	LOAD_ATTR         '_addDiscoveredStartRef'
1662	LOAD_FAST         'attr'
1665	LOAD_FAST         'objRef'
1668	CALL_FUNCTION_2   None
1671	POP_TOP           None

1672	LOAD_FAST         'curObjRef'
1675	LOAD_CONST        None
1678	COMPARE_OP        'is'
1681	JUMP_IF_FALSE     '1714'
1684	LOAD_GLOBAL       'random'
1687	LOAD_ATTR         'randrange'
1690	LOAD_FAST         'numAttrsLeft'
1693	CALL_FUNCTION_1   None
1696	LOAD_CONST        0
1699	COMPARE_OP        '=='
1702_0	COME_FROM         '1681'
1702	JUMP_IF_FALSE     '1714'

1705	LOAD_FAST         'objRef'
1708	STORE_FAST        'curObjRef'
1711	JUMP_ABSOLUTE     '1717'
1714	JUMP_ABSOLUTE     '1720'
1717	JUMP_ABSOLUTE     '1723'
1720	JUMP_BACK         '1433'
1723	JUMP_BACK         '1433'
1726	POP_BLOCK         None
1727_0	COME_FROM         '1426'

1727	DELETE_FAST       'attr'
1730	POP_BLOCK         None
1731	JUMP_FORWARD      '1753'
1734_0	COME_FROM         '1338'

1734	DUP_TOP           None
1735	LOAD_GLOBAL       'StopIteration'
1738	COMPARE_OP        'exception match'
1741	JUMP_IF_FALSE     '1752'
1744	POP_TOP           None
1745	STORE_FAST        'e'
1748	POP_TOP           None

1749	JUMP_FORWARD      '1753'
1752	END_FINALLY       None
1753_0	COME_FROM         '1731'
1753_1	COME_FROM         '1752'

1753	DELETE_FAST       'itr'

1756	CONTINUE          '21'
1759_0	COME_FROM         '1337'
1759	JUMP_BACK         '21'
1762	JUMP_BACK         '21'
1765	POP_BLOCK         None
1766_0	COME_FROM         '18'
1766	POP_BLOCK         None
1767	JUMP_FORWARD      '1810'
1770_0	COME_FROM         '0'

1770	DUP_TOP           None
1771	LOAD_GLOBAL       'Exception'
1774	COMPARE_OP        'exception match'
1777	JUMP_IF_FALSE     '1809'
1780	POP_TOP           None
1781	STORE_FAST        'e'
1784	POP_TOP           None

1785	LOAD_CONST        'FindContainers job caught exception: %s'
1788	LOAD_FAST         'e'
1791	BINARY_MODULO     None
1792	PRINT_ITEM        None
1793	PRINT_NEWLINE_CONT None

1794	LOAD_GLOBAL       '__dev__'
1797	JUMP_IF_FALSE     '1806'

1800	RAISE_VARARGS_0   None
1803	JUMP_ABSOLUTE     '1810'
1806	JUMP_FORWARD      '1810'
1809	END_FINALLY       None
1810_0	COME_FROM         '1767'
1810_1	COME_FROM         '1809'

1810	LOAD_GLOBAL       'Job'
1813	LOAD_ATTR         'Done'
1816	YIELD_VALUE       None
1817	LOAD_CONST        None
1820	RETURN_VALUE      None

Syntax error at or near `SETUP_EXCEPT' token at offset 43


class CheckContainers(Job):
    __module__ = __name__
    ReprItems = 5

    def __init__(self, name, leakDetector, index):
        Job.__init__(self, name)
        self._leakDetector = leakDetector
        self.notify = self._leakDetector.notify
        self._index = index
        ContainerLeakDetector.addPrivateObj(self.__dict__)

    def destroy(self):
        ContainerLeakDetector.removePrivateObj(self.__dict__)
        Job.destroy(self)

    def getPriority(self):
        return Job.Priorities.Normal

    def run--- This code section failed: ---

0	SETUP_EXCEPT      '1388'

3	BUILD_MAP         None
6	LOAD_FAST         'self'
9	LOAD_ATTR         '_leakDetector'
12	LOAD_ATTR         '_index2containerId2len'
15	LOAD_FAST         'self'
18	LOAD_ATTR         '_index'
21	STORE_SUBSCR      None

22	LOAD_FAST         'self'
25	LOAD_ATTR         '_leakDetector'
28	LOAD_ATTR         'getContainerIds'
31	CALL_FUNCTION_0   None
34	STORE_FAST        'ids'

37	SETUP_LOOP        '490'
40	LOAD_FAST         'ids'
43	GET_ITER          None
44	FOR_ITER          '489'
47	STORE_FAST        'objId'

50	LOAD_CONST        None
53	YIELD_VALUE       None

54	SETUP_EXCEPT      '100'

57	SETUP_LOOP        '90'
60	LOAD_FAST         'self'
63	LOAD_ATTR         '_leakDetector'
66	LOAD_ATTR         'getContainerByIdGen'
69	LOAD_FAST         'objId'
72	CALL_FUNCTION_1   None
75	GET_ITER          None
76	FOR_ITER          '89'
79	STORE_FAST        'result'

82	LOAD_CONST        None
85	YIELD_VALUE       None
86	JUMP_BACK         '76'
89	POP_BLOCK         None
90_0	COME_FROM         '57'

90	LOAD_FAST         'result'
93	STORE_FAST        'container'
96	POP_BLOCK         None
97	JUMP_FORWARD      '215'
100_0	COME_FROM         '54'

100	DUP_TOP           None
101	LOAD_GLOBAL       'Exception'
104	COMPARE_OP        'exception match'
107	JUMP_IF_FALSE     '214'
110	POP_TOP           None
111	STORE_FAST        'e'
114	POP_TOP           None

115	LOAD_FAST         'self'
118	LOAD_ATTR         'notify'
121	LOAD_ATTR         'getDebug'
124	CALL_FUNCTION_0   None
127	JUMP_IF_FALSE     '192'

130	SETUP_LOOP        '163'
133	LOAD_FAST         'self'
136	LOAD_ATTR         '_leakDetector'
139	LOAD_ATTR         'getContainerNameByIdGen'
142	LOAD_FAST         'objId'
145	CALL_FUNCTION_1   None
148	GET_ITER          None
149	FOR_ITER          '162'
152	STORE_FAST        'contName'

155	LOAD_CONST        None
158	YIELD_VALUE       None
159	JUMP_BACK         '149'
162	POP_BLOCK         None
163_0	COME_FROM         '130'

163	LOAD_FAST         'self'
166	LOAD_ATTR         'notify'
169	LOAD_ATTR         'debug'
172	LOAD_CONST        '%s no longer exists; caught exception in getContainerById (%s)'
175	LOAD_FAST         'contName'
178	LOAD_FAST         'e'
181	BUILD_TUPLE_2     None
184	BINARY_MODULO     None
185	CALL_FUNCTION_1   None
188	POP_TOP           None
189	JUMP_FORWARD      '192'
192_0	COME_FROM         '189'

192	LOAD_FAST         'self'
195	LOAD_ATTR         '_leakDetector'
198	LOAD_ATTR         'removeContainerById'
201	LOAD_FAST         'objId'
204	CALL_FUNCTION_1   None
207	POP_TOP           None

208	CONTINUE          '44'
211	JUMP_FORWARD      '215'
214	END_FINALLY       None
215_0	COME_FROM         '97'
215_1	COME_FROM         '214'

215	LOAD_FAST         'container'
218	LOAD_CONST        None
221	COMPARE_OP        'is'
224	JUMP_IF_FALSE     '320'

227	LOAD_FAST         'self'
230	LOAD_ATTR         'notify'
233	LOAD_ATTR         'getDebug'
236	CALL_FUNCTION_0   None
239	JUMP_IF_FALSE     '298'

242	SETUP_LOOP        '275'
245	LOAD_FAST         'self'
248	LOAD_ATTR         '_leakDetector'
251	LOAD_ATTR         'getContainerNameByIdGen'
254	LOAD_FAST         'objId'
257	CALL_FUNCTION_1   None
260	GET_ITER          None
261	FOR_ITER          '274'
264	STORE_FAST        'contName'

267	LOAD_CONST        None
270	YIELD_VALUE       None
271	JUMP_BACK         '261'
274	POP_BLOCK         None
275_0	COME_FROM         '242'

275	LOAD_FAST         'self'
278	LOAD_ATTR         'notify'
281	LOAD_ATTR         'debug'
284	LOAD_CONST        '%s no longer exists; getContainerById returned None'
287	LOAD_FAST         'contName'
290	BINARY_MODULO     None
291	CALL_FUNCTION_1   None
294	POP_TOP           None
295	JUMP_FORWARD      '298'
298_0	COME_FROM         '295'

298	LOAD_FAST         'self'
301	LOAD_ATTR         '_leakDetector'
304	LOAD_ATTR         'removeContainerById'
307	LOAD_FAST         'objId'
310	CALL_FUNCTION_1   None
313	POP_TOP           None

314	CONTINUE          '44'
317	JUMP_FORWARD      '320'
320_0	COME_FROM         '317'

320	SETUP_EXCEPT      '339'

323	LOAD_GLOBAL       'len'
326	LOAD_FAST         'container'
329	CALL_FUNCTION_1   None
332	STORE_FAST        'cLen'
335	POP_BLOCK         None
336	JUMP_FORWARD      '463'
339_0	COME_FROM         '320'

339	DUP_TOP           None
340	LOAD_GLOBAL       'Exception'
343	COMPARE_OP        'exception match'
346	JUMP_IF_FALSE     '462'
349	POP_TOP           None
350	STORE_FAST        'e'
353	POP_TOP           None

354	LOAD_FAST         'self'
357	LOAD_ATTR         'notify'
360	LOAD_ATTR         'getDebug'
363	CALL_FUNCTION_0   None
366	JUMP_IF_FALSE     '440'

369	SETUP_LOOP        '402'
372	LOAD_FAST         'self'
375	LOAD_ATTR         '_leakDetector'
378	LOAD_ATTR         'getContainerNameByIdGen'
381	LOAD_FAST         'objId'
384	CALL_FUNCTION_1   None
387	GET_ITER          None
388	FOR_ITER          '401'
391	STORE_FAST        'contName'

394	LOAD_CONST        None
397	YIELD_VALUE       None
398	JUMP_BACK         '388'
401	POP_BLOCK         None
402_0	COME_FROM         '369'

402	LOAD_FAST         'self'
405	LOAD_ATTR         'notify'
408	LOAD_ATTR         'debug'
411	LOAD_CONST        '%s is no longer a container, it is now %s (%s)'
414	LOAD_FAST         'contName'
417	LOAD_GLOBAL       'safeRepr'
420	LOAD_FAST         'container'
423	CALL_FUNCTION_1   None
426	LOAD_FAST         'e'
429	BUILD_TUPLE_3     None
432	BINARY_MODULO     None
433	CALL_FUNCTION_1   None
436	POP_TOP           None
437	JUMP_FORWARD      '440'
440_0	COME_FROM         '437'

440	LOAD_FAST         'self'
443	LOAD_ATTR         '_leakDetector'
446	LOAD_ATTR         'removeContainerById'
449	LOAD_FAST         'objId'
452	CALL_FUNCTION_1   None
455	POP_TOP           None

456	CONTINUE          '44'
459	JUMP_FORWARD      '463'
462	END_FINALLY       None
463_0	COME_FROM         '336'
463_1	COME_FROM         '462'

463	LOAD_FAST         'cLen'
466	LOAD_FAST         'self'
469	LOAD_ATTR         '_leakDetector'
472	LOAD_ATTR         '_index2containerId2len'
475	LOAD_FAST         'self'
478	LOAD_ATTR         '_index'
481	BINARY_SUBSCR     None
482	LOAD_FAST         'objId'
485	STORE_SUBSCR      None
486	JUMP_BACK         '44'
489	POP_BLOCK         None
490_0	COME_FROM         '37'

490	LOAD_FAST         'self'
493	LOAD_ATTR         '_index'
496	LOAD_CONST        0
499	COMPARE_OP        '>'
502	JUMP_IF_FALSE     '1384'

505	LOAD_FAST         'self'
508	LOAD_ATTR         '_leakDetector'
511	LOAD_ATTR         '_index2containerId2len'
514	STORE_FAST        'idx2id2len'

517	SETUP_LOOP        '1384'
520	LOAD_FAST         'idx2id2len'
523	LOAD_FAST         'self'
526	LOAD_ATTR         '_index'
529	BINARY_SUBSCR     None
530	GET_ITER          None
531	FOR_ITER          '1380'
534	STORE_FAST        'objId'

537	LOAD_CONST        None
540	YIELD_VALUE       None

541	LOAD_FAST         'objId'
544	LOAD_FAST         'idx2id2len'
547	LOAD_FAST         'self'
550	LOAD_ATTR         '_index'
553	LOAD_CONST        1
556	BINARY_SUBTRACT   None
557	BINARY_SUBSCR     None
558	COMPARE_OP        'in'
561	JUMP_IF_FALSE     '1377'

564	LOAD_FAST         'idx2id2len'
567	LOAD_FAST         'self'
570	LOAD_ATTR         '_index'
573	BINARY_SUBSCR     None
574	LOAD_FAST         'objId'
577	BINARY_SUBSCR     None
578	LOAD_FAST         'idx2id2len'
581	LOAD_FAST         'self'
584	LOAD_ATTR         '_index'
587	LOAD_CONST        1
590	BINARY_SUBTRACT   None
591	BINARY_SUBSCR     None
592	LOAD_FAST         'objId'
595	BINARY_SUBSCR     None
596	BINARY_SUBTRACT   None
597	STORE_FAST        'diff'

600	LOAD_FAST         'self'
603	LOAD_ATTR         '_index'
606	LOAD_CONST        2
609	COMPARE_OP        '>'
612	JUMP_IF_FALSE     '1374'
615	LOAD_FAST         'objId'
618	LOAD_FAST         'idx2id2len'
621	LOAD_FAST         'self'
624	LOAD_ATTR         '_index'
627	LOAD_CONST        2
630	BINARY_SUBTRACT   None
631	BINARY_SUBSCR     None
632	COMPARE_OP        'in'
635	JUMP_IF_FALSE     '1374'
638	LOAD_FAST         'objId'
641	LOAD_FAST         'idx2id2len'
644	LOAD_FAST         'self'
647	LOAD_ATTR         '_index'
650	LOAD_CONST        3
653	BINARY_SUBTRACT   None
654	BINARY_SUBSCR     None
655	COMPARE_OP        'in'
658_0	COME_FROM         '612'
658_1	COME_FROM         '635'
658	JUMP_IF_FALSE     '1374'

661	LOAD_FAST         'idx2id2len'
664	LOAD_FAST         'self'
667	LOAD_ATTR         '_index'
670	LOAD_CONST        1
673	BINARY_SUBTRACT   None
674	BINARY_SUBSCR     None
675	LOAD_FAST         'objId'
678	BINARY_SUBSCR     None
679	LOAD_FAST         'idx2id2len'
682	LOAD_FAST         'self'
685	LOAD_ATTR         '_index'
688	LOAD_CONST        2
691	BINARY_SUBTRACT   None
692	BINARY_SUBSCR     None
693	LOAD_FAST         'objId'
696	BINARY_SUBSCR     None
697	BINARY_SUBTRACT   None
698	STORE_FAST        'diff2'

701	LOAD_FAST         'idx2id2len'
704	LOAD_FAST         'self'
707	LOAD_ATTR         '_index'
710	LOAD_CONST        2
713	BINARY_SUBTRACT   None
714	BINARY_SUBSCR     None
715	LOAD_FAST         'objId'
718	BINARY_SUBSCR     None
719	LOAD_FAST         'idx2id2len'
722	LOAD_FAST         'self'
725	LOAD_ATTR         '_index'
728	LOAD_CONST        3
731	BINARY_SUBTRACT   None
732	BINARY_SUBSCR     None
733	LOAD_FAST         'objId'
736	BINARY_SUBSCR     None
737	BINARY_SUBTRACT   None
738	STORE_FAST        'diff3'

741	LOAD_FAST         'self'
744	LOAD_ATTR         '_index'
747	LOAD_CONST        4
750	COMPARE_OP        '<='
753	JUMP_IF_FALSE     '953'

756	LOAD_FAST         'diff'
759	LOAD_CONST        0
762	COMPARE_OP        '>'
765	JUMP_IF_FALSE     '950'
768	LOAD_FAST         'diff2'
771	LOAD_CONST        0
774	COMPARE_OP        '>'
777	JUMP_IF_FALSE     '950'
780	LOAD_FAST         'diff3'
783	LOAD_CONST        0
786	COMPARE_OP        '>'
789_0	COME_FROM         '765'
789_1	COME_FROM         '777'
789	JUMP_IF_FALSE     '950'

792	LOAD_FAST         'self'
795	LOAD_ATTR         '_leakDetector'
798	LOAD_ATTR         'getContainerNameById'
801	LOAD_FAST         'objId'
804	CALL_FUNCTION_1   None
807	STORE_FAST        'name'

810	SETUP_EXCEPT      '850'

813	SETUP_LOOP        '846'
816	LOAD_FAST         'self'
819	LOAD_ATTR         '_leakDetector'
822	LOAD_ATTR         'getContainerByIdGen'
825	LOAD_FAST         'objId'
828	CALL_FUNCTION_1   None
831	GET_ITER          None
832	FOR_ITER          '845'
835	STORE_FAST        'container'

838	LOAD_CONST        None
841	YIELD_VALUE       None
842	JUMP_BACK         '832'
845	POP_BLOCK         None
846_0	COME_FROM         '813'
846	POP_BLOCK         None
847	JUMP_FORWARD      '873'
850_0	COME_FROM         '810'

850	POP_TOP           None
851	POP_TOP           None
852	POP_TOP           None

853	LOAD_FAST         'self'
856	LOAD_ATTR         'notify'
859	LOAD_ATTR         'debug'
862	LOAD_CONST        'caught exception in getContainerByIdGen (2)'
865	CALL_FUNCTION_1   None
868	POP_TOP           None
869	JUMP_FORWARD      '943'
872	END_FINALLY       None
873_0	COME_FROM         '847'

873	LOAD_CONST        '%s (%s) consistently increased in size over the last 3 periods (%s items at last measurement, current contents: %s)'
876	LOAD_FAST         'name'
879	LOAD_GLOBAL       'itype'
882	LOAD_FAST         'container'
885	CALL_FUNCTION_1   None
888	LOAD_FAST         'idx2id2len'
891	LOAD_FAST         'self'
894	LOAD_ATTR         '_index'
897	BINARY_SUBSCR     None
898	LOAD_FAST         'objId'
901	BINARY_SUBSCR     None
902	LOAD_GLOBAL       'fastRepr'
905	LOAD_FAST         'container'
908	LOAD_CONST        'maxLen'
911	LOAD_GLOBAL       'CheckContainers'
914	LOAD_ATTR         'ReprItems'
917	CALL_FUNCTION_257 None
920	BUILD_TUPLE_4     None
923	BINARY_MODULO     None
924	STORE_FAST        'msg'

927	LOAD_FAST         'self'
930	LOAD_ATTR         'notify'
933	LOAD_ATTR         'warning'
936	LOAD_FAST         'msg'
939	CALL_FUNCTION_1   None
942	POP_TOP           None
943_0	COME_FROM         '872'

943	LOAD_CONST        None
946	YIELD_VALUE       None
947	JUMP_ABSOLUTE     '1371'
950	JUMP_ABSOLUTE     '1374'

953	LOAD_FAST         'objId'
956	LOAD_FAST         'idx2id2len'
959	LOAD_FAST         'self'
962	LOAD_ATTR         '_index'
965	LOAD_CONST        4
968	BINARY_SUBTRACT   None
969	BINARY_SUBSCR     None
970	COMPARE_OP        'in'
973	JUMP_IF_FALSE     '1371'
976	LOAD_FAST         'objId'
979	LOAD_FAST         'idx2id2len'
982	LOAD_FAST         'self'
985	LOAD_ATTR         '_index'
988	LOAD_CONST        5
991	BINARY_SUBTRACT   None
992	BINARY_SUBSCR     None
993	COMPARE_OP        'in'
996_0	COME_FROM         '973'
996	JUMP_IF_FALSE     '1371'

999	LOAD_FAST         'idx2id2len'
1002	LOAD_FAST         'self'
1005	LOAD_ATTR         '_index'
1008	LOAD_CONST        3
1011	BINARY_SUBTRACT   None
1012	BINARY_SUBSCR     None
1013	LOAD_FAST         'objId'
1016	BINARY_SUBSCR     None
1017	LOAD_FAST         'idx2id2len'
1020	LOAD_FAST         'self'
1023	LOAD_ATTR         '_index'
1026	LOAD_CONST        4
1029	BINARY_SUBTRACT   None
1030	BINARY_SUBSCR     None
1031	LOAD_FAST         'objId'
1034	BINARY_SUBSCR     None
1035	BINARY_SUBTRACT   None
1036	STORE_FAST        'diff4'

1039	LOAD_FAST         'idx2id2len'
1042	LOAD_FAST         'self'
1045	LOAD_ATTR         '_index'
1048	LOAD_CONST        4
1051	BINARY_SUBTRACT   None
1052	BINARY_SUBSCR     None
1053	LOAD_FAST         'objId'
1056	BINARY_SUBSCR     None
1057	LOAD_FAST         'idx2id2len'
1060	LOAD_FAST         'self'
1063	LOAD_ATTR         '_index'
1066	LOAD_CONST        5
1069	BINARY_SUBTRACT   None
1070	BINARY_SUBSCR     None
1071	LOAD_FAST         'objId'
1074	BINARY_SUBSCR     None
1075	BINARY_SUBTRACT   None
1076	STORE_FAST        'diff5'

1079	LOAD_FAST         'diff'
1082	LOAD_CONST        0
1085	COMPARE_OP        '>'
1088	JUMP_IF_FALSE     '1368'
1091	LOAD_FAST         'diff2'
1094	LOAD_CONST        0
1097	COMPARE_OP        '>'
1100	JUMP_IF_FALSE     '1368'
1103	LOAD_FAST         'diff3'
1106	LOAD_CONST        0
1109	COMPARE_OP        '>'
1112	JUMP_IF_FALSE     '1368'
1115	LOAD_FAST         'diff4'
1118	LOAD_CONST        0
1121	COMPARE_OP        '>'
1124	JUMP_IF_FALSE     '1368'
1127	LOAD_FAST         'diff5'
1130	LOAD_CONST        0
1133	COMPARE_OP        '>'
1136_0	COME_FROM         '1088'
1136_1	COME_FROM         '1100'
1136_2	COME_FROM         '1112'
1136_3	COME_FROM         '1124'
1136	JUMP_IF_FALSE     '1368'

1139	LOAD_FAST         'self'
1142	LOAD_ATTR         '_leakDetector'
1145	LOAD_ATTR         'getContainerNameById'
1148	LOAD_FAST         'objId'
1151	CALL_FUNCTION_1   None
1154	STORE_FAST        'name'

1157	SETUP_EXCEPT      '1197'

1160	SETUP_LOOP        '1193'
1163	LOAD_FAST         'self'
1166	LOAD_ATTR         '_leakDetector'
1169	LOAD_ATTR         'getContainerByIdGen'
1172	LOAD_FAST         'objId'
1175	CALL_FUNCTION_1   None
1178	GET_ITER          None
1179	FOR_ITER          '1192'
1182	STORE_FAST        'container'

1185	LOAD_CONST        None
1188	YIELD_VALUE       None
1189	JUMP_BACK         '1179'
1192	POP_BLOCK         None
1193_0	COME_FROM         '1160'
1193	POP_BLOCK         None
1194	JUMP_FORWARD      '1220'
1197_0	COME_FROM         '1157'

1197	POP_TOP           None
1198	POP_TOP           None
1199	POP_TOP           None

1200	LOAD_FAST         'self'
1203	LOAD_ATTR         'notify'
1206	LOAD_ATTR         'debug'
1209	LOAD_CONST        'caught exception in getContainerByIdGen (3)'
1212	CALL_FUNCTION_1   None
1215	POP_TOP           None
1216	JUMP_ABSOLUTE     '1368'
1219	END_FINALLY       None
1220_0	COME_FROM         '1194'

1220	LOAD_CONST        'leak detected: %s (%s) consistently increased in size over the last 5 periods (%s items at last measurement, current contents: %s)'
1223	LOAD_FAST         'name'
1226	LOAD_GLOBAL       'itype'
1229	LOAD_FAST         'container'
1232	CALL_FUNCTION_1   None
1235	LOAD_FAST         'idx2id2len'
1238	LOAD_FAST         'self'
1241	LOAD_ATTR         '_index'
1244	BINARY_SUBSCR     None
1245	LOAD_FAST         'objId'
1248	BINARY_SUBSCR     None
1249	LOAD_GLOBAL       'fastRepr'
1252	LOAD_FAST         'container'
1255	LOAD_CONST        'maxLen'
1258	LOAD_GLOBAL       'CheckContainers'
1261	LOAD_ATTR         'ReprItems'
1264	CALL_FUNCTION_257 None
1267	BUILD_TUPLE_4     None
1270	BINARY_MODULO     None
1271	STORE_FAST        'msg'

1274	LOAD_FAST         'self'
1277	LOAD_ATTR         'notify'
1280	LOAD_ATTR         'warning'
1283	LOAD_FAST         'msg'
1286	CALL_FUNCTION_1   None
1289	POP_TOP           None

1290	LOAD_CONST        None
1293	YIELD_VALUE       None

1294	LOAD_GLOBAL       'messenger'
1297	LOAD_ATTR         'send'
1300	LOAD_FAST         'self'
1303	LOAD_ATTR         '_leakDetector'
1306	LOAD_ATTR         'getLeakEvent'
1309	CALL_FUNCTION_0   None
1312	LOAD_FAST         'container'
1315	LOAD_FAST         'name'
1318	BUILD_LIST_2      None
1321	CALL_FUNCTION_2   None
1324	POP_TOP           None

1325	LOAD_GLOBAL       'config'
1328	LOAD_ATTR         'GetBool'
1331	LOAD_CONST        'pdb-on-leak-detect'
1334	LOAD_CONST        0
1337	CALL_FUNCTION_2   None
1340	JUMP_IF_FALSE     '1365'

1343	LOAD_CONST        None
1346	IMPORT_NAME       'pdb'
1349	STORE_FAST        'pdb'
1352	LOAD_FAST         'pdb'
1355	LOAD_ATTR         'set_trace'
1358	CALL_FUNCTION_0   None
1361	POP_TOP           None
1362_0	COME_FROM         '1219'

1362	JUMP_ABSOLUTE     '1368'
1365	JUMP_ABSOLUTE     '1371'
1368	JUMP_ABSOLUTE     '1374'
1371	JUMP_ABSOLUTE     '1377'
1374	CONTINUE          '531'
1377	JUMP_BACK         '531'
1380	POP_BLOCK         None
1381_0	COME_FROM         '517'
1381	JUMP_FORWARD      '1384'
1384_0	COME_FROM         '1381'
1384	POP_BLOCK         None
1385	JUMP_FORWARD      '1428'
1388_0	COME_FROM         '0'

1388	DUP_TOP           None
1389	LOAD_GLOBAL       'Exception'
1392	COMPARE_OP        'exception match'
1395	JUMP_IF_FALSE     '1427'
1398	POP_TOP           None
1399	STORE_FAST        'e'
1402	POP_TOP           None

1403	LOAD_CONST        'CheckContainers job caught exception: %s'
1406	LOAD_FAST         'e'
1409	BINARY_MODULO     None
1410	PRINT_ITEM        None
1411	PRINT_NEWLINE_CONT None

1412	LOAD_GLOBAL       '__dev__'
1415	JUMP_IF_FALSE     '1424'

1418	RAISE_VARARGS_0   None
1421	JUMP_ABSOLUTE     '1428'
1424	JUMP_FORWARD      '1428'
1427	END_FINALLY       None
1428_0	COME_FROM         '1385'
1428_1	COME_FROM         '1427'

1428	LOAD_GLOBAL       'Job'
1431	LOAD_ATTR         'Done'
1434	YIELD_VALUE       None
1435	LOAD_CONST        None
1438	RETURN_VALUE      None

Syntax error at or near `SETUP_EXCEPT' token at offset 54


class FPTObjsOfType(Job):
    __module__ = __name__

    def __init__(self, name, leakDetector, otn, doneCallback = None):
        Job.__init__(self, name)
        self._leakDetector = leakDetector
        self.notify = self._leakDetector.notify
        self._otn = otn
        self._doneCallback = doneCallback
        self._ldde = self._leakDetector._getDestroyEvent()
        self.accept(self._ldde, self._handleLDDestroy)
        ContainerLeakDetector.addPrivateObj(self.__dict__)

    def destroy(self):
        self.ignore(self._ldde)
        self._leakDetector = None
        self._doneCallback = None
        ContainerLeakDetector.removePrivateObj(self.__dict__)
        Job.destroy(self)
        return

    def _handleLDDestroy(self):
        self.destroy()

    def getPriority(self):
        return Job.Priorities.High

    def run--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_leakDetector'
6	LOAD_ATTR         'getContainerIds'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'ids'

15	SETUP_EXCEPT      '273'

18	SETUP_LOOP        '269'
21	LOAD_FAST         'ids'
24	GET_ITER          None
25	FOR_ITER          '268'
28	STORE_FAST        'id'

31	LOAD_FAST         'self'
34	LOAD_ATTR         '_otn'
37	LOAD_ATTR         'lower'
40	CALL_FUNCTION_0   None
43	LOAD_CONST        'dict'
46	COMPARE_OP        'not in'
49	STORE_FAST        'getInstance'

52	LOAD_CONST        None
55	YIELD_VALUE       None

56	SETUP_EXCEPT      '102'

59	SETUP_LOOP        '98'
62	LOAD_FAST         'self'
65	LOAD_ATTR         '_leakDetector'
68	LOAD_ATTR         'getContainerByIdGen'
71	LOAD_FAST         'id'
74	LOAD_CONST        'getInstance'
77	LOAD_FAST         'getInstance'
80	CALL_FUNCTION_257 None
83	GET_ITER          None
84	FOR_ITER          '97'
87	STORE_FAST        'container'

90	LOAD_CONST        None
93	YIELD_VALUE       None
94	JUMP_BACK         '84'
97	POP_BLOCK         None
98_0	COME_FROM         '59'
98	POP_BLOCK         None
99	JUMP_FORWARD      '109'
102_0	COME_FROM         '56'

102	POP_TOP           None
103	POP_TOP           None
104	POP_TOP           None

105	JUMP_BACK         '25'
108	END_FINALLY       None
109_0	COME_FROM         '99'

109	LOAD_GLOBAL       'hasattr'
112	LOAD_FAST         'container'
115	LOAD_CONST        '__class__'
118	CALL_FUNCTION_2   None
121	JUMP_IF_FALSE     '139'

124	LOAD_FAST         'container'
127	LOAD_ATTR         '__class__'
130	LOAD_ATTR         '__name__'
133	STORE_FAST        'cName'
136	JUMP_FORWARD      '148'

139	LOAD_FAST         'container'
142	LOAD_ATTR         '__name__'
145	STORE_FAST        'cName'
148_0	COME_FROM         '136'

148	LOAD_FAST         'self'
151	LOAD_ATTR         '_otn'
154	LOAD_ATTR         'lower'
157	CALL_FUNCTION_0   None
160	LOAD_FAST         'cName'
163	LOAD_ATTR         'lower'
166	CALL_FUNCTION_0   None
169	COMPARE_OP        'in'
172	JUMP_IF_FALSE     '265'

175	SETUP_EXCEPT      '221'

178	SETUP_LOOP        '217'
181	LOAD_FAST         'self'
184	LOAD_ATTR         '_leakDetector'
187	LOAD_ATTR         'getContainerNameByIdGen'
190	LOAD_FAST         'id'
193	LOAD_CONST        'getInstance'
196	LOAD_FAST         'getInstance'
199	CALL_FUNCTION_257 None
202	GET_ITER          None
203	FOR_ITER          '216'
206	STORE_FAST        'ptc'

209	LOAD_CONST        None
212	YIELD_VALUE       None
213	JUMP_BACK         '203'
216	POP_BLOCK         None
217_0	COME_FROM         '178'
217	POP_BLOCK         None
218	JUMP_FORWARD      '228'
221_0	COME_FROM         '175'

221	POP_TOP           None
222	POP_TOP           None
223	POP_TOP           None

224	JUMP_ABSOLUTE     '265'
227	END_FINALLY       None
228_0	COME_FROM         '218'

228	LOAD_CONST        'GPTC('
231	LOAD_FAST         'self'
234	LOAD_ATTR         '_otn'
237	BINARY_ADD        None
238	LOAD_CONST        '):'
241	BINARY_ADD        None
242	LOAD_FAST         'self'
245	LOAD_ATTR         'getJobName'
248	CALL_FUNCTION_0   None
251	BINARY_ADD        None
252	LOAD_CONST        ': '
255	BINARY_ADD        None
256	LOAD_FAST         'ptc'
259	BINARY_ADD        None
260	PRINT_ITEM        None
261	PRINT_NEWLINE_CONT None
262_0	COME_FROM         '227'
262	JUMP_BACK         '25'
265_0	COME_FROM         '108'
265	JUMP_BACK         '25'
268	POP_BLOCK         None
269_0	COME_FROM         '18'
269	POP_BLOCK         None
270	JUMP_FORWARD      '313'
273_0	COME_FROM         '15'

273	DUP_TOP           None
274	LOAD_GLOBAL       'Exception'
277	COMPARE_OP        'exception match'
280	JUMP_IF_FALSE     '312'
283	POP_TOP           None
284	STORE_FAST        'e'
287	POP_TOP           None

288	LOAD_CONST        'FPTObjsOfType job caught exception: %s'
291	LOAD_FAST         'e'
294	BINARY_MODULO     None
295	PRINT_ITEM        None
296	PRINT_NEWLINE_CONT None

297	LOAD_GLOBAL       '__dev__'
300	JUMP_IF_FALSE     '309'

303	RAISE_VARARGS_0   None
306	JUMP_ABSOLUTE     '313'
309	JUMP_FORWARD      '313'
312	END_FINALLY       None
313_0	COME_FROM         '270'
313_1	COME_FROM         '312'

313	LOAD_GLOBAL       'Job'
316	LOAD_ATTR         'Done'
319	YIELD_VALUE       None
320	LOAD_CONST        None
323	RETURN_VALUE      None

Syntax error at or near `SETUP_EXCEPT' token at offset 56

    def finished(self):
        if self._doneCallback:
            self._doneCallback(self)


class FPTObjsNamed(Job):
    __module__ = __name__

    def __init__(self, name, leakDetector, on, doneCallback = None):
        Job.__init__(self, name)
        self._leakDetector = leakDetector
        self.notify = self._leakDetector.notify
        self._on = on
        self._doneCallback = doneCallback
        self._ldde = self._leakDetector._getDestroyEvent()
        self.accept(self._ldde, self._handleLDDestroy)
        ContainerLeakDetector.addPrivateObj(self.__dict__)

    def destroy(self):
        self.ignore(self._ldde)
        self._leakDetector = None
        self._doneCallback = None
        ContainerLeakDetector.removePrivateObj(self.__dict__)
        Job.destroy(self)
        return

    def _handleLDDestroy(self):
        self.destroy()

    def getPriority(self):
        return Job.Priorities.High

    def run--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_leakDetector'
6	LOAD_ATTR         'getContainerIds'
9	CALL_FUNCTION_0   None
12	STORE_FAST        'ids'

15	SETUP_EXCEPT      '223'

18	SETUP_LOOP        '219'
21	LOAD_FAST         'ids'
24	GET_ITER          None
25	FOR_ITER          '218'
28	STORE_FAST        'id'

31	LOAD_CONST        None
34	YIELD_VALUE       None

35	SETUP_EXCEPT      '75'

38	SETUP_LOOP        '71'
41	LOAD_FAST         'self'
44	LOAD_ATTR         '_leakDetector'
47	LOAD_ATTR         'getContainerByIdGen'
50	LOAD_FAST         'id'
53	CALL_FUNCTION_1   None
56	GET_ITER          None
57	FOR_ITER          '70'
60	STORE_FAST        'container'

63	LOAD_CONST        None
66	YIELD_VALUE       None
67	JUMP_BACK         '57'
70	POP_BLOCK         None
71_0	COME_FROM         '38'
71	POP_BLOCK         None
72	JUMP_FORWARD      '82'
75_0	COME_FROM         '35'

75	POP_TOP           None
76	POP_TOP           None
77	POP_TOP           None

78	JUMP_BACK         '25'
81	END_FINALLY       None
82_0	COME_FROM         '72'

82	LOAD_FAST         'self'
85	LOAD_ATTR         '_leakDetector'
88	LOAD_ATTR         '_id2ref'
91	LOAD_FAST         'id'
94	BINARY_SUBSCR     None
95	LOAD_ATTR         'getFinalIndirectionStr'
98	CALL_FUNCTION_0   None
101	STORE_FAST        'name'

104	LOAD_FAST         'self'
107	LOAD_ATTR         '_on'
110	LOAD_ATTR         'lower'
113	CALL_FUNCTION_0   None
116	LOAD_FAST         'name'
119	LOAD_ATTR         'lower'
122	CALL_FUNCTION_0   None
125	COMPARE_OP        'in'
128	JUMP_IF_FALSE     '215'

131	SETUP_EXCEPT      '171'

134	SETUP_LOOP        '167'
137	LOAD_FAST         'self'
140	LOAD_ATTR         '_leakDetector'
143	LOAD_ATTR         'getContainerNameByIdGen'
146	LOAD_FAST         'id'
149	CALL_FUNCTION_1   None
152	GET_ITER          None
153	FOR_ITER          '166'
156	STORE_FAST        'ptc'

159	LOAD_CONST        None
162	YIELD_VALUE       None
163	JUMP_BACK         '153'
166	POP_BLOCK         None
167_0	COME_FROM         '134'
167	POP_BLOCK         None
168	JUMP_FORWARD      '178'
171_0	COME_FROM         '131'

171	POP_TOP           None
172	POP_TOP           None
173	POP_TOP           None

174	JUMP_ABSOLUTE     '215'
177	END_FINALLY       None
178_0	COME_FROM         '168'

178	LOAD_CONST        'GPTCN('
181	LOAD_FAST         'self'
184	LOAD_ATTR         '_on'
187	BINARY_ADD        None
188	LOAD_CONST        '):'
191	BINARY_ADD        None
192	LOAD_FAST         'self'
195	LOAD_ATTR         'getJobName'
198	CALL_FUNCTION_0   None
201	BINARY_ADD        None
202	LOAD_CONST        ': '
205	BINARY_ADD        None
206	LOAD_FAST         'ptc'
209	BINARY_ADD        None
210	PRINT_ITEM        None
211	PRINT_NEWLINE_CONT None
212_0	COME_FROM         '177'
212	JUMP_BACK         '25'
215_0	COME_FROM         '81'
215	JUMP_BACK         '25'
218	POP_BLOCK         None
219_0	COME_FROM         '18'
219	POP_BLOCK         None
220	JUMP_FORWARD      '263'
223_0	COME_FROM         '15'

223	DUP_TOP           None
224	LOAD_GLOBAL       'Exception'
227	COMPARE_OP        'exception match'
230	JUMP_IF_FALSE     '262'
233	POP_TOP           None
234	STORE_FAST        'e'
237	POP_TOP           None

238	LOAD_CONST        'FPTObjsNamed job caught exception: %s'
241	LOAD_FAST         'e'
244	BINARY_MODULO     None
245	PRINT_ITEM        None
246	PRINT_NEWLINE_CONT None

247	LOAD_GLOBAL       '__dev__'
250	JUMP_IF_FALSE     '259'

253	RAISE_VARARGS_0   None
256	JUMP_ABSOLUTE     '263'
259	JUMP_FORWARD      '263'
262	END_FINALLY       None
263_0	COME_FROM         '220'
263_1	COME_FROM         '262'

263	LOAD_GLOBAL       'Job'
266	LOAD_ATTR         'Done'
269	YIELD_VALUE       None
270	LOAD_CONST        None
273	RETURN_VALUE      None

Syntax error at or near `SETUP_EXCEPT' token at offset 35

    def finished(self):
        if self._doneCallback:
            self._doneCallback(self)


class PruneObjectRefs(Job):
    __module__ = __name__

    def __init__(self, name, leakDetector):
        Job.__init__(self, name)
        self._leakDetector = leakDetector
        self.notify = self._leakDetector.notify
        ContainerLeakDetector.addPrivateObj(self.__dict__)

    def destroy(self):
        ContainerLeakDetector.removePrivateObj(self.__dict__)
        Job.destroy(self)

    def getPriority(self):
        return Job.Priorities.Normal

    def run--- This code section failed: ---

0	SETUP_EXCEPT      '306'

3	LOAD_FAST         'self'
6	LOAD_ATTR         '_leakDetector'
9	LOAD_ATTR         'getContainerIds'
12	CALL_FUNCTION_0   None
15	STORE_FAST        'ids'

18	SETUP_LOOP        '102'
21	LOAD_FAST         'ids'
24	GET_ITER          None
25	FOR_ITER          '101'
28	STORE_FAST        'id'

31	LOAD_CONST        None
34	YIELD_VALUE       None

35	SETUP_EXCEPT      '75'

38	SETUP_LOOP        '71'
41	LOAD_FAST         'self'
44	LOAD_ATTR         '_leakDetector'
47	LOAD_ATTR         'getContainerByIdGen'
50	LOAD_FAST         'id'
53	CALL_FUNCTION_1   None
56	GET_ITER          None
57	FOR_ITER          '70'
60	STORE_FAST        'container'

63	LOAD_CONST        None
66	YIELD_VALUE       None
67	JUMP_BACK         '57'
70	POP_BLOCK         None
71_0	COME_FROM         '38'
71	POP_BLOCK         None
72	JUMP_BACK         '25'
75_0	COME_FROM         '35'

75	POP_TOP           None
76	POP_TOP           None
77	POP_TOP           None

78	LOAD_FAST         'self'
81	LOAD_ATTR         '_leakDetector'
84	LOAD_ATTR         'removeContainerById'
87	LOAD_FAST         'id'
90	CALL_FUNCTION_1   None
93	POP_TOP           None
94	JUMP_BACK         '25'
97	END_FINALLY       None
98_0	COME_FROM         '97'
98	JUMP_BACK         '25'
101	POP_BLOCK         None
102_0	COME_FROM         '18'

102	LOAD_FAST         'self'
105	LOAD_ATTR         '_leakDetector'
108	LOAD_ATTR         '_findContainersJob'
111	LOAD_ATTR         '_id2baseStartRef'
114	STORE_FAST        '_id2baseStartRef'

117	LOAD_FAST         '_id2baseStartRef'
120	LOAD_ATTR         'keys'
123	CALL_FUNCTION_0   None
126	STORE_FAST        'ids'

129	SETUP_LOOP        '202'
132	LOAD_FAST         'ids'
135	GET_ITER          None
136	FOR_ITER          '201'
139	STORE_FAST        'id'

142	LOAD_CONST        None
145	YIELD_VALUE       None

146	SETUP_EXCEPT      '184'

149	SETUP_LOOP        '180'
152	LOAD_FAST         '_id2baseStartRef'
155	LOAD_FAST         'id'
158	BINARY_SUBSCR     None
159	LOAD_ATTR         'getContainerGen'
162	CALL_FUNCTION_0   None
165	GET_ITER          None
166	FOR_ITER          '179'
169	STORE_FAST        'container'

172	LOAD_CONST        None
175	YIELD_VALUE       None
176	JUMP_BACK         '166'
179	POP_BLOCK         None
180_0	COME_FROM         '149'
180	POP_BLOCK         None
181	JUMP_BACK         '136'
184_0	COME_FROM         '146'

184	POP_TOP           None
185	POP_TOP           None
186	POP_TOP           None

187	LOAD_FAST         '_id2baseStartRef'
190	LOAD_FAST         'id'
193	DELETE_SUBSCR     None
194	JUMP_BACK         '136'
197	END_FINALLY       None
198_0	COME_FROM         '197'
198	JUMP_BACK         '136'
201	POP_BLOCK         None
202_0	COME_FROM         '129'

202	LOAD_FAST         'self'
205	LOAD_ATTR         '_leakDetector'
208	LOAD_ATTR         '_findContainersJob'
211	LOAD_ATTR         '_id2discoveredStartRef'
214	STORE_FAST        '_id2discoveredStartRef'

217	LOAD_FAST         '_id2discoveredStartRef'
220	LOAD_ATTR         'keys'
223	CALL_FUNCTION_0   None
226	STORE_FAST        'ids'

229	SETUP_LOOP        '302'
232	LOAD_FAST         'ids'
235	GET_ITER          None
236	FOR_ITER          '301'
239	STORE_FAST        'id'

242	LOAD_CONST        None
245	YIELD_VALUE       None

246	SETUP_EXCEPT      '284'

249	SETUP_LOOP        '280'
252	LOAD_FAST         '_id2discoveredStartRef'
255	LOAD_FAST         'id'
258	BINARY_SUBSCR     None
259	LOAD_ATTR         'getContainerGen'
262	CALL_FUNCTION_0   None
265	GET_ITER          None
266	FOR_ITER          '279'
269	STORE_FAST        'container'

272	LOAD_CONST        None
275	YIELD_VALUE       None
276	JUMP_BACK         '266'
279	POP_BLOCK         None
280_0	COME_FROM         '249'
280	POP_BLOCK         None
281	JUMP_BACK         '236'
284_0	COME_FROM         '246'

284	POP_TOP           None
285	POP_TOP           None
286	POP_TOP           None

287	LOAD_FAST         '_id2discoveredStartRef'
290	LOAD_FAST         'id'
293	DELETE_SUBSCR     None
294	JUMP_BACK         '236'
297	END_FINALLY       None
298_0	COME_FROM         '297'
298	JUMP_BACK         '236'
301	POP_BLOCK         None
302_0	COME_FROM         '229'
302	POP_BLOCK         None
303	JUMP_FORWARD      '346'
306_0	COME_FROM         '0'

306	DUP_TOP           None
307	LOAD_GLOBAL       'Exception'
310	COMPARE_OP        'exception match'
313	JUMP_IF_FALSE     '345'
316	POP_TOP           None
317	STORE_FAST        'e'
320	POP_TOP           None

321	LOAD_CONST        'PruneObjectRefs job caught exception: %s'
324	LOAD_FAST         'e'
327	BINARY_MODULO     None
328	PRINT_ITEM        None
329	PRINT_NEWLINE_CONT None

330	LOAD_GLOBAL       '__dev__'
333	JUMP_IF_FALSE     '342'

336	RAISE_VARARGS_0   None
339	JUMP_ABSOLUTE     '346'
342	JUMP_FORWARD      '346'
345	END_FINALLY       None
346_0	COME_FROM         '303'
346_1	COME_FROM         '345'

346	LOAD_GLOBAL       'Job'
349	LOAD_ATTR         'Done'
352	YIELD_VALUE       None
353	LOAD_CONST        None
356	RETURN_VALUE      None

Syntax error at or near `SETUP_EXCEPT' token at offset 35


class ContainerLeakDetector(Job):
    __module__ = __name__
    notify = directNotify.newCategory('ContainerLeakDetector')
    PrivateIds = set()

    def __init__(self, name, firstCheckDelay = None):
        Job.__init__(self, name)
        self._serialNum = serialNum()
        self._findContainersJob = None
        self._checkContainersJob = None
        self._pruneContainersJob = None
        if firstCheckDelay is None:
            firstCheckDelay = 60.0 * 15.0
        self._nextCheckDelay = firstCheckDelay / 2.0
        self._checkDelayScale = config.GetFloat('leak-detector-check-delay-scale', 1.5)
        self._pruneTaskPeriod = config.GetFloat('leak-detector-prune-period', 60.0 * 30.0)
        self._id2ref = {}
        self._index2containerId2len = {}
        self._index2delay = {}
        if config.GetBool('leak-container', 0):
            _createContainerLeak()
        if config.GetBool('leak-tasks', 0):
            _createTaskLeak()
        ContainerLeakDetector.addPrivateObj(ContainerLeakDetector.PrivateIds)
        ContainerLeakDetector.addPrivateObj(self.__dict__)
        self.setPriority(Job.Priorities.Min)
        jobMgr.add(self)
        return

    def destroy(self):
        messenger.send(self._getDestroyEvent())
        self.ignoreAll()
        if self._pruneContainersJob is not None:
            jobMgr.remove(self._pruneContainersJob)
            self._pruneContainersJob = None
        if self._checkContainersJob is not None:
            jobMgr.remove(self._checkContainersJob)
            self._checkContainersJob = None
        jobMgr.remove(self._findContainersJob)
        self._findContainersJob = None
        del self._id2ref
        del self._index2containerId2len
        del self._index2delay
        return

    def _getDestroyEvent(self):
        return 'cldDestroy-%s' % self._serialNum

    def getLeakEvent(self):
        return 'containerLeakDetected-%s' % self._serialNum

    @classmethod
    def addPrivateObj(cls, obj):
        cls.PrivateIds.add(id(obj))

    @classmethod
    def removePrivateObj(cls, obj):
        cls.PrivateIds.remove(id(obj))

    def _getCheckTaskName(self):
        return 'checkForLeakingContainers-%s' % self._serialNum

    def _getPruneTaskName(self):
        return 'pruneLeakingContainerRefs-%s' % self._serialNum

    def getContainerIds(self):
        return self._id2ref.keys()

    def getContainerByIdGen(self, id, **kwArgs):
        return self._id2ref[id].getContainerGen(**kwArgs)

    def getContainerById(self, id):
        for result in self._id2ref[id].getContainerGen():
            pass

        return result

    def getContainerNameByIdGen(self, id, **kwArgs):
        return self._id2ref[id].getEvalStrGen(**kwArgs)

    def getContainerNameById(self, id):
        if id in self._id2ref:
            return repr(self._id2ref[id])
        return '<unknown container>'

    def removeContainerById(self, id):
        if id in self._id2ref:
            self._id2ref[id].destroy()
            del self._id2ref[id]

    def run--- This code section failed: ---

0	LOAD_GLOBAL       'FindContainers'
3	LOAD_CONST        '%s-findContainers'
6	LOAD_FAST         'self'
9	LOAD_ATTR         'getJobName'
12	CALL_FUNCTION_0   None
15	BINARY_MODULO     None
16	LOAD_FAST         'self'
19	CALL_FUNCTION_2   None
22	LOAD_FAST         'self'
25	STORE_ATTR        '_findContainersJob'

28	LOAD_GLOBAL       'jobMgr'
31	LOAD_ATTR         'add'
34	LOAD_FAST         'self'
37	LOAD_ATTR         '_findContainersJob'
40	CALL_FUNCTION_1   None
43	POP_TOP           None

44	LOAD_FAST         'self'
47	LOAD_ATTR         '_scheduleNextLeakCheck'
50	CALL_FUNCTION_0   None
53	POP_TOP           None

54	LOAD_FAST         'self'
57	LOAD_ATTR         '_scheduleNextPruning'
60	CALL_FUNCTION_0   None
63	POP_TOP           None

64	SETUP_LOOP        '84'
67	LOAD_GLOBAL       'True'
70	JUMP_IF_FALSE     '83'

73	LOAD_GLOBAL       'Job'
76	LOAD_ATTR         'Sleep'
79	YIELD_VALUE       None
80	JUMP_BACK         '67'
83	POP_BLOCK         None
84_0	COME_FROM         '64'

Syntax error at or near `POP_BLOCK' token at offset 83

    def getPathsToContainers(self, name, ot, doneCallback = None):
        j = FPTObjsOfType(name, self, ot, doneCallback)
        jobMgr.add(j)
        return j

    def getPathsToContainersNamed(self, name, on, doneCallback = None):
        j = FPTObjsNamed(name, self, on, doneCallback)
        jobMgr.add(j)
        return j

    def _scheduleNextLeakCheck(self):
        taskMgr.doMethodLater(self._nextCheckDelay, self._checkForLeaks, self._getCheckTaskName())
        self._nextCheckDelay = self._nextCheckDelay * self._checkDelayScale

    def _checkForLeaks(self, task = None):
        self._index2delay[len(self._index2containerId2len)] = self._nextCheckDelay
        self._checkContainersJob = CheckContainers('%s-checkForLeaks' % self.getJobName(), self, len(self._index2containerId2len))
        self.acceptOnce(self._checkContainersJob.getFinishedEvent(), self._scheduleNextLeakCheck)
        jobMgr.add(self._checkContainersJob)
        return task.done

    def _scheduleNextPruning(self):
        taskMgr.doMethodLater(self._pruneTaskPeriod, self._pruneObjectRefs, self._getPruneTaskName())

    def _pruneObjectRefs(self, task = None):
        self._pruneContainersJob = PruneObjectRefs('%s-pruneObjectRefs' % self.getJobName(), self)
        self.acceptOnce(self._pruneContainersJob.getFinishedEvent(), self._scheduleNextPruning)
        jobMgr.add(self._pruneContainersJob)
        return task.done# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:32 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ContainerLeakDetector.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'FindContainers'
3	LOAD_CONST        '%s-findContainers'
6	LOAD_FAST         'self'
9	LOAD_ATTR         'getJobName'
12	CALL_FUNCTION_0   None
15	BINARY_MODULO     None
16	LOAD_FAST         'self'
19	CALL_FUNCTION_2   None
22	LOAD_FAST         'self'
25	STORE_ATTR        '_findContainersJob'

28	LOAD_GLOBAL       'jobMgr'
31	LOAD_ATTR         'add'
34	LOAD_FAST         'self'
37	LOAD_ATTR         '_findContainersJob'
40	CALL_FUNCTION_1   None
43	POP_TOP           None

44	LOAD_FAST         'self'
47	LOAD_ATTR         '_scheduleNextLeakCheck'
50	CALL_FUNCTION_0   None
53	POP_TOP           None

54	LOAD_FAST         'self'
57	LOAD_ATTR         '_scheduleNextPruning'
60	CALL_FUNCTION_0   None
63	POP_TOP           None

64	SETUP_LOOP        '84'
67	LOAD_GLOBAL       'True'
70	JUMP_IF_FALSE     '83'

73	LOAD_GLOBAL       'Job'
76	LOAD_ATTR         'Sleep'
79	YIELD_VALUE       None
80	JUMP_BACK         '67'
83	POP_BLOCK         None
84_0	COME_FROM         '64'

Syntax error at or near `POP_BLOCK' token at offset 83

