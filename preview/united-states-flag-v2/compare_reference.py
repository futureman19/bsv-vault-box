from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import hashlib,json
R=Path(__file__).resolve().parent
ref=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-usa-flag-fireworks/united-states-flag-fireworks.png')
a=Image.open(ref).convert('RGB');b=Image.open(R/'poster.png').convert('RGB')
board=Image.new('RGB',(1200,650),(16,21,26));d=ImageDraw.Draw(board)
for x,im,label in [(0,a,'APPROVED ILLUSTRATION (not model)'),(600,b,'ACTUAL FLAG V2 MODEL (Cycles poster; no FX)')]:
 thumb=ImageOps.contain(im,(590,590));board.paste(thumb,(x+(600-thumb.width)//2,40+(590-thumb.height)//2));d.text((x+15,15),label,fill='white')
board.save(R/'reference-comparison.jpg',quality=92)
(R/'reference-provenance.json').write_text(json.dumps({'path':str(ref),'sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'dimensions':a.size,'comparison':'Full images proportion-preserved, not pixel-equivalence or exact geometry claim.'},indent=2))
