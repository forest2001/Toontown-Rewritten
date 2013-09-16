# 2013.08.22 22:13:33 Pacific Daylight Time
# Embedded file name: textwrap
__revision__ = '$Id: textwrap.py,v 1.1.1.1 2005/04/12 20:52:45 skyler Exp $'
import string, re
try:
    (True, False)
except NameError:
    True, False = (1, 0)

__all__ = ['TextWrapper', 'wrap', 'fill']
_whitespace = '\t\n\x0b\x0c\r '

class TextWrapper():
    __module__ = __name__
    whitespace_trans = string.maketrans(_whitespace, ' ' * len(_whitespace))
    unicode_whitespace_trans = {}
    uspace = ord(u' ')
    for x in map(ord, _whitespace):
        unicode_whitespace_trans[x] = uspace

    wordsep_re = re.compile('(\\s+|[^\\s\\w]*\\w+[a-zA-Z]-(?=\\w+[a-zA-Z])|(?<=[\\w\\!\\"\\\'\\&\\.\\,\\?])-{2,}(?=\\w))')
    sentence_end_re = re.compile('[%s][\\.\\!\\?][\\"\\\']?' % string.lowercase)

    def __init__(self, width = 70, initial_indent = '', subsequent_indent = '', expand_tabs = True, replace_whitespace = True, fix_sentence_endings = False, break_long_words = True):
        self.width = width
        self.initial_indent = initial_indent
        self.subsequent_indent = subsequent_indent
        self.expand_tabs = expand_tabs
        self.replace_whitespace = replace_whitespace
        self.fix_sentence_endings = fix_sentence_endings
        self.break_long_words = break_long_words

    def _munge_whitespace(self, text):
        if self.expand_tabs:
            text = text.expandtabs()
        if self.replace_whitespace:
            if isinstance(text, str):
                text = text.translate(self.whitespace_trans)
            elif isinstance(text, unicode):
                text = text.translate(self.unicode_whitespace_trans)
        return text

    def _split(self, text):
        chunks = self.wordsep_re.split(text)
        chunks = filter(None, chunks)
        return chunks

    def _fix_sentence_endings(self, chunks):
        i = 0
        pat = self.sentence_end_re
        while i < len(chunks) - 1:
            if chunks[i + 1] == ' ' and pat.search(chunks[i]):
                chunks[i + 1] = '  '
                i += 2
            else:
                i += 1

    def _handle_long_word(self, chunks, cur_line, cur_len, width):
        space_left = max(width - cur_len, 1)
        if self.break_long_words:
            cur_line.append(chunks[0][0:space_left])
            chunks[0] = chunks[0][space_left:]
        elif not cur_line:
            cur_line.append(chunks.pop(0))

    def _wrap_chunks(self, chunks):
        lines = []
        if self.width <= 0:
            raise ValueError('invalid width %r (must be > 0)' % self.width)
        while chunks:
            cur_line = []
            cur_len = 0
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            width = self.width - len(indent)
            if chunks[0].strip() == '' and lines:
                del chunks[0]
            while chunks:
                l = len(chunks[0])
                if cur_len + l <= width:
                    cur_line.append(chunks.pop(0))
                    cur_len += l
                else:
                    break

            if chunks and len(chunks[0]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)
            if cur_line and cur_line[-1].strip() == '':
                del cur_line[-1]
            if cur_line:
                lines.append(indent + ''.join(cur_line))

        return lines

    def wrap(self, text):
        text = self._munge_whitespace(text)
        indent = self.initial_indent
        chunks = self._split(text)
        if self.fix_sentence_endings:
            self._fix_sentence_endings(chunks)
        return self._wrap_chunks(chunks)

    def fill(self, text):
        return '\n'.join(self.wrap(text))


def wrap(text, width = 70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)


def fill(text, width = 70, **kwargs):
    w = TextWrapper(width=width, **kwargs)
    return w.fill(text)


def dedent(text):
    lines = text.expandtabs().split('\n')
    margin = None
    for line in lines:
        content = line.lstrip()
        if not content:
            continue
        indent = len(line) - len(content)
        if margin is None:
            margin = indent
        else:
            margin = min(margin, indent)

    if margin is not None and margin > 0:
        for i in range(len(lines)):
            lines[i] = lines[i][margin:]

    return '\n'.join(lines)
# okay decompyling C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\textwrap.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2013.08.22 22:13:33 Pacific Daylight Time
