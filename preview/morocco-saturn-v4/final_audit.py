from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
from glb_tools import load,view,accessor
import numpy as np
R=Path(__file__).resolve().parent;O=R.parent/'morocco-sandstone-v3'
a,ab=load(R/'baseline/morocco.glb');b,bb=load(R/'morocco.glb')
imageviews={a['images'][i]['bufferView'] for i in [3,4,5]}
for i in range(len(a['bufferViews'])):
 if i not in imageviews:assert view(a,ab,i)==view(b,bb,i),i
assert a['nodes']==b['nodes'] and a['meshes']==b['meshes'] and a['materials'][:7]==b['materials'][:7]
for f in ['viewer.js','motion.mjs','template.html','viewer.bundle.js']:
 assert (O/f).read_bytes()==(R/f).read_bytes(),f
for name in ['saturn-color.png','saturn-normal.png','saturn-orm.png']:
 ar=np.asarray(Image.open(R/'maps'/name),dtype=int);assert np.array_equal(ar[:,0],ar[:,-1]),name
checks=['preservation-check','source-preservation-check','source-check','parity-check','browser-check','extended-check','runtime-material-check']
for name in checks:assert (R/(name+'.json')).is_file(),name
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
result={'all_nonbody_and_geometry_buffer_views_byte_identical':True,'body_uv_bytes_also_identical_to_v3':True,'nodes_meshes_nonbody_materials_exact':True,'viewer_motion_template_bundle_byte_identical':True,'all_three_map_wrap_endpoints_exact':True,'fresh_mechanism_samples':81,'html_bytes':(R/'morocco-saturn-v4.html').stat().st_size,'visual_verdict':'Recognizable stylized Saturn bands in closeup; cream-gold flow remains visible on mobile. Not unmistakable NASA realism: can also read banded onyx. One targeted localized-shear correction, no further loop.'}
assert result['html_bytes']<5000000
(R/'final-audit.json').write_text(json.dumps(result,indent=2))
# Factual reference board: NASA is morphology reference only, never a model map.
canvas=Image.new('RGB',(1600,1140),'#172027');d=ImageDraw.Draw(canvas)
items=[('NASA/JPL/SSI PIA06655: infrared morphology reference only','references/saturn-nasa-reference.jpg'),('Original Morocco concept: retain lid/tile/mountains/hardware','references/primary-morocco.png'),('Independent generated cloud painting + localized shear','swatch-B.png'),('V4 ACTUAL BROWSER MODEL - not an AI box render','v4-matched-closed.png')]
for k,(label,f) in enumerate(items):
 x=(k%2)*800;y=(k//2)*560;d.text((x+16,y+15),label,fill='#f1dec2');im=Image.open(R/f).convert('RGB');im.thumbnail((770,510));canvas.paste(im,(x+(800-im.width)//2,y+45+(510-im.height)//2))
d.text((16,1120),'NASA: https://science.nasa.gov/resource/waves-on-saturn/ | No endorsement; no NASA pixels in model maps.',fill='#dddddd')
canvas.save(R/'material-reference-board.jpg',quality=92)
print(json.dumps(result,indent=2))
