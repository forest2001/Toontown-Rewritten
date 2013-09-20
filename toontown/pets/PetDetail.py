# 2013.08.22 22:23:52 Pacific Daylight Time
# Embedded file name: toontown.pets.PetDetail
from direct.directnotify import DirectNotifyGlobal
from otp.avatar import AvatarDetail
from toontown.pets import DistributedPet

class PetDetail(AvatarDetail.AvatarDetail):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PetDetail')

    def getDClass(self):
        return 'DistributedPet'

    def createHolder(self):
        pet = DistributedPet.DistributedPet(base.cr, bFake=True)
        pet.forceAllowDelayDelete()
        pet.generateInit()
        pet.generate()
        return pet
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\toontown\pets\PetDetail.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:23:52 Pacific Daylight Time
