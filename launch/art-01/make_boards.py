from PIL import Image,ImageOps,ImageDraw
import pathlib,json
R=pathlib.Path(__file__).resolve().parent
(R/'boards').mkdir(exist_ok=True)
for s in json.loads((R/'assigned.json').read_text()):
 paths=[R/'marketing'/f'{s}.webp']+[R/'smoke'/s/f'{m}-{p}.png' for m,p in [('desktop','closed'),('desktop','open'),('mobile','closed'),('mobile','open')]]
 if not all(p.exists() for p in paths): continue
 board=Image.new('RGB',(1800,1050),'#232323'); d=ImageDraw.Draw(board);d.text((15,10),s+' | promotional illustration vs actual unchanged viewer',fill='white')
 for i,p in enumerate(paths):
  im=Image.open(p).convert('RGB')
  if i in [1,2]: im=im.crop((200,270,1240,850))
  x,y,w,h=[(0,40,600,500),(600,40,600,500),(1200,40,600,500),(300,550,600,480),(900,550,600,480)][i]
  im=ImageOps.contain(im,(w,h-25));board.paste(im,(x+(w-im.width)//2,y+25));d.text((x+15,y),['MARKETING','DESKTOP CLOSED','DESKTOP OPEN','MOBILE CLOSED','MOBILE OPEN'][i],fill='white')
 board.save(R/'boards'/f'{s}.jpg',quality=92)
