"""Preserve every review record and produce explicit bounded repair queues."""
from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parent
raw=(R/'baseline-ledger.json').read_bytes();d=json.loads(raw)
mechanical='afghanistan algeria chile croatia ghana guyana iceland lithuania malta mozambique panama saint-kitts-and-nevis tonga venezuela'.split()
finish='argentina bangladesh cambodia comoros djibouti eritrea gambia guinea-bissau lebanon malawi mexico myanmar nigeria palestine qatar samoa southern-ocean tajikistan tunisia zambia'.split()
changed=['united-states','cabo-verde','saint-vincent-and-the-grenadines'];packaged=['iceland','morocco','rwanda','namibia','new-zealand','paraguay']
rows=[]
for e in d['entries']:
 ident=e['id'];actions=[]
 if ident in changed:actions.append('new-review-candidate; USA seam repaired; crater camera trials remain partial')
 if ident in packaged:actions.append('canonical-source-package repaired; history and visual approvals unchanged')
 if ident in mechanical:actions.append('remaining targeted attachment/rim/landmark investigation and repair when reproduced; not proven breakage')
 if ident in finish:actions.append('remaining ordinary finish inspection; do not edit promotional-only differences or infer broken model')
 if not actions:actions.append('owner art/finish acceptance; no proven runtime defect recorded; no autonomous redesign')
 rows.append({'id':ident,'baseline_verdict':e['verdict'],'actions':actions,'approval':False,'original_review':e['independent_review'],'package_history':e['package_history']})
assert len(rows)==201 and len({r['id'] for r in rows})==201
counts=collections.Counter(r['baseline_verdict'] for r in rows);assert counts['needs-user-review']==73
out={'baseline_ledger_sha256':hashlib.sha256(raw).hexdigest(),'counts':dict(counts),'approved':0,'changed_candidates':changed,'repaired_packages':packaged,'remaining_mechanical_queue':mechanical,'remaining_finish_queue':finish,'records':rows}
(R/'dispositions.json').write_text(json.dumps(out,indent=2))
def texts(v):
 if isinstance(v,dict):
  for k,a in v.items():
   if k in ('visual_review','independent_visual','reason','parent_reason','package_holds','remaining_gates','missing_gates','caveats','concrete_defects','uncertainties'):yield k+': '+json.dumps(a,ensure_ascii=False)
   elif isinstance(a,(dict,list)):yield from texts(a)
 elif isinstance(v,list):
  for a in v:yield from texts(a)
lines=['# Consolidated owner packet — no approvals inferred','', 'All 201 records remain preserved in dispositions.json. This packet is not another no-change audit: three actual viewer candidates and six canonical source packages accompany it. It does not call all 201 finished.','', '## Completed engineering versus decisions', 'USA: seam stencil now spans moving lid and fixed body rim; top-to-side-to-main-wall continuation is NOT claimed. Accept/reject this specific interpretation. Cabo Verde and Saint Vincent: camera trials still have weak small crater readability; deeper/wider/contrasting crater requires an explicit art choice. Package identity defects repaired without changing artwork.','', '## Remaining targeted engineering queue', ', '.join(mechanical), '', '## Remaining ordinary finish inspection queue', ', '.join(finish), '', 'These are actionable investigation targets from concrete observations, not proof of broken geometry. Reproduce, fix ordinary faults, then preserve substantive taste decisions. Promotional-only differences must not silently become model redesign.','', '## All 73 inherited holds (unchanged; source package repairs are separately recorded)']
for r in rows:
 if r['baseline_verdict']!='needs-user-review':continue
 lines += ['', '### '+r['id'],*list(dict.fromkeys(texts(r['original_review'])))]
lines += ['','## 128 limited candidates (also not approved)',', '.join(r['id'] for r in rows if r['baseline_verdict']!='needs-user-review'),'','## Production boundaries','201 one-of-ones (195 countries, five oceans, Moon); one independent inner collectible plus detached signed record. No accessory or certificate NFT, no reuse covenant claim. All final art approval, rights, preservation/storage, authentic keys/issuer/origins, real-wallet signing/payment/chain finality, external security review, economics/legal, mint/sale and exact production release remain blocked. The separate continuous local fixture d02b279d8ea41871c4f4af6760576a3926617fb6 is neither integrated nor deployed by this art repair branch.']
(R/'OWNER-DECISIONS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
