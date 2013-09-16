# 2013.08.22 22:14:54 Pacific Daylight Time
# Embedded file name: direct.task.FrameProfiler
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.StatePush import FunctionCall
from direct.showbase.PythonUtil import formatTimeExact, normalDistrib
from direct.task import Task

class FrameProfiler():
    __module__ = __name__
    notify = directNotify.newCategory('FrameProfiler')
    Minute = 60
    Hour = 60 * Minute
    Day = 24 * Hour

    def __init__(self):
        Hour = FrameProfiler.Hour
        self._period = 2 * FrameProfiler.Minute
        if config.GetBool('frequent-frame-profiles', 0):
            self._period = 1 * FrameProfiler.Minute
        self._jitterMagnitude = self._period * 0.75
        self._logSchedule = [1 * FrameProfiler.Hour,
         4 * FrameProfiler.Hour,
         12 * FrameProfiler.Hour,
         1 * FrameProfiler.Day]
        if config.GetBool('frequent-frame-profiles', 0):
            self._logSchedule = [1 * FrameProfiler.Minute,
             4 * FrameProfiler.Minute,
             12 * FrameProfiler.Minute,
             24 * FrameProfiler.Minute]
        for t in self._logSchedule:
            pass

        for i in xrange(len(self._logSchedule)):
            e = self._logSchedule[i]
            for j in xrange(i, len(self._logSchedule)):
                pass

        self._enableFC = FunctionCall(self._setEnabled, taskMgr.getProfileFramesSV())
        self._enableFC.pushCurrentState()

    def destroy(self):
        self._enableFC.set(False)
        self._enableFC.destroy()

    def _setEnabled(self, enabled):
        if enabled:
            self.notify.info('frame profiler started')
            self._startTime = globalClock.getFrameTime()
            self._profileCounter = 0
            self._jitter = None
            self._period2aggregateProfile = {}
            self._id2session = {}
            self._id2task = {}
            self._task = taskMgr.doMethodLater(self._period, self._scheduleNextProfileDoLater, 'FrameProfilerStart-%s' % serialNum())
        else:
            self._task.remove()
            del self._task
            for session in self._period2aggregateProfile.itervalues:
                session.release()

            del self._period2aggregateProfile
            for task in self._id2task.itervalues():
                task.remove()

            del self._id2task
            for session in self._id2session.itervalues():
                session.release()

            del self._id2session
            self.notify.info('frame profiler stopped')
        return

    def _scheduleNextProfileDoLater(self, task):
        self._scheduleNextProfile()
        return task.done

    def _scheduleNextProfile(self):
        self._profileCounter += 1
        self._timeElapsed = self._profileCounter * self._period
        time = self._startTime + self._timeElapsed
        jitter = self._jitter
        if jitter is None:
            jitter = normalDistrib(-self._jitterMagnitude, self._jitterMagnitude)
            time += jitter
        else:
            time -= jitter
            jitter = None
        self._jitter = jitter
        sessionId = serialNum()
        session = taskMgr.getProfileSession('FrameProfile-%s' % sessionId)
        self._id2session[sessionId] = session
        taskMgr.profileFrames(num=1, session=session, callback=Functor(self._analyzeResults, sessionId))
        delay = max(time - globalClock.getFrameTime(), 0.0)
        self._task = taskMgr.doMethodLater(delay, self._scheduleNextProfileDoLater, 'FrameProfiler-%s' % serialNum())
        return

    def _analyzeResults(self, sessionId):
        self._id2task[sessionId] = taskMgr.add(Functor(self._doAnalysis, sessionId), 'FrameProfilerAnalysis-%s' % sessionId)

    def _doAnalysis(self, sessionId, task):
        if hasattr(task, '_generator'):
            gen = task._generator
        else:
            gen = self._doAnalysisGen(sessionId)
            task._generator = gen
        result = gen.next()
        if result == Task.done:
            del task._generator
        return result

    def _doAnalysisGen--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_period2aggregateProfile'
