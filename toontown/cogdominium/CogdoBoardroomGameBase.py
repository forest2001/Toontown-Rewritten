from toontown.cogdominium import CogdoBoardroomGameSpec
from toontown.cogdominium import CogdoBoardroomGameConsts as Consts

class CogdoBoardroomGameBase:
    __module__ = __name__

    def getConsts(self):
        return Consts

    def getSpec(self):
        return CogdoBoardroomGameSpec
