# decompiled 0 files: 0 okay, 1 failed, 0 verify failed

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\quest\Quests.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 105, in uncompyle
    tokens, customize = scanner.disassemble(co)
  File "C:\python27\lib\uncompyle2\scanner24.py", line 61, in disassemble
    self.restructBytecode()
  File "C:\python27\lib\uncompyle2\scanner24.py", line 420, in restructBytecode
    self.restructRelativeJump()
  File "C:\python27\lib\uncompyle2\scanner24.py", line 468, in restructRelativeJump
    self.restructJump(i, target)
  File "C:\python27\lib\uncompyle2\scanner24.py", line 489, in restructJump
    raise 'TODO'
TypeError: exceptions must be old-style classes or derived from BaseException, not str
