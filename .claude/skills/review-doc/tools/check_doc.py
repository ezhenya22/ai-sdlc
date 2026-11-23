#!/usr/bin/env python3
"""review-doc, layer 1 and the merge step. Deterministic: same document in, same findings out.

  check_doc.py <doc.md>                         rule checks → <app>/reviews/<doc>.review.json + .review.md
  check_doc.py <doc.md> --judgments <j.json>    + merge the model's judgments (schema- and quote-checked)
  check_doc.py <doc.md> --stub                  print the judgment criteria to fill (for the model)
  check_doc.py <doc.md> --today YYYY-MM-DD      pin the date (tests)

Grades: Fix = the gate sends it back · Check = worth a look · Note = for information.
Status: Ready (no Fix) · Needs work (any Fix). The script never edits the document.
Exit code: 0 Ready, 1 Needs work, 2 the document or the judgments could not be read.
"""
import argparse, datetime as dt, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'reference')

REQUIRED = {
    'brief': ['Problem', 'Who it affects', 'How it works today', 'Evidence', 'Success metric', 'Constraints',
              'Out of scope', 'Assumptions to confirm', 'Risks'],
    'prd': ['Summary', 'Users and jobs', 'Requirements', 'User stories', 'Non-functional requirements',
            'Non-goals', 'Open questions', 'Dependencies'],
}
HEADER_KEYS = ['doc_type', 'app', 'version', 'status', 'owner']
BLANK_RX = re.compile(r'\b(TBD|TODO|TBC|XXX)\b|\?\?\?|\[fill[^\]]*\]|lorem ipsum', re.I)
CONFIRM_RX = re.compile(r'confirm\s*[—–-]\s*(?P<who>[^,\n|]*?)\s*,\s*by\s+(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}|[^\s|,.;)]+)', re.I)
CONFIRM_LOOSE = re.compile(r'\bconfirm\s*[—–-]', re.I)


# ── reading ──────────────────────────────────────────────────────────────────
def parse(path):
    raw = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
    head, body = {}, raw
    if m:
        body = raw[m.end():]
        key = None
        for line in m.group(1).splitlines():
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            item = re.match(r'^\s+-\s+(.*)$', line)
            if item and key:
                head.setdefault(key, [])
                if isinstance(head[key], list):
                    head[key].append(item.group(1).split('  #')[0].strip())
                continue
            kv = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
            if kv:
                key, val = kv.group(1), kv.group(2).split('  #')[0].strip()
                head[key] = val if val else []
    sections, order, cur = {}, [], None
    for line in body.splitlines():
        h = re.match(r'^##\s+(.*?)\s*$', line)
        if h and not line.startswith('###'):
            cur = h.group(1)
            order.append(cur)
            sections[cur] = []
        elif cur is not None:
            sections[cur].append(line)
    sections = {k: '\n'.join(v).strip() for k, v in sections.items()}
    return raw, head, body, sections, order


def line_of(raw, needle):
    i = raw.find(needle)
    return raw.count('\n', 0, i) + 1 if i >= 0 else None


def table_rows(text):
    rows = []
    for line in text.splitlines():
        if line.strip().startswith('|') and not re.match(r'^\s*\|[\s:\-|]+\|\s*$', line):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            rows.append(cells)
    return rows[1:] if rows else []   # drop the header row


# ── findings ─────────────────────────────────────────────────────────────────
class Findings:
    def __init__(self):
        self.items = []

    def add(self, rule, grade, where, message, fix=None, quote=None):
        fid = hashlib.sha1(f'{rule}|{where}|{message}'.encode()).hexdigest()[:8]
        self.items.append({'id': fid, 'rule': rule, 'grade': grade, 'where': where, 'message': message,
                           'suggested': fix, 'quote': quote, 'source': 'rule'})


