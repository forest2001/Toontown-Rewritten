# 2013.08.22 22:12:55 Pacific Daylight Time
# Embedded file name: difflib
# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:12:56 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\difflib.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 128, in uncompyle
    walk.gen_source(ast, customize)
  File "C:\python27\lib\uncompyle2\walker.py", line 1414, in gen_source
    self.print_(self.traverse(ast, isLambda=isLambda))
  File "C:\python27\lib\uncompyle2\walker.py", line 500, in traverse
    self.preorder(node)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 687, in preorder
    func(node)
  File "C:\python27\lib\uncompyle2\walker.py", line 976, in n_classdef
    self.build_class(node[2][-2].attr)
  File "C:\python27\lib\uncompyle2\walker.py", line 1397, in build_class
    self.gen_source(ast, code._customize)
  File "C:\python27\lib\uncompyle2\walker.py", line 1414, in gen_source
    self.print_(self.traverse(ast, isLambda=isLambda))
  File "C:\python27\lib\uncompyle2\walker.py", line 500, in traverse
    self.preorder(node)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 694, in preorder
    self.preorder(kid)
  File "C:\python27\lib\uncompyle2\spark.py", line 689, in preorder
    self.default(node)
  File "C:\python27\lib\uncompyle2\walker.py", line 1188, in default
    self.engine(table[key], node)
  File "C:\python27\lib\uncompyle2\walker.py", line 1138, in engine
    self.preorder(node[entry[arg]])
  File "C:\python27\lib\uncompyle2\spark.py", line 687, in preorder
    func(node)
  File "C:\python27\lib\uncompyle2\walker.py", line 886, in n_mkfunc
    self.make_function(node, isLambda=0)
  File "C:\python27\lib\uncompyle2\walker.py", line 1289, in make_function
    code = Code(code, self.scanner, self.currentclass)
  File "C:\python27\lib\uncompyle2\scanner.py", line 60, in __init__
    self._tokens, self._customize = scanner.disassemble(co, classname)
  File "C:\python27\lib\uncompyle2\scanner24.py", line 61, in disassemble
    self.restructBytecode()
  File "C:\python27\lib\uncompyle2\scanner24.py", line 437, in restructBytecode
    ret = self.getOpcodeToDel(i)
  File "C:\python27\lib\uncompyle2\scanner24.py", line 290, in getOpcodeToDel
    if nameDel == self.get_argument(end):
  File "C:\python27\lib\uncompyle2\scanner.py", line 96, in get_argument
    arg = self.code[pos+1] + self.code[pos+2] * 256
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
