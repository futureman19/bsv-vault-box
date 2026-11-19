import json,pathlib,subprocess,hashlib
from PIL import Image,ImageDraw
root=pathlib.Path(__file__).resolve().parent
inputs=root.parent/'inputs'
b=json.loads((inputs/'baseline.json').read_text())
held=sorted([e for e in b['entries'] if e['verdict']=='needs-user-review'],key=lambda e:e['id'])
excluded={e['id'] for e in json.loads((inputs/'structural.json').read_text())['records']}|{e['id'] for e in json.loads((inputs/'ordinary.json').read_text())['entries']}|{'united-states','cabo-verde','saint-vincent-and-the-grenadines'}
scope=[e for e in held[len(held)//2:] if e['id'] not in excluded]
boards={e['id']:e for e in b['comparison_boards']}
(root/'boards').mkdir(exist_ok=True)
for e in scope:
 r=boards[e['id']]; data=subprocess.check_output(['git','show',r['commit']+':'+r['path']]); assert hashlib.sha256(data).hexdigest()==r['sha256']; (root/'boards'/ (e['id']+'.jpg')).write_bytes(data)
(root/'scope.json').write_text(json.dumps(scope,indent=2))
print('held',len(held),'midpoint',len(held)//2,'scope',len(scope))
for e in scope: print(e['id'],json.dumps(e['independent_review'].get('visual_review',e['independent_review']),ensure_ascii=True))
print('dimensions',Image.open(root/'boards'/(scope[0]['id']+'.jpg')).size)
for i in range(0,len(scope),4):
 group=scope[i:i+4]; sheet=Image.new('RGB',(1600, len(group)*600),'white'); draw=ImageDraw.Draw(sheet)
 for j,e in enumerate(group):
  im=Image.open(root/'boards'/(e['id']+'.jpg')); im.thumbnail((1600,570)); sheet.paste(im,(0,j*600+30)); draw.text((10,j*600+8),e['id'],fill='black')
 sheet.save(root/f'sheet-{i//4+1}.jpg',quality=94)
