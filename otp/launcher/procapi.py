import ctypes
from ctypes.wintypes import *
TH32CS_SNAPPROCESS = 2
INVALID_HANDLE_VALUE = -1
cwk = ctypes.windll.kernel32

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [('dwSize', DWORD),
     ('cntUsage', DWORD),
     ('th32ProcessID', DWORD),
     ('th32DefaultHeapId', HANDLE),
     ('th32ModuleID', DWORD),
     ('cntThreads', DWORD),
     ('th32ParentProcessID', DWORD),
     ('pcPriClassBase', LONG),
     ('dwFlags', DWORD),
     ('szExeFile', c_char * MAX_PATH)]


class ProcessEntryPY:

    def __init__(self, name, pid):
        self.name = name
        self.pid = pid


def getProcessList--- This code section failed: ---

0	LOAD_GLOBAL       'cwk'
3	LOAD_ATTR         'CreateToolhelp32Snapshot'
6	LOAD_GLOBAL       'TH32CS_SNAPPROCESS'
9	LOAD_CONST        0
12	CALL_FUNCTION_2   None
15	STORE_FAST        'hProcessSnap'

18	BUILD_LIST_0      None
21	STORE_FAST        'processList'

24	LOAD_FAST         'hProcessSnap'
27	LOAD_GLOBAL       'INVALID_HANDLE_VALUE'
30	COMPARE_OP        '!='
33	JUMP_IF_FALSE     '184'

36	LOAD_GLOBAL       'PROCESSENTRY32'
39	CALL_FUNCTION_0   None
42	STORE_FAST        'pe32'

45	LOAD_GLOBAL       'sizeof'
48	LOAD_FAST         'pe32'
51	CALL_FUNCTION_1   None
54	LOAD_FAST         'pe32'
57	STORE_ATTR        'dwSize'

60	LOAD_GLOBAL       'cwk'
63	LOAD_ATTR         'Process32First'
66	LOAD_FAST         'hProcessSnap'
69	LOAD_GLOBAL       'ctypes'
72	LOAD_ATTR         'byref'
75	LOAD_FAST         'pe32'
78	CALL_FUNCTION_1   None
81	CALL_FUNCTION_2   None
84	JUMP_IF_FALSE     '168'

87	SETUP_LOOP        '168'

90	LOAD_FAST         'processList'
93	LOAD_ATTR         'append'
96	LOAD_GLOBAL       'ProcessEntryPY'
99	LOAD_FAST         'pe32'
102	LOAD_ATTR         'szExeFile'
105	LOAD_ATTR         'lower'
108	CALL_FUNCTION_0   None
111	LOAD_GLOBAL       'int'
114	LOAD_FAST         'pe32'
117	LOAD_ATTR         'th32ProcessID'
120	CALL_FUNCTION_1   None
123	CALL_FUNCTION_2   None
126	CALL_FUNCTION_1   None
129	POP_TOP           None

130	LOAD_GLOBAL       'cwk'
133	LOAD_ATTR         'Process32Next'
136	LOAD_FAST         'hProcessSnap'
139	LOAD_GLOBAL       'ctypes'
142	LOAD_ATTR         'byref'
145	LOAD_FAST         'pe32'
148	CALL_FUNCTION_1   None
151	CALL_FUNCTION_2   None
154	JUMP_IF_TRUE      '161'

157	BREAK_LOOP        None
158	JUMP_BACK         '90'
161	JUMP_BACK         '90'
164	POP_BLOCK         None
165_0	COME_FROM         '87'
165	JUMP_FORWARD      '168'
168_0	COME_FROM         '165'

168	LOAD_GLOBAL       'cwk'
171	LOAD_ATTR         'CloseHandle'
174	LOAD_FAST         'hProcessSnap'
177	CALL_FUNCTION_1   None
180	POP_TOP           None
181	JUMP_FORWARD      '184'
184_0	COME_FROM         '181'

184	LOAD_FAST         'processList'
187	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 164

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\launcher\procapi.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'cwk'
3	LOAD_ATTR         'CreateToolhelp32Snapshot'
6	LOAD_GLOBAL       'TH32CS_SNAPPROCESS'
9	LOAD_CONST        0
12	CALL_FUNCTION_2   None
15	STORE_FAST        'hProcessSnap'

18	BUILD_LIST_0      None
21	STORE_FAST        'processList'

24	LOAD_FAST         'hProcessSnap'
27	LOAD_GLOBAL       'INVALID_HANDLE_VALUE'
30	COMPARE_OP        '!='
33	JUMP_IF_FALSE     '184'

36	LOAD_GLOBAL       'PROCESSENTRY32'
39	CALL_FUNCTION_0   None
42	STORE_FAST        'pe32'

45	LOAD_GLOBAL       'sizeof'
48	LOAD_FAST         'pe32'
51	CALL_FUNCTION_1   None
54	LOAD_FAST         'pe32'
57	STORE_ATTR        'dwSize'

60	LOAD_GLOBAL       'cwk'
63	LOAD_ATTR         'Process32First'
66	LOAD_FAST         'hProcessSnap'
69	LOAD_GLOBAL       'ctypes'
72	LOAD_ATTR         'byref'
75	LOAD_FAST         'pe32'
78	CALL_FUNCTION_1   None
81	CALL_FUNCTION_2   None
84	JUMP_IF_FALSE     '168'

87	SETUP_LOOP        '168'

90	LOAD_FAST         'processList'
93	LOAD_ATTR         'append'
96	LOAD_GLOBAL       'ProcessEntryPY'
99	LOAD_FAST         'pe32'
102	LOAD_ATTR         'szExeFile'
105	LOAD_ATTR         'lower'
108	CALL_FUNCTION_0   None
111	LOAD_GLOBAL       'int'
114	LOAD_FAST         'pe32'
117	LOAD_ATTR         'th32ProcessID'
120	CALL_FUNCTION_1   None
123	CALL_FUNCTION_2   None
126	CALL_FUNCTION_1   None
129	POP_TOP           None

130	LOAD_GLOBAL       'cwk'
133	LOAD_ATTR         'Process32Next'
136	LOAD_FAST         'hProcessSnap'
139	LOAD_GLOBAL       'ctypes'
142	LOAD_ATTR         'byref'
145	LOAD_FAST         'pe32'
148	CALL_FUNCTION_1   None
151	CALL_FUNCTION_2   None
154	JUMP_IF_TRUE      '161'

157	BREAK_LOOP        None
158	JUMP_BACK         '90'
161	JUMP_BACK         '90'
164	POP_BLOCK         None
165_0	COME_FROM         '87'
165	JUMP_FORWARD      '168'
168_0	COME_FROM         '165'

168	LOAD_GLOBAL       'cwk'
171	LOAD_ATTR         'CloseHandle'
174	LOAD_FAST         'hProcessSnap'
177	CALL_FUNCTION_1   None
180	POP_TOP           None
181	JUMP_FORWARD      '184'
184_0	COME_FROM         '181'

184	LOAD_FAST         'processList'
187	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 164

