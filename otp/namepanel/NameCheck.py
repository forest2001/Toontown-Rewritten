import string
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import NSError
from pandac.PandaModules import TextEncoder, TextNode
notify = DirectNotifyGlobal.directNotify.newCategory('NameCheck')

def filterString(str, filter):
    result = ''
    for char in str:
        if char in filter:
            result = result + char

    return result


def justLetters(str):
    letters = ''
    for c in str:
        if c.isalpha():
            letters = letters + c

    return letters


def justUpper(str):
    upperCaseLetters = ''
    for c in str:
        if c.upper() != c.lower():
            if c == c.upper():
                upperCaseLetters = upperCaseLetters + c

    return upperCaseLetters


def wordList(str):
    words = str.split()
    result = []
    for word in words:
        subWords = word.split('-')
        for sw in subWords:
            if sw:
                result.append(sw)

    return result


def checkName(name, otherCheckFuncs = [], font = None):

    def longEnough(name):
        if len(name) < 2:
            notify.info('name is too short')
            return OTPLocalizer.NCTooShort

    def emptyName(name):
        if name.strip() == '':
            notify.info('name is empty')
            return OTPLocalizer.NCTooShort

    def printableChars(name):
        for char in name:
            if ord(char) < 128 and char not in string.printable:
                notify.info('name contains non-printable char #%s' % ord(char))
                return OTPLocalizer.NCGeneric

    validAsciiChars = set(".,'-" + string.letters + string.whitespace)

    def _validCharacter(c, validAsciiChars = validAsciiChars, font = font):
        if c in validAsciiChars:
            return True
        if c.isalpha() or c.isspace():
            return True
        return False

    def badCharacters(name, _validCharacter = _validCharacter):
        for char in name:
            if not _validCharacter(char):
                if char in string.digits:
                    notify.info('name contains digits')
                    return OTPLocalizer.NCNoDigits
                else:
                    notify.info('name contains bad char: %s' % TextEncoder().encodeWtext(char))
                    return OTPLocalizer.NCBadCharacter % TextEncoder().encodeWtext(char)

    def fontHasCharacters(name, font = font):
        if font:
            tn = TextNode('NameCheck')
            tn.setFont(font)
            for c in name:
                if not tn.hasCharacter(ord(c)):
                    notify.info('name contains bad char: %s' % TextEncoder().encodeWtext(c))
                    return OTPLocalizer.NCBadCharacter % TextEncoder().encodeWtext(c)

    def hasLetters(name):
        words = wordList(name)
        for word in words:
            letters = justLetters(word)
            if len(letters) == 0:
                notify.info('word "%s" has no letters' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCNeedLetters

    def hasVowels(name):

        def perWord(word):
            if '.' in word:
                return None
            for char in word:
                if ord(char) >= 128:
                    return None

            letters = filterString(word, string.letters)
            if len(letters) > 2:
                vowels = filterString(letters, 'aeiouyAEIOUY')
                if len(vowels) == 0:
                    notify.info('word "%s" has no vowels' % TextEncoder().encodeWtext(word))
                    return OTPLocalizer.NCNeedVowels
            return None

        for word in wordList(name):
            problem = perWord(word)
            if problem:
                return problem

    def monoLetter(name):

        def perWord(word):
            word = word
            letters = justLetters(word)
            if len(letters) > 2:
                letters = TextEncoder().decodeText(TextEncoder.lower(TextEncoder().encodeWtext(letters)))
                filtered = filterString(letters, letters[0])
                if filtered == letters:
                    notify.info('word "%s" uses only one letter' % TextEncoder().encodeWtext(word))
                    return OTPLocalizer.NCGeneric

        for word in wordList(name):
            problem = perWord(word)
            if problem:
                return problem

    def checkDashes--- This code section failed: ---

0	LOAD_FAST         'name'
3	LOAD_CLOSURE      'i'
6	LOAD_CONST        '<code_object validDash>'
9	MAKE_CLOSURE_1    None
12	STORE_FAST        'validDash'

15	LOAD_CONST        0
18	STORE_DEREF       'i'

21	SETUP_LOOP        '119'

24	LOAD_FAST         'name'
27	LOAD_ATTR         'find'
30	LOAD_CONST        '-'
33	LOAD_DEREF        'i'
36	LOAD_GLOBAL       'len'
39	LOAD_FAST         'name'
42	CALL_FUNCTION_1   None
45	CALL_FUNCTION_3   None
48	STORE_DEREF       'i'

51	LOAD_DEREF        'i'
54	LOAD_CONST        0
57	COMPARE_OP        '<'
60	JUMP_IF_FALSE     '70'

63	LOAD_CONST        None
66	RETURN_VALUE      None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'validDash'
73	LOAD_DEREF        'i'
76	CALL_FUNCTION_1   None
79	JUMP_IF_TRUE      '105'

82	LOAD_GLOBAL       'notify'
85	LOAD_ATTR         'info'
88	LOAD_CONST        'name makes invalid use of dashes'
91	CALL_FUNCTION_1   None
94	POP_TOP           None

95	LOAD_GLOBAL       'OTPLocalizer'
98	LOAD_ATTR         'NCDashUsage'
101	RETURN_VALUE      None
102	JUMP_FORWARD      '105'
105_0	COME_FROM         '102'

105	LOAD_DEREF        'i'
108	LOAD_CONST        1
111	INPLACE_ADD       None
112	STORE_DEREF       'i'
115	JUMP_BACK         '24'
118	POP_BLOCK         None
119_0	COME_FROM         '21'
119	LOAD_CONST        None
122	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 118

    def checkCommas--- This code section failed: ---

0	LOAD_FAST         'name'
3	LOAD_CLOSURE      'i'
6	LOAD_CONST        '<code_object validComma>'
9	MAKE_CLOSURE_1    None
12	STORE_FAST        'validComma'

15	LOAD_CONST        0
18	STORE_DEREF       'i'

21	SETUP_LOOP        '122'

24	LOAD_FAST         'name'
27	LOAD_ATTR         'find'
30	LOAD_CONST        ','
33	LOAD_DEREF        'i'
36	LOAD_GLOBAL       'len'
39	LOAD_FAST         'name'
42	CALL_FUNCTION_1   None
45	CALL_FUNCTION_3   None
48	STORE_DEREF       'i'

51	LOAD_DEREF        'i'
54	LOAD_CONST        0
57	COMPARE_OP        '<'
60	JUMP_IF_FALSE     '70'

63	LOAD_CONST        None
66	RETURN_VALUE      None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'validComma'
73	LOAD_DEREF        'i'
76	CALL_FUNCTION_1   None
79	STORE_FAST        'problem'

82	LOAD_FAST         'problem'
85	JUMP_IF_FALSE     '108'

88	LOAD_GLOBAL       'notify'
91	LOAD_ATTR         'info'
94	LOAD_CONST        'name makes invalid use of commas'
97	CALL_FUNCTION_1   None
100	POP_TOP           None

101	LOAD_FAST         'problem'
104	RETURN_VALUE      None
105	JUMP_FORWARD      '108'
108_0	COME_FROM         '105'

108	LOAD_DEREF        'i'
111	LOAD_CONST        1
114	INPLACE_ADD       None
115	STORE_DEREF       'i'
118	JUMP_BACK         '24'
121	POP_BLOCK         None
122_0	COME_FROM         '21'
122	LOAD_CONST        None
125	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 121

    def checkPeriods(name):
        words = wordList(name)
        for word in words:
            if word[-1] == ',':
                word = word[:-1]
            numPeriods = word.count('.')
            if not numPeriods:
                continue
            letters = justLetters(word)
            numLetters = len(letters)
            if word[-1] != '.':
                notify.info('word "%s" does not end in a period' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCPeriodUsage
            if numPeriods > 2:
                notify.info('word "%s" has too many periods' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCPeriodUsage
            if numPeriods == 2:
                if word[1] == '.':
                    word[3] == '.' or notify.info('word "%s" does not fit the J.T. pattern' % TextEncoder().encodeWtext(word))
                    return OTPLocalizer.NCPeriodUsage

        return None

    def checkApostrophes(name):
        words = wordList(name)
        for word in words:
            numApos = word.count("'")
            if numApos > 2:
                notify.info('word "%s" has too many apostrophes.' % TextEncoder().encodeWtext(word))
                return OTPLocalizer.NCApostrophes

        numApos = name.count("'")
        if numApos > 3:
            notify.info('name has too many apostrophes.')
            return OTPLocalizer.NCApostrophes

    def tooManyWords(name):
        if len(wordList(name)) > 4:
            notify.info('name has too many words')
            return OTPLocalizer.NCTooManyWords

    def allCaps(name):
        letters = justLetters(name)
        if len(letters) > 2:
            upperLetters = TextEncoder().decodeText(TextEncoder.upper(TextEncoder().encodeWtext(letters)))
            for i in xrange(len(upperLetters)):
                if not upperLetters[0].isupper():
                    return

            if upperLetters == letters:
                notify.info('name is all caps')
                return OTPLocalizer.NCAllCaps

    def mixedCase(name):
        words = wordList(name)
        for word in words:
            if len(word) > 2:
                capitals = justUpper(word)
                if len(capitals) > 2:
                    notify.info('name has mixed case')
                    return OTPLocalizer.NCMixedCase

    def checkJapanese--- This code section failed: ---

0	LOAD_GLOBAL       'range'
3	LOAD_CONST        32
6	LOAD_CONST        33
9	CALL_FUNCTION_2   None
12	STORE_FAST        'asciiSpace'

15	LOAD_GLOBAL       'range'
18	LOAD_CONST        48
21	LOAD_CONST        64
24	CALL_FUNCTION_2   None
27	STORE_FAST        'asciiDigits'

30	LOAD_GLOBAL       'range'
33	LOAD_CONST        12353
36	LOAD_CONST        12448
39	CALL_FUNCTION_2   None
42	STORE_FAST        'hiragana'

45	LOAD_GLOBAL       'range'
48	LOAD_CONST        12449
51	LOAD_CONST        12544
54	CALL_FUNCTION_2   None
57	STORE_FAST        'katakana'

60	LOAD_GLOBAL       'range'
63	LOAD_CONST        65381
66	LOAD_CONST        65440
69	CALL_FUNCTION_2   None
72	STORE_FAST        'halfwidthKatakana'

75	LOAD_GLOBAL       'set'
78	LOAD_FAST         'asciiSpace'
81	LOAD_FAST         'halfwidthKatakana'
84	BINARY_ADD        None
85	CALL_FUNCTION_1   None
88	STORE_FAST        'halfwidthCharacter'

91	LOAD_GLOBAL       'set'
94	LOAD_FAST         'asciiSpace'
97	LOAD_FAST         'hiragana'
100	BINARY_ADD        None
101	LOAD_FAST         'katakana'
104	BINARY_ADD        None
105	LOAD_FAST         'halfwidthKatakana'
108	BINARY_ADD        None
109	CALL_FUNCTION_1   None
112	STORE_FAST        'allowedUtf8'

115	LOAD_GLOBAL       'TextEncoder'
118	CALL_FUNCTION_0   None
121	STORE_FAST        'te'

124	LOAD_CONST        0.0
127	STORE_FAST        'dc'

130	SETUP_LOOP        '294'
133	LOAD_CONST        '<code_object <generator expression>>'
136	MAKE_FUNCTION_0   None
139	LOAD_FAST         'te'
142	LOAD_ATTR         'decodeText'
145	LOAD_FAST         'name'
148	CALL_FUNCTION_1   None
151	GET_ITER          None
152	CALL_FUNCTION_1   None
155	GET_ITER          None
156	FOR_ITER          '293'
159	STORE_FAST        'char'

162	LOAD_FAST         'char'
165	LOAD_FAST         'allowedUtf8'
168	COMPARE_OP        'not in'
171	JUMP_IF_FALSE     '255'

174	LOAD_FAST         'char'
177	LOAD_FAST         'asciiDigits'
180	COMPARE_OP        'in'
183	JUMP_IF_FALSE     '209'

186	LOAD_GLOBAL       'notify'
189	LOAD_ATTR         'info'
192	LOAD_CONST        'name contains not allowed ascii digits'
195	CALL_FUNCTION_1   None
198	POP_TOP           None

199	LOAD_GLOBAL       'OTPLocalizer'
202	LOAD_ATTR         'NCNoDigits'
205	RETURN_VALUE      None
206	JUMP_ABSOLUTE     '290'

209	LOAD_GLOBAL       'notify'
212	LOAD_ATTR         'info'
215	LOAD_CONST        'name contains not allowed utf8 char: 0x%04x'
218	LOAD_FAST         'char'
221	BINARY_MODU
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\otp\namepanel\NameCheck.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_GLOBAL       'range'
3	LOAD_CONST        32
6	LOAD_CONST        33
9	CALL_FUNCTION_2   None
12	STORE_FAST        'asciiSpace'

15	LOAD_GLOBAL       'range'
18	LOAD_CONST        48
21	LOAD_CONST        64
24	CALL_FUNCTION_2   None
27	STORE_FAST        'asciiDigits'

30	LOAD_GLOBAL       'range'
33	LOAD_CONST        12353
36	LOAD_CONST        12448
39	CALL_FUNCTION_2   None
42	STORE_FAST        'hiragana'

45	LOAD_GLOBAL       'range'
48	LOAD_CONST        12449
51	LOAD_CONST        12544
54	CALL_FUNCTION_2   None
57	STORE_FAST        'katakana'

60	LOAD_GLOBAL       'range'
63	LOAD_CONST        65381
66	LOAD_CONST        65440
69	CALL_FUNCTION_2   None
72	STORE_FAST        'halfwidthKatakana'

75	LOAD_GLOBAL       'set'
78	LOAD_FAST         'asciiSpace'
81	LOAD_FAST         'halfwidthKatakana'
84	BINARY_ADD        None
85	CALL_FUNCTION_1   None
88	STORE_FAST        'halfwidthCharacter'

91	LOAD_GLOBAL       'set'
94	LOAD_FAST         'asciiSpace'
97	LOAD_FAST         'hiragana'
100	BINARY_ADD        None
101	LOAD_FAST         'katakana'
104	BINARY_ADD        None
105	LOAD_FAST         'halfwidthKatakana'
108	BINARY_ADD        None
109	CALL_FUNCTION_1   None
112	STORE_FAST        'allowedUtf8'

115	LOAD_GLOBAL       'TextEncoder'
118	CALL_FUNCTION_0   None
121	STORE_FAST        'te'

124	LOAD_CONST        0.0
127	STORE_FAST        'dc'

130	SETUP_LOOP        '294'
133	LOAD_CONST        '<code_object <generator expression>>'
136	MAKE_FUNCTION_0   None
139	LOAD_FAST         'te'
142	LOAD_ATTR         'decodeText'
145	LOAD_FAST         'name'
148	CALL_FUNCTION_1   None
151	GET_ITER          None
152	CALL_FUNCTION_1   None
155	GET_ITER          None
156	FOR_ITER          '293'
159	STORE_FAST        'char'

162	LOAD_FAST         'char'
165	LOAD_FAST         'allowedUtf8'
168	COMPARE_OP        'not in'
171	JUMP_IF_FALSE     '255'

174	LOAD_FAST         'char'
177	LOAD_FAST         'asciiDigits'
180	COMPARE_OP        'in'
183	JUMP_IF_FALSE     '209'

186	LOAD_GLOBAL       'notify'
189	LOAD_ATTR         'info'
192	LOAD_CONST        'name contains not allowed ascii digits'
195	CALL_FUNCTION_1   None
198	POP_TOP           None

199	LOAD_GLOBAL       'OTPLocalizer'
202	LOAD_ATTR         'NCNoDigits'
205	RETURN_VALUE      None
206	JUMP_ABSOLUTE     '290'

209	LOAD_GLOBAL       'notify'
212	LOAD_ATTR         'info'
215	LOAD_CONST        'name contains not allowed utf8 char: 0x%04x'
218	LOAD_FAST         'char'
221	BINARY_MODULO     None
222	CALL_FUNCTION_1   None
225	POP_TOP           None

226	LOAD_GLOBAL       'OTPLocalizer'
229	LOAD_ATTR         'NCBadCharacter'
232	LOAD_FAST         'te'
235	LOAD_ATTR         'encodeWtext'
238	LOAD_GLOBAL       'unichr'
241	LOAD_FAST         'char'
244	CALL_FUNCTION_1   None
247	CALL_FUNCTION_1   None
250	BINARY_MODULO     None
251	RETURN_VALUE      None
252	JUMP_BACK         '156'

255	LOAD_FAST         'char'
258	LOAD_FAST         'halfwidthCharacter'
261	COMPARE_OP        'in'
264	JUMP_IF_FALSE     '280'

267	LOAD_FAST         'dc'
270	LOAD_CONST        0.5
273	INPLACE_ADD       None
274	STORE_FAST        'dc'
277	JUMP_BACK         '156'

280	LOAD_FAST         'dc'
283	LOAD_CONST        1
286	INPLACE_ADD       None
287	STORE_FAST        'dc'
290	JUMP_BACK         '156'
293	POP_BLOCK         None
294_0	COME_FROM         '130'

294	LOAD_FAST         'dc'
297	LOAD_CONST        2
300	COMPARE_OP        '<'
303	JUMP_IF_FALSE     '333'

306	LOAD_GLOBAL       'notify'
309	LOAD_ATTR         'info'
312	LOAD_CONST        'name is too short: %0.1f'
315	LOAD_FAST LO     None
222	CALL_FUNCTION_1   None
225	POP_TOP           None

226	LOAD_GLOBAL       'OTPLocalizer'
229	LOAD_ATTR         'NCBadCharacter'
232	LOAD_FAST         'te'
235	LOAD_ATTR         'encodeWtext'
238	LOAD_GLOBAL       'unichr'
241	LOAD_FAST         'char'
244	CALL_FUNCTION_1   None
247	CALL_FUNCTION_1   None
250	BINARY_MODULO     None
251	RETURN_VALUE      None
252	JUMP_BACK         '156'

255	LOAD_FAST         'char'
258	LOAD_FAST         'halfwidthCharacter'
261	COMPARE_OP        'in'
264	JUMP_IF_FALSE     '280'

267	LOAD_FAST         'dc'
270	LOAD_CONST        0.5
273	INPLACE_ADD       None
274	STORE_FAST        'dc'
277	JUMP_BACK         '156'

280	LOAD_FAST         'dc'
283	LOAD_CONST        1
286	INPLACE_ADD       None
287	STORE_FAST        'dc'
290	JUMP_BACK         '156'
293	POP_BLOCK         None
294_0	COME_FROM         '130'

294	LOAD_FAST         'dc'
297	LOAD_CONST        2
300	COMPARE_OP        '<'
303	JUMP_IF_FALSE     '333'

306	LOAD_GLOBAL       'notify'
309	LOAD_ATTR         'info'
312	LOAD_CONST        'name is too short: %0.1f'
315	LOAD_FAST         'dc'
318	BINARY_MODULO     None
319	CALL_FUNCTION_1   None
322	POP_TOP           None

323	LOAD_GLOBAL       'OTPLocalizer'
326	LOAD_ATTR         'NCTooShort'
329	RETURN_VALUE      None
330	JUMP_FORWARD      '372'

333	LOAD_FAST         'dc'
336	LOAD_CONST        8
339	COMPARE_OP        '>'
342	JUMP_IF_FALSE     '372'

345	LOAD_GLOBAL       'notify'
348	LOAD_ATTR         'info'
351	LOAD_CONST        'name has been occupied more than eight display cells: %0.1f'
354	LOAD_FAST         'dc'
357	BINARY_MODULO     None
358	CALL_FUNCTION_1   None
361	POP_TOP           None

362	LOAD_GLOBAL       'OTPLocalizer'
365	LOAD_ATTR         'NCGeneric'
368	RETURN_VALUE      None
369	JUMP_FORWARD      '372'
372_0	COME_FROM         '330'
372_1	COME_FROM         '369'

Syntax error at or near `CALL_FUNCTION_1' token at offset 152

    def repeatedChars(name):
        count = 1
        lastChar = None
        i = 0
        while i < len(name):
            char = name[i]
            i += 1
            if char == lastChar:
                count += 1
            else:
                count = 1
            lastChar = char
            if count > 2:
                notify.info('character %s is repeated too many times' % TextEncoder().encodeWtext(char))
                return OTPLocalizer.NCRepeatedChar % TextEncoder().encodeWtext(char)

        return

    checks = [printableChars,
     badCharacters,
     fontHasCharacters,
     longEnough,
     emptyName,
     hasLetters,
     hasVowels,
     monoLetter,
     checkDashes,
     checkCommas,
     checkPeriods,
     checkApostrophes,
     tooManyWords,
     allCaps,
     mixedCase,
     repeatedChars] + otherCheckFuncs
    symmetricChecks = []
    name = TextEncoder().decodeText(name)
    notify.info('checking name "%s"...' % TextEncoder().encodeWtext(name))
    for check in checks:
        problem = check(name[:])
        if not problem and check in symmetricChecks:
            nName = name[:]
            bName.reverse()
            problem = check(bName)
            print 'problem = %s' % problem
        if problem:
            return problem

    return None


severity = notify.getSeverity()
notify.setSeverity(NSError)
for i in xrange(32):
    pass

for c in '!"#$%&()*+/:;<=>?@[\\]^_`{|}~':
    pass

notify.setSeverity(severity)
del severity
        'dc'
318	BINARY_MODULO     None
319	CALL_FUNCTION_1   None
322	POP_TOP           None

323	LOAD_GLOBAL       'OTPLocalizer'
326	LOAD_ATTR         'NCTooShort'
329	RETURN_VALUE      None
330	JUMP_FORWARD      '372'

333	LOAD_FAST         'dc'
336	LOAD_CONST        8
339	COMPARE_OP        '>'
342	JUMP_IF_FALSE     '372'

345	LOAD_GLOBAL       'notify'
348	LOAD_ATTR         'info'
351	LOAD_CONST        'name has been occupied more than eight display cells: %0.1f'
354	LOAD_FAST         'dc'
357	BINARY_MODULO     None
358	CALL_FUNCTION_1   None
361	POP_TOP           None

362	LOAD_GLOBAL       'OTPLocalizer'
365	LOAD_ATTR         'NCGeneric'
368	RETURN_VALUE      None
369	JUMP_FORWARD      '372'
372_0	COME_FROM         '330'
372_1	COME_FROM         '369'

Syntax error at or near `CALL_FUNCTION_1' token at offset 152

