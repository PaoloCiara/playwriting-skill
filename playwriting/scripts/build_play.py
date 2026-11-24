#!/usr/bin/env python3
"""Build a .docx play from marked text in the writer's own formatting, copied from their document.

  python3 -I build_play.py --describe ORIGINAL.docx        how the writer formats, scene by scene
  python3 -I build_play.py ORIGINAL.docx play.txt OUT.docx

play.txt: one paragraph per line, CODE|text
  T| title line          H| front-matter heading    P| front-matter or costume paragraph
  N| scene heading       (| direction on its own    /| direction inside a speech
  NAME| cue and first line of the speech (any capitals)     +| more of the same speech
  E| end line
  blank line   a blank paragraph, kept exactly (ignored after @open, which adds its own)
  @open        from here, a blank paragraph between speeches and around (| directions
  @tight       from here, only the blank lines you type (the default)
  @blank       one blank paragraph, in either mode
  @page        the next paragraph starts a new page
  # comment

Each code takes the paragraph and font settings the writer uses most for that kind of line, so nothing
is reflowed. Quotes and dashes are kept as typed. The original is only read. OUT must not already exist.
Standard library only.
"""
import argparse, collections, html, os, re, sys, zipfile
from xml.sax.saxutils import escape

def load(path):
    z = zipfile.ZipFile(path); return z, z.read('word/document.xml').decode('utf-8')

def paras(d):
    out = []
    for m in re.finditer(r'<w:p\b(?:[^>]*/>|.*?</w:p>)', d, re.S):
        x = m.group(0)
        ppr = (re.search(r'<w:pPr>.*?</w:pPr>', x, re.S) or [''])[0]
        rest = x.replace(ppr, '', 1) if ppr else x
        rpr = next((r for r in re.findall(r'<w:r\b[^>]*>\s*(<w:rPr>.*?</w:rPr>)', rest, re.S) if 'rFonts' in r or 'w:sz' in r), '')
        t = html.unescape(''.join('\t' if a.startswith('<w:tab') else '\n' if a.startswith(('<w:br', '<w:cr')) else b
            for a, b in re.findall(r'(<w:t(?: [^>]*)?>|<w:tab/>|<w:br\b[^>]*>|<w:cr/>)([^<]*)', rest)))
        out.append([ppr, rpr, t, x])
    return out

SCENE = re.compile(r'^(ACT|SCENE)\b')
def classify(ps):
    c = collections.Counter(p[2].strip() for p in ps if re.fullmatch(r"[A-Z][A-Z0-9 .'’-]{0,24}", p[2].strip()))
    cues = {k for k, n in c.items() if n >= 3}
    kinds, prev, scene = [], '', False
    for ppr, rpr, t, x in ps:
        s = t.strip()
        if not s: k = 'blank'
        elif SCENE.match(s) and s == s.upper(): k, scene = 'scene', True
        elif re.match(r'(THE END|END OF|CURTAIN)', s) and s == s.upper(): k = 'end'
        elif s in cues and scene: k = 'cue'
        elif s.startswith('(') and s.endswith(')'):
            k = 'inner' if 'firstLine="0"' not in ppr and ('w:firstLine=' in ppr or t.startswith('\t') or 'w:left="' in ppr and 'w:left="0"' not in ppr) else 'direction'
        elif not scene: k = 'front'
        else: k = 'speech'
        kinds.append(k)
    return kinds

def most(v, default=''):
    v = [x for x in v if x]; return collections.Counter(v).most_common(1)[0][0] if v else default

def styles(ps, kinds):
    st = {}
    for k in set(kinds):
        mine = [p for p, q in zip(ps, kinds) if q == k]
        st[k] = (most([p[0].replace('<w:pageBreakBefore/>', '') for p in mine]), most([p[1] for p in mine]))
    base = st.get('speech') or ('', '')
    for k in ('front', 'scene', 'cue', 'speech', 'direction', 'end', 'blank'): st.setdefault(k, base)
    st.setdefault('inner', st['direction'])
    return {k: (a or base[0], b or base[1]) for k, (a, b) in st.items()}

def short(ppr):
    f = []
    j = re.search(r'<w:jc w:val="(\w+)"', ppr); f.append(j[1] if j else 'left')
    i = re.search(r'<w:ind ([^/]*)/>', ppr)
    if i and re.search(r'"[1-9]', i[1]): f.append('indent ' + i[1].replace('w:', '').strip())
    l = re.search(r'w:line="(\d+)"', ppr)
    if l: f.append(f'{int(l[1])/240:g} line spacing')
    return ', '.join(f)

