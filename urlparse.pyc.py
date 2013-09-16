# 2013.08.22 22:13:39 Pacific Daylight Time
# Embedded file name: urlparse
__all__ = ['urlparse',
 'urlunparse',
 'urljoin',
 'urldefrag',
 'urlsplit',
 'urlunsplit']
uses_relative = ['ftp',
 'http',
 'gopher',
 'nntp',
 'imap',
 'wais',
 'file',
 'https',
 'shttp',
 'mms',
 'prospero',
 'rtsp',
 'rtspu',
 '']
uses_netloc = ['ftp',
 'http',
 'gopher',
 'nntp',
 'telnet',
 'imap',
 'wais',
 'file',
 'mms',
 'https',
 'shttp',
 'snews',
 'prospero',
 'rtsp',
 'rtspu',
 'rsync',
 '']
non_hierarchical = ['gopher',
 'hdl',
 'mailto',
 'news',
 'telnet',
 'wais',
 'imap',
 'snews',
 'sip']
uses_params = ['ftp',
 'hdl',
 'prospero',
 'http',
 'imap',
 'https',
 'shttp',
 'rtsp',
 'rtspu',
 'sip',
 'mms',
 '']
uses_query = ['http',
 'wais',
 'imap',
 'https',
 'shttp',
 'mms',
 'gopher',
 'rtsp',
 'rtspu',
 'sip',
 '']
uses_fragment = ['ftp',
 'hdl',
 'http',
 'gopher',
 'news',
 'nntp',
 'wais',
 'https',
 'shttp',
 'snews',
 'file',
 'prospero',
 '']
scheme_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.'
MAX_CACHE_SIZE = 20
_parse_cache = {}

def clear_cache():
    global _parse_cache
    _parse_cache = {}


def urlparse(url, scheme = '', allow_fragments = 1):
    tuple = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = tuple
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    return (scheme,
     netloc,
     url,
     params,
     query,
     fragment)


def _splitparams(url):
    if '/' in url:
        i = url.find(';', url.rfind('/'))
        if i < 0:
            return (url, '')
    else:
        i = url.find(';')
    return (url[:i], url[i + 1:])


def _splitnetloc(url, start = 0):
    for c in '/?#':
        delim = url.find(c, start)
        if delim >= 0:
            break
    else:
        delim = len(url)

    return (url[start:delim], url[delim:])


def urlsplit(url, scheme = '', allow_fragments = 1):
    key = (url, scheme, allow_fragments)
    cached = _parse_cache.get(key, None)
    if cached:
        return cached
    if len(_parse_cache) >= MAX_CACHE_SIZE:
        clear_cache()
    netloc = query = fragment = ''
    i = url.find(':')
    if i > 0:
        if url[:i] == 'http':
            scheme = url[:i].lower()
            url = url[i + 1:]
            if url[:2] == '//':
                netloc, url = _splitnetloc(url, 2)
            if allow_fragments and '#' in url:
                url, fragment = url.split('#', 1)
            if '?' in url:
                url, query = url.split('?', 1)
            tuple = (scheme,
             netloc,
             url,
             query,
             fragment)
            _parse_cache[key] = tuple
            return tuple
        for c in url[:i]:
            if c not in scheme_chars:
                break
        else:
            scheme, url = url[:i].lower(), url[i + 1:]

    if scheme in uses_netloc and url[:2] == '//':
        netloc, url = _splitnetloc(url, 2)
    if allow_fragments and scheme in uses_fragment and '#' in url:
        url, fragment = url.split('#', 1)
    if scheme in uses_query and '?' in url:
        url, query = url.split('?', 1)
    tuple = (scheme,
     netloc,
     url,
     query,
     fragment)
    _parse_cache[key] = tuple
    return tuple


def urlunparse((scheme, netloc, url, params, query, fragment)):
    if params:
        url = '%s;%s' % (url, params)
    return urlunsplit((scheme,
     netloc,
     url,
     query,
     fragment))


def urlunsplit((scheme, netloc, url, query, fragment)):
    if netloc or scheme and scheme in uses_netloc and url[:2] != '//':
        if url and url[:1] != '/':
            url = '/' + url
        url = '//' + (netloc or '') + url
    if scheme:
        url = scheme + ':' + url
    if query:
        url = url + '?' + query
    if fragment:
        url = url + '#' + fragment
    return url


def urljoin--- This code section failed: ---

0	LOAD_FAST         'base'
3	JUMP_IF_TRUE      '13'

