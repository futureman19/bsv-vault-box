import io,json,pathlib,subprocess
from PIL import Image,ImageOps,ImageDraw
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'launch-candidates.json').read_text()); ids=['afghanistan','arctic-ocean','iceland','japan','morocco','the-moon','united-states']
board=Image.new('RGB',(1080,280*len(ids)+40),'#171a1f'); draw=ImageDraw.Draw(board)
draw.text((12,12),'Published promotional illustration | actual delivered model desktop | actual model mobile (closed)',fill='white')
for i,slug in enumerate(ids):
    e=next(e for e in D['entries'] if e['id']==slug); m=e['marketing']; raw=subprocess.check_output(['git','show',m['commit']+':'+m['path']]); images=[Image.open(io.BytesIO(raw)),Image.open(R/'smoke'/slug/'desktop-closed.png'),Image.open(R/'smoke'/slug/'mobile-closed.png')]
    for col,image in enumerate(images):
        image=ImageOps.contain(image.convert('RGB'),(350,245)); board.paste(image,(col*360+(350-image.width)//2,40+i*280))
    draw.text((12,40+i*280+250),slug+' — candidate, not final approval',fill='white')
board.save(R/'representative-comparison.jpg',quality=88)
