from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import json, hashlib
root=Path('launch/ordinary-finish-20')
ids='argentina bangladesh cambodia comoros djibouti eritrea gambia guinea-bissau lebanon malawi'.split()
out=root/'reviewer-a'; out.mkdir(exist_ok=True)
records=[]
for ident in ids:
    board=Image.new('RGB',(1500,1000),'#303030'); draw=ImageDraw.Draw(board)
    files=[root/'captures'/ident/f'{device}-{state}.png' for device,state in [('desktop','closed'),('desktop','open'),('mobile','closed'),('mobile','open')]]
    files+=list((root/'baseline'/ident).glob('*.webp'))[:1]
    boxes=[(0,25,550,490),(550,25,1100,490),(0,520,390,1000),(400,520,790,1000),(1100,25,1500,490)]
    for f,box in zip(files,boxes):
        im=Image.open(f).convert('RGB')
        if f.name.startswith('desktop'): im=im.crop((280,230,1000,850))
        draw.text((box[0]+5,box[1]),f.name,fill='white')
        fit=ImageOps.contain(im,(box[2]-box[0],box[3]-box[1]-20))
        board.paste(fit,(box[0],box[1]+20))
        records.append({'id':ident,'path':f.as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':im.size})
    board.save(out/f'{ident}.jpg',quality=95)
(out/'inspected-inputs.json').write_text(json.dumps(records,indent=2))
print('Created',len(ids),'boards and',len(records),'input hash records')
