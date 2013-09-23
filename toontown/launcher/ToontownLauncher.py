--- This code section failed: ---

0	LOAD_CONST        None
3	IMPORT_NAME       'os'
6	STORE_NAME        'os'

9	LOAD_CONST        None
12	IMPORT_NAME       'sys'
15	STORE_NAME        'sys'

18	LOAD_CONST        None
21	IMPORT_NAME       'time'
24	STORE_NAME        'time'

27	LOAD_CONST        None
30	IMPORT_NAME       'types'
33	STORE_NAME        'types'

36	LOAD_NAME         'time'
39	LOAD_ATTR         'localtime'
42	CALL_FUNCTION_0   None
45	STORE_NAME        'ltime'

48	LOAD_CONST        '%02d%02d%02d_%02d%02d%02d'
51	LOAD_NAME         'ltime'
54	LOAD_CONST        0
57	BINARY_SUBSCR     None
58	LOAD_CONST        2000
61	BINARY_SUBTRACT   None
62	LOAD_NAME         'ltime'
65	LOAD_CONST        1
68	BINARY_SUBSCR     None
69	LOAD_NAME         'ltime'
72	LOAD_CONST        2
75	BINARY_SUBSCR     None
76	LOAD_NAME         'ltime'
79	LOAD_CONST        3
82	BINARY_SUBSCR     None
83	LOAD_NAME         'ltime'
86	LOAD_CONST        4
89	BINARY_SUBSCR     None
90	LOAD_NAME         'ltime'
93	LOAD_CONST        5
96	BINARY_SUBSCR     None
97	BUILD_TUPLE_6     None
100	BINARY_MODULO     None
101	STORE_NAME        'logSuffix'

104	LOAD_CONST        'toontownD-'
107	LOAD_NAME         'logSuffix'
110	BINARY_ADD        None
111	LOAD_CONST        '.log'
114	BINARY_ADD        None
115	STORE_NAME        'logfile'

118	LOAD_CONST        'LogAndOutput'
121	BUILD_TUPLE_0     None
124	LOAD_CONST        '<code_object LogAndOutput>'
127	MAKE_FUNCTION_0   None
130	CALL_FUNCTION_0   None
133	BUILD_CLASS       None
134	STORE_NAME        'LogAndOutput'

137	LOAD_NAME         'open'
140	LOAD_NAME         'logfile'
143	LOAD_CONST        'a'
146	CALL_FUNCTION_2   None
149	STORE_NAME        'log'

152	LOAD_NAME         'LogAndOutput'
155	LOAD_NAME         'sys'
158	LOAD_ATTR         '__stdout__'
161	LOAD_NAME         'log'
164	CALL_FUNCTION_2   None
167	STORE_NAME        'logOut'

170	LOAD_NAME         'LogAndOutput'
173	LOAD_NAME         'sys'
176	LOAD_ATTR         '__stderr__'
179	LOAD_NAME         'log'
182	CALL_FUNCTION_2   None
185	STORE_NAME        'logErr'

188	LOAD_NAME         'logOut'
191	LOAD_NAME         'sys'
194	STORE_ATTR        'stdout'

197	LOAD_NAME         'logErr'
200	LOAD_NAME         'sys'
203	STORE_ATTR        'stderr'

206	LOAD_CONST        '\n\nStarting Toontown...'
209	PRINT_ITEM        None
210	PRINT_NEWLINE_CONT None

211	LOAD_CONST        'Current time: '
214	LOAD_NAME         'time'
217	LOAD_ATTR         'asctime'
220	LOAD_NAME         'time'
223	LOAD_ATTR         'localtime'
226	LOAD_NAME         'time'
229	LOAD_ATTR         'time'
232	CALL_FUNCTION_0   None
235	CALL_FUNCTION_1   None
238	CALL_FUNCTION_1   None
241	BINARY_ADD        None
242	LOAD_CONST        ' '
245	BINARY_ADD        None
246	LOAD_NAME         'time'
249	LOAD_ATTR         'tzname'
252	LOAD_CONST        0
255	BINARY_SUBSCR     None
256	BINARY_ADD        None
257	PRINT_ITEM        None
258	PRINT_NEWLINE_CONT None

259	LOAD_CONST        'sys.path = '
262	PRINT_ITEM        None
263	LOAD_NAME         'sys'
266	LOAD_ATTR         'path'
269	PRINT_ITEM_CONT   None
270	PRINT_NEWLINE_CONT None

271	LOAD_CONST        'sys.argv = '
274	PRINT_ITEM        None
275	LOAD_NAME         'sys'
278	LOAD_ATTR         'argv'
281	PRINT_ITEM_CONT   None
282	PRINT_NEWLINE_CONT None
283	JUMP_FORWARD      '286'
286_0	COME_FROM         '283'

286	LOAD_CONST        ('LauncherBase',)
289	IMPORT_NAME       'otp.launcher.LauncherBase'
292	IMPORT_FROM       'LauncherBase'
295	STORE_NAME        'LauncherBase'
298	POP_TOP           None

299	LOAD_CONST        ('OTPLauncherGlobals',)
302	IMPORT_NAME       'otp.otpbase'
305	IMPORT_FROM       'OTPLauncherGlobals'
308	STORE_NAME        'OTPLauncherGlobals'
311	POP_TOP           None

312	LOAD_CONST        ('*',)
315	IMPORT_NAME       'pandac.libpandaexpressModules'
318	IMPORT_STAR       None

319	LOAD_CONST        ('TTLocalizer',)
322	IMPORT_NAME       'toontown.toonbase'
325	IMPORT_FROM       'TTLocalizer'
328	STORE_NAME        'TTLocalizer'
331	POP_TOP           None

332	LOAD_CONST        'ToontownLauncher'
335	LOAD_NAME         'LauncherBase'
338	BUILD_TUPLE_1     None
341	LOAD_CONST        '<code_object ToontownLauncher>'
344	MAKE_FUNCTION_0   None
347	CALL_FUNCTION_0   None
350	BUILD_CLASS       None
351	STORE_NAME        'ToontownLauncher'

Syntax error at or near `COME_FROM' token at offset 286_0