def check_common(raw, head, body, sections, order, kind, today, F, path):
    for k in HEADER_KEYS:
        if k not in head or head[k] in ('', []):
            F.add('C01', 'Fix', 'header', f'Header field `{k}` is missing.', f'Add `{k}:` to the header (see sdlc/ids.md).')
    for name in REQUIRED.get(kind, []):
        if name not in sections:
            F.add('C02', 'Fix', name, f'Section "## {name}" is missing.', f'Add a "## {name}" section.')
        elif not re.sub(r'<!--.*?-->', '', sections[name], flags=re.S).strip():
            F.add('C02', 'Fix', name, f'Section "## {name}" is empty.', 'Fill it, or write `None` and say why.')
    for i, line in enumerate(raw.splitlines(), 1):
        if line.startswith('#') or line.strip().startswith('<!--'):
            continue
        for m in BLANK_RX.finditer(line):
            F.add('C03', 'Fix', f'line {i}', f'"{m.group(0)}" counts as blank.',
                  'Answer it, or write `confirm — <who>, by <YYYY-MM-DD>`.', quote=line.strip()[:160])
    for i, line in enumerate(raw.splitlines(), 1):
        if not CONFIRM_LOOSE.search(line):
            continue
        ms = list(CONFIRM_RX.finditer(line))
        if not ms:
            F.add('C04', 'Fix', f'line {i}', 'A `confirm —` placeholder is missing its owner or date.',
                  'Write it as `confirm — <who>, by <YYYY-MM-DD>`.', quote=line.strip()[:160])
            continue
        for m in ms:
            who, date = m.group('who').strip(), m.group('date')
            if not who or who.lower() in ('who', '<who>', 'someone', 'tbd'):
                F.add('C04', 'Fix', f'line {i}', 'A `confirm —` placeholder has no named owner.',
                      'Name the person who will confirm it.', quote=line.strip()[:160])
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
                F.add('C04', 'Fix', f'line {i}', f'Confirm-by date "{date}" is not a date.',
                      'Use YYYY-MM-DD.', quote=line.strip()[:160])
            elif dt.date.fromisoformat(date) < today:
                F.add('C04', 'Check', f'line {i}', f'The confirm-by date {date} has passed.',
                      'Get the answer, or move the date and say why.', quote=line.strip()[:160])
    srcs = head.get('sources', [])
    if isinstance(srcs, str):
        srcs = [srcs] if srcs else []
    if not srcs:
        F.add('C05', 'Check', 'header', 'No sources listed.', 'List every source the content relies on under `sources:`.')
    root = repo_root(path)
    for s in srcs:
        if not re.match(r'^https?://', s) and not os.path.exists(os.path.join(root, s)):
            F.add('C05', 'Fix', 'header', f'Source `{s}` does not exist in the repo.', 'Fix the path or remove it.')
    return srcs


def repo_root(path):
    d = os.path.dirname(os.path.abspath(path))
    while d != '/' and not os.path.isdir(os.path.join(d, 'sdlc')):
        d = os.path.dirname(d)
    return d if d != '/' else os.path.dirname(os.path.abspath(path))


def check_brief(raw, sections, F):
    prob = sections.get('Problem', '') + '\n' + sections.get('Evidence', '')
    if prob.strip() and not re.search(r'\d', prob) and not CONFIRM_RX.search(prob):
        F.add('B01', 'Check', 'Evidence', 'The problem has no number behind it.',
              'Add one measured fact (how many, how long, how often), or a `confirm —` placeholder for it.')
    rows = [r for r in table_rows(sections.get('Success metric', '')) if r and re.match(r'M-\d{2}$', r[0])]
    if not rows:
        F.add('B02', 'Fix', 'Success metric', 'No metric row with an `M-nn` id.',
              'One row: | M-01 | metric | baseline | target | by date |')
    for r in rows:
        if len(r) < 5 or any(not c for c in r[:5]):
            F.add('B02', 'Fix', r[0], f'{r[0]} needs a metric, a baseline, a target and a by-date.',
                  'Fill all five columns; an unknown baseline is a `confirm —` placeholder.')
        elif not re.search(r'\d{4}-\d{2}-\d{2}', r[4]) and not CONFIRM_RX.search(r[4]):
            F.add('B02', 'Fix', r[0], f'{r[0]} "by" is not a date.', 'Use YYYY-MM-DD.')
    if len(rows) > 3:
        F.add('B02', 'Check', 'Success metric', f'{len(rows)} metrics. A brief leads with one.', 'Keep one primary metric; move the rest to the PRD.')
    arows = [r for r in table_rows(sections.get('Assumptions to confirm', '')) if r and r[0]]
    for r in arows:
        if not re.match(r'A-\d{2}$', r[0]):
            F.add('B03', 'Fix', 'Assumptions to confirm', f'Assumption id "{r[0]}" is not `A-nn`.', 'Number assumptions A-01, A-02…')
        if len(r) < 4 or not r[2] or not re.search(r'\d{4}-\d{2}-\d{2}', r[3]):
            F.add('B03', 'Fix', r[0], f'{r[0]} needs an owner and a confirm-by date.', 'Fill Owner and Confirm by (YYYY-MM-DD).')
    who = sections.get('Who it affects', '')
    if who and not re.search(r'^\s*[-*|]', who, re.M):
        F.add('B04', 'Check', 'Who it affects', 'Users are not listed one per line.', 'List each role on its own line or row.')


