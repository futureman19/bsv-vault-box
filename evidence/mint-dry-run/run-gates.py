"""Fresh local-only CLI and VM evidence. Refuses to overwrite operator DB."""
from pathlib import Path
import json
import subprocess
import sys
root = Path(__file__).resolve().parents[2]
out = root / 'evidence/mint-dry-run'
commands = []
def run(name, args, cwd=root):
    p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
    (out / (name + '.txt')).write_bytes(p.stdout)
    commands.append({'name': name, 'command': args, 'cwd': str(cwd), 'exitCode': p.returncode})
    (out / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    print(name, p.returncode, p.stdout.decode(errors='replace')[-180:], flush=True)
    assert p.returncode == 0
run('final-tests', [sys.executable, 'launch/mint/test_dry_run.py'])
base = [sys.executable, 'launch/mint/dry_run.py']
db = ['--db', 'evidence/mint-dry-run/operator.sqlite']
run('cli-init', base + ['init', *db, '--config', 'launch/mint/fixture-proposal.json', '--manifest', 'launch/assets/candidate-manifest.json'])
for request in sorted((root/'launch/mint/fixtures').glob('*.json')):
    run('cli-'+request.stem, base + ['apply', *db, '--request', str(request)])
run('cli-inspect', base + ['inspect', *db])
run('cli-audit', base + ['audit', *db])
run('vm', ['node', 'node_modules/mocha/bin/mocha.js', '--no-config', 'tests/ordinal-pair.test.js', 'tests/ordinal-sponsored.test.js', 'tests/native-custody.test.js', 'tests/launch-record.test.js'], root/'vault')
run('security-challenges', ['node', '--test', 'evidence/security/challenges.test.js'])
run('typecheck', ['node', 'node_modules/typescript/bin/tsc', '--noEmit'], root/'vault')
