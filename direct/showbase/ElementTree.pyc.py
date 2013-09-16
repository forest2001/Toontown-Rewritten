# 2013.08.22 22:14:33 Pacific Daylight Time
# Embedded file name: direct.showbase.ElementTree
__all__ = ['Comment',
 'dump',
 'Element',
 'ElementTree',
 'fromstring',
 'iselement',
 'iterparse',
 'parse',
 'PI',
 'ProcessingInstruction',
 'QName',
 'SubElement',
 'tostring',
 'TreeBuilder',
 'VERSION',
 'XML',
 'XMLTreeBuilder']
import string, sys, re

class _SimpleElementPath():
    __module__ = __name__

    def find(self, element, tag):
        for elem in element:
            if elem.tag == tag:
                return elem

        return None

    def findtext(self, element, tag, default = None):
        for elem in element:
            if elem.tag == tag:
                return elem.text or ''

        return default

    def findall(self, element, tag):
        if tag[:3] == './/':
            return element.getiterator(tag[3:])
        result = []
        for elem in element:
            if elem.tag == tag:
                result.append(elem)

        return result


try:
    import ElementPath
except ImportError:
    ElementPath = _SimpleElementPath()

VERSION = '1.2.6'

class _ElementInterface():
    __module__ = __name__
    tag = None
    attrib = None
    text = None
    tail = None

    def __init__(self, tag, attrib):
        self.tag = tag
        self.attrib = attrib
        self._children = []

    def __repr__(self):
        return '<Element %s at %x>' % (self.tag, id(self))

    def makeelement(self, tag, attrib):
        return Element(tag, attrib)

    def __len__(self):
        return len(self._children)

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, element):
        self._children[index] = element

    def __delitem__(self, index):
        del self._children[index]

    def __getslice__(self, start, stop):
        return self._children[start:stop]

    def __setslice__(self, start, stop, elements):
        for element in elements:
            pass

        self._children[start:stop] = list(elements)

    def __delslice__(self, start, stop):
        del self._children[start:stop]

    def append(self, element):
        self._children.append(element)

    def insert(self, index, element):
        self._children.insert(index, element)

    def remove(self, element):
        self._children.remove(element)

    def getchildren(self):
        return self._children

    def find(self, path):
        return ElementPath.find(self, path)

    def findtext(self, path, default = None):
        return ElementPath.findtext(self, path, default)

    def findall(self, path):
        return ElementPath.findall(self, path)

    def clear(self):
        self.attrib.clear()
        self._children = []
        self.text = self.tail = None
        return

    def get(self, key, default = None):
        return self.attrib.get(key, default)

    def set(self, key, value):
        self.attrib[key] = value

    def keys(self):
        return self.attrib.keys()

    def items(self):
        return self.attrib.items()

    def getiterator(self, tag = None):
        nodes = []
        if tag == '*':
            tag = None
        if tag is None or self.tag == tag:
            nodes.append(self)
        for node in self._children:
            nodes.extend(node.getiterator(tag))

        return nodes


_Element = _ElementInterface

def Element(tag, attrib = {}, **extra):
    attrib = attrib.copy()
    attrib.update(extra)
    return _ElementInterface(tag, attrib)


def SubElement(parent, tag, attrib = {}, **extra):
    attrib = attrib.copy()
    attrib.update(extra)
    element = parent.makeelement(tag, attrib)
    parent.append(element)
    return element


def Comment(text = None):
    element = Element(Comment)
    element.text = text
    return element


def ProcessingInstruction(target, text = None):
    element = Element(ProcessingInstruction)
    element.text = target
    if text:
        element.text = element.text + ' ' + text
    return element


PI = ProcessingInstruction

class QName():
    __module__ = __name__

    def __init__(self, text_or_uri, tag = None):
        if tag:
            text_or_uri = '{%s}%s' % (text_or_uri, tag)
        self.text = text_or_uri

    def __str__(self):
        return self.text

    def __hash__(self):
        return hash(self.text)

    def __cmp__(self, other):
        if isinstance(other, QName):
            return cmp(self.text, other.text)
        return cmp(self.text, other)


class ElementTree():
    __module__ = __name__

    def __init__(self, element = None, file = None):
        self._root = element
        if file:
            self.parse(file)

    def getroot(self):
        return self._root

    def _setroot(self, element):
        self._root = element

    def parse--- This code section failed: ---

