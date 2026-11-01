from pathlib import Path
import shutil,hashlib,json
R=Path(__file__).resolve().parent; S=R.parent/'iceland-moss-v7'
paths=[p for p in S.rglob('*') if p.is_file() and 'node_modules' not in p.parts]
P=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-promotional/iceland-promotional.png');paths.append(P)
(R/'preserved-inputs.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2))
for n in ['viewer.js','motion.mjs','template.html','verify_source.py','verify_parity.py','verify_browser.py','verify_extra.py','build.py','package_delivery.py','THREE-LICENSE.txt','package.json','package-lock.json']:
 text=(S/n).read_text(encoding='utf8').replace('iceland-moss-v7','iceland-stone-ice-v8').replace('Moss v7','Stone + Ice v8')
 if n=='verify_extra.py':text=text.replace("t['width']==128","t['width']==512").replace('V7 /','V8 /')
 (R/n).write_text(text,encoding='utf8')
for n in ['motion.mjs','viewer.js']:shutil.copy2(S/n,R/n)
shutil.copy2(S/'iceland.blend',R/'approved-v7.blend');shutil.copy2(S/'iceland.glb',R/'approved-v7.glb')
(R/'acceptance-gaps.md').write_text('''# Visible acceptance gaps — before authoring
Primary AI promo and actual v7-matched.png inspected independently through vision.
- Stone: v7 broad flat pillar facets lack fine grain; joints alone do not supply missing chunks. Cut nonrepeating wedges into individual exterior blocks on all four sides, with varied depths and broken ledges. Preserve continuous inner liner and wide silhouette, charcoal values, hardware.
- Texture: compact portable fine porous normal and charcoal color map, not cloudy pale paint or random drilled holes. Real medium-scale chipped planes must remain legible separately.
- River: thin flat cyan ribbon needs connected deep center, widening/narrowing and shallow integrated banks. Preserve its route, real inset and glossy black lid; cascade remains an articulated miniature motif, not simulated water.
- Ice: small pale faceted mountain cluster needs asymmetrical jagged relief, interrupted crevasses, snowy high ridges and blue deeper ice, with low terminus feeding same channel. No symmetrical cone forest.
- Moss: retain visible v7 green accents; re-conform only displaced patches to chipped stone.
- Acceptance: same camera and lighting old/new plus rear and macro views, actual offline GLTFLoader. 81 motion samples with unchanged exclusions, source reopen/parity, shell rays, actual decoded maps, finite nondegenerate export, desktop/mobile offline interactions. HTML <=5,000,000 bytes; target <=4,500,000.
''')
print('SETUP',len(paths))
