# 2013.08.22 22:14:39 Pacific Daylight Time
# Embedded file name: direct.showbase.ObjectCount
from direct.showbase.Job import Job
import gc

class ObjectCount(Job):
    __module__ = __name__

    def __init__(self, name, immediate = False, doneCallback = None):
        Job.__init__(self, name)
        self._doneCallback = doneCallback
        jobMgr.add(self)
        if immediate:
            jobMgr.finish(self)

    def destroy(self):
        self._doneCallback = None
        Job.destroy(self)
        return

    def finished(self):
        if self._doneCallback:
            self._doneCallback(self)
        self.destroy()

    def run--- This code section failed: ---

0	LOAD_GLOBAL       'gc'
3	LOAD_ATTR         'get_objects'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'objs'

12	LOAD_CONST        None
15	YIELD_VALUE       None

16	BUILD_MAP         None
19	STORE_FAST        'type2count'

22	SETUP_LOOP        '87'
25	LOAD_FAST         'objs'
28	GET_ITER          None
29	FOR_ITER          '86'
32	STORE_FAST        'obj'

35	LOAD_GLOBAL       'safeTypeName'
38	LOAD_FAST         'obj'
41	CALL_FUNCTION_1   None
44	STORE_FAST        'tn'

47	LOAD_FAST         'type2count'
50	LOAD_ATTR         'setdefault'
53	LOAD_FAST         'tn'
56	LOAD_CONST        0
59	CALL_FUNCTION_2   None
62	POP_TOP           None

63	LOAD_FAST         'type2count'
66	LOAD_FAST         'tn'
69	DUP_TOPX_2        None
72	BINARY_SUBSCR     None
73	LOAD_CONST        1
76	INPLACE_ADD       None
77	ROT_THREE         None
78	STORE_SUBSCR      None

79	LOAD_CONST        None
82	YIELD_VALUE       None
83	JUMP_BACK         '29'
86	POP_BLOCK         None
87_0	COME_FROM         '22'

87	DELETE_FAST       'objs'

90	LOAD_CONST        None
93	YIELD_VALUE       None

94	LOAD_GLOBAL       'invertDictLossless'
97	LOAD_FAST         'type2count'
100	CALL_FUNCTION_1   None
103	STORE_FAST        'count2type'

106	LOAD_CONST        None
109	YIELD_VALUE       None

110	LOAD_FAST         'count2type'
113	LOAD_ATTR         'keys'
116	CALL_FUNCTION_0   None
119	STORE_FAST        'counts'

122	LOAD_CONST        None
125	YIELD_VALUE       None

126	LOAD_FAST         'counts'
129	LOAD_ATTR         'sort'
132	CALL_FUNCTION_0   None
135	POP_TOP           None

136	LOAD_CONST        None
139	YIELD_VALUE       None

140	LOAD_FAST         'counts'
143	LOAD_ATTR         'reverse'
146	CALL_FUNCTION_0   None
149	POP_TOP           None

150	LOAD_CONST        None
153	YIELD_VALUE       None

154	LOAD_CONST        "===== ObjectCount: '%s' ====="
157	LOAD_FAST         'self'
160	LOAD_ATTR         'getJobName'
163	CALL_FUNCTION_0   None
166	BINARY_MODULO     None
167	PRINT_ITEM        None
168	PRINT_NEWLINE_CONT None

169	SETUP_LOOP        '232'
172	LOAD_FAST         'counts'
175	GET_ITER          None
176	FOR_ITER          '231'
179	STORE_FAST        'count'

182	LOAD_FAST         'count2type'
185	LOAD_FAST         'count'
188	BINARY_SUBSCR     None
189	STORE_FAST        'types'

192	SETUP_LOOP        '228'
195	LOAD_FAST         'types'
198	GET_ITER          None
199	FOR_ITER          '227'
202	STORE_FAST        'type'

205	LOAD_CONST        '%s: %s'
208	LOAD_FAST         'count'
211	LOAD_FAST         'type'
214	BUILD_TUPLE_2     None
217	BINARY_MODULO     None
218	PRINT_ITEM        None
219	PRINT_NEWLINE_CONT None

220	LOAD_CONST        None
223	YIELD_VALUE       None
224	JUMP_BACK         '199'
227	POP_BLOCK         None
228_0	COME_FROM         '192'
228	JUMP_BACK         '176'
231	POP_BLOCK         None
232_0	COME_FROM         '169'