6	STORE_FAST        'p2ap'

9	LOAD_FAST         'self'
12	LOAD_ATTR         '_id2task'
15	LOAD_ATTR         'pop'
18	LOAD_FAST         'sessionId'
21	CALL_FUNCTION_1   None
24	POP_TOP           None

25	LOAD_FAST         'self'
28	LOAD_ATTR         '_id2session'
31	LOAD_ATTR         'pop'
34	LOAD_FAST         'sessionId'
37	CALL_FUNCTION_1   None
40	STORE_FAST        'session'

43	LOAD_FAST         'session'
46	LOAD_ATTR         'profileSucceeded'
49	CALL_FUNCTION_0   None
52	JUMP_IF_FALSE     '122'

55	LOAD_FAST         'self'
58	LOAD_ATTR         '_logSchedule'
61	LOAD_CONST        0
64	BINARY_SUBSCR     None
65	STORE_FAST        'period'

68	LOAD_FAST         'period'
71	LOAD_FAST         'self'
74	LOAD_ATTR         '_period2aggregateProfile'
77	COMPARE_OP        'not in'
80	JUMP_IF_FALSE     '102'

83	LOAD_FAST         'session'
86	LOAD_ATTR         'getReference'
89	CALL_FUNCTION_0   None
92	LOAD_FAST         'p2ap'
95	LOAD_FAST         'period'
98	STORE_SUBSCR      None
99	JUMP_ABSOLUTE     '138'

102	LOAD_FAST         'p2ap'
105	LOAD_FAST         'period'
108	BINARY_SUBSCR     None
109	LOAD_ATTR         'aggregate'
112	LOAD_FAST         'session'
115	CALL_FUNCTION_1   None
118	POP_TOP           None
119	JUMP_FORWARD      '138'

122	LOAD_FAST         'self'
125	LOAD_ATTR         'notify'
128	LOAD_ATTR         'warning'
131	LOAD_CONST        'frame profile did not succeed'
134	CALL_FUNCTION_1   None
137	POP_TOP           None
138_0	COME_FROM         '119'

138	LOAD_FAST         'session'
141	LOAD_ATTR         'release'
144	CALL_FUNCTION_0   None
147	POP_TOP           None

148	LOAD_CONST        None
151	STORE_FAST        'session'

154	LOAD_CONST        0
157	STORE_FAST        'counter'

160	SETUP_LOOP        '473'
163	LOAD_GLOBAL       'xrange'
166	LOAD_GLOBAL       'len'
169	LOAD_FAST         'self'
172	LOAD_ATTR         '_logSchedule'
175	CALL_FUNCTION_1   None
178	CALL_FUNCTION_1   None
181	GET_ITER          None
182	FOR_ITER          '472'
185	STORE_FAST        'pi'

188	LOAD_FAST         'self'
191	LOAD_ATTR         '_logSchedule'
194	LOAD_FAST         'pi'
197	BINARY_SUBSCR     None
198	STORE_FAST        'period'

201	LOAD_FAST         'self'
204	LOAD_ATTR         '_timeElapsed'
207	LOAD_FAST         'period'
210	BINARY_MODULO     None
211	LOAD_CONST        0
214	COMPARE_OP        '=='
217	JUMP_IF_FALSE     '468'

220	LOAD_FAST         'period'
223	LOAD_FAST         'p2ap'
226	COMPARE_OP        'in'
229	JUMP_IF_FALSE     '465'

232	LOAD_FAST         'counter'
235	LOAD_CONST        3
238	COMPARE_OP        '>='
241	JUMP_IF_FALSE     '260'

244	LOAD_CONST        0
247	STORE_FAST        'counter'

250	LOAD_GLOBAL       'Task'
253	LOAD_ATTR         'cont'
256	YIELD_VALUE       None
257	JUMP_FORWARD      '260'
260_0	COME_FROM         '257'

