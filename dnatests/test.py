import sys
sys.path.insert(0, '../toontown')#hacky hack
from toontown.dna import DNAParser
from pandac.PandaModules import *
loadPrcFile('config/dev.prc')

#At the end the dna loader will be much cleaner to call, consider this
#the internals of the function you call to load DNA
loader = DNAParser.DNALoader()
loader.getData().read(open('dnatests/test.dna'))
loader.getData().getDnaStorage().ls()
graph = loader.buildGraph()
import sys
sys.stderr = open('test.out', 'w')
graph.ls()
graph.writeBamFile("test.bam")