from direct.distributed.AstronInternalRepository import AstronInternalRepository
from otp.distributed.OtpDoGlobals import *

class ToontownInternalRepository(AstronInternalRepository):
    GameGlobalsId = OTP_DO_ID_TOONTOWN
    dbId = 4003

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFF

    def getAccountIdFromSender(self):
        return (self.getMsgSender()>>32) & 0xFFFFFFFF

    def _isValidPlayerLocation(self, parentId, zoneId):
        if zoneId < 1000:
            return False

        return True
