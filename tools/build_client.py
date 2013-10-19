#!/usr/bin/python2.7 -OO
# Yes, the above flags matter: We have to do this on 2.7 and we have to optimize.

from panda3d.core import Filename
from panda3d.direct import DCFile
from modulefinder import ModuleFinder
import os
import sys
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

    def include_dcimports(self):
        for m in xrange(self.dcf.getNumImportModules()):
            mod = self.dcf.getImportModule(m).split('/')[0]
            self.mf.import_hook(mod)
            for s in xrange(self.dcf.getNumImportSymbols(m)):
                sym = self.dcf.getImportSymbol(m,s).split('/')[0]
                try:
                    self.mf.import_hook('%s.%s' % (mod,sym))
                except ImportError:
                    pass

    def build(self, outfile):
        self.outfile = outfile

        self.find_dcfiles()
        self.find_excludes()

        self.mf.import_hook('toontown.toonbase.ToontownStart')

        for dc in self.dcfiles:
            self.dcf.read(Filename(dc))

        self.include_dcimports()

        zip = zipfile.ZipFile(outfile, 'w')
        for modname, mod in self.mf.modules.items():
            if not (mod.__file__ and mod.__file__.endswith('.py')): continue
            is_package = mod.__file__.endswith('__init__.py')
            an = modname.replace('.','/')
            if is_package:
                an += '/__init__.py'
            else:
                an += '.py'
            zip.write(mod.__file__, an)
        zip.close()

if __name__ == '__main__':
    cb = ClientBuilder(root)
    cb.build(sys.argv[1])