6	LOAD_FAST         'url'
9	RETURN_VALUE      None
10	JUMP_FORWARD      '13'
13_0	COME_FROM         '10'

13	LOAD_FAST         'url'
16	JUMP_IF_TRUE      '26'

19	LOAD_FAST         'base'
22	RETURN_VALUE      None
23	JUMP_FORWARD      '26'
26_0	COME_FROM         '23'

26	LOAD_GLOBAL       'urlparse'
29	LOAD_FAST         'base'
32	LOAD_CONST        ''
35	LOAD_FAST         'allow_fragments'
38	CALL_FUNCTION_3   None
41	UNPACK_SEQUENCE_6 None
44	STORE_FAST        'bscheme'
47	STORE_FAST        'bnetloc'
50	STORE_FAST        'bpath'
53	STORE_FAST        'bparams'
56	STORE_FAST        'bquery'
59	STORE_FAST        'bfragment'

62	LOAD_GLOBAL       'urlparse'
65	LOAD_FAST         'url'
68	LOAD_FAST         'bscheme'
71	LOAD_FAST         'allow_fragments'
74	CALL_FUNCTION_3   None
77	UNPACK_SEQUENCE_6 None
80	STORE_FAST        'scheme'
83	STORE_FAST        'netloc'
86	STORE_FAST        'path'
89	STORE_FAST        'params'
92	STORE_FAST        'query'
95	STORE_FAST        'fragment'

98	LOAD_FAST         'scheme'
101	LOAD_FAST         'bscheme'
104	COMPARE_OP        '!='
107	JUMP_IF_TRUE      '122'
110	LOAD_FAST         'scheme'
113	LOAD_GLOBAL       'uses_relative'
116	COMPARE_OP        'not in'
119_0	COME_FROM         '107'
119	JUMP_IF_FALSE     '129'

122	LOAD_FAST         'url'
125	RETURN_VALUE      None
126	JUMP_FORWARD      '129'
129_0	COME_FROM         '126'

129	LOAD_FAST         'scheme'
132	LOAD_GLOBAL       'uses_netloc'
135	COMPARE_OP        'in'
138	JUMP_IF_FALSE     '187'

141	LOAD_FAST         'netloc'
144	JUMP_IF_FALSE     '178'

147	LOAD_GLOBAL       'urlunparse'
150	LOAD_FAST         'scheme'
153	LOAD_FAST         'netloc'
156	LOAD_FAST         'path'
159	LOAD_FAST         'params'
162	LOAD_FAST         'query'
165	LOAD_FAST         'fragment'
168	BUILD_TUPLE_6     None
171	CALL_FUNCTION_1   None
174	RETURN_VALUE      None
175	JUMP_FORWARD      '178'
178_0	COME_FROM         '175'

178	LOAD_FAST         'bnetloc'
181	STORE_FAST        'netloc'
184	JUMP_FORWARD      '187'
187_0	COME_FROM         '184'

187	LOAD_FAST         'path'
190	LOAD_CONST        1
193	SLICE+2           None
194	LOAD_CONST        '/'
197	COMPARE_OP        '=='
200	JUMP_IF_FALSE     '234'

203	LOAD_GLOBAL       'urlunparse'
206	LOAD_FAST         'scheme'
209	LOAD_FAST         'netloc'
212	LOAD_FAST         'path'
215	LOAD_FAST         'params'
218	LOAD_FAST         'query'
221	LOAD_FAST         'fragment'
224	BUILD_TUPLE_6     None
227	CALL_FUNCTION_1   None
230	RETURN_VALUE      None
231	JUMP_FORWARD      '234'
234_0	COME_FROM         '231'

234	LOAD_FAST         'path'
237	JUMP_IF_TRUE      '249'
240	LOAD_FAST         'params'
243	JUMP_IF_TRUE      '249'
246	LOAD_FAST         'query'
249	JUMP_IF_TRUE      '283'

252	LOAD_GLOBAL       'urlunparse'
255	LOAD_FAST         'scheme'
258	LOAD_FAST         'netloc'
261	LOAD_FAST         'bpath'
264	LOAD_FAST         'bparams'
267	LOAD_FAST         'bquery'
270	LOAD_FAST         'fragment'
273	BUILD_TUPLE_6     None
276	CALL_FUNCTION_1   None
279	RETURN_VALUE      None
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'

