#!/usr/bin/env python3
"""Read a stage play (.docx or .txt), label it, and flag lines worth a second look.

  python3 -I read_play.py PLAY            counts and flagged lines, by scene
  python3 -I read_play.py PLAY --text     the labelled script
  python3 -I read_play.py PLAY --json     counts only, for comparing drafts

Flags are candidates, not verdicts. Standard library only.
"""
import argparse, collections, json, re, sys, zipfile
import xml.etree.ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def paragraphs(path):
    if path.lower().endswith('.docx'):
        root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml'))
        for p in root.iter(W + 'p'):
            out = []
            for el in p.iter():
                if el.tag == W + 't': out.append(el.text or '')
                elif el.tag == W + 'tab': out.append(' ')
                elif el.tag in (W + 'br', W + 'cr'): out.append('\n')
            for piece in ''.join(out).split('\n'):
                yield piece.strip()
    else:
        with open(path, encoding='utf-8') as f:
            for line in f: yield line.strip()

SCENE = re.compile(r'^(ACT|SCENE)\b[ .:]*[A-Z0-9]', re.I)
CUE = re.compile(r"^([A-Z][A-Z0-9 .'’-]{0,24}?)(\s*\((?:con|CON)[^)]*\))?$")

NOT_NAMES = re.compile(r'^(THE END|END OF|CURTAIN|BLACKOUT|CHARACTERS?|SETTING|PLACE|TIME|CAST|PROLOGUE|EPILOGUE|AT RISE)\b')

def parse(path):
    paras = [p for p in paragraphs(path) if p]
    counts = collections.Counter(m.group(1).strip() for p in paras
                                 if (m := CUE.match(p)) and not SCENE.match(p) and not NOT_NAMES.match(p))
    need = 3 if len(paras) > 60 else 1      # a short scene may have a one-line part
    cues = {c for c, n in counts.items() if n >= need}
    items, scene, who, started = [], 'FRONT MATTER', None, False
    for p in paras:
        if SCENE.match(p) and p == p.upper():
            scene, who, started = p, None, True; continue
        m = CUE.match(p)
        if m and m.group(1).strip() in cues:
            who, started = m.group(1).strip(), True; continue
        if not started: continue
        if re.match(r'^(THE END|END OF (THE )?(PLAY|ACT|SCENE)|CURTAIN|BLACKOUT)\b', p) and p == p.upper():
            who = None; continue
        # split leading or trailing parentheticals from spoken text
        for part in re.split(r'(\([^()]*\))', p):
            part = part.strip()
            if not part: continue
            if part.startswith('('): items.append((scene, 'DIR', None, part))
            elif who: items.append((scene, 'SAY', who, part))
    return items, cues

FEEL = r"angry|mad|sad|hurt|happy|ashamed|afraid|scared|lonely|sorry|jealous|proud|upset|annoyed|embarrassed|guilty"
FLAGS = [
 ('feeling stated', re.compile(rf"\b(I feel|I felt|I'?m|I am|I was|you'?re|you are|you were|makes? me)\s+(so |just |still |really )?({FEEL})\b|\bI (miss|forgive|forgave|hate) you\b|\bhurt me\b|\bmy feelings\b", re.I)),
 ('abstract relationship word', re.compile(r"\b(closure|accountab\w*|trust(ed)?|loyal\w*|communicat\w*|relationship|innocence|honest with|respect(ed)?|vulnerab\w*|boundar\w*|commitment|of value)\b", re.I)),
 ('shared history', re.compile(r"\b(as you know|remember when|you always|you never|you used to|I used to|we used to|we were|(a few|three|two|four|five|seven|\d+) (months|years)( ago)?)\b", re.I)),
 ('self or other analysed', re.compile(r"\b(you'?re (just )?(not letting|choosing)|you think (it|that)|because (I|you|it) was|I (was|have been|'ve been) (ashamed|waiting)|that'?s what makes|the (strong|right) thing)\b", re.I)),
]
OUTWARD = re.compile(r"to the audience|out front|\baside\b|to us\b|to the house", re.I)
INNER = re.compile(r"\b(regrets?|realiz\w+|realis\w+|knows?|wants? to|doesn'?t want|feels?|remembers?|hopes?|decides?|understands?|means? to|meant|thinks better|both (hear|know))\b", re.I)
norm = lambda s: s.replace('’', "'")
words = lambda s: len(re.findall(r"[\w'’]+", s))

