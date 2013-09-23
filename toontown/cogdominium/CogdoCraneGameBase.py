from toontown.cogdominium import CogdoCraneGameSpec
from toontown.cogdominium import CogdoCraneGameConsts as Consts

class CogdoCraneGameBase:
    __module__ = __name__

    def getConsts(self):
        return Consts

    def getSpec(self):
        return CogdoCraneGameSpec
