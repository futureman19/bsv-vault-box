from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish';ref=R/'preview/algeria-repair-v2'
for row in json.loads((D/'targets.json').read_text()):
 slug=row['id']
 if slug=='iceland':continue
 root=R/'preview'/f'{slug}-repair-v2';root.mkdir(exist_ok=False);old=R/row['root']/'original'
 shutil.copytree(old,root/'historical-v1')
 for name in ['template.html','viewer.bundle.js','viewer.js','motion.mjs','package.json','package-lock.json','THREE-LICENSE.txt','test_motion.mjs','tests.mjs']:
  if (old/name).exists():shutil.copyfile(old/name,root/name)
 for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py']:
  (root/name).write_text((ref/name).read_text().replace('algeria',slug))
 (root/'.gitattributes').write_text('* -text\n');(root/'.gitignore').write_text('node_modules/\n*.blend1\n__pycache__/\n')
 shutil.copytree(R/row['root']/'before',root/'before')
 shutil.copyfile(R/row['root']/'immutable-source.json',root/'immutable-source.json')
 print(slug)