0	LOAD_GLOBAL       'hasattr'
3	LOAD_FAST         'source'
6	LOAD_CONST        'read'
9	CALL_FUNCTION_2   None
12	JUMP_IF_TRUE      '33'

15	LOAD_GLOBAL       'open'
18	LOAD_FAST         'source'
21	LOAD_CONST        'rb'
24	CALL_FUNCTION_2   None
27	STORE_FAST        'source'
30	JUMP_FORWARD      '33'
33_0	COME_FROM         '30'

33	LOAD_FAST         'parser'
36	JUMP_IF_TRUE      '51'

39	LOAD_GLOBAL       'XMLTreeBuilder'
42	CALL_FUNCTION_0   None
45	STORE_FAST        'parser'
48	JUMP_FORWARD      '51'
51_0	COME_FROM         '48'

51	SETUP_LOOP        '96'

54	LOAD_FAST         'source'
57	LOAD_ATTR         'read'
60	LOAD_CONST        32768
63	CALL_FUNCTION_1   None
66	STORE_FAST        'data'

69	LOAD_FAST         'data'
72	JUMP_IF_TRUE      '79'

75	BREAK_LOOP        None
76	JUMP_FORWARD      '79'
79_0	COME_FROM         '76'

79	LOAD_FAST         'parser'
82	LOAD_ATTR         'feed'
85	LOAD_FAST         'data'
88	CALL_FUNCTION_1   None
91	POP_TOP           None
92	JUMP_BACK         '54'
95	POP_BLOCK         None
96_0	COME_FROM         '51'

96	LOAD_FAST         'parser'
99	LOAD_ATTR         'close'
102	CALL_FUNCTION_0   None
105	LOAD_FAST         'self'
108	STORE_ATTR        '_root'

111	LOAD_FAST         'self'
114	LOAD_ATTR         '_root'
117	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 95

    def getiterator(self, tag = None):
        return self._root.getiterator(tag)

    def find(self, path):
        if path[:1] == '/':
            path = '.' + path
        return self._root.find(path)

    def findtext(self, path, default = None):
        if path[:1] == '/':
            path = '.' + path
        return self._root.findtext(path, default)

    def findall(self, path):
        if path[:1] == '/':
            path = '.' + path
        return self._root.findall(path)

    def write(self, file, encoding = 'us-ascii'):
        if not hasattr(file, 'write'):
            file = open(file, 'wb')
        if not encoding:
            encoding = 'us-ascii'
        elif encoding != 'utf-8' and encoding != 'us-ascii':
            file.write("<?xml version='1.0' encoding='%s'?>\n" % encoding)
        self._write(file, self._root, encoding, {})

    def _write(self, file, node, encoding, namespaces):
        tag = node.tag
        if tag is Comment:
            file.write('<!-- %s -->' % _escape_cdata(node.text, encoding))
        elif tag is ProcessingInstruction:
            file.write('<?%s?>' % _escape_cdata(node.text, encoding))
        else:
            items = node.items()
            xmlns_items = []
            try:
                if isinstance(tag, QName) or tag[:1] == '{':
                    tag, xmlns = fixtag(tag, namespaces)
                    if xmlns:
                        xmlns_items.append(xmlns)
            except TypeError:
                _raise_serialization_error(tag)

            file.write('<' + _encode(tag, encoding))
            if items or xmlns_items:
                items.sort()
                for k, v in items:
                    try:
                        if isinstance(k, QName) or k[:1] == '{':
                            k, xmlns = fixtag(k, namespaces)
                            if xmlns:
                                xmlns_items.append(xmlns)
                    except TypeError:
                        _raise_serialization_error(k)

                    try:
                        if isinstance(v, QName):
                            v, xmlns = fixtag(v, namespaces)
                            if xmlns:
                                xmlns_items.append(xmlns)
                    except TypeError:
                        _raise_serialization_error(v)

                    file.write(' %s="%s"' % (_encode(k, encoding), _escape_attrib(v, encoding)))

                for k, v in xmlns_items:
                    file.write(' %s="%s"' % (_encode(k, encoding), _escape_attrib(v, encoding)))

            if node.text or len(node):
                file.write('>')
                if node.text:
                    file.write(_escape_cdata(node.text, encoding))
                for n in node:
                    self._write(file, n, encoding, namespaces)

                file.write('</' + _encode(tag, encoding) + '>')
            else:
                file.write(' />')
            for k, v in xmlns_items:
                del namespaces[v]

        if node.tail:
            file.write(_escape_cdata(node.tail, encoding))


