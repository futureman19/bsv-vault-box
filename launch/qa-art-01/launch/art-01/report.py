import pathlib,json,base64,html,hashlib,io
from PIL import Image
R=pathlib.Path(__file__).resolve().parent
d=json.loads((R/'review-results.json').read_text()); parts=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ART-01 review</title><style>body{background:#17191d;color:#eee;font:16px system-ui;margin:auto;padding:20px;max-width:1200px}img{width:100%;height:auto}article{margin:35px 0}p{line-height:1.5}</style><h1>26 BoxSV candidate reviews</h1><p>Poster-only comparison report — no interactive models. 9 bounded-review passes; 17 need an artistic decision. None is final user-approved. Marketing illustrations differ from actual model captures. All 52 offline desktop/mobile interaction cases passed; this is not source/collision certification.</p>']
for e in d['entries']:
 im=Image.open(R/e['comparison']); im.thumbnail((1400,900)); buf=io.BytesIO(); im.save(buf,format='JPEG',quality=80)
 parts.append('<article><h2>'+html.escape(e['id']+' — '+e['status'])+'</h2><p>'+html.escape(e['visual_findings'])+'</p><p>Viewer: '+str(e['viewer']['bytes'])+' bytes. Candidate '+e['selection']['commit']+'</p><img alt="'+e['id']+' marketing and actual desktop/mobile closed/open comparison" src="data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()+'"></article>')
(R/'review.html').write_text('\n'.join(parts),encoding='utf-8')
inv=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and p.name!='evidence-inventory.json' and '__pycache__' not in p.parts:
  b=p.read_bytes();inv.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(R/'evidence-inventory.json').write_text(json.dumps({'files':inv},indent=2)+'\n');print('files',len(inv),'report bytes',(R/'review.html').stat().st_size)
