#!/usr/bin/env python3
"""Runs check_doc.py on the perfect and broken fixtures and fails if the results drift from examples/expected.json.
Also proves the judgment merge: a finding with a real quote is kept, a made-up quote is rejected, an unknown criterion
is rejected. Usage: python3 test_check_doc.py   (exit 0 = all pass)"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.join(HERE, '..', 'examples')
CHECK = os.path.join(HERE, 'check_doc.py')
TODAY = '2026-11-23'


def run(doc, *extra):
    p = subprocess.run([sys.executable, CHECK, doc, '--today', TODAY, '--quiet', *extra], capture_output=True, text=True)
    out = os.path.join(os.path.dirname(doc), 'reviews', os.path.splitext(os.path.basename(doc))[0] + '.review.json')
    return p.returncode, json.load(open(out)), p.stderr


def main():
    expected = json.load(open(os.path.join(EX, 'expected.json')))
    tmp = tempfile.mkdtemp()
    for d in ('perfect', 'broken'):
        shutil.copytree(os.path.join(EX, d), os.path.join(tmp, d))
    os.makedirs(os.path.join(tmp, 'sdlc'))          # marks the temp folder as the repo root
    failures, lines = [], []
    for rel, exp in expected.items():
        if rel.startswith('_'):
            continue
        code, rep, err = run(os.path.join(tmp, rel))
        fixes = {f['rule'] for f in rep['findings'] if f['grade'] == 'Fix'}
        checks = {f['rule'] for f in rep['findings'] if f['grade'] == 'Check'}
        ok = rep['status'] == exp['status']
        if exp.get('fix') == []:
            ok &= not fixes
        else:
            missing = set(exp['fix']) - fixes
            ok &= not missing
            if missing:
                failures.append(f'{rel}: expected Fix rules not reported: {sorted(missing)}')
        miss_c = set(exp.get('check', [])) - checks
        ok &= not miss_c
        if miss_c:
            failures.append(f'{rel}: expected Check rules not reported: {sorted(miss_c)}')
        if 'coverage' in exp:
            cov = f'{rep["coverage"]["covered"]} of {rep["coverage"]["requirements"]}'
            ok &= cov == exp['coverage']
            if cov != exp['coverage']:
                failures.append(f'{rel}: coverage {cov}, expected {exp["coverage"]}')
        if exp.get('fix') == [] and fixes:
            failures.append(f'{rel}: perfect fixture got Fix findings: {sorted(fixes)}')
        if rep['status'] != exp['status']:
            failures.append(f'{rel}: status {rep["status"]}, expected {exp["status"]}')
        lines.append(f'{"PASS" if ok else "FAIL"}  {rel:22} {rep["status"]:10} Fix {rep["counts"]["Fix"]:>2} · Check {rep["counts"]["Check"]:>2}'
                     + (f' · coverage {rep["coverage"]["covered"]} of {rep["coverage"]["requirements"]}' if rep.get('coverage') else ''))
    # judgment merge: real quote kept, invented quote rejected, unknown criterion rejected
    jf = os.path.join(tmp, 'j.json')
    json.dump([
        {'id': 'J4', 'verdict': 'fix', 'quote': 'Number of bookings made in the app', 'finding': 'Counts activity, not the problem.',
         'suggested': 'Room collisions per month'},
        {'id': 'J1', 'verdict': 'fix', 'quote': 'There is no app for booking rooms, so people book rooms in a spreadsheet.',
         'finding': 'Problem phrased as a missing feature.', 'suggested': 'Name who collides and what it costs.'},
        {'id': 'J2', 'verdict': 'check', 'quote': 'Collisions cost the company $2 million a year.', 'finding': 'Invented quote.', 'suggested': 'x'},
        {'id': 'J9', 'verdict': 'fix', 'quote': 'Time travel.', 'finding': 'Not a criterion.', 'suggested': 'x'},
        {'id': 'J3', 'verdict': 'pass'}, {'id': 'J5', 'verdict': 'pass'}, {'id': 'J6', 'verdict': 'pass'},
    ], open(jf, 'w'))
    code, rep, err = run(os.path.join(tmp, 'broken/00-brief.md'), '--judgments', jf)
    js = rep['judgments']
    kept = {f['rule'] for f in rep['findings'] if f['source'] == 'judgment'}
    jok = kept == {'J1', 'J4'} and len(js['rejected']) == 2 and js['missing'] == ['J2']
    lines.append(f'{"PASS" if jok else "FAIL"}  judgment merge        kept {sorted(kept)} · rejected {len(js["rejected"])} (made-up quote, unknown id) · unanswered {js["missing"]}')
    if not jok:
        failures.append(f'judgment merge: kept {kept}, rejected {js["rejected"]}, missing {js["missing"]}')
    print('\n'.join(lines))
    shutil.rmtree(tmp)
    if failures:
        print('\n'.join('  ✗ ' + f for f in failures))
        sys.exit(1)
    print('all checks pass')


if __name__ == '__main__':
    main()
