import xml.sax

class DNAError(Exception): pass
class DNAParseError(DNAError): pass

elementRegistry = {}
def registerElement(element):
    elementRegistry[element.TAG] = element

class DNASaxHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

        self.stack = []
        self.root = None

    def startElement(self, tag, attrs):
        if self.stack:
            parent = self.stack[-1]
            parentTag = parent.TAG
        else:
            parent = None
            parentTag = None

        element = elementRegistry.get(tag)
        if not element:
            raise DNAParseError('Unknown element type: ' + tag)

        if parentTag not in element.PARENTS:
            raise DNAParseError('Cannot put %s below %s element' % (tag, parentTag))

        element = element(**attrs)
        self.stack.append(element)
        element.reparentTo(parent)

        if not self.root:
            self.root = element

    def endElement(self, tag):
        self.stack.pop(-1)

    def characters(self, chars):
        if not self.stack:
            return

        self.stack[-1].handleText(chars)

def parse(stream):
    handler = DNASaxHandler()
    xml.sax.parse(stream, handler)
    return handler.root