260	LOAD_FAST         'self'
263	LOAD_ATTR         'notify'
266	LOAD_ATTR         'info'
269	LOAD_CONST        'aggregate profile of sampled frames over last %s\n%s'
272	LOAD_GLOBAL       'formatTimeExact'
275	LOAD_FAST         'period'
278	CALL_FUNCTION_1   None
281	LOAD_FAST         'p2ap'
284	LOAD_FAST         'period'
287	BINARY_SUBSCR     None
288	LOAD_ATTR         'getResults'
291	CALL_FUNCTION_0   None
294	BUILD_TUPLE_2     None
297	BINARY_MODULO     None
298	CALL_FUNCTION_1   None
301	POP_TOP           None

302	LOAD_FAST         'counter'
305	LOAD_CONST        1
308	INPLACE_ADD       None
309	STORE_FAST        'counter'

312	LOAD_FAST         'pi'
315	LOAD_CONST        1
318	BINARY_ADD        None
319	STORE_FAST        'nextIndex'

322	LOAD_FAST         'nextIndex'
325	LOAD_GLOBAL       'len'
328	LOAD_FAST         'self'
331	LOAD_ATTR         '_logSchedule'
334	CALL_FUNCTION_1   None
337	COMPARE_OP        '>='
340	JUMP_IF_FALSE     '372'

343	LOAD_FAST         'period'
346	LOAD_CONST        2
349	BINARY_MULTIPLY   None
350	STORE_FAST        'nextPeriod'

353	LOAD_FAST         'self'
356	LOAD_ATTR         '_logSchedule'
359	LOAD_ATTR         'append'
362	
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\task\FrameProfiler.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_period2aggregateProfile'
6	STORE_FAST        'p2ap'

9	LOAD_FAST         'self'
12	LOAD_ATTR         '_id2task'
15	LOAD_ATTR         'pop'
18	LOAD_FAST         'sessionId'
21	CALL_FUNCTION_1   None
24	POP_TOP           None

25	LOAD_FAST         'self'
28	LOAD_ATTR         '_id2session'
31	LOAD_ATTR         'pop'
34	LOAD_FAST         'sessionId'
37	CALL_FUNCTION_1   None
40	STORE_FAST        'session'

43	LOAD_FAST         'session'
46	LOAD_ATTR         'profileSucceeded'
49	CALL_FUNCTION_0   None
52	JUMP_IF_FALSE     '122'

55	LOAD_FAST         'self'
58	LOAD_ATTR         '_logSchedule'
61	LOAD_CONST        0
64	BINARY_SUBSCR     None
65	STORE_FAST        'period'

68	LOAD_FAST         'period'
71	LOAD_FAST         'self'
74	LOAD_ATTR         '_period2aggregateProfile'
77	COMPARE_OP        'not in'
80	JUMP_IF_FALSE     '102'

83	LOAD_FAST         'session'
86	LOAD_ATTR         'getReference'
89	CALL_FUNCTION_0   None
92	LOAD_FAST         'p2ap'
95	LOAD_FAST         'period'
98	STORE_SUBSCR      None
99	JUMP_ABSOLUTE     '138'

102	LOAD_FAST         'p2ap'
105	LOAD_FAST         'period'
108	BINARY_SUBSCR     None
109	LOAD_ATTR         'aggregate'
112	LOAD_FAST         'session'
115	CALL_FUNCTION_1   None
118	POP_TOP           None
119	JUMP_FORWARD      '138'

122	LOAD_FAST         'self'
125	LOAD_ATTR         'notify'
128	LOAD_ATTR         'warning'
131	LOAD_CONST        'frame profile did not succeed'
134	CALL_FUNCTION_1   None
137	POP_TOP           None
138_0	COME_FROM         '119'

138	LOAD_FAST         'session'
141	LOAD_ATTR         'release'
144	CALL_FUNCTION_0   None
147	POP_TOP           None

