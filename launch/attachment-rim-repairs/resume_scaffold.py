from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[2];ref=R/'preview/chile-repair-v2'
for slug in ['algeria','guyana']:
 root=R/'preview'/f'{slug}-repair-v2';old=root/'historical-v1'
 for name in ['template.html','viewer.bundle.js','viewer.js','motion.mjs','package.json','package-lock.json','THREE-LICENSE.txt','test_motion.mjs']:
  if (old/name).exists():shutil.copyfile(old/name,root/name)
 for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py']:
  (root/name).write_text((ref/name).read_text().replace('chile',slug))
 # Source parity only needs the existing embedded images, no texture regeneration.
 for name in ['verify_extended.py']:
  text=(ref/name).read_text().replace('chile',slug).replace("assert 'Chile / Atacama Salt & Copper' in p.locator('h1').inner_text()",f"assert '{slug.title()} /' in p.locator('h1').inner_text()")
  if slug=='algeria':text=text.replace("{'map','normalMap','roughnessMap'}","{'map','roughnessMap'}")
  (root/name).write_text(text)
print('copied bounded verification helpers; original viewer and motion bytes retained')