def check_prd(raw, head, sections, F, path):
    reqs = {}
    for r in table_rows(sections.get('Requirements', '')):
        if not r or not r[0]:
            continue
        rid = r[0]
        if not re.match(r'REQ-\d{2}$', rid):
            F.add('P01', 'Fix', 'Requirements', f'Requirement id "{rid}" is not `REQ-nn`.', 'Use REQ-01, REQ-02…')
            continue
        if rid in reqs:
            F.add('P01', 'Fix', rid, f'{rid} is used twice.', 'Give each requirement its own id; never reuse one.')
        reqs[rid] = r
        prio = r[2] if len(r) > 2 else ''
        if prio not in ('Must', 'Should', 'Could'):
            F.add('P05', 'Fix', rid, f'{rid} priority "{prio}" is not Must, Should or Could.', 'Set the priority.')
        if len(r) < 4 or not r[3]:
            F.add('P05', 'Check', rid, f'{rid} does not trace to the brief.', 'Name the brief item it serves (M-01, a pain point, a constraint).')
    stories_txt = sections.get('User stories', '')
    blocks = re.split(r'(?m)^###\s+', stories_txt)[1:]
    sids, covered = set(), {}
    for b in blocks:
        head_line = b.splitlines()[0]
        sm = re.match(r'(ST-\d{2})\b', head_line)
        if not sm:
            F.add('P01', 'Fix', head_line[:40], f'Story heading "{head_line[:40]}" has no `ST-nn` id.', 'Start the heading with ST-nn.')
            continue
        sid = sm.group(1)
        if sid in sids:
            F.add('P01', 'Fix', sid, f'{sid} is used twice.', 'Give each story its own id.')
        sids.add(sid)
        rm = re.findall(r'Requirement[s]?:\s*([^\n]+)', b)
        cited = re.findall(r'REQ-\d{2}', ' '.join(rm))
        if not cited:
            F.add('P02', 'Fix', sid, f'{sid} names no requirement.', 'Add a line `Requirement: REQ-nn`.')
        for c in cited:
            if c not in reqs:
                F.add('P02', 'Fix', sid, f'{sid} cites {c}, which does not exist.', 'Cite an existing requirement or add it.')
            covered.setdefault(c, []).append(sid)
        acs = re.findall(r'(AC-(\d{2})\.(\d+))\**\s*(.*)', b)
        if not acs:
            F.add('P04', 'Fix', sid, f'{sid} has no acceptance criteria.', 'Add at least one `AC-nn.m` written as Given … When … Then ….')
        seen_ac = set()
        for full, snum, _, text in acs:
            if f'ST-{snum}' != sid:
                F.add('P01', 'Fix', full, f'{full} sits under {sid}; its number must match the story.', f'Renumber it AC-{sid[3:]}.x.')
            if full in seen_ac:
                F.add('P01', 'Fix', full, f'{full} is used twice.', 'Number criteria .1, .2, .3…')
            seen_ac.add(full)
            if not (re.search(r'\bGiven\b', text) and re.search(r'\bWhen\b', text) and re.search(r'\bThen\b', text)):
                F.add('P04', 'Fix', full, f'{full} is not written as Given … When … Then ….',
                      'Rewrite: Given <state>, When <action>, Then <observable result>.', quote=text.strip()[:160])
    uncovered = sorted(r for r in reqs if r not in covered)
    for r in uncovered:
        F.add('P03', 'Fix', r, f'{r} has no story.', 'Write a story for it, or move it to Non-goals.')
    ng = sections.get('Non-goals', '')
    if ng and len(re.findall(r'^\s*[-*]', ng, re.M)) < 2:
        F.add('P06', 'Check', 'Non-goals', 'Fewer than two non-goals.', 'Say what this release deliberately will not do.')
    nfr = sections.get('Non-functional requirements', '').lower()
    for word, rule in (('accessib', 'accessibility'), ('privacy', 'privacy'), ('security', 'security')):
        if nfr and word not in nfr:
            F.add('P07', 'Check', 'Non-functional requirements', f'No {rule} requirement.', f'State the {rule} requirement, even if it is short.')
    brief = head.get('brief')
    if not brief:
        F.add('P08', 'Fix', 'header', 'The header does not name the brief this PRD builds on.', 'Add `brief: docs/<app>/00-brief.md`.')
    else:
        bp = os.path.join(repo_root(path), brief)
        if not os.path.exists(bp):
            F.add('P08', 'Fix', 'header', f'Brief `{brief}` not found.', 'Fix the path.')
        else:
            _, bh, *_ = parse(bp)
            if bh.get('status') != 'approved':
                F.add('P08', 'Fix', 'header', 'The brief is not approved (gate G1 not passed).', 'Pass G1 before the PRD goes to G2.')
    return {'requirements': len(reqs), 'stories': len(sids), 'covered': len(reqs) - len(uncovered)}


