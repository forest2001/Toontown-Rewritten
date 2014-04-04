class DNAElement:
    TAG = '*'
    PARENTS = []

    def __init__(self):
        self._parent = None
        self._children = []

    def reparentTo(self, parent):
        if self._parent:
            self._parent._children.remove(self)

        self._parent = parent

        if parent:
            self._parent._children.append(self)

    def handleText(self, chars):
        pass