def analyse(items):
    per = collections.OrderedDict()
    flagged = []
    run = {}
    for scene, kind, who, text in items:
        d = per.setdefault(scene, collections.Counter())
        t = norm(text)
        if kind == 'SAY':
            d['spoken words'] += words(t); d['lines'] += 1; d[f'words {who}'] += words(t)
            if words(t) > 40: d['long passages'] += 1; flagged.append((scene, 'over 40 words', who, text))
            for name, rx in FLAGS:
                if rx.search(t): d[name] += 1; flagged.append((scene, name, who, text))
        else:
            d['direction words'] += words(t)
            if re.fullmatch(r"\((a )?(long )?beat[.\s]*\)?", t, re.I) or re.match(r"\(beat\b", t, re.I): d['beats'] += 1
            if OUTWARD.search(t): d['played outward'] += 1; flagged.append((scene, 'played outward', 'DIR', text))
            if INNER.search(t): d['inner state in direction'] += 1; flagged.append((scene, 'inner state in direction', 'DIR', text))
    return per, flagged

ROUGH = re.compile(r"(—|–|-|…|\.\.\.)\s*$|[—–]\s|\b(uh|um|I mean|like, |you know|I don'?t know|hang on|sort of|kind of|or something)\b|\b(\w+), \1\b|\b(I'?m|I was|she'?s|he'?s|it'?s|that'?s not), (?!(okay|fine)\b)", re.I)
def speeches(items):
    """Whole turns: consecutive lines by one person in one scene, joined."""
    out = []
    for scene, kind, who, text in items:
        if kind != 'SAY': continue
        if out and out[-1][0] == scene and out[-1][1] == who: out[-1][2] += ' ' + norm(text)
        else: out.append([scene, who, norm(text)])
    return out

def rhythm(items):
    sp = speeches(items); n = [words(t) for _, _, t in sp]
    run = best = 0
    for k in n:
        run = run + 1 if k <= 8 else 0; best = max(best, run)
    rough = sum(1 for _, _, t in sp if ROUGH.search(t))
    parts = [words(x) for _, _, t in sp for x in re.split(r'(?<=[.!?…])\s+', t) if words(x)]
    sent = sum(parts) / max(1, len(parts))
    dirs = sum(words(t) for _, kind, _, t in items if kind != 'SAY')
    return (f'turns {len(sp)} | average {sum(n)/len(n):.1f} words | 8 words or fewer {100*sum(k <= 8 for k in n)//len(n)}% '
            f'| longest run of those {best} | turns that stumble, restart or trail off {rough} ({100*rough//len(sp)}%)\n  '
            f'turns of 20 words or more {100*sum(k >= 20 for k in n)//len(n)}% | average sentence {sent:.1f} words '
            f'| direction words per spoken word {dirs/max(1, sum(n)):.2f}')

def echoes(items):
    seen = collections.Counter(re.sub(r'[^\w ]', '', norm(t).lower()).strip()
                               for _, k, _, t in items if k == 'SAY')
    return [(s, n) for s, n in seen.most_common() if n >= 2 and len(s.split()) >= 3]

def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('play'); a.add_argument('--text', action='store_true'); a.add_argument('--json', action='store_true')
    o = a.parse_args()
    items, cues = parse(o.play)
    if not any(k == 'SAY' for _, k, _, _ in items): sys.exit('No dialogue found. Cues should be names in capitals on their own line.')
    if o.text:
        last = None
        for scene, kind, who, text in items:
            if scene != last: print(f'\n## {scene}'); last = scene
            print(text if kind == 'DIR' else f'{who}: {text}')
        return
    per, flagged = analyse(items)
    total = sum(per.values(), collections.Counter())
    if o.json:
        print(json.dumps({'total': total, 'scenes': per}, indent=1)); return
    print('Characters:', ', '.join(sorted(cues)))
    for scene, d in list(per.items()) + [('WHOLE PLAY', total)]:
        print(f'\n{scene}'); print('  ' + ' | '.join(f'{k} {v}' for k, v in d.items()))
    print('\nRHYTHM\n  ' + rhythm(items))
    print('\nLINES TO LOOK AT (candidates, not verdicts)')
    for scene, name, who, text in flagged:
        print(f'  [{name}] {scene.split(":")[0]} {who}: {text[:150]}')
    e = echoes(items)
    print(f'\nREPEATED LINES ({len(e)})')
    for s, n in e: print(f'  x{n}  {s}')

if __name__ == '__main__': main()
