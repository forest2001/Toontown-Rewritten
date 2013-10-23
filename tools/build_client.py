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
import pytz
import tempfile
import shutil
import atexit
import argparse
import zipfile

root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def determineVersion(cwd):
    git = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                           stdout=subprocess.PIPE,
                           cwd=cwd).stdout.read()
    git = git.strip()[:7]
    return 'ttr-alpha-g%s' % (git,)

class ClientBuilder(object):
    MAINMODULE = 'toontown.toonbase.MiraiStart'

    def __init__(self, directory):
        self.directory = directory

        self.dcfiles = [os.path.join(directory, 'config/otp.dc'),
                        os.path.join(directory, 'config/toon.dc')]
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

        # Now add pytz timezones:
        zoneinfo = {}
        for zone in pytz.all_timezones:
            zoneinfo['zoneinfo/'+zone] = pytz.open_resource(zone).read()

        md = 'CONFIG = %r\nDC = %r\nZONEINFO = %r\n' % (configData, dcData, zoneinfo)

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

    def load_modules(self):
        #self.find_dcfiles()
        self.find_excludes()

        for dc in self.dcfiles:
            self.dcf.read(Filename.fromOsSpecific(dc))

        self.create_miraidata()

        self.mf.import_hook(self.MAINMODULE)
        self.modules['__main__'] = (False, compile('import %s' % self.MAINMODULE,
                                                   '__main__', 'exec'))

        self.include_dcimports()

        self.build_modules()


    def write_zip(self, outfile):
        zip = zipfile.ZipFile(outfile, 'w')
        for modname, (is_package, code) in self.modules.items():
            mcode = imp.get_magic() + '\x00'*4 + marshal.dumps(code)
            name = modname.replace('.','/')
            if is_package:
                name += '/__init__'
            name += '.pyo'
            zip.writestr(name, mcode)
        zip.close()

    def write_list(self, outfile):
        with open(outfile,'w') as out:
            for modname in sorted(self.modules.keys()):
                is_package, code = self.modules[modname]
                out.write('%s%s\n' % (modname, ' [PKG]' if is_package else ''))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mirai-path', help='The path to the Mirai repository root.')
    parser.add_argument('--format', default='mirai', choices=['mirai', 'zip', 'list'],
                        help='The output format to produce. Choices are:\n'
                        'mirai -- a Mirai package\n'
                        'zip -- a zip file of pyos\n'
                        'list -- a plaintext list of included modules')
    parser.add_argument('output', help='The filename of the built file to output.')

    args = parser.parse_args()
    if args.mirai_path:
        sys.path.append(args.mirai_path)


    cb = ClientBuilder(root)
    cb.load_modules()

    if args.format == 'zip':
        cb.write_zip(args.output)
    elif args.format == 'list':
        cb.write_list(args.output)
    elif args.format == 'mirai':
        try:
            from mirai.packager import MiraiPackager
        except ImportError:
            sys.stderr.write('Could not import Mirai! Check your --mirai-path\n')
            sys.exit(1)

        mp = MiraiPackager(args.output)
        mp.write_modules(cb.modules)
        mp.close()