def describe(path):
    z, d = load(path); ps = paras(d); kinds = classify(ps)
    f = re.search(r'w:ascii="([^"]+)"', most([p[1] for p in ps])); s = re.search(r'<w:sz w:val="(\d+)"', most([p[1] for p in ps]))
    print('font', f[1] if f else '?', int(s[1]) / 2 if s else '?', 'pt |', re.sub(r'\s+', ' ', ' '.join(re.findall(r'<w:pgMar[^>]*>', d)))[:160])
    print('bold', len(re.findall(r'<w:b(?: w:val="1")?/>', d)), '| italic', len(re.findall(r'<w:i(?: w:val="1")?/>', d)), '| underline', d.count('<w:u '), '| page breaks', len(re.findall(r'w:type="page"|pageBreakBefore', d)))
    for n in z.namelist():
        if re.match(r'word/(header|footer)\d*\.xml', n):
            t = z.read(n).decode('utf-8'); print(n, repr(''.join(re.findall(r'<w:t[^>]*>([^<]*)', t))), 'page number' if 'PAGE' in t else 'no page number')
    groups, cur = [], ['FRONT MATTER', []]
    for i, k in enumerate(kinds):
        if k == 'scene': groups.append(cur); cur = [ps[i][2].strip(), []]
        cur[1].append(i)
    groups.append(cur)
    for name, ix in groups:
        print('\n##', name)
        by = collections.defaultdict(list)
        for i in ix: by[kinds[i]].append(i)
        run = best = 0
        for i in ix:
            run = run + 1 if kinds[i] == 'blank' else 0; best = max(best, run)
        for k in ('front', 'scene', 'cue', 'speech', 'direction', 'inner', 'end'):
            if by[k]:
                look = collections.Counter(short(ps[i][0]) + (', tab' if ps[i][2].startswith('\t') else '') for i in by[k]).most_common(3)
                b = sum(1 for i in by[k] if i and kinds[i - 1] == 'blank')
                print(f'  {k:9} x{len(by[k]):<3} blank before {b}/{len(by[k])} | ' + ' ; '.join(f'{n}× {x}' for x, n in look))
        t = '\n'.join(ps[i][2] for i in ix)
        print(f'  longest run of blanks {best} | straight/curly apostrophes {t.count(chr(39))}/{t.count("’")} | dashes -{len(re.findall(r"-(?=$)", t, re.M))} –{t.count("–")} —{t.count("—")} at breaks')

def build(original, text, out):
    if os.path.exists(out): sys.exit(f'{out} already exists; choose another name.')
    z, d = load(original); ps = paras(d); st = styles(ps, classify(ps))
    body, mode, page, prev = [], 'tight', False, ''
    def add(kind, t=''):
        nonlocal page, prev
        ppr, rpr = st[kind]
        if page: ppr = (ppr or '<w:pPr></w:pPr>').replace('<w:pPr>', '<w:pPr><w:pageBreakBefore/>', 1); page = False
        run = f'<w:r>{rpr}<w:t xml:space="preserve">{escape(t)}</w:t></w:r>' if t else ''
        body.append(f'<w:p>{ppr}{run}</w:p>'); prev = kind
    def gap():
        if mode == 'open' and prev not in ('', 'blank', 'scene') and not page: add('blank')
    for n, raw in enumerate(open(text, encoding='utf-8'), 1):
        l = raw.rstrip('\n')
        if l.startswith('#'): continue
        if not l.strip():
            if mode == 'tight': add('blank')
            continue
        if l[0] == '@':
            if l[1:] in ('open', 'tight'): mode = l[1:]
            elif l == '@blank': add('blank')
            elif l == '@page': page = True
            else: sys.exit(f'line {n}: unknown setting {l}')
            continue
        if '|' not in l: sys.exit(f'line {n}: expected CODE|text')
        k, t = l.split('|', 1)
        if k in ('T', 'H', 'P'): add('front', t)
        elif k == 'N': gap(); add('scene', t)
        elif k == '(': gap(); add('direction', t)
        elif k == '/': add('inner', t)
        elif k == '+':
            if prev == 'direction': gap()
            add('speech', t)
        elif k == 'E': add('end', t)
        elif k == k.upper() and re.match(r'[A-Z]', k): gap(); add('cue', k); add('speech', t)
        else: sys.exit(f'line {n}: unknown code {k!r}')
    i = d.index('<w:body>') + len('<w:body>')
    sect = re.findall(r'<w:sectPr\b.*?</w:sectPr>', d, re.S)
    new = d[:i] + ''.join(body) + (sect[-1] if sect else '') + '</w:body></w:document>'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as o:
        for it in z.infolist():
            if not it.is_dir(): o.writestr(it.filename, new if it.filename == 'word/document.xml' else z.read(it.filename))
    print('wrote', out)

def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('--describe', metavar='ORIGINAL'); a.add_argument('files', nargs='*')
    o = a.parse_args()
    if o.describe: describe(o.describe)
    elif len(o.files) == 3: build(*o.files)
    else: a.error('give ORIGINAL.docx play.txt OUT.docx, or --describe ORIGINAL.docx')

if __name__ == '__main__': main()
