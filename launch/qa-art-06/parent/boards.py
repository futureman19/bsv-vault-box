import json,pathlib
from PIL import Image,ImageOps,ImageDraw
R=pathlib.Path(__file__).resolve().parent
rows=json.loads((R/'packaging-results.json').read_text())
for e in rows:
 s=e['id']; paths=[R/'sources'/s/'marketing.webp']+[R/'smoke'/s/(mode+'-'+pose+'.png') for mode in ['desktop','mobile'] for pose in ['closed','open']]
 if not all(p.exists() for p in paths): continue
 board=Image.new('RGB',(1800,620),'#202028');d=ImageDraw.Draw(board);d.text((20,12),s,fill='white')
 for i,p in enumerate(paths):
  im=Image.open(p).convert('RGB')
  if i in (1,2):im=im.crop((220,190,1220,940))
  im=ImageOps.contain(im,(350,550));board.paste(im,(i*360+(350-im.width)//2,55));d.text((i*360+8,36),['PROMOTIONAL','desktop closed','desktop open','mobile closed','mobile open'][i],fill='white')
 (R/'boards').mkdir(exist_ok=True);board.save(R/'boards'/(s+'.jpg'),quality=90)
print('boards',len(list((R/'boards').glob('*.jpg'))))