148	LOAD_CONST        None
151	STORE_FAST        'session'

154	LOAD_CONST        0
157	STORE_FAST        'counter'

160	SETUP_LOOP        '473'
163	LOAD_GLOBAL       'xrange'
166	LOAD_GLOBAL       'len'
169	LOAD_FAST         'self'
172	LOAD_ATTR         '_logSchedule'
175	CALL_FUNCTION_1   None
178	CALL_FUNCTION_1   None
181	GET_ITER          None
182	FOR_ITER          '472'
185	STORE_FAST        'pi'

188	LOAD_FAST         'self'
191	LOAD_ATTR         '_logSchedule'
194	LOAD_FAST         'pi'
197	BINARY_SUBSCR     None
198	STORE_FAST        'period'

201	LOAD_FAST         'self'
204	LOAD_ATTR         '_timeElapsed'
207	LOAD_FAST         'period'
210	BINARY_MODULO     None
211	LOAD_CONST        0
214	COMPARE_OP        '=='
217	JUMP_IF_FALSE     '468'

220	LOAD_FAST         'period'
223	LOAD_FAST         'p2ap'
226	COMPARE_OP        'in'
229	JUMP_IF_FALSE     '465'

232	LOAD_FAST         'counter'
235	LOAD_CONST        3
238	COMPARE_OP        '>='
241	JUMP_IF_FALSE     '260'

244	LOAD_CONST        0
247	STORE_FAST        'counter'

250	LOAD_GLOBAL       'Task'
253	LOAD_ATTR         'cont'
256	YIELD_VALUE       None
257	JUMP_FORWARD      '260'
260_0	COME_FROM         '257'

260	LOAD_FAST         'self'
263	LOAD_ATTR         'notify'
266	LOAD_ATTR         'info'
269	LOAD_CONST        'aggregate profile of sampled frames over last %s\n%s'
272	LOAD_GLOBAL       'formatTimeExact'
275	LOAD_FAST         'period'
278	CALL_FUNCTION_1   None
281	LOAD_FAST         'p2ap'
284	LOAD_FAST         'period'
287	BINARY_SUBSCR     None
288	LOAD_ATTR         'getResults'
291	CALL_FUNCTION_0   None
294	BUILD_TUPLE_2     None
297	BINARY_MODULO     None
298	CALL_FUNCTION_1   None
301	POP_TOP           None

302	LOAD_FAST         'counter'
305	LOAD_CONST        1
308	INPLACE_ADD       None
309	STORE_FAST        'counter'

312	LOAD_FAST         'pi'
315	LOAD_LOAD_FAST         'nextPeriod'
365	CALL_FUNCTION_1   None
368	POP_TOP           None
369	JUMP_FORWARD      '385'

372	LOAD_FAST         'self'
375	LOAD_ATTR         '_logSchedule'
378	LOAD_FAST         'nextIndex'
381	BINARY_SUBSCR     None
382	STORE_FAST        'nextPeriod'
385_0	COME_FROM         '369'

385	LOAD_FAST         'nextPeriod'
388	LOAD_FAST         'p2ap'
391	COMPARE_OP        'not in'
394	JUMP_IF_FALSE     '420'

397	LOAD_FAST         'p2ap'
400	LOAD_FAST         'period'
403	BINARY_SUBSCR     None
404	LOAD_ATTR         'getReference'
407	CALL_FUNCTION_0   None
410	LOAD_FAST         'p2ap'
413	LOAD_FAST         'nextPeriod'
416	STORE_SUBSCR      None
417	JUMP_FORWARD      '441'

420	LOAD_FAST         'p2ap'
423	LOAD_FAST         'nextPeriod'
426	BINARY_SUBSCR     None
427	LOAD_ATTR         'aggregate'
430	LOAD_FAST         'p2ap'
433	LOAD_FAST         'period'
436	BINARY_SUBSCR     None
437	CALL_FUNCTION_1   None
440	POP_TOP           None
441_0	COME_FROM         '417'

