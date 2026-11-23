#!/usr/bin/env python3
"""Closing report for every skill run, plus one metrics entry. Refuses to run without "not_done".

  run_report.py spec.json          (or:  ... | run_report.py -)

spec = {
  "app": "travel", "skill": "write-prd", "stage": "2 Define",
  "title": "PRD v1 drafted",
  "yours":     ["What the person at the gate must do next, in order"],
  "decisions": [{"q": "...", "rec": "...", "overturn": "how to reverse it"}],
  "produced":  [{"artifact": "docs/travel/01-prd.md", "state": "draft v1"}],
  "findings":  ["The two or three things that matter"],
  "not_done":  ["What this run did NOT do"],          # required, never empty
  "metrics":   {"minutes": 34, "fix_first": 9, "fix_final": 0, "human_edits": 6, "tokens": null}
}
Writes docs/<app>/run-reports/<YYYY-MM-DD>-<skill>.md (same day + skill = overwrite in place, never a _v2)
and appends {date, stage, skill, title, ...metrics} to metrics/run_metrics.json.
"""
import datetime as dt, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    spec = json.load(sys.stdin if sys.argv[1] == '-' else open(sys.argv[1], encoding='utf-8'))
    for k in ('app', 'skill', 'stage', 'title', 'yours'):
        if not spec.get(k):
            sys.exit(f'!! "{k}" is required')
    if not spec.get('not_done'):
        sys.exit('!! "not_done" is required and cannot be empty. Something was always left undone: name it.')
    today = dt.date.today().isoformat()
    d = os.path.join(ROOT, 'docs', spec['app'], 'run-reports')
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f'{today}-{spec["skill"]}.md')
    L = [f'# Run report · {spec["skill"]} · {spec["title"]}', '', f'Stage {spec["stage"]} · {today}', '', '## Yours to do', '']
    L += [f'- [ ] {x}' for x in spec['yours']] + ['']
    if spec.get('decisions'):
        L += ['## Decisions', '']
        L += [f'- **{x["q"]}** Recommendation: {x["rec"]}' + (f' (To reverse: {x["overturn"]})' if x.get('overturn') else '') for x in spec['decisions']] + ['']
    if spec.get('produced'):
        L += ['## Produced', '', '| Artifact | State |', '|---|---|']
        L += [f'| `{x["artifact"]}` | {x.get("state", "")} |' for x in spec['produced']] + ['']
    if spec.get('findings'):
        L += ['## Findings', ''] + [f'- {x}' for x in spec['findings']] + ['']
    L += ['## What I did NOT do', ''] + [f'- {x}' for x in spec['not_done']] + ['']
    open(path, 'w', encoding='utf-8').write('\n'.join(L))
    mp = os.path.join(ROOT, 'metrics', 'run_metrics.json')
    m = json.load(open(mp, encoding='utf-8')) if os.path.exists(mp) else []
    entry = {'date': today, 'stage': spec['stage'], 'skill': spec['skill'], 'title': spec['title'], **(spec.get('metrics') or {})}
    m.append(entry)
    tmp = mp + '.tmp'
    json.dump(m, open(tmp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    os.replace(tmp, mp)
    print(f'→ {os.path.relpath(path, ROOT)} · metrics entry {len(m)}')


if __name__ == '__main__':
    main()
