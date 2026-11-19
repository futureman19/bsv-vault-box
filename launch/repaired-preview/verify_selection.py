"""Independent selection checks and explicit regression negatives."""
import base64,copy,hashlib,io,json,re,unittest
from collections import Counter
from pathlib import Path
from PIL import Image
from build import ROOT,OUT,MASTER,sha,blob,dump,PINS
EXPECTED={'united-states':'preview/united-states-flag-v10/united-states-flag-v10.html','cabo-verde':'preview/cabo-verde-view-v2/cabo-verde-view-v2.html','saint-vincent-and-the-grenadines':'preview/saint-vincent-and-the-grenadines-view-v2/saint-vincent-and-the-grenadines-view-v2.html','bangladesh':'preview/bangladesh-finish-v2/bangladesh-finish-v2.html'}
STRUCTURAL=['afghanistan','algeria','chile','croatia','ghana','guyana','lithuania','malta','mozambique','panama','saint-kitts-and-nevis','tonga','venezuela']
EXPECTED.update({id:f'preview/{id}-repair-v2/{id}-repair-v2.html' for id in STRUCTURAL})
MANIFEST=json.loads((OUT/'manifest.json').read_bytes());BASE=json.loads((ROOT/'inputs/baseline.json').read_bytes());ROSTER=json.loads(blob(PINS['baseline'][0],'launch/collection/upstream/roster.json'))
def validate_manifest(m):
 es=m['entries'];assert len(es)==len({e['id'] for e in es})==201
 assert {e['id']:e['category'] for e in es}==ROSTER
 assert Counter(e['category'] for e in es)=={'Country':195,'Ocean':5,'Moon':1}
 assert m['production_base']==MASTER and m['minted'] is False and m['sale_active'] is False
 base={e['id']:e for e in BASE['entries']}
 for e in es:
  id=e['id'];assert e['launch_ready'] is False and e['final_user_approved'] is False
  if id in EXPECTED:
   assert e['viewer']['path']==EXPECTED[id],id
   key='structural' if id in STRUCTURAL else 'ordinary' if id=='bangladesh' else 'repairs'
   assert e['viewer']['commit']==PINS[key][0]
   assert e['viewer']['sha256']!=base[id]['viewer']['sha256']
  else:assert e['viewer']['sha256']==base[id]['viewer']['sha256'],id
  if id in ['united-states','cabo-verde','saint-vincent-and-the-grenadines']:assert e['disposition']=='substantive-feature-hold'
  if id=='united-states':assert 'main wall' in e['issue']
 return True
class Regressions(unittest.TestCase):
 def test_real_manifest(self):self.assertTrue(validate_manifest(MANIFEST))
 def test_duplicate_id_rejected(self):
  m=copy.deepcopy(MANIFEST);m['entries'][-1]=m['entries'][0]
  with self.assertRaises(AssertionError):validate_manifest(m)
 def test_stale_usa_rejected(self):
  m=copy.deepcopy(MANIFEST);e=next(e for e in m['entries'] if e['id']=='united-states');e['viewer']=next(e for e in BASE['entries'] if e['id']=='united-states')['viewer']
  with self.assertRaises(AssertionError):validate_manifest(m)
 def test_waived_requested_feature_rejected(self):
  m=copy.deepcopy(MANIFEST);next(e for e in m['entries'] if e['id']=='united-states')['disposition']='preview-accepted-with-limitations'
  with self.assertRaises(AssertionError):validate_manifest(m)
 def test_accidental_approval_rejected(self):
  m=copy.deepcopy(MANIFEST);m['entries'][0]['final_user_approved']=True
  with self.assertRaises(AssertionError):validate_manifest(m)
def full():
 validate_manifest(MANIFEST);checked=[]
 for e in MANIFEST['entries']:
  html=(OUT/e['viewer']['url']).read_bytes();assert sha(html)==e['viewer']['sha256'];assert len(html)==e['viewer']['bytes']<5000000
  assert html==blob(e['viewer']['commit'],e['viewer']['path'])
  for kind in ['poster','marketing']:
   data=(OUT/e[kind]['url']).read_bytes();assert sha(data)==e[kind]['sha256'];assert len(data)==e[kind]['bytes'];Image.open(io.BytesIO(data)).verify()
  assert (OUT/e['marketing']['url']).read_bytes()==blob(MASTER,e['marketing']['path'])
  matches=re.findall(rb'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)',html);poster=base64.b64decode(matches[0][1]);assert sha(poster)==e['poster']['embedded_poster_sha256']
  im=Image.open(io.BytesIO(poster)).convert('RGB');im.thumbnail((440,350));buf=io.BytesIO();im.save(buf,format='WEBP',quality=77);assert sha(buf.getvalue())==e['poster']['sha256']
  hist=json.loads((ROOT/'history'/f"{e['id']}.json").read_bytes());assert hist['baseline_record']==next(x for x in BASE['entries'] if x['id']==e['id'])
  checked.append({'id':e['id'],'viewer':e['viewer']['sha256'],'current_package':e['current_source_package']['sha256'] if e['current_source_package'] else None})
 report={'pass':True,'coverage':201,'viewer_git_byte_matches':201,'image_hashes_dimensions_decoded':402,'poster_derivatives_reproduced':201,'baseline_records_preserved':201,'new_archive_selected_payloads_reconciled':sum(x['current_package'] is not None for x in checked),'changed_viewers':len(EXPECTED),'records':checked,'scope':'No fresh Blender/whole-collection collision sampling. Immutable prior evidence retained.'}
 dump(ROOT/'selection-check.json',report);print(json.dumps({k:v for k,v in report.items() if k!='records'}))
if __name__=='__main__':
 result=unittest.main(exit=False);assert result.result.wasSuccessful();full()
