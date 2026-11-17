"""Read approved-source bytes only; writes card-local hashes, never changes art."""
import json, hashlib, subprocess
from pathlib import Path
base = Path(__file__).resolve().parent
source = Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-collection-review/manifest.json')
raw = source.read_bytes(); manifest = json.loads(raw)
e = next(e for e in manifest['entries'] if e['id'] == 'iceland')
def gitbytes(ref, path):
    return subprocess.check_output(['git','show',ref+':'+path])
paths = subprocess.check_output(['git','ls-tree','-r','--name-only', e['commit'], 'preview/iceland-backright-v10']).decode().splitlines()
glbs = [p for p in paths if p.endswith('.glb')]
assert len(glbs) == 1, glbs
master = subprocess.check_output(['git','rev-parse','origin/master']).decode().strip()
artpath = 'docs/assets/gallery/iceland.webp'
media = {}
for kind, ref, path in [('model', e['commit'], glbs[0]), ('art',master,artpath)]:
    data = gitbytes(ref,path)
    media[kind] = dict(commit=ref,path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
roster = {k:manifest[k] for k in ['roster_definition','expected_country_slugs','expected_ocean_slugs']}
roster['moon_slugs'] = [x['id'] for x in manifest['entries'] if x['category']=='Moon']
ids=roster['expected_country_slugs']+roster['expected_ocean_slugs']+roster['moon_slugs']
assert len(ids)==len(set(ids))==201 and len(roster['expected_country_slugs'])==195 and len(roster['expected_ocean_slugs'])==5 and len(roster['moon_slugs'])==1
assert 'iceland' in ids
roster.update(source=str(source),sourceSha256=hashlib.sha256(raw).hexdigest())
(base/'roster.json').write_text(json.dumps(roster,indent=2)+'\n')
(base/'media.json').write_text(json.dumps(media,indent=2)+'\n')
print(json.dumps(media,indent=2)); print('Explicit roster: 195 country + 5 ocean + 1 Moon; no assets issued')