# ── judgments (the model's layer) ───────────────────────────────────────────
def criteria(kind):
    p = os.path.join(REF, f'rubric_{kind}.md')
    if not os.path.exists(p):
        return []
    return re.findall(r'^###\s+(J\d+)\s+[·—-]\s+(.+)$', open(p, encoding='utf-8').read(), re.M)


def norm(s):
    return re.sub(r'\s+', ' ', s.replace('’', "'").replace('“', '"').replace('”', '"')).strip().lower()


def merge_judgments(jpath, kind, raw, F):
    try:
        js = json.load(open(jpath, encoding='utf-8'))
    except Exception as e:
        print(f'!! judgments file unreadable: {e}', file=sys.stderr)
        sys.exit(2)
    ids = {c[0]: c[1] for c in criteria(kind)}
    seen, rejected = set(), []
    for j in js if isinstance(js, list) else []:
        jid, verdict = j.get('id'), j.get('verdict')
        if jid not in ids:
            rejected.append(f'{jid}: not a {kind} criterion'); continue
        if verdict not in ('pass', 'check', 'fix'):
            rejected.append(f'{jid}: verdict must be pass, check or fix'); continue
        if verdict == 'pass':
            seen.add(jid)
            continue
        quote = (j.get('quote') or '').strip()
        if not quote:
            rejected.append(f'{jid}: a {verdict} finding must quote the document'); continue
        if norm(quote) not in norm(raw):
            rejected.append(f'{jid}: quote not found in the document (a finding must quote it word for word)'); continue
        seen.add(jid)   # only a valid answer counts; a rejected one leaves the criterion unanswered
        F.items.append({'id': hashlib.sha1(f'{jid}|{quote}'.encode()).hexdigest()[:8], 'rule': jid,
                        'grade': 'Fix' if verdict == 'fix' else 'Check', 'where': ids[jid],
                        'message': j.get('finding', '').strip(), 'suggested': j.get('suggested'),
                        'quote': quote, 'source': 'judgment'})
    missing = [k for k in ids if k not in seen]
    return {'criteria': len(ids), 'answered': len(seen), 'missing': missing, 'rejected': rejected}


