#!/usr/bin/python2.7 -OO
# Yes, the above flags matter: We have to do this on 2.7 and we have to optimize.

from panda3d.core import Filename, StringStream
from panda3d.direct import DCFile
from modulefinder import ModuleFinder
import os
import sys
import subprocess
import imp
import marshal
import tempfile
import shutil
import atexit
import zipfile

root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def determineVersion(cwd):
    git = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                           stdout=subprocess.PIPE,
                           cwd=cwd).stdout.read()
    git = git.strip()[:7]
    return 'ttr-alpha-g%s' % (git,)

class ClientBuilder(object):
    def __init__(self, directory):
        self.directory = directory

        self.dcfiles = []
        self.modules = {}

        self.mf = ModuleFinder(sys.path+[self.directory])
        self.dcf = DCFile()

    def should_exclude(self, modname):
        # The NonRepeatableRandomSource modules are imported by the dc file explicitly,
        # so we have to allow them.
        if 'NonRepeatableRandomSource' in modname:
            return False

        if modname.endswith('AI'):
            return True
        if modname.endswith('UD'):
            return True
        if modname.endswith('.ServiceStart'):
            return True

    def find_excludes(self):
        for path, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = os.path.join(path, filename)
                filepath = os.path.relpath(filepath, self.directory)
                if not filepath.endswith('.py'): continue
                filepath = filepath[:-3]
                modname = filepath.replace(os.path.sep, '.')
                if modname.endswith('.__init__'): modname = modname[:-9]
                if self.should_exclude(modname):
                    self.mf.excludes.append(modname)

    def find_dcfiles(self):
        for path, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = os.path.join(path, filename)
                if filename.endswith('.dc'):
                    self.dcfiles.append(filepath)

    def create_miraidata(self):
        # Create a temporary _miraidata.py and throw it on the path somewhere...

        # First, we need the minified DC file contents:
        dcStream = StringStream()
        self.dcf.write(dcStream, True)
        dcData = dcStream.getData()

        # Next we need config files...
        configData = []
        with open(os.path.join(self.directory, 'config/public_client.prc')) as f:
            fd = f.read()
            fd = fd.replace('SERVER_VERSION_HERE', determineVersion(self.directory))
            configData.append(fd)

        md = 'CONFIG = %r\nDC = %r\n' % (configData, dcData)

        # Now we use tempfile to dump md:
        td = tempfile.mkdtemp()
        with open(os.path.join(td, '_miraidata.py'), 'w') as f:
            f.write(md)

        self.mf.path.append(td)

        atexit.register(shutil.rmtree, td)

    def include_dcimports(self):
        for m in xrange(self.dcf.getNumImportModules()):
            modparts = self.dcf.getImportModule(m).split('/')
            mods = [modparts[0]]
            if 'OV' in modparts[1:]:
                mods.append(modparts[0]+'OV')
            for mod in mods:
                self.mf.import_hook(mod)
                for s in xrange(self.dcf.getNumImportSymbols(m)):
                    symparts = self.dcf.getImportSymbol(m,s).split('/')
                    syms = [symparts[0]]
                    if 'OV' in symparts[1:]:
                        syms.append(symparts[0]+'OV')
                    for sym in syms:
                        try:
                            self.mf.import_hook('%s.%s' % (mod,sym))
                        except ImportError:
                            pass

    def build_modules(self):
        for modname, mod in self.mf.modules.items():
            modfile = mod.__file__
            if not (modfile and modfile.endswith('.py')): continue
            is_package = modfile.endswith('__init__.py')
            with open(modfile, 'r') as f:
                code = compile(f.read(), modname, 'exec')
            self.modules[modname] = (is_package, code)

    def build(self, outfile):
        self.outfile = outfile

        self.find_dcfiles()
        self.find_excludes()

        for dc in self.dcfiles:
            self.dcf.read(Filename(dc))

        self.create_miraidata()

        self.mf.import_hook('toontown.toonbase.MiraiStart')

        self.include_dcimports()

        self.build_modules()

        zip = zipfile.ZipFile(outfile, 'w')
        for modname, (is_package, code) in self.modules.items():
            mcode = imp.get_magic() + '\x00'*4 + marshal.dumps(code)
            name = modname.replace('.','/')
            if is_package:
                name += '/__init__'
            name += '.pyc'
            zip.writestr(name, mcode)
        zip.close()

if __name__ == '__main__':
    cb = ClientBuilder(root)
    cb.build(sys.argv[1])