441	LOAD_FAST         'p2ap'
444	LOAD_FAST         'period'
447	BINARY_SUBSCR     None
448	LOAD_ATTR         'release'
451	CALL_FUNCTION_0   None
454	POP_TOP           None

455	LOAD_FAST         'p2ap'
458	LOAD_FAST         'period'
461	DELETE_SUBSCR     None
462	JUMP_ABSOLUTE     '469'
465	JUMP_BACK         '182'

468	BREAK_LOOP        None
469	JUMP_BACK         '182'
472	POP_BLOCK         None
473_0	COME_FROM         '160'

473	LOAD_GLOBAL       'Task'
476	LOAD_ATTR         'done'
479	YIELD_VALUE       None
480	LOAD_CONST        None
483	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 260_0# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:54 Pacific Daylight Time
CONST        1
318	BINARY_ADD        None
319	STORE_FAST        'nextIndex'

322	LOAD_FAST         'nextIndex'
325	LOAD_GLOBAL       'len'
328	LOAD_FAST         'self'
331	LOAD_ATTR         '_logSchedule'
334	CALL_FUNCTION_1   None
337	COMPARE_OP        '>='
340	JUMP_IF_FALSE     '372'

343	LOAD_FAST         'period'
346	LOAD_CONST        2
349	BINARY_MULTIPLY   None
350	STORE_FAST        'nextPeriod'

353	LOAD_FAST         'self'
356	LOAD_ATTR         '_logSchedule'
359	LOAD_ATTR         'append'
362	LOAD_FAST         'nextPeriod'
365	CALL_FUNCTION_1   None
368	POP_TOP           None
369	JUMP_FORWARD      '385'

372	LOAD_FAST         'self'
375	LOAD_ATTR         '_logSchedule'
378	LOAD_FAST         'nextIndex'
381	BINARY_SUBSCR     None
382	STORE_FAST        'nextPeriod'
385_0	COME_FROM         '369'

385	LOAD_FAST         'nextPeriod'
388	LOAD_FAST         'p2ap'
391	COMPARE_OP        'not in'
394	JUMP_IF_FALSE     '420'

397	LOAD_FAST         'p2ap'
400	LOAD_FAST         'period'
403	BINARY_SUBSCR     None
404	LOAD_ATTR         'getReference'
407	CALL_FUNCTION_0   None
410	LOAD_FAST         'p2ap'
413	LOAD_FAST         'nextPeriod'
416	STORE_SUBSCR      None
417	JUMP_FORWARD      '441'

420	LOAD_FAST         'p2ap'
423	LOAD_FAST         'nextPeriod'
426	BINARY_SUBSCR     None
427	LOAD_ATTR         'aggregate'
430	LOAD_FAST         'p2ap'
433	LOAD_FAST         'period'
436	BINARY_SUBSCR     None
437	CALL_FUNCTION_1   None
440	POP_TOP           None
441_0	COME_FROM         '417'

441	LOAD_FAST         'p2ap'
444	LOAD_FAST         'period'
447	BINARY_SUBSCR     None
448	LOAD_ATTR         'release'
451	CALL_FUNCTION_0   None
454	POP_TOP           None

455	LOAD_FAST         'p2ap'
458	LOAD_FAST         'period'
461	DELETE_SUBSCR     None
462	JUMP_ABSOLUTE     '469'
465	JUMP_BACK         '182'

468	BREAK_LOOP        None
469	JUMP_BACK         '182'
472	POP_BLOCK         None
473_0	COME_FROM         '160'

473	LOAD_GLOBAL       'Task'
476	LOAD_ATTR         'done'
479	YIELD_VALUE       None
480	LOAD_CONST        None
483	RETURN_VALUE      None

Syntax error at or near `COME_FROM' token at offset 260_0

