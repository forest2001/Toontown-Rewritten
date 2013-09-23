

class PickANamePattern:
    __module__ = __name__

    def __init__(self, nameStr, gender):
        self._nameStr = nameStr
        self._namePattern = self._compute(self._nameStr, gender)

    def hasNamePattern(self):
        return self._namePattern is not None

    def getNamePattern(self):
        return self._namePattern

    def getNameString(self, pattern, gender):
        nameParts = self._getNameParts(gender)
        invNameParts = []
        for i in xrange(len(nameParts)):
            invNameParts.append(invertDict(nameParts[i]))

        name = ''
        for i in xrange(len(pattern)):
            if pattern[i] != -1:
                if len(name):
                    name += ' '
                name += invNameParts[i][pattern[i]]

        return name

    def getNamePartString(self, gender, patternIndex, partIndex):
        nameParts = self._getNameParts(gender)
        invNamePart = invertDict(nameParts[patternIndex])
        return invNamePart[partIndex]

    def _genWordListSplitPermutations--- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'words'
6	CALL_FUNCTION_1   None
9	JUMP_IF_TRUE      '19'

12	LOAD_CONST        None
15	RETURN_VALUE      None
16	JUMP_FORWARD      '19'
19_0	COME_FROM         '16'

19	LOAD_GLOBAL       'len'
22	LOAD_FAST         'words'
25	CALL_FUNCTION_1   None
28	LOAD_CONST        1
31	COMPARE_OP        '=='
34	JUMP_IF_FALSE     '48'

37	LOAD_FAST         'words'
40	YIELD_VALUE       None

41	LOAD_CONST        None
44	RETURN_VALUE      None
45	JUMP_FORWARD      '48'
48_0	COME_FROM         '45'

48	SETUP_LOOP        '124'
51	LOAD_FAST         'self'
54	LOAD_ATTR         '_genWordListSplitPermutations'
57	LOAD_FAST         'words'
60	LOAD_CONST        1
63	SLICE+1           None
64	CALL_FUNCTION_1   None
67	GET_ITER          None
68	FOR_ITER          '123'
71	STORE_FAST        'permutation'

74	LOAD_FAST         'words'
77	LOAD_CONST        0
80	BINARY_SUBSCR     None
81	BUILD_LIST_1      None
84	LOAD_FAST         'permutation'
87	BINARY_ADD        None
88	YIELD_VALUE       None

89	LOAD_FAST         'words'
92	LOAD_CONST        0
95	BINARY_SUBSCR     None
96	LOAD_CONST        ' '
99	BINARY_ADD        None
100	LOAD_FAST         'permutation'
103	LOAD_CONST        0
106	BINARY_SUBSCR     None
107	BINARY_ADD        None
108	BUILD_LIST_1      None
111	LOAD_FAST         'permutation'
114	LOAD_CONST        1
117	SLICE+1           None
118	BINARY_ADD        None
119	YIELD_VALUE       None
120	JUMP_BACK         '68'
123	POP_BLOCK         None
124_0	COME_FROM         '48'

Syntax error at or near `RETURN_VALUE' token at offset 44

    def _genNameSplitPermutations--- This code section failed: ---

0	SETUP_LOOP        '36'
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_genWordListSplitPermutations'
9	LOAD_FAST         'name'
12	LOAD_ATTR         'split'
15	CALL_FUNCTION_0   None
18	CALL_FUNCTION_1   None
21	GET_ITER          None
22	FOR_ITER          '35'
25	STORE_FAST        'splitName'

28	LOAD_FAST         'splitName'
31	YIELD_VALUE       None
32	JUMP_BACK         '22'
35	POP_BLOCK         None
36_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 35

    def _compute(self, nameStr, gender):
        return self._computeWithNameParts(nameStr, self._getNameParts(gender))

    def _computeWithNameParts(self, nameStr, nameParts):
        for splitPermutation in self._genNameSplitPermutations(nameStr):
            pattern = self._recursiveCompute(splitPermutation, nameParts)
            if pattern is not None:
                return pattern

        return

    def _getNameParts(self, gender):
        pass

    def _recursiveCompute(self, words, nameParts, wi = 0, nwli = 0, pattern = None):
        if wi >= len(words):
            return pattern
        if nwli >= len(nameParts):
            return
        if words[wi] in nameParts[nwli]:
            if pattern is None:
                pattern = [-1] * len(nameParts)
            word2index = nameParts[nwli]
            newPattern = pattern[:]
            newPattern[nwli] = word2index[words[wi]]
            result = self._recursiveCompute(words, nameParts, wi + 1, nwli + 1, newPattern)
            if result:
                return result
        return self._recursiveCompute(words, nameParts, wi, nwli + 1, pattern)


class PickANamePatternTwoPartLastName(PickANamePattern):
    __module__ = __name__

    def getNameString(self, pattern, gender):
        name = PickANamePattern.getNameString(self, pattern, gender)
        if pattern[-2] != -1:
            words = name.split()
            name = ''
            for word in words[:-2]:
                if len(name):
                    name += ' '
                name += word

            if len(name):
                name += ' '
            name += words[-2]
            if words[-2] in set(self._getLastNameCapPrefixes()):
                name += words[-1].capitalize()
            else:
                name += words[-1]
        return name

    def _getLastNameCapPrefixes(self):
        return []

    def _compute(self, nameStr, gender):
        nameParts = self._getNameParts(gender)
        combinedNameParts = nameParts[:-2]
        combinedNameParts.append({})
        combinedIndex2indices = {}
        lastNamePrefixesCapped = set(self._getLastNameCapPrefixes())
        k = 0
        for first, i in nameParts[-2].iteritems():
            capitalize = first in lastNamePrefixesCapped
            for second, j in nameParts[-1].iteritems():
                combinedLastName = first
                if capitalize:
                    combinedLastName += second.capitalize()
                else:
                    combinedLastName += second
                combinedNameParts[-1][combinedLastName] = k
                combinedIndex2indices[k] = (i, j)
                k += 1

        pattern = self._computeWithNameParts(nameStr, combinedNameParts)
        if pattern:
            combinedIndex = pattern[-1]
            pattern = pattern[:-1]
            pattern.append(-1)
            pattern.append(-1)
            if combinedIndex != -1:
                pattern[-2] = combinedIndex2indices[combinedIndex][0]
                pattern[-1] = combinedIndex2indices[combinedIndex][1]
        return pattern

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\namepanel\PickANamePattern.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '36'
3	LOAD_FAST         'self'
6	LOAD_ATTR         '_genWordListSplitPermutations'
9	LOAD_FAST         'name'
12	LOAD_ATTR         'split'
15	CALL_FUNCTION_0   None
18	CALL_FUNCTION_1   None
21	GET_ITER          None
22	FOR_ITER          '35'
25	STORE_FAST        'splitName'

28	LOAD_FAST         'splitName'
31	YIELD_VALUE       None
32	JUMP_BACK         '22'
35	POP_BLOCK         None
36_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 35