232	LOAD_GLOBAL       'Job'
235	LOAD_ATTR         'Done'
238	YIELD_VALUE       None
239	LOAD_CONST        None
242	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 19# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:39 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ObjectCount.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'gc'
3	LOAD_ATTR         'get_objects'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'objs'

12	LOAD_CONST        None
15	YIELD_VALUE       None

16	BUILD_MAP         None
19	STORE_FAST        'type2count'

22	SETUP_LOOP        '87'
25	LOAD_FAST         'objs'
28	GET_ITER          None
29	FOR_ITER          '86'
32	STORE_FAST        'obj'

35	LOAD_GLOBAL       'safeTypeName'
38	LOAD_FAST         'obj'
41	CALL_FUNCTION_1   None
44	STORE_FAST        'tn'

47	LOAD_FAST         'type2count'
50	LOAD_ATTR         'setdefault'
53	LOAD_FAST         'tn'
56	LOAD_CONST        0
59	CALL_FUNCTION_2   None
62	POP_TOP           None

63	LOAD_FAST         'type2count'
66	LOAD_FAST         'tn'
69	DUP_TOPX_2        None
72	BINARY_SUBSCR     None
73	LOAD_CONST        1
76	INPLACE_ADD       None
77	ROT_THREE         None
78	STORE_SUBSCR      None

79	LOAD_CONST        None
82	YIELD_VALUE       None
83	JUMP_BACK         '29'
86	POP_BLOCK         None
87_0	COME_FROM         '22'

87	DELETE_FAST       'objs'

90	LOAD_CONST        None
93	YIELD_VALUE       None

94	LOAD_GLOBAL       'invertDictLossless'
97	LOAD_FAST         'type2count'
100	CALL_FUNCTION_1   None
103	STORE_FAST        'count2type'

106	LOAD_CONST        None
109	YIELD_VALUE       None

110	LOAD_FAST         'count2type'
113	LOAD_ATTR         'keys'
116	CALL_FUNCTION_0   None
119	STORE_FAST        'counts'

122	LOAD_CONST        None
125	YIELD_VALUE       None

126	LOAD_FAST         'counts'
129	LOAD_ATTR         'sort'
132	CALL_FUNCTION_0   None
135	POP_TOP           None

136	LOAD_CONST        None
139	YIELD_VALUE       None

140	LOAD_FAST         'counts'
143	LOAD_ATTR         'reverse'
146	CALL_FUNCTION_0   None
149	POP_TOP           None

150	LOAD_CONST        None
153	YIELD_VALUE       None

154	LOAD_CONST        "===== ObjectCount: '%s' ====="
157	LOAD_FAST         'self'
160	LOAD_ATTR         'getJobName'
163	CALL_FUNCTION_0   None
166	BINARY_MODULO     None
167	PRINT_ITEM        None
168	PRINT_NEWLINE_CONT None

169	SETUP_LOOP        '232'
172	LOAD_FAST         'counts'
175	GET_ITER          None
176	FOR_ITER          '231'
179	STORE_FAST        'count'

182	LOAD_FAST         'count2type'
185	LOAD_FAST         'count'
188	BINARY_SUBSCR     None
189	STORE_FAST        'types'

192	SETUP_LOOP        '228'
195	LOAD_FAST         'types'
198	GET_ITER          None
199	FOR_ITER          '227'
202	STORE_FAST        'type'

205	LOAD_CONST        '%s: %s'
208	LOAD_FAST         'count'
211	LOAD_FAST         'type'
214	BUILD_TUPLE_2     None
217	BINARY_MODULO     None
218	PRINT_ITEM        None
219	PRINT_NEWLINE_CONT None

220	LOAD_CONST        None
223	YIELD_VALUE       None
224	JUMP_BACK         '199'
227	POP_BLOCK         None
228_0	COME_FROM         '192'
228	JUMP_BACK         '176'
231	POP_BLOCK         None
232_0	COME_FROM         '169'

232	LOAD_GLOBAL       'Job'
235	LOAD_ATTR         'Done'
238	YIELD_VALUE       None
239	LOAD_CONST        None
242	RETURN_VALUE      None

Syntax error at or near `STORE_FAST' token at offset 19

