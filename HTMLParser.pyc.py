# 2013.08.22 22:13:05 Pacific Daylight Time
# Embedded file name: HTMLParser
import markupbase
import re
interesting_normal = re.compile('[&<]')
interesting_cdata = re.compile('<(/|\\Z)')
incomplete = re.compile('&[a-zA-Z#]')
entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile('--\\s*>')
tagfind = re.compile('[a-zA-Z][-.a-zA-Z0-9:_]*')
attrfind = re.compile('\\s*([a-zA-Z_][-.:a-zA-Z_0-9]*)(\\s*=\\s*(\\\'[^\\\']*\\\'|"[^"]*"|[-a-zA-Z0-9./,:;+*%?!&$\\(\\)_#=~@]*))?')
locatestarttagend = re.compile('\n  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name\n  (?:\\s+                             # whitespace before attribute name\n    (?:[a-zA-Z_][-.:a-zA-Z0-9_]*     # attribute name\n      (?:\\s*=\\s*                     # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |\\"[^\\"]*\\"                # LIT-enclosed value\n          |[^\'\\">\\s]+                # bare value\n         )\n       )?\n     )\n   )*\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
endendtag = re.compile('>')
endtagfind = re.compile('</\\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\\s*>')

class HTMLParseError(Exception):
    __module__ = __name__

    def __init__(self, msg, position = (None, None)):
        self.msg = msg
        self.lineno = position[0]
        self.offset = position[1]

    def __str__(self):
        result = self.msg
        if self.lineno is not None:
            result = result + ', at line %d' % self.lineno
        if self.offset is not None:
            result = result + ', column %d' % (self.offset + 1)
        return result


class HTMLParser(markupbase.ParserBase):
    __module__ = __name__
    CDATA_CONTENT_ELEMENTS = ('script', 'style')

    def __init__(self):
        self.reset()

    def reset(self):
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        markupbase.ParserBase.reset(self)

    def feed(self, data):
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        self.goahead(1)

    def error(self, message):
        raise HTMLParseError(message, self.getpos())

    __starttag_text = None

    def get_starttag_text(self):
        return self.__starttag_text

    def set_cdata_mode(self):
        self.interesting = interesting_cdata

    def clear_cdata_mode(self):
        self.interesting = interesting_normal

    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            match = self.interesting.search(rawdata, i)
            if match:
                j = match.start()
            else:
                j = n
            if i < j:
                self.handle_data(rawdata[i:j])
            i = self.updatepos(i, j)
            if i == n:
                break
            startswith = rawdata.startswith
            if startswith('<', i):
                if starttagopen.match(rawdata, i):
                    k = self.parse_starttag(i)
                elif startswith('</', i):
                    k = self.parse_endtag(i)
                elif startswith('<!--', i):
                    k = self.parse_comment(i)
                elif startswith('<?', i):
                    k = self.parse_pi(i)
                elif startswith('<!', i):
                    k = self.parse_declaration(i)
                elif i + 1 < n:
                    self.handle_data('<')
                    k = i + 1
                else:
                    break
                if k < 0:
                    if end:
                        self.error('EOF in middle of construct')
                    break
                i = self.updatepos(i, k)
            elif startswith('&#', i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                else:
                    break
            elif startswith('&', i):
                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    if end and match.group() == rawdata[i:]:
                        self.error('EOF in middle of entity or char ref')
                    break
                elif i + 1 < n:
                    self.handle_data('&')
                    i = self.updatepos(i, i + 1)
                else:
                    break

        if end and i < n:
            self.handle_data(rawdata[i:n])
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    def parse_pi(self, i):
        rawdata = self.rawdata
        match = piclose.search(rawdata, i + 2)
        if not match:
            return -1
        j = match.start()
        self.handle_pi(rawdata[i + 2:j])
        j = match.end()
        return j

    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]
        attrs = []
        match = tagfind.match(rawdata, i + 1)
        k = match.end()
        self.lasttag = tag = rawdata[i + 1:k].lower()
        while k < endpos:
            m = attrfind.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == "'" == attrvalue[-1:] or attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
                attrvalue = self.unescape(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in ('>', '/>'):
            lineno, offset = self.getpos()
            if '\n' in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count('\n')
                offset = len(self.__starttag_text) - self.__starttag_text.rfind('\n')
            else:
                offset = offset + len(self.__starttag_text)
            self.error('junk characters in start tag: %r' % (rawdata[k:endpos][:20],))
        if end.endswith('/>'):
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode()
        return endpos

    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j + 1]
            if next == '>':
                return j + 1
            if next == '/':
                if rawdata.startswith('/>', j):
                    return j + 2
                if rawdata.startswith('/', j):
                    return -1
                self.updatepos(i, j + 1)
                self.error('malformed empty start tag')
            if next == '':
                return -1
            if next in 'abcdefghijklmnopqrstuvwxyz=/ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                return -1
            self.updatepos(i, j)
            self.error('malformed start tag')
        raise AssertionError('we should not get here!')

    def parse_endtag(self, i):
        rawdata = self.rawdata
        match = endendtag.search(rawdata, i + 1)
        if not match:
            return -1
        j = match.end()
        match = endtagfind.match(rawdata, i)
        if not match:
            self.error('bad end tag: %r' % (rawdata[i:j],))
        tag = match.group(1)
        self.handle_endtag(tag.lower())
        self.clear_cdata_mode()
        return j

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        self.error('unknown declaration: %r' % (data,))

    def unescape(self, s):
        if '&' not in s:
            return s
        s = s.replace('&lt;', '<')
        s = s.replace('&gt;', '>')
        s = s.replace('&apos;', "'")
        s = s.replace('&quot;', '"')
        s = s.replace('&amp;', '&')
        return s
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\HTMLParser.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:05 Pacific Daylight Time
