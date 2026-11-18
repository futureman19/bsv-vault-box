from pathlib import Path
from PIL import Image, ImageDraw
import json,hashlib
root=Path(__file__).resolve().parent.parent
out=Path(__file__).resolve().parent
ids='mexico myanmar nigeria palestine qatar samoa southern-ocean tajikistan tunisia zambia'.split()
evidence=[]
for ident in ids:
    board=Image.new('RGB',(1570,1340),'#222222'); draw=ImageDraw.Draw(board)
    for row,state in enumerate(['closed','open']):
        for mode,x in [('desktop',0),('mobile',680)]:
            p=root/'captures'/ident/f'{mode}-{state}.png'
            im=Image.open(p).convert('RGB')
            evidence.append({'id':ident,'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':im.size})
            im=im.crop((300,240,980,800)) if mode=='desktop' else im.crop((0,100,390,740))
            board.paste(im,(x,row*670+25));draw.text((x+8,row*670+7),f'{ident} {mode} {state}',fill='white')
    p=root/'baseline'/ident/f'{ident}.webp'
    im=Image.open(p).convert('RGB');im.thumbnail((500,630));board.paste(im,(1070,25));draw.text((1078,7),'PROMOTIONAL ONLY',fill='white')
    evidence.append({'id':ident,'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    board.save(out/f'{ident}.jpg',quality=95)
(out/'inspected-inputs.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(f'Created {len(ids)} boards; recorded {len(evidence)} input hashes')