def iselement(element):
    return isinstance(element, _ElementInterface) or hasattr(element, 'tag')


def dump(elem):
    if not isinstance(elem, ElementTree):
        elem = ElementTree(elem)
    elem.write(sys.stdout)
    tail = elem.getroot().tail
    if not tail or tail[-1] != '\n':
        sys.stdout.write('\n')


def _encode(s, encoding):
    try:
        return s.encode(encoding)
    except AttributeError:
        return s


if sys.version[:3] == '1.5':
    _escape = re.compile('[&<>\\"\\x80-\\xff]+')
else:
    _escape = re.compile(eval('u"[&<>\\"\\u0080-\\uffff]+"'))
_escape_map = {'&': '&amp;',
 '<': '&lt;',
 '>': '&gt;',
 '"': '&quot;'}
_namespace_map = {'http://www.w3.org/XML/1998/namespace': 'xml',
 'http://www.w3.org/1999/xhtml': 'html',
 'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf',
 'http://schemas.xmlsoap.org/wsdl/': 'wsdl'}

def _raise_serialization_error(text):
    raise TypeError('cannot serialize %r (type %s)' % (text, type(text).__name__))


def _encode_entity(text, pattern = _escape):

    def escape_entities(m, map = _escape_map):
        out = []
        append = out.append
        for char in m.group():
            text = map.get(char)
            if text is None:
                text = '&#%d;' % ord(char)
            append(text)

        return string.join(out, '')

    try:
        return _encode(pattern.sub(escape_entities, text), 'ascii')
    except TypeError:
        _raise_serialization_error(text)


