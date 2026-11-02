# Historical one-time scaffolding record, NOT part of regeneration.
# All required inputs are now in the archive. See README for safe rebuild commands.
raise SystemExit('Scaffolding disabled: use materials.py, author.py, finalize_glb.py, build.py')
from pathlib import Path
import shutil,requests,json
R=Path(__file__).resolve().parent;OLD=R.parent/'morocco-sandstone-v3'
files=['viewer.js','viewer.bundle.js','motion.mjs','template.html','build.py','verify_browser.py','verify_extended.py','verify_source.py','verify_parity.py','THREE-LICENSE.txt','package.json','glb_tools.py','author.py','finalize_glb.py','verify_preservation.py','verify_source_preservation.py','verify_material_runtime.py','review.py','package_delivery.py']
for f in files:
 s=(OLD/f).read_text(encoding='utf8').replace('morocco-sandstone-v3','morocco-saturn-v4')
 (R/f).write_text(s,encoding='utf8')
for d in ['baseline','maps','references']: (R/d).mkdir(exist_ok=True)
for f in ['morocco.blend','morocco.glb']:shutil.copy2(OLD/f,R/'baseline'/f)
shutil.copy2(OLD/'references/primary-morocco.png',R/'references/primary-morocco.png')
urls={'saturn-nasa-reference.jpg':'https://assets.science.nasa.gov/content/dam/science/psd/solar/2023/09/p/PIA06655.jpg','generated-cloud-master.png':'https://files-cdn.x.ai/zreTJJP2Rli-S7tQAKfPVA/file_80287699-b063-4a08-901e-4d805d2e3da5.png'}
for name,url in urls.items():
 r=requests.get(url);r.raise_for_status();(R/'references'/name).write_bytes(r.content)
(R/'references/provenance.json').write_text(json.dumps({'reference_page':'https://science.nasa.gov/resource/waves-on-saturn/','reference_image':urls['saturn-nasa-reference.jpg'],'credit':'NASA/JPL/Space Science Institute','reference_id':'PIA06655','reference_scope':'Informational morphological comparison only. Infrared grayscale, NOT color evidence. No NASA pixels used in model texture. No endorsement.','rights_guidance':'https://www.nasa.gov/nasa-brand-center/images-and-media/','rights_note':'NASA guidelines allow factual informational use with acknowledgement, note third-party exceptions and specifically discourage NFT use. This reference is not minted or used as a model map. Generated texture is independently generated and is not NASA imagery. No commercial clearance claimed.','texture_source':urls['generated-cloud-master.png'],'texture_generator':'xAI grok-imagine-image via image_generate, original text prompt, no source image input','texture_status':'AI generated art, not scientific Saturn data'},indent=2))
print('Copied bounded source and downloaded references')