# ── output ───────────────────────────────────────────────────────────────────
def write_outputs(path, kind, head, F, stats, jstats, today):
    base = os.path.splitext(os.path.basename(path))[0]
    outdir = os.path.join(os.path.dirname(os.path.abspath(path)), 'reviews')
    os.makedirs(outdir, exist_ok=True)
    # A rule-only run writes <doc>.rules.*; only a judged run writes <doc>.review.*. So a maker's self-check can never
    # overwrite a judged review, and "since last run" always compares judged review to judged review.
    # (corrections.jsonl, 2026-11-23: a rule-only run wiped the v1 travel-brief review.)
    kind_out = 'review' if jstats else 'rules'
    jp, mp = os.path.join(outdir, f'{base}.{kind_out}.json'), os.path.join(outdir, f'{base}.{kind_out}.md')
    prev_p = os.path.join(outdir, base + '.review.json')
    prev, had_prev = {}, bool(jstats) and os.path.exists(prev_p)
    if had_prev:
        try:
            prev = {f['id']: f for f in json.load(open(prev_p, encoding='utf-8'))['findings']}
        except Exception:
            prev = {}
    cur = {f['id'] for f in F.items}
    counts = {g: sum(1 for f in F.items if f['grade'] == g) for g in ('Fix', 'Check', 'Note')}
    # Ready needs every judgment criterion answered, so a rule-only run can at best say "Rules pass".
    if counts['Fix']:
        status = 'Needs work'
    elif not jstats:
        status = 'Rules pass'
    else:
        status = 'Needs work' if jstats['missing'] else 'Ready'
    out = {'schema': 'review-doc/1', 'document': os.path.relpath(path, repo_root(path)), 'doc_type': kind,
           'version': head.get('version'), 'reviewed_on': today.isoformat(), 'status': status, 'counts': counts,
           'coverage': stats, 'judgments': jstats,
           'since_last_run': {'new': len(cur - set(prev)), 'resolved': len(set(prev) - cur)} if had_prev else None,
           'findings': F.items}
    tmp = jp + '.tmp'
    json.dump(out, open(tmp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    os.replace(tmp, jp)
    L = [f'# {"Review" if jstats else "Rule checks"}: {out["document"]} (v{head.get("version")})', '',
         f'**Status: {status}** · Fix {counts["Fix"]} · Check {counts["Check"]} · Note {counts["Note"]} · reviewed {today}', '']
    if stats:
        L.append(f'Coverage: {stats.get("covered")} of {stats.get("requirements")} requirements have a story · {stats.get("stories")} stories.')
    if jstats:
        L.append(f'Judgment criteria answered: {jstats["answered"]} of {jstats["criteria"]}.'
                 + (f' Missing: {", ".join(jstats["missing"])}.' if jstats['missing'] else '')
                 + (f' Rejected: {len(jstats["rejected"])}.' if jstats['rejected'] else ''))
        for r in jstats['rejected']:
            L.append(f'- ⛔ rejected judgment — {r}')
    else:
        L.append('Judgment criteria: not run (rule checks only). This file never says Ready; the judged review is <doc>.review.md.')
    if out['since_last_run']:
        L.append(f'Since last run: {out["since_last_run"]["new"]} new, {out["since_last_run"]["resolved"]} resolved.')
    L.append('')
    for g in ('Fix', 'Check', 'Note'):
        items = [f for f in F.items if f['grade'] == g]
        if not items:
            continue
        L += [f'## {g} ({len(items)})', '']
        for f in items:
            L.append(f'- **{f["rule"]} · {f["where"]}** — {f["message"]}')
            if f.get('quote'):
                L.append(f'  > {f["quote"]}')
            if f.get('suggested'):
                L.append(f'  Suggested: {f["suggested"]}')
        L.append('')
    open(mp, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return out, jp, mp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('doc')
    ap.add_argument('--judgments')
    ap.add_argument('--stub', action='store_true')
    ap.add_argument('--today')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    if not os.path.exists(a.doc):
        print(f'!! {a.doc} not found', file=sys.stderr); sys.exit(2)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    raw, head, body, sections, order = parse(a.doc)
    kind = head.get('doc_type')
    if kind not in REQUIRED:
        print(f'!! unknown or missing doc_type "{kind}" (expected one of {", ".join(REQUIRED)})', file=sys.stderr); sys.exit(2)
    if a.stub:
        print(json.dumps([{'id': c[0], 'criterion': c[1], 'verdict': 'pass|check|fix', 'quote': '', 'finding': '', 'suggested': ''}
                          for c in criteria(kind)], indent=1, ensure_ascii=False))
        return
    F = Findings()
    check_common(raw, head, body, sections, order, kind, today, F, a.doc)
    stats = None
    if kind == 'brief':
        check_brief(raw, sections, F)
    elif kind == 'prd':
        stats = check_prd(raw, head, sections, F, a.doc)
    jstats = merge_judgments(a.judgments, kind, raw, F) if a.judgments else None
    out, jp, mp = write_outputs(a.doc, kind, head, F, stats, jstats, today)
    if not a.quiet:
        c = out['counts']
        print(f'{out["status"]}: Fix {c["Fix"]} · Check {c["Check"]} · Note {c["Note"]}'
              + (f' · coverage {stats["covered"]} of {stats["requirements"]}' if stats else '')
              + (f' · judgments {jstats["answered"]}/{jstats["criteria"]}, rejected {len(jstats["rejected"])}' if jstats else ' · judgments not run'))
        print(f'→ {os.path.relpath(mp)}')
    sys.exit(0 if out['status'] in ('Ready', 'Rules pass') else 1)


if __name__ == '__main__':
    main()
