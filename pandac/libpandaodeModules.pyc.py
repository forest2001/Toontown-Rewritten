# 2013.08.22 22:15:54 Pacific Daylight Time
# Embedded file name: pandac.libpandaodeModules
from extension_native_helpers import *
Dtool_PreloadDLL('libpandaode')
from libpandaode import *
from extension_native_helpers import *
Dtool_PreloadDLL('libpanda')
from libpanda import *

def convert(self):
    if self.getClass() == OdeGeom.GCSphere:
        return self.convertToSphere()
    elif self.getClass() == OdeGeom.GCBox:
        return self.convertToBox()
    elif self.getClass() == OdeGeom.GCCappedCylinder:
        return self.convertToCappedCylinder()
    elif self.getClass() == OdeGeom.GCPlane:
        return self.convertToPlane()
    elif self.getClass() == OdeGeom.GCRay:
        return self.convertToRay()
    elif self.getClass() == OdeGeom.GCTriMesh:
        return self.convertToTriMesh()
    elif self.getClass() == OdeGeom.GCSimpleSpace:
        return self.convertToSimpleSpace()
    elif self.getClass() == OdeGeom.GCHashSpace:
        return self.convertToHashSpace()
    elif self.getClass() == OdeGeom.GCQuadTreeSpace:
        return self.convertToQuadTreeSpace()


Dtool_funcToMethod(convert, OdeGeom)
del convert

def getConvertedSpace(self):
    return self.getSpace().convert()


Dtool_funcToMethod(getConvertedSpace, OdeGeom)
del getConvertedSpace

def getAABounds(self):
    min = Point3()
    max = Point3()
    self.getAABB(min, max)
    return (min, max)


Dtool_funcToMethod(getAABounds, OdeGeom)
del getAABounds
from extension_native_helpers import *
Dtool_PreloadDLL('libpanda')
from libpanda import *

def convert(self):
    if self.getClass() == OdeGeom.GCSimpleSpace:
        return self.convertToSimpleSpace()
    elif self.getClass() == OdeGeom.GCHashSpace:
        return self.convertToHashSpace()
    elif self.getClass() == OdeGeom.GCQuadTreeSpace:
        return self.convertToQuadTreeSpace()


Dtool_funcToMethod(convert, OdeSpace)
del convert

def getConvertedGeom(self, index):
    return self.getGeom(index).convert()


Dtool_funcToMethod(getConvertedGeom, OdeSpace)
del getConvertedGeom

def getConvertedSpace(self):
    return self.getSpace().convert()


Dtool_funcToMethod(getConvertedSpace, OdeSpace)
del getConvertedSpace

def getAABounds(self):
    min = Point3()
    max = Point3()
    self.getAABB(min, max)
    return (min, max)


Dtool_funcToMethod(getAABounds, OdeSpace)
del getAABounds
from extension_native_helpers import *
Dtool_PreloadDLL('libpanda')
from libpanda import *

def attach(self, body1, body2):
    if body1 and body2:
        self.attachBodies(body1, body2)
    elif body1 and not body2:
        self.attachBody(body1, 0)
    elif not body1 and body2:
        self.attachBody(body2, 1)


Dtool_funcToMethod(attach, OdeJoint)
del attach

def convert(self):
    if self.getJointType() == OdeJoint.JTBall:
        return self.convertToBall()
    elif self.getJointType() == OdeJoint.JTHinge:
        return self.convertToHinge()
    elif self.getJointType() == OdeJoint.JTSlider:
        return self.convertToSlider()
    elif self.getJointType() == OdeJoint.JTContact:
        return self.convertToContact()
    elif self.getJointType() == OdeJoint.JTUniversal:
        return self.convertToUniversal()
    elif self.getJointType() == OdeJoint.JTHinge2:
        return self.convertToHinge2()
    elif self.getJointType() == OdeJoint.JTFixed:
        return self.convertToFixed()
    elif self.getJointType() == OdeJoint.JTNull:
        return self.convertToNull()
    elif self.getJointType() == OdeJoint.JTAMotor:
        return self.convertToAMotor()
    elif self.getJointType() == OdeJoint.JTLMotor:
        return self.convertToLMotor()
    elif self.getJointType() == OdeJoint.JTPlane2d:
        return self.convertToPlane2d()


Dtool_funcToMethod(convert, OdeJoint)
del convert
from extension_native_helpers import *
Dtool_PreloadDLL('libpanda')
from libpanda import *

def getConvertedJoint(self, index):
    return self.getJoint(index).convert()


Dtool_funcToMethod(getConvertedJoint, OdeBody)
del getConvertedJoint
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\pandac\libpandaodeModules.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:15:54 Pacific Daylight Time