283	LOAD_FAST         'bpath'
286	LOAD_ATTR         'split'
289	LOAD_CONST        '/'
292	CALL_FUNCTION_1   None
295	LOAD_CONST        -1
298	SLICE+2           None
299	LOAD_FAST         'path'
302	LOAD_ATTR         'split'
305	LOAD_CONST        '/'
308	CALL_FUNCTION_1   None
311	BINARY_ADD        None
312	STORE_FAST        'segments'

315	LOAD_FAST         'segments'
318	LOAD_CONST        -1
321	BINARY_SUBSCR     None
322	LOAD_CONST        '.'
325	COMPARE_OP        '=='
328	JUMP_IF_FALSE     '344'

331	LOAD_CONST        ''
334	LOAD_FAST         'segments'
337	LOAD_CONST        -1
340	STORE_SUBSCR      None
341	JUMP_FORWARD      '344'
344_0	COME_FROM         '341'

344	SETUP_LOOP        '376'
347	LOAD_CONST        '.'
350	LOAD_FAST         'segments'
353	COMPARE_OP        'in'
356	JUMP_IF_FALSE     '375'

359	LOAD_FAST         'segments'
362	LOAD_ATTR         'remove'
365	LOAD_CONST        '.'
368	CALL_FUNCTION_1   None
371	POP_TOP           None
372	JUMP_BACK         '347'
375	POP_BLOCK         None
376_0	COME_FROM         '344'

376	SETUP_LOOP        '493'

379	LOAD_CONST        1
382	STORE_FAST        'i'

385	LOAD_GLOBAL       'len'
388	LOAD_FAST         'segments'
391	CALL_FUNCTION_1   None
394	LOAD_CONST        1
397	BINARY_SUBTRACT   None
398	STORE_FAST        'n'

401	SETUP_LOOP        '489'
404	LOAD_FAST         'i'
407	LOAD_FAST         'n'
410	COMPARE_OP        '<'
413	JUMP_IF_FALSE     '487'

416	LOAD_FAST         'segments'
419	LOAD_FAST         'i'
422	BINARY_SUBSCR     None
423	LOAD_CONST        '..'
426	COMPARE_OP        '=='
429	JUMP_IF_FALSE     '474'
432	LOAD_FAST         'segments'
435	LOAD_FAST         'i'
438	LOAD_CONST        1
441	BINARY_SUBTRACT   None
442	BINARY_SUBSCR     None
443	LOAD_CONST        ('', '..')
446	COMPARE_OP        'not in'
449_0	COME_FROM         '429'
449	JUMP_IF_FALSE     '474'

452	LOAD_FAST         'segments'
455	LOAD_FAST         'i'
458	LOAD_CONST        1
461	BINARY_SUBTRACT   None
462	LOAD_FAST         'i'
465	LOAD_CONST        1
468	BINARY_ADD        None
469	DELETE_SLICE+3    None

470	BREAK_LOOP        None
471	JUMP_FORWARD      '474'
474_0	COME_FROM         '471'

474	LOAD_FAST         'i'
477	LOAD_CONST        1
480	BINARY_ADD        None
481	STORE_FAST        'i'
484	JUMP_BACK         '404'
487	POP_BLOCK         None

488	BREAK_LOOP        None
489_0	COME_FROM         '401'
489	JUMP_BACK         '379'
492	POP_BLOCK         None
493_0	COME_FROM         '376'

493	LOAD_FAST         'segments'
496	LOAD_CONST        ''
499	LOAD_CONST        '..'
502	BUILD_LIST_2      None
505	COMPARE_OP        '=='
508	JUMP_IF_FALSE     '524'

511	LOAD_CONST        ''
514	LOAD_FAST         'segments'
517	LOAD_CONST        -1
520	STORE_SUBSCR      None
521	JUMP_FORWARD      '574'

524	LOAD_GLOBAL       'len'
527	LOAD_FAST         'segments'
530	CALL_FUNCTION_1   None
533	LOAD_CONST        2
536	COMPARE_OP        '>='
539	JUMP_IF_FALSE     '574'
542	LOAD_FAST         'segments'
545	LOAD_CONST        -1
548	BINARY_SUBSCR     None
549	LOAD_CONST        '..'
552	COMPARE_OP        '=='
555_0	COME_FROM         '539'
555	JUMP_IF_FALSE     '574'

558	LOAD_CONST        ''
561	BUILD_LIST_1      None
564	LOAD_FAST         'segments'
567	LOAD_CONST        -2
570	STORE_SLICE+1     None
571	JUMP_FORWARD      '574'
574_0	COME_FROM         '521'
574_1	COME_FROM         '571'

