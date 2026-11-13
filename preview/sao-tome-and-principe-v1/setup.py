"""Copy only mechanics/runtime harnesses; construct a new landscape author."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copy2(B/n,R/n)
 if n in ['motion.mjs','package.json']:
  (R/n).write_text((R/n).read_text().replace('Invalid Japan geometry','Invalid Sao Tome and Principe geometry').replace('boxsv-japan-cedar-v1','boxsv-sao-tome-and-principe-v1'))
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','sao-tome-and-principe-v1').replace('japan.glb','sao-tome-and-principe.glb').replace('japan.blend','sao-tome-and-principe.blend')
 s=s.replace('Japan / Cedar & Moss','Sao Tome and Principe / Phonolite & Rainforest').replace('Japan Cedar and Moss','Sao Tome and Principe Phonolite and Rainforest').replace('Yakushima cedar. Mossed granite. Quiet brass.','A volcanic needle above the Gulf of Guinea forest.').replace('inspired by the original Japan concept','inspired by Sao Tome’s volcanic needle and the archipelago’s rainforests').replace('JAPAN ·','SAO TOME & PRINCIPE ·')
 if n=='viewer.js':
  s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.1,7)')
  s=s.replace("target=target?0:1;open.textContent", "target=target?0:1;if(reduced.matches){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;}open.textContent")
  s=s.replace("controls.reset();open.textContent", "controls.reset();lid.rotation.x=latch.rotation.x=0;window.pilot.progress=0;open.textContent")
 if n=='verify_browser.py':s=s.replace("timeout=25000","timeout=60000")
 (R/n).write_text(s,encoding='utf8')
s=(B/'author.py').read_text(encoding='utf8')
# Keep generic mesh/material helpers only. No Japan skins, tree or needle sprays.
header=s[s.index('import bpy'):s.index('wood=mat')]
helpers=s[s.index('def uv'):s.index('for o in bpy.data.objects:')]
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
helpers=helpers.replace("layer.data[li].uv=(u/3.72+.5,v/1.7+.5)","layer.data[li].uv=(u*.65+.5,v*.65+.5)")
stone=s[s.index('def stone'):s.index('for sx in [-1,1]:',s.index('def stone'))]
ornament=s[s.index('def disk'):s.index('# Clean obsolete')]
end=s[s.index('# Clean obsolete'):].replace('japan.blend','sao-tome-and-principe.blend').replace('japan.glb','sao-tome-and-principe.glb').replace('JAPAN AUTHORED','SAO TOME AND PRINCIPE AUTHORED')
end=end.replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.2)').replace('Vector((0,0,1.17))','Vector((0,0,1.35))').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=1000').replace('resolution_y=1000','resolution_y=900')
custom=(R/'landscape.py.inc').read_text(encoding='utf8')
materials='''granite=mat('Phonolite / graphite olive',(.15,.17,.13),.8);maptex(granite,'stone-color.png','Base Color');maptex(granite,'stone-roughness.png','Roughness',True)
wood=granite
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Forest / green reveal',(.035,.07,.032),.9)
forest=mat('Forest / terrain',(.055,.13,.035),.9);maptex(forest,'forest-color.png','Base Color')
canopy=[mat('Forest / canopy '+str(i),c,.9) for i,c in enumerate([(.055,.13,.027),(.075,.17,.035),(.10,.20,.045)])]
'''
(R/'author.py').write_text(header+materials+helpers+stone+custom+ornament+end,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('New scoped author and inherited mechanics/runtime harnesses ready')
