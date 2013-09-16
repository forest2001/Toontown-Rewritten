# 2013.08.22 22:14:28 Pacific Daylight Time
# Embedded file name: direct.particles.SpriteParticleRendererExt
from pandac.PandaModules import SpriteParticleRenderer

class SpriteParticleRendererExt(SpriteParticleRenderer):
    __module__ = __name__
    sourceTextureName = None
    sourceFileName = None
    sourceNodeName = None

    def getSourceTextureName(self):
        if self.sourceTextureName == None:
            SpriteParticleRendererExt.sourceTextureName = base.config.GetString('particle-sprite-texture', 'maps/lightbulb.rgb')
        return self.sourceTextureName

    def setSourceTextureName(self, name):
        self.sourceTextureName = name

    def setTextureFromFile(self, fileName = None):
        if fileName == None:
            fileName = self.getSourceTextureName()
        t = loader.loadTexture(fileName)
        if t != None:
            self.setTexture(t, t.getYSize())
            self.setSourceTextureName(fileName)
            return True
        else:
            print "Couldn't find rendererSpriteTexture file: %s" % fileName
            return False
        return

    def addTextureFromFile(self, fileName = None):
        if self.getNumAnims() == 0:
            return self.setTextureFromFile(fileName)
        if fileName == None:
            fileName = self.getSourceTextureName()
        t = loader.loadTexture(fileName)
        if t != None:
            self.addTexture(t, t.getYSize())
            return True
        else:
            print "Couldn't find rendererSpriteTexture file: %s" % fileName
            return False
        return

    def getSourceFileName(self):
        if self.sourceFileName == None:
            SpriteParticleRendererExt.sourceFileName = base.config.GetString('particle-sprite-model', 'models/misc/smiley')
        return self.sourceFileName

    def setSourceFileName(self, name):
        self.sourceFileName = name

    def getSourceNodeName(self):
        if self.sourceNodeName == None:
            SpriteParticleRendererExt.sourceNodeName = base.config.GetString('particle-sprite-node', '**/*')
        return self.sourceNodeName

    def setSourceNodeName(self, name):
        self.sourceNodeName = name

    def setTextureFromNode(self, modelName = None, nodeName = None, sizeFromTexels = False):
        if modelName == None:
            modelName = self.getSourceFileName()
            if nodeName == None:
                nodeName = self.getSourceNodeName()
        m = loader.loadModel(modelName)
        if m == None:
            print "SpriteParticleRendererExt: Couldn't find model: %s!" % modelName
            return False
        np = m.find(nodeName)
        if np.isEmpty():
            print "SpriteParticleRendererExt: Couldn't find node: %s!" % nodeName
            m.removeNode()
            return False
        self.setFromNode(np, modelName, nodeName, sizeFromTexels)
        self.setSourceFileName(modelName)
        self.setSourceNodeName(nodeName)
        m.removeNode()
        return True

    def addTextureFromNode(self, modelName = None, nodeName = None, sizeFromTexels = False):
        if self.getNumAnims() == 0:
            return self.setTextureFromNode(modelName, nodeName, sizeFromTexels)
        if modelName == None:
            modelName = self.getSourceFileName()
            if nodeName == None:
                nodeName = self.getSourceNodeName()
        m = loader.loadModel(modelName)
        if m == None:
            print "SpriteParticleRendererExt: Couldn't find model: %s!" % modelName
            return False
        np = m.find(nodeName)
        if np.isEmpty():
            print "SpriteParticleRendererExt: Couldn't find node: %s!" % nodeName
            m.removeNode()
            return False
        self.addFromNode(np, modelName, nodeName, sizeFromTexels)
        m.removeNode()
        return True
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\particles\SpriteParticleRendererExt.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:28 Pacific Daylight Time