574	LOAD_GLOBAL       'urlunparse'
577	LOAD_FAST         'scheme'
580	LOAD_FAST         'netloc'
583	LOAD_CONST        '/'
586	LOAD_ATTR         'join'
589	LOAD_FAST         'segments'
592	CALL_FUNCTION_1   None
595	LOAD_FAST         'params'
598	LOAD_FAST         'query'
601	LOAD_FAST         'fragment'
604	BUILD_TUPLE_6     None
607	CALL_FUNCTION_1   None
610	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 492


def urldefrag(url):
    if '#' in url:
        s, n, p, a, q, frag = urlparse(url)
        defrag = urlunparse((s,
         n,
         p,
         a,
         q,
         ''))
        return (defrag, frag)
    else:
        return (url, '')


test_input = '\n      http://a/b/c/d\n\n      g:h        = <URL:g:h>\n      http:g     = <URL:http://a/b/c/g>\n      http:      = <URL:http://a/b/c/d>\n      g          = <URL:http://a/b/c/g>\n      ./g        = <URL:http://a/b/c/g>\n      g/         = <URL:http://a/b/c/g/>\n      /g         = <URL:http://a/g>\n      //g        = <URL:http://g>\n      ?y         = <URL:http://a/b/c/d?y>\n      g?y        = <URL:http://a/b/c/g?y>\n      g?y/./x    = <URL:http://a/b/c/g?y/./x>\n      .          = <URL:http://a/b/c/>\n      ./         = <URL:http://a/b/c/>\n      ..         = <URL:http://a/b/>\n      ../        = <URL:http://a/b/>\n      ../g       = <URL:http://a/b/g>\n      ../..      = <URL:http://a/>\n      ../../g    = <URL:http://a/g>\n      ../../../g = <URL:http://a/../g>\n      ./../g     = <URL:http://a/b/g>\n      ./g/.      = <URL:http://a/b/c/g/>\n      /./g       = <URL:http://a/./g>\n      g/./h      = <URL:http://a/b/c/g/h>\n      g/../h     = <URL:http://a/b/c/h>\n      http:g     = <URL:http://a/b/c/g>\n      http:      = <URL:http://a/b/c/d>\n      http:?y         = <URL:
# Can't uncompyle C:\Users\Maverick\Documents\Visual Studio 2010\Projects\Unfreezer\py2\urlparse.pyc
Traceback (most recent call last):
  File "C:\python27\lib\uncompyle2\__init__.py", line 206, in main
    uncompyle_file(infile, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 143, in uncompyle_file
    uncompyle(version, co, outstream, showasm, showast)
  File "C:\python27\lib\uncompyle2\__init__.py", line 132, in uncompyle
    raise walk.ERROR
ParserError: --- This code section failed: ---

0	LOAD_CONST        None
3	IMPORT_NAME       'sys'
6	STORE_FAST        'sys'

9	LOAD_CONST        ''
12	STORE_FAST        'base'

15	LOAD_FAST         'sys'
18	LOAD_ATTR         'argv'
21	LOAD_CONST        1
24	SLICE+1           None
25	JUMP_IF_FALSE     '80'

28	LOAD_FAST         'sys'
31	LOAD_ATTR         'argv'
34	LOAD_CONST        1
37	BINARY_SUBSCR     None
38	STORE_FAST        'fn'

41	LOAD_FAST         'fn'
44	LOAD_CONST        '-'
47	COMPARE_OP        '=='
50	JUMP_IF_FALSE     '65'

53	LOAD_FAST         'sys'
56	LOAD_ATTR         'stdin'
59	STORE_FAST        'fp'
62	JUMP_ABSOLUTE     '104'

65	LOAD_GLOBAL       'open'
68	LOAD_FAST         'fn'
71	CALL_FUNCTION_1   None
74	STORE_FAST        'fp'
77	JUMP_FORWARD      '104'

80	LOAD_CONST        None
83	IMPORT_NAME       'StringIO'
86	STORE_FAST        'StringIO'

89	LOAD_FAST         'StringIO'
92	LOAD_ATTR         'StringIO'
95	LOAD_GLOBAL       'test_input'
98	CALL_FUNCTION_1   None
101	STORE_FAST        'fp'
104_0	COME_FROM         '77'

104	SETUP_LOOP        '322'

107	LOAD_FAST         'fp'
110	LOAD_ATTR         'readline'
113	CALL_FUNCTION_0   None
116	STORE_FAST        'line'

119	LOAD_FAST         'line'
122	JUMP_IF_TRUE      '129'
125	BREAK_LOOP        None
126	JUMP_FORWARD      '129'
129_0	COME_FROM         '126'

129	LOAD_FAST         'line'
132	LOAD_ATTR         'split'
135	CALL_FUNCTION_0   None
138	STORE_FAST        'words'

141	LOAD_FAST         'words'
144	JUMP_IF_TRUE      '153'

147	CONTINUE          '107'
150	JUMP_FORWARD      '153'
153_0	COME_FROM         '150'

153	LOAD_FAST         'words'
156	LOAD_CONST        0
159	BINARY_SUBSCR     None
160	STORE_FAST        'url'

163	LOAD_GLOBAL       'urlparse'
166	LOAD_FAST         'url'
169	CALL_FUNCTION_1   None
172	STORE_FAST        'parts'

175	LOAD_CONST        '%-10s : %s'
178	LOAD_FAST         'url'
181	LOAD_FAST         'parts'
184	BUILD_TUPLE_2     None
187	BINARY_MODULO     None
188	PRINT_ITEM        None
189	PRINT_NEWLINE_CONT None

190	LOAD_GLOBAL       'urljoin'
193	LOAD_FAST         'base'
196	LOAD_FAST         'url'
199	CALL_FUNCTION_2   None
202	STORE_FAST        'abs'

205	LOAD_FAST         'base'
208	JUMP_IF_TRUE      '220'

211	LOAD_FAST         'abs'
214	STORE_FAST        'base'
217	JUMP_FORWARD      '220'
220_0	COME_FROM         '217'

220	LOAD_CONST        '<URL:%s>'
223	LOAD_FAST         'abs'
226	BINARY_MODULO     None
227	STORE_FAST        'wrapped'

230	LOAD_CONST        '%-10s = %s'
233	LOAD_FAST         'url'
236	LOAD_FAST         'wrapped'
239	BUILD_TUPLE_2     None
242	BINARY_MODULO     None
243	PRINT_ITEM        None
244	PRINT_NEWLINE_CONT None

245	LOAD_GLOBAL       'len'
248	LOAD_FAST         'words'
251	CALL_FUNCTION_1   None
254	LOAD_CONST        3
257	COMPARE_OP        '=='
260	JUMP_IF_FALSE     '318'
263	LOAD_FAST         'words'
266	LOAD_CONST        1
269	BINARY_SUBSCR     None
270	LOAD_CONST        '='
273	COMPARE_OP        '=='
276_0	COME_FROM         '260'
276	JUMP_IF_FALSE     '318'

279	LOAD_FAST         'wrapped'
282	LOAD_FAST         'words'
285	LOAD_CONST        2
288	BINARY_SUBSCR     None
289	COMPARE_OP        '!='
292	JUMP_IF_FALSE     '315'

295	LOAD_CONST        'EXPECTED'
298	PRINT_ITEM        None
299	LOAD_FAST         'words'
302	LOAD_CONST        2
305	BINARY_SUBSCR     None
306	PRINT_ITEM_CONT   None
307	LOAD_CONST        '!!!!!!!!!!'
310	PRINT_ITEM_CONT   None
311	PRINT_NEWLINE_CONT None
312	JUMP_ABSOLUTE     '318'
315	JUMP_BACK         '107'
318	JUMP_BACK         '107'
321	POP_BLOCK         None
322_0	COME_FROM         '1http://a/b/c/d?y>\n      http:g?y        = <URL:http://a/b/c/g?y>\n      http:g?y/./x    = <URL:http://a/b/c/g?y/./x>\n'

def test--- This code section failed: ---

0	LOAD_CONST        None
3	IMPORT_NAME       'sys'
6	STORE_FAST        'sys'

9	LOAD_CONST        ''
12	STORE_FAST        'base'

15	LOAD_FAST         'sys'
18	LOAD_ATTR         'argv'
21	LOAD_CONST        1
24	SLICE+1           None
25	JUMP_IF_FALSE     '80'

28	LOAD_FAST         'sys'
31	LOAD_ATTR         'argv'
34	LOAD_CONST        1
37	BINARY_SUBSCR     None
38	STORE_FAST        'fn'

41	LOAD_FAST         'fn'
44	LOAD_CONST        '-'
47	COMPARE_OP        '=='
50	JUMP_IF_FALSE     '65'

53	LOAD_FAST         'sys'
56	LOAD_ATTR         'stdin'
59	STORE_FAST        'fp'
62	JUMP_ABSOLUTE     '104'

65	LOAD_GLOBAL       'open'
68	LOAD_FAST         'fn'
71	CALL_FUNCTION_1   None
74	STORE_FAST        'fp'
77	JUMP_FORWARD      '104'

80	LOAD_CONST        None
83	IMPORT_NAME       'StringIO'
86	STORE_FAST        'StringIO'

89	LOAD_FAST         'StringIO'
92	LOAD_ATTR         'StringIO'
95	LOAD_GLOBAL       'test_input'
98	CALL_FUNCTION_1   None
101	STORE_FAST        'fp'
104_0	COME_FROM         '77'

104	SETUP_LOOP        '322'

107	LOAD_FAST         'fp'
110	LOAD_ATTR         'readline'
113	CALL_FUNCTION_0   None
116	STORE_FAST        'line'

119	LOAD_FAST         'line'
122	JUMP_IF_TRUE      '129'
125	BREAK_LOOP        None
126	JUMP_FORWARD      '129'
129_0	COME_FROM         '126'

129	LOAD_FAST         'line'
132	LOAD_ATTR         'split'
135	CALL_FUNCTION_0   None
138	STORE_FAST        'words'

141	LOAD_FAST         'words'
144	JUMP_IF_TRUE      '153'

147	CONTINUE          '107'
150	JUMP_FORWARD      '153'
153_0	COME_FROM         '150'

153	LOAD_FAST         'words'
156	LOAD_CONST        0
159	BINARY_SUBSCR     None
160	STORE_FAST        'url'

163	LOAD_GLOBAL       'urlparse'
166	LOAD_FAST         'url'
169	CALL_FUNCTION_1   None
172	STORE_FAST        'parts'

175	LOAD_CONST        '%-10s : %s'
178	LOAD_FAST         'url'
181	LOAD_FAST         'parts'
184	BUILD_TUPLE_2     None
187	BINARY_MODULO     None
188	PRINT_ITEM        None
189	PRINT_NEWLINE_CONT None

190	LOAD_GLOBAL       'urljoin'
193	LOAD_FAST         'base'
196	LOAD_FAST         'url'
199	CALL_FUNCTION_2   None
202	STORE_FAST        'abs'

205	LOAD_FAST         'base'
208	JUMP_IF_TRUE      '220'

211	LOAD_FAST         'abs'
214	STORE_FAST        'base'
217	JUMP_FORWARD      '220'
220_0	COME_FROM         '217'

220	LOAD_CONST        '<URL:%s>'
223	LOAD_FAST         'abs'
226	BINARY_MODULO     None
227	STORE_FAST        'wrapped'

230	LOAD_CONST        '%-10s = %s'
233	LOAD_FAST         'url'
236	LOAD_FAST         'wrapped'
239	BUILD_TUPLE_2     None
242	BINARY_MODULO     None
243	PRINT_ITEM        None
244	PRINT_NEWLINE_CONT None

245	LOAD_GLOBAL       'len'
248	LOAD_FAST         'words'
251	CALL_FUNCTION_1   None
254	LOAD_CONST        3
257	COMPARE_OP        '=='
260	JUMP_IF_FALSE     '318'
263	LOAD_FAST         'words'
266	LOAD_CONST        1
269	BINARY_SUBSCR     None
270	LOAD_CONST        '='
273	COMPARE_OP        '=='
276_0	COME_FROM         '260'
276	JUMP_IF_FALSE     '318'

279	LOAD_FAST         'wrapped'
282	LOAD_FAST         'words'
285	LOAD_CONST        2
288	BINARY_SUBSCR     None
289	COMPARE_OP        '!='
292	JUMP_IF_FALSE     '315'

295	LOAD_CONST        'EXPECTED'
298	PRINT_ITEM        None
299	LOAD_FAST         'words'
302	LOAD_CONST        2
305	BINARY_SUBSCR     None
306	PRINT_ITEM_CONT   None
307	LOAD_CONST        '!!!!!!!!!!'
310	PRINT_ITEM_CONT   None
311	PRINT_NEWLINE_CONT None
312	JUMP_ABSOLUTE     '318'
315	JUMP_BACK         '107'
318	JUMP_BACK         '107'
321	POP_BLOCK         None
322_0	COME_FROM         '104'

Syntax error at or near `POP_BLOCK' token at offset 321


if __name__ == '__main__':
    test()# decompiled 0 files: 0 okay, 1 failed, 0 verify failed
# 2013.08.22 22:13:39 Pacific Daylight Time
04'

Syntax error at or near `POP_BLOCK' token at offset 321

