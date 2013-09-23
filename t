[1mdiff --git a/otp/namepanel/PickANamePattern.py b/otp/namepanel/PickANamePattern.py[m
[1mindex 4de58df..af573b7 100644[m
[1m--- a/otp/namepanel/PickANamePattern.py[m
[1m+++ b/otp/namepanel/PickANamePattern.py[m
[36m@@ -32,93 +32,18 @@[m [mclass PickANamePattern:[m
         invNamePart = invertDict(nameParts[patternIndex])[m
         return invNamePart[partIndex][m
 [m
[31m-    def _genWordListSplitPermutations--- This code section failed: ---[m
[31m-[m
[31m-0	LOAD_GLOBAL       'len'[m
[31m-3	LOAD_FAST         'words'[m
[31m-6	CALL_FUNCTION_1   None[m
[31m-9	JUMP_IF_TRUE      '19'[m
[31m-[m
[31m-12	LOAD_CONST        None[m
[31m-15	RETURN_VALUE      None[m
[31m-16	JUMP_FORWARD      '19'[m
[31m-19_0	COME_FROM         '16'[m
[31m-[m
[31m-19	LOAD_GLOBAL       'len'[m
[31m-22	LOAD_FAST         'words'[m
[31m-25	CALL_FUNCTION_1   None[m
[31m-28	LOAD_CONST        1[m
[31m-31	COMPARE_OP        '=='[m
[31m-34	JUMP_IF_FALSE     '48'[m
[31m-[m
[31m-37	LOAD_FAST         'words'[m
[31m-40	YIELD_VALUE       None[m
[31m-[m
[31m-41	LOAD_CONST        None[m
[31m-44	RETURN_VALUE      None[m
[31m-45	JUMP_FORWARD      '48'[m
[31m-48_0	COME_FROM         '45'[m
[31m-[m
[31m-48	SETUP_LOOP        '124'[m
[31m-51	LOAD_FAST         'self'[m
[31m-54	LOAD_ATTR         '_genWordListSplitPermutations'[m
[31m-57	LOAD_FAST         'words'[m
[31m-60	LOAD_CONST        1[m
[31m-63	SLICE+1           None[m
[31m-64	CALL_FUNCTION_1   None[m
[31m-67	GET_ITER          None[m
[31m-68	FOR_ITER          '123'[m
[31m-71	STORE_FAST        'permutation'[m
[31m-[m
[31m-74	LOAD_FAST         'words'[m
[31m-77	LOAD_CONST        0[m
[31m-80	BINARY_SUBSCR     None[m
[31m-81	BUILD_LIST_1      None[m
[31m-84	LOAD_FAST         'permutation'[m
[31m-87	BINARY_ADD        None[m
[31m-88	YIELD_VALUE       None[m
[31m-[m
[31m-89	LOAD_FAST         'words'[m
[31m-92	LOAD_CONST        0[m
[31m-95	BINARY_SUBSCR     None[m
[31m-96	LOAD_CONST        ' '[m
[31m-99	BINARY_ADD        None[m
[31m-100	LOAD_FAST         'permutation'[m
[31m-103	LOAD_CONST        0[m
[31m-106	BINARY_SUBSCR     None[m
[31m-107	BINARY_ADD        None[m
[31m-108	BUILD_LIST_1      None[m
[31m-111	LOAD_FAST         'permutation'[m
[31m-114	LOAD_CONST        1[m
[31m-117	SLICE+1           None[m
[31m-118	BINARY_ADD        None[m
[31m-119	YIELD_VALUE       None[m
[31m-120	JUMP_BACK         '68'[m
[31m-123	POP_BLOCK         None[m
[31m-124_0	COME_FROM         '48'[m
[31m-[m
[31m-Syntax error at or near `RETURN_VALUE' token at offset 44[m
[31m-[m
[31m-    def _genNameSplitPermutations--- This code section failed: ---[m
[31m-[m
[31m-0	SETUP_LOOP        '36'[m
[31m-3	LOAD_FAST         'self'[m
[31m-6	LOAD_ATTR         '_genWordListSplitPermutations'[m
[31m-9	LOAD_FAST         'name'[m
[31m-12	LOAD_ATTR         'split'[m
[31m-15	CALL_FUNCTION_0   None[m
[31m-18	CALL_FUNCTION_1   None[m
[31m-21	GET_ITER          None[m
[31m-22	FOR_ITER          '35'[m
[31m-25	STORE_FAST        'splitName'[m
[31m-[m
[31m-28	LOAD_FAST         'splitName'[m
[31m-31	YIELD_VALUE       None[m
[31m-32	JUMP_BACK         '22'[m
[31m-35	POP_BLOCK         None[m
[31m-36_0	COME_FROM         '0'[m
[31m-[m
[31m-Syntax error at or near `POP_BLOCK' token at offset 35[m
[32m+[m[32m    def _genWordListSplitPermutations(self, words):[m
[32m+[m[32m        if not len(words):[m
[32m+[m[32m            return[m
[32m+[m[32m        if len(words) == 1:[m
[32m+[m[32m            yield words[m
[32m+[m[32m        for permutation in self._genWordListSplitPermutations(words[1:]):[m
[32m+[m[32m            yield permutation+[words[0]][m
[32m+[m[32m            yield permutation[1:] + [permutation[0] + (words[0] + ' ')][m
[32m+[m
[32m+[m[32m    def _genNameSplitPermutations(self, name):[m
[32m+[m[32m        for splitName in self._genWordListSplitPermutations(name.split()):[m
[32m+[m[32m            yield splitName[m
 [m
     def _compute(self, nameStr, gender):[m
         return self._computeWithNameParts(nameStr, self._getNameParts(gender))[m
[36m@@ -204,33 +129,3 @@[m [mclass PickANamePatternTwoPartLastName(PickANamePattern):[m
                 pattern[-2] = combinedIndex2indices[combinedIndex][0][m
                 pattern[-1] = combinedIndex2indices[combinedIndex][1][m
         return pattern[m
[31m-[m
[31m-# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\namepanel\PickANamePattern.pyc[m
[31m-Traceback (most recent call last):[m
[31m-  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main[m
[31m-    uncompyle_file(infile, outstream, showasm, showast)[m
[31m-  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file[m
[31m-    uncompyle(version, co, outstream, showasm, showast)[m
[31m-  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle[m
[31m-    raise walk.ERROR[m
[31m-ParserError: --- This code section failed: ---[m
[31m-[m
[31m-0	SETUP_LOOP        '36'[m
[31m-3	LOAD_FAST         'self'[m
[31m-6	LOAD_ATTR         '_genWordListSplitPermutations'[m
[31m-9	LOAD_FAST         'name'[m
[31m-12	LOAD_ATTR         'split'[m
[31m-15	CALL_FUNCTION_0   None[m
[31m-18	CALL_FUNCTION_1   None[m
[31m-21	GET_ITER          None[m
[31m-22	FOR_ITER          '35'[m
[31m-25	STORE_FAST        'splitName'[m
[31m-[m
[31m-28	LOAD_FAST         'splitName'[m
[31m-31	YIELD_VALUE       None[m
[31m-32	JUMP_BACK         '22'[m
[31m-35	POP_BLOCK         None[m
[31m-36_0	COME_FROM         '0'[m
[31m-[m
[31m-Syntax error at or near `POP_BLOCK' token at offset 35[m
[31m-[m
