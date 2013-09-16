# 2013.08.22 22:14:26 Pacific Daylight Time
# Embedded file name: direct.particles.ParticleEffect
from pandac.PandaModules import *
import Particles
import ForceGroup
from direct.directnotify import DirectNotifyGlobal

class ParticleEffect(NodePath):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ParticleEffect')
    pid = 1

    def __init__(self, name = None, particles = None):
        if name == None:
            name = 'particle-effect-%d' % ParticleEffect.pid
            ParticleEffect.pid += 1
        NodePath.__init__(self, name)
        self.name = name
        self.fEnabled = 0
        self.particlesDict = {}
        self.forceGroupDict = {}
        if particles != None:
            self.addParticles(particles)
        self.renderParent = None
        return

    def cleanup(self):
        self.removeNode()
        self.disable()
        if self.__isValid():
            for f in self.forceGroupDict.values():
                f.cleanup()

            for p in self.particlesDict.values():
                p.cleanup()

            del self.forceGroupDict
            del self.particlesDict
        del self.renderParent

    def getName(self):
        return self.name

    def reset(self):
        self.removeAllForces()
        self.removeAllParticles()
        self.forceGroupDict = {}
        self.particlesDict = {}

    def start(self, parent = None, renderParent = None):
        self.renderParent = renderParent
        self.enable()
        if parent != None:
            self.reparentTo(parent)
        return

    def enable(self):
        if self.__isValid():
            if self.renderParent:
                for p in self.particlesDict.values():
                    p.setRenderParent(self.renderParent.node())

            for f in self.forceGroupDict.values():
                f.enable()

            for p in self.particlesDict.values():
                p.enable()

            self.fEnabled = 1

    def disable(self):
        self.detachNode()
        if self.__isValid():
            for p in self.particlesDict.values():
                p.setRenderParent(p.node)

            for f in self.forceGroupDict.values():
                f.disable()

            for p in self.particlesDict.values():
                p.disable()

            self.fEnabled = 0

    def isEnabled(self):
        return self.fEnabled

    def addForceGroup(self, forceGroup):
        forceGroup.nodePath.reparentTo(self)
        forceGroup.particleEffect = self
        self.forceGroupDict[forceGroup.getName()] = forceGroup
        for i in range(len(forceGroup)):
            self.addForce(forceGroup[i])

    def addForce(self, force):
        for p in self.particlesDict.values():
            p.addForce(force)

    def removeForceGroup(self, forceGroup):
        for i in range(len(forceGroup)):
            self.removeForce(forceGroup[i])

        forceGroup.nodePath.removeNode()
        forceGroup.particleEffect = None
        self.forceGroupDict.pop(forceGroup.getName(), None)
        return

    def removeForce(self, force):
        for p in self.particlesDict.values():
            p.removeForce(force)

    def removeAllForces(self):
        for fg in self.forceGroupDict.values():
            self.removeForceGroup(fg)

    def addParticles(self, particles):
        particles.nodePath.reparentTo(self)
        self.particlesDict[particles.getName()] = particles
        for fg in self.forceGroupDict.values():
            for i in range(len(fg)):
                particles.addForce(fg[i])

    def removeParticles(self, particles):
        if particles == None:
            self.notify.warning('removeParticles() - particles == None!')
            return
        particles.nodePath.detachNode()
        self.particlesDict.pop(particles.getName(), None)
        for fg in self.forceGroupDict.values():
            for f in fg:
                particles.removeForce(f)

        return

    def removeAllParticles(self):
        for p in self.particlesDict.values():
            self.removeParticles(p)

    def getParticlesList(self):
        return self.particlesDict.values()

    def getParticlesNamed(self, name):
        return self.particlesDict.get(name, None)

    def getParticlesDict(self):
        return self.particlesDict

    def getForceGroupList(self):
        return self.forceGroupDict.values()

    def getForceGroupNamed(self, name):
        return self.forceGroupDict.get(name, None)

    def getForceGroupDict(self):
        return self.forceGroupDict

    def saveConfig(self, filename):
        f = open(filename.toOsSpecific(), 'wb')
        f.write('\n')
        f.write('self.reset()\n')
        pos = self.getPos()
        hpr = self.getHpr()
        scale = self.getScale()
        f.write('self.setPos(%0.3f, %0.3f, %0.3f)\n' % (pos[0], pos[1], pos[2]))
        f.write('self.setHpr(%0.3f, %0.3f, %0.3f)\n' % (hpr[0], hpr[1], hpr[2]))
        f.write('self.setScale(%0.3f, %0.3f, %0.3f)\n' % (scale[0], scale[1], scale[2]))
        num = 0
        for p in self.particlesDict.values():
            target = 'p%d' % num
            num = num + 1
            f.write(target + " = Particles.Particles('%s')\n" % p.getName())
            p.printParams(f, target)
            f.write('self.addParticles(%s)\n' % target)

        num = 0
        for fg in self.forceGroupDict.values():
            target = 'f%d' % num
            num = num + 1
            f.write(target + " = ForceGroup.ForceGroup('%s')\n" % fg.getName())
            fg.printParams(f, target)
            f.write('self.addForceGroup(%s)\n' % target)

        f.close()

    def loadConfig(self, filename):
        data = vfs.readFile(filename, 1)
        data = data.replace('\r', '')
        try:
            if not isClient():
                print 'EXECWARNING ParticleEffect: %s' % data
                printStack()
            exec data
        except:
            self.notify.warning('loadConfig: failed to load particle file: ' + repr(filename))
            raise

    def accelerate(self, time, stepCount = 1, stepTime = 0.0):
        for particles in self.getParticlesList():
            particles.accelerate(time, stepCount, stepTime)

    def clearToInitial(self):
        for particles in self.getParticlesList():
            particles.clearToInitial()

    def softStop(self):
        for particles in self.getParticlesList():
            particles.softStop()

    def softStart(self):
        if self.__isValid():
            for particles in self.getParticlesList():
                particles.softStart()

        else:
            self.notify.error('Trying to start effect(%s) after cleanup.' % (self.getName(),))

    def __isValid(self):
        return hasattr(self, 'forceGroupDict') and hasattr(self, 'particlesDict')
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\particles\ParticleEffect.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:14:27 Pacific Daylight Time
