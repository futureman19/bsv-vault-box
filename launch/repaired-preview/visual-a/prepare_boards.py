import json,pathlib,subprocess,hashlib
from PIL import Image,ImageDraw
out=pathlib.Path(__file__).parent
p=out.parent/'inputs'
b=json.loads((p/'baseline.json').read_text())
ex={r['id'] for r in json.loads((p/'structural.json').read_text())['records']}|{r['id'] for r in json.loads((p/'ordinary.json').read_text())['entries']}|{'united-states','cabo-verde','saint-vincent-and-the-grenadines'}
rows=sorted([e for e in b['entries'] if e['verdict']=='needs-user-review' and e['id'] not in ex],key=lambda e:e['id'])
rows=rows[:len(rows)//2]
boards={e['id']:e for e in b['comparison_boards']}
(out/'boards').mkdir(exist_ok=True)
reviews=[]
for e in rows:
 ref=boards[e['id']]; data=subprocess.check_output(['git','show',ref['commit']+':'+ref['path']]); assert hashlib.sha256(data).hexdigest()==ref['sha256']; (out/'boards'/f"{e['id']}.jpg").write_bytes(data)
 r=e['independent_review']; selected={k:v for k,v in r.items() if ('visual' in k or k in ['parent_decision','parent_quality','hinge_assessment'])}; reviews.append({'id':e['id'],'review':selected})
(out/'observations.json').write_text(json.dumps(reviews,indent=2))
(out/'scope.json').write_text(json.dumps([{'id':e['id'],'evidence':{k:boards[e['id']][k] for k in ['commit','path','sha256']}} for e in rows],indent=2))
for start in range(0,len(rows),4):
 ims=[]
 for e in rows[start:start+4]:
  im=Image.open(out/'boards'/f"{e['id']}.jpg"); print(e['id'],im.size); im.thumbnail((1450,850)); ims.append((e['id'],im.copy()))
 sheet=Image.new('RGB',(1450,sum(im.height+28 for _,im in ims)), '#dddddd'); d=ImageDraw.Draw(sheet); y=0
 for id,im in ims: d.text((8,y+4),id,fill='black'); sheet.paste(im,(0,y+28)); y+=im.height+28
 sheet.save(out/f'sheet-{start//4+1}.jpg')
print('Validated',len(rows),'boards')