def _escape_cdata(text, encoding = None, replace = string.replace):
    try:
        if encoding:
            try:
                text = _encode(text, encoding)
            except UnicodeError:
                return _encode_entity(text)

        text = replace(text, '&', '&amp;')
        text = replace(text, '<', '&lt;')
        text = replace(text, '>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def _escape_attrib(text, encoding = None, replace = string.replace):
    try:
        if encoding:
            try:
                text = _encode(text, encoding)
            except UnicodeError:
                return _encode_entity(text)

        text = replace(text, '&', '&amp;')
        text = replace(text, "'", '&apos;')
        text = replace(text, '"', '&quot;')
        text = replace(text, '<', '&lt;')
        text = replace(text, '>', '&gt;')
        return text
    except (TypeError, AttributeError):
        _raise_serialization_error(text)


def fixtag(tag, namespaces):
    if isinstance(tag, QName):
        tag = tag.text
    namespace_uri, tag = string.split(tag[1:], '}', 1)
    prefix = namespaces.get(namespace_uri)
    if prefix is None:
        prefix = _namespace_map.get(namespace_uri)
        if prefix is None:
            prefix = 'ns%d' % len(namespaces)
        namespaces[namespace_uri] = prefix
        if prefix == 'xml':
            xmlns = None
        else:
            xmlns = ('xmlns:%s' % prefix, namespace_uri)
    else:
        xmlns = None
    return ('%s:%s' % (prefix, tag), xmlns)


def parse(source, parser = None):
    tree = ElementTree()
    tree.parse(source, parser)
    return tree


class iterparse():
    __module__ = __name__

    def __init__(self, source, events = None):
        if not hasattr(source, 'read'):
            source = open(source, 'rb')
        self._file = source
        self._events = []
        self._index = 0
        self.root = self._root = None
        self._parser = XMLTreeBuilder()
        parser = self._parser._parser
        append = self._events.append
        if events is None:
            events = ['end']
        for event in events:
            if event == 'start':
                try:
                    parser.ordered_attributes = 1
                    parser.specified_attributes = 1

                    def handler(tag, attrib_in, event = event, append = append, start = self._parser._start_list):
                        append((event, start(tag, attrib_in)))

                    parser.StartElementHandler = handler
                except AttributeError:

                    def handler(tag, attrib_in, event = event, append = append, start = self._parser._start):
                        append((event, start(tag, attrib_in)))

                    parser.StartElementHandler = handler

            elif event == 'end':

                def handler(tag, event = event, append = append, end = self._parser._end):
                    append((event, end(tag)))

                parser.EndElementHandler = handler
            elif event == 'start-ns':

                def handler(prefix, uri, event = event, append = append):
                    try:
                        uri = _encode(uri, 'ascii')
                    except UnicodeError:
                        pass

                    append((event, prefix or ('', uri)))

                parser.StartNamespaceDeclHandler = handler
            elif event == 'end-ns':

                def handler(prefix, event = event, append = append):
                    append((event, None))
                    return

                parser.EndNamespaceDeclHandler = handler

        return

    def next--- This code section failed: ---

0	SETUP_LOOP        '219'

3	SETUP_EXCEPT      '26'

6	LOAD_FAST         'self'
9	LOAD_ATTR         '_events'
12	LOAD_FAST         'self'
15	LOAD_ATTR         '_index'
18	BINARY_SUBSCR     None
19	STORE_FAST        'item'
22	POP_BLOCK         None
23	JUMP_FORWARD      '195'
26_0	COME_FROM         '3'

26	DUP_TOP           None
27	LOAD_GLOBAL       'IndexError'
30	COMPARE_OP        'exception match'
33	JUMP_IF_FALSE     '194'
36	POP_TOP           None
37	POP_TOP           None
38	POP_TOP           None

39	LOAD_FAST         'self'
42	LOAD_ATTR         '_parser'
45	LOAD_CONST        None
48	COMPARE_OP        'is'
51	JUMP_IF_FALSE     '105'

54	LOAD_FAST         'self'
57	LOAD_ATTR         '_root'
60	LOAD_FAST         'self'
63	STORE_ATTR        'root'

66	SETUP_EXCEPT      '79'

69	LOAD_GLOBAL       'StopIteration'
72	RAISE_VARARGS_1   None
75	POP_BLOCK         None
76	JUMP_ABSOLUTE     '105'
79_0	COME_FROM         '66'

79	DUP_TOP           None
80	LOAD_GLOBAL       'NameError'
83	COMPARE_OP        'exception match'
86	JUMP_IF_FALSE     '101'
89	POP_TOP           None
90	POP_TOP           None
91	POP_TOP           None

92	LOAD_GLOBAL       'IndexError'
95	RAISE_VARARGS_1   None
98	JUMP_ABSOLUTE     '105'
101	END_FINALLY       None
102_0	COME_FROM         '101'
102	JUMP_FORWARD      '105'
105_0	COME_FROM         '102'

105	LOAD_FAST         'self'
108	LOAD_ATTR         '_events'
111	DELETE_SLICE+0    None

112	LOAD_CONST        0
115	LOAD_FAST         'self'
118	STORE_ATTR        '_index'

121	LOAD_FAST         'self'
124	LOAD_ATTR         '_file'
127	LOAD_ATTR         'read'
130	LOAD_CONST        16384
133	CALL_FUNCTION_1   None
136	STORE_FAST        'data'

139	LOAD_FAST         'data'
142	JUMP_IF_FALSE     '164'

145	LOAD_FAST         'self'
148	LOAD_ATTR         '_parser'
151	LOAD_ATTR         'feed'
154	LOAD_FAST         'data'
157	CALL_FUNCTION_1   None
160	POP_TOP           None
161	JUMP_ABSOLUTE     '215'

164	LOAD_FAST         'self'
167	LOAD_ATTR         '_parser'
170	LOAD_ATTR         'close'
173	CALL_FUNCTION_0   None
176	LOAD_FAST         'self'
179	STORE_ATTR        '_root'

182	LOAD_CONST        None
185	LOAD_FAST         'self'
188	STORE_ATTR        '_parser'
191	JUMP_BACK         '3'
194	END_FINALLY       None
195_0	COME_FROM         '23'

195	LOAD_FAST         'self'
198	LOAD_ATTR         '_index'
201	LOAD_CONST        1
204	BINARY_ADD        None
205	LOAD_FAST         'self'
208	STORE_ATTR        '_index'

211	LOAD_FAST         'item'
214	RETURN_VALUE      None
215_0	COME_FROM         '194'
215	JUMP_BACK         '3'
218	POP_BLOCK         None
219_0	COME_FROM         '0'
219	LOAD_CONST        None
222	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 218

    try:
        iter

        def __iter__(self):
            return self

    except NameError:

        def __getitem__(self, index):
            return self.next()


def XML(text):
    parser = XMLTreeBuilder()
    parser.feed(text)
    return parser.close()


def XMLID(text):
    parser = XMLTreeBuilder()
    parser.feed(text)
    tree = parser.close()
    ids = {}
    for elem in tree.getiterator():
        id = elem.get('id')
        if id:
            ids[id] = elem

    return (tree, ids)


fromstring = XML

def tostring(element, encoding = None):

    class dummy():
        __module__ = __name__

    data = []
    file = dummy()
    file.write = data.append
    ElementTree(element).write(file, encoding)
    return string.join(data, '')


class TreeBuilder():
    __module__ = __name__

    def __init__(self, element_factory = None):
        self._data = []
        self._elem = []
        self._last = None
        self._tail = None
        if element_factory is None:
            element_factory = _ElementInterface
        self._factory = element_factory
        return

    def close(self):
        return self._last

    def _flush(self):
        if self._data:
            if self._last is not None:
                text = string.join(self._data, '')
                if self._tail:
                    self._last.tail = text
                else:
                    self._last.text = text
            self._data = []
        return

    def data(self, data):
        self._data.append(data)

    def start(self, tag, attrs):
        self._flush()
        self._last = elem = self._factory(tag, attrs)
        if self._elem:
            self._elem[-1].append(elem)
        self._elem.append(elem)
        self._tail = 0
        return elem

    def end(self, tag):
        self._flush()
        self._last = self._elem.pop()
        self._tail = 1
        return self._last


class XMLTreeBuilder():
    __module__ = __name__

    def __init__(self, html = 0, target = None):
        try:
            from xml.parsers import expat
        except ImportError:
            raise ImportError('No module named expat; use SimpleXMLTreeBuilder instead')

        self._parser = parser = expat.ParserCreate(None, '}')
        if target is None:
            target = TreeBuilder()
        self._target = target
        self._names = {}
        parser.DefaultHandlerExpand = self._default
        parser.StartElementHandler = self._start
        parser.EndElementHandler = self._end
        parser.CharacterDataHandler = self._data
        try:
            self._parser.buffer_text = 1
        except AttributeError:
            pass

        try:
            self._parser.ordered_attributes = 1
            self._parser.specified_attributes = 1
            parser.StartElementHandler = self._start_list
        except AttributeError:
            pass

        encoding = None
        if not parser.returns_unicode:
            encoding = 'utf-8'
        self._doctype = None
        self.entity = {}
        return

    def _fixtext(self, text):
        try:
            return _encode(text, 'ascii')
        except UnicodeError:
            return text

    def _fixname(self, key):
        try:
            name = self._names[key]
        except KeyError:
            name = key
            if '}' in name:
                name = '{' + name
            self._names[key] = name = self._fixtext(name)

        return name

    def _start(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = {}
        for key, value in attrib_in.items():
            attrib[fixname(key)] = self._fixtext(value)

        return self._target.start(tag, attrib)

    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = {}
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[fixname(attrib_in[i])] = self._fixtext(attrib_in[i + 1])

        return self._target.start(tag, attrib)

    def _data(self, text):
        return self._target.data(self._fixtext(text))

    def _end(self, tag):
        return self._target.end(self._fixname(tag))

    def _default(self, text):
        prefix = text[:1]
        if prefix == '&':
            try:
                self._target.data(self.entity[text[1:-1]])
            except KeyError:
                from xml.parsers import expat
                raise expat.error('undefined entity %s: line %d, column %d' % (text, self._parser.ErrorLineNumber, self._parser.ErrorColumnNumber))

        elif prefix == '<' and text[:9] == '<!DOCTYPE':
            self._doctype = []
        elif self._doctype is not None:
            if prefix == '>':
                self._doctype = None
                return
            text = string.strip(text)
            if not text:
                return
            self._doctype.append(text)
            n = len(self._doctype)
            if n > 2:
                type = self._doctype[1]
                if type == 'PUBLIC' and n == 4:
                    name, type, pubid, system = self._doctype
                elif type == 'SYSTEM' and n == 3:
                    name, type, system = self._doctype
                    pubid = None
                else:
                    return
                if pubid:
                    pubid = pubid[1:-1]
                self.doctype(name, pubid, system[1:-1])
                self._doctype = None
        return

    def doctype(self, name, pubid, system):
        pass

    def feed(self, data):
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse('', 1)
        tree = self._target.close()
        del self._target
        del self._parser
        return tree# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:14:34 Pacific Daylight Time

# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\direct\showbase\ElementTree.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	SETUP_LOOP        '219'

3	SETUP_EXCEPT      '26'

6	LOAD_FAST         'self'
9	LOAD_ATTR         '_events'
12	LOAD_FAST         'self'
15	LOAD_ATTR         '_index'
18	BINARY_SUBSCR     None
19	STORE_FAST        'item'
22	POP_BLOCK         None
23	JUMP_FORWARD      '195'
26_0	COME_FROM         '3'

26	DUP_TOP           None
27	LOAD_GLOBAL       'IndexError'
30	COMPARE_OP        'exception match'
33	JUMP_IF_FALSE     '194'
36	POP_TOP           None
37	POP_TOP           None
38	POP_TOP           None

39	LOAD_FAST         'self'
42	LOAD_ATTR         '_parser'
45	LOAD_CONST        None
48	COMPARE_OP        'is'
51	JUMP_IF_FALSE     '105'

54	LOAD_FAST         'self'
57	LOAD_ATTR         '_root'
60	LOAD_FAST         'self'
63	STORE_ATTR        'root'

66	SETUP_EXCEPT      '79'

69	LOAD_GLOBAL       'StopIteration'
72	RAISE_VARARGS_1   None
75	POP_BLOCK         None
76	JUMP_ABSOLUTE     '105'
79_0	COME_FROM         '66'

79	DUP_TOP           None
80	LOAD_GLOBAL       'NameError'
83	COMPARE_OP        'exception match'
86	JUMP_IF_FALSE     '101'
89	POP_TOP           None
90	POP_TOP           None
91	POP_TOP           None

92	LOAD_GLOBAL       'IndexError'
95	RAISE_VARARGS_1   None
98	JUMP_ABSOLUTE     '105'
101	END_FINALLY       None
102_0	COME_FROM         '101'
102	JUMP_FORWARD      '105'
105_0	COME_FROM         '102'

105	LOAD_FAST         'self'
108	LOAD_ATTR         '_events'
111	DELETE_SLICE+0    None

112	LOAD_CONST        0
115	LOAD_FAST         'self'
118	STORE_ATTR        '_index'

121	LOAD_FAST         'self'
124	LOAD_ATTR         '_file'
127	LOAD_ATTR         'read'
130	LOAD_CONST        16384
133	CALL_FUNCTION_1   None
136	STORE_FAST        'data'

139	LOAD_FAST         'data'
142	JUMP_IF_FALSE     '164'

145	LOAD_FAST         'self'
148	LOAD_ATTR         '_parser'
151	LOAD_ATTR         'feed'
154	LOAD_FAST         'data'
157	CALL_FUNCTION_1   None
160	POP_TOP           None
161	JUMP_ABSOLUTE     '215'

164	LOAD_FAST         'self'
167	LOAD_ATTR         '_parser'
170	LOAD_ATTR         'close'
173	CALL_FUNCTION_0   None
176	LOAD_FAST         'self'
179	STORE_ATTR        '_root'

182	LOAD_CONST        None
185	LOAD_FAST         'self'
188	STORE_ATTR        '_parser'
191	JUMP_BACK         '3'
194	END_FINALLY       None
195_0	COME_FROM         '23'

195	LOAD_FAST         'self'
198	LOAD_ATTR         '_index'
201	LOAD_CONST        1
204	BINARY_ADD        None
205	LOAD_FAST         'self'
208	STORE_ATTR        '_index'

211	LOAD_FAST         'item'
214	RETURN_VALUE      None
215_0	COME_FROM         '194'
215	JUMP_BACK         '3'
218	POP_BLOCK         None
219_0	COME_FROM         '0'
219	LOAD_CONST        None
222	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 218

