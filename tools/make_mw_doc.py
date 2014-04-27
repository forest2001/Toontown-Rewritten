#!/usr/bin/env python2
import argparse
import os
import sys

root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

class SpellbookLoader(object):
    """Loads all client and/or AI modules in order to get the spellbook
    initialized.
    """

    DC_FILES = ['config/otp.dc', 'config/toon.dc']

    def __init__(self, root):
        self.root = root
        sys.path.append(root)
        os.chdir(self.root)

        # We haven't loaded this yet:
        self.spellbook = None

        from panda3d.direct import DCFile
        self.dcf = DCFile()

    def load_modules(self, client=True, ai=True):
        self.start_headless()
        self.load_dc()
        self.load_spellbook()

        if client:
            self.load_suffix('')
        if ai:
            self.load_suffix('AI')

    def start_headless(self):
        # Start a headless Panda3D base.
        from direct.showbase.ShowBase import ShowBase
        base = ShowBase(windowType = 'none')
        base.wantKarts = False
        base.wantPets = False

        import __builtin__
        class game:
            name = 'uberDog'
        __builtin__.game = game
        __builtin__.simbase = base
        __builtin__.__dev__ = False


        from panda3d.core import loadPrcFileData
        loadPrcFileData('', 'model-path resources\ndefault-model-extension .bam')

    def load_dc(self):
        # Load and parse toon.dc and otp.dc...
        from panda3d.core import Filename
        for dc in self.DC_FILES:
            full_path = os.path.join(self.root, dc)
            self.dcf.read(Filename.fromOsSpecific(full_path))

    def load_spellbook(self):
        from otp.ai.MagicWordGlobal import spellbook
        self.spellbook = spellbook

    def load_suffix(self, suffix):
        for m in xrange(self.dcf.getNumImportModules()):
            modparts = self.dcf.getImportModule(m).split('/')
            if not suffix or suffix in modparts[1:]:
                mod = modparts[0]+suffix
            else:
                mod = modparts[0]
            __import__(mod)
            for s in xrange(self.dcf.getNumImportSymbols(m)):
                symparts = self.dcf.getImportSymbol(m,s).split('/')
                syms = [symparts[0]]
                if not suffix or suffix in symparts[1:]:
                    sym = symparts[0]+suffix
                else:
                    continue
                try:
                    __import__('%s.%s' % (mod,sym))
                except ImportError:
                    pass

class SpellbookWalker(object):
    """Enumerates all categories and magic words in the spellbook to provide
    to the documentation generator.
    """

    def __init__(self, generator):
        self.generator = generator

    def walk(self, spellbook):
        for category in spellbook.categories:
            self._walk_category(category)

    def _walk_category(self, category):
        self.generator.enter_category(category)
        for word in category.words:
            self.generator.magic_word(word)
        self.generator.exit_category(category)

class MediaWikiGenerator(object):
    def __init__(self, output):
        self.output = output

        self.depth = 1 # Heading depth

    def enter_category(self, category):
        self.depth += 1
        edge = '=' * self.depth
        self.output.write('%s %s %s\n' % (edge, category.name, edge))
        self.output.write("'''Default access:''' %s\n" % category.defaultAccess)
        self.output.write('%s\n' % category.doc)

    def exit_category(self, category):
        self.depth -= 1
        self.output.write('\n')

    def magic_word(self, mw):
        self.output.write('{{MagicWord')

        self.output.write('|name=%s' % mw.name)

        self.output.write('|usage=%s' % mw.getUsage())

        if mw.doc:
            self.output.write('|description=%s' % mw.doc)

        self.output.write('|access=%s' % mw.access)

        self.output.write('}}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', default='mediawiki', choices=['mediawiki'],
                        help='The format for the generated documentation.\n'
                             'Choices are:\n'
                             'mediawiki -- MediaWiki wiki syntax')
    parser.add_argument('output', nargs='?',
                        help='The path to output the documentation to. If '
                             'unspecified, defaults to stdout')
    args = parser.parse_args()

    if args.output:
        output_file = open(args.output, 'w')
    else:
        output_file = sys.stdout

    loader = SpellbookLoader(root)
    loader.load_modules()

    if args.format == 'mediawiki':
        gen = MediaWikiGenerator(output_file)

    walker = SpellbookWalker(gen)
    walker.walk(loader.spellbook)
