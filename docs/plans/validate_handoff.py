"""Validate engineering-brief coverage, retained clauses and local navigation."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
import json
import re

ROOT = Path(__file__).resolve().parents[2]
PLANS = ROOT / 'docs/plans'
errors = []
coverage = json.loads((PLANS / 'coverage.json').read_text())
register = (ROOT / 'docs/requirements.md').read_text()
requirements = {}
for line in register.splitlines():
    match = re.match(r'\| <a id="req-([^"]+)"></a>([^<|]+)', line)
    if match:
        cells = line.strip('|').split('|')
        requirements[match[2].strip()] = cells[1].strip()
assert len(requirements) == coverage['requirements'] == 302
assert len(coverage['tasks']) == 62
primary = Counter()
issues = {t['issue']: t for t in coverage['tasks']}
for task in coverage['tasks']:
    body = (PLANS / task['file']).read_text()
    for heading in ['Start here', 'Inputs and outputs', 'Product rules for this task',
                    'Exact PRD sections', 'Behaviour to demonstrate',
                    'Dependencies and decisions', 'Engineering choices and review']:
        if f'## {heading}' not in body:
            errors.append(f"#{task['issue']}: missing {heading}")
    for rid in task['requirements']:
        if rid not in requirements:
            errors.append(f"#{task['issue']}: unknown requirement {rid}")
        elif requirements[rid] not in body:
            # UI-02/UI-03 retain two source variants in the register, separated by a break.
            variants = [re.sub(r'^§[0-9.]+: ', '', v) for v in re.split(r'; (?=§[0-9.]+: )', requirements[rid])]
            if not any(v and v in body for v in variants):
                errors.append(f"#{task['issue']}: altered or missing clause {rid}")
    primary.update(task['primary_requirements'])
    for n in task['dependencies']:
        if n not in issues:
            errors.append(f"#{task['issue']}: missing dependency #{n}")
if set(primary) != set(requirements) or any(n != 1 for n in primary.values()):
    errors.append('Every requirement must have exactly one primary task')
seen, active = set(), set()
def visit(n):
    if n in active:
        errors.append(f'Dependency cycle at #{n}')
        return
    if n in seen:
        return
    active.add(n)
    for d in issues[n]['dependencies']:
        if d in issues:
            visit(d)
    active.remove(n)
    seen.add(n)
for n in issues:
    visit(n)

def prose(text):
    return re.sub(r'```.*?```', '', text, flags=re.S)
def anchors(path):
    text = prose(path.read_text())
    result = set(re.findall(r'<a id="([^"]+)"', text))
    counts = Counter()
    for heading in re.findall(r'^#+ (.+)$', text, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        count = counts[slug]
        counts[slug] += 1
        result.add(slug + (f'-{count}' if count else ''))
    return result
links = 0
for path in list(PLANS.rglob('*.md')) + list((ROOT / 'docs/prd').glob('*.md')):
    for raw in re.findall(r'\]\(([^)]+)\)', prose(path.read_text())):
        if re.match(r'^[a-z][a-z0-9+.-]*:', raw):
            continue
        file, _, anchor = unquote(raw).partition('#')
        dest = (path.parent / file).resolve() if file else path
        links += 1
        if not dest.exists():
            errors.append(f'{path.relative_to(ROOT)}: missing {raw}')
        elif anchor and dest.suffix == '.md' and anchor not in anchors(dest):
            errors.append(f'{path.relative_to(ROOT)}: missing anchor {raw}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'PASS: {len(issues)} briefs, 302 singly owned requirements, source clauses retained, no dependency cycles, {links} local links/anchors.')
