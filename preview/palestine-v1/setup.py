from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs','package.json','build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html','maps.py']:
 if n.endswith(('.blend','.txt')): shutil.copy2(B/n,R/n);continue
 s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','palestine-v1').replace('japan.glb','palestine.glb').replace('japan.blend','palestine.blend').replace('Japan','Palestine').replace('Cedar & Moss','Crimson Stitch').replace('Cedar &amp; Moss','Crimson Stitch')
 (R/n).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
s=(B/'author.py').read_text();lines=s.splitlines()
s='\n'.join(lines[:86]+lines[90:103])+'''
cloth=mat('Charcoal linen / woven',(.025,.024,.022),.95);maptex(cloth,'weave.png','Base Color')
red=mat('Crimson thread',(.45,.018,.035),.65)
ivory=mat('Ivory border',(.68,.58,.40),.8)
cube('Textile / inset',(0,0,2.005),(2.90,1.70,.05),cloth,lid,.015)
for sy in [-1,1]:cube('Textile / border long',(0,sy*.81,2.037),(2.82,.022,.012),ivory,lid,.003)
for sx in [-1,1]:cube('Textile / border short',(sx*1.40,0,2.037),(.022,1.60,.012),ivory,lid,.003)
for cx in [-.88,0,.88]:
 for k in range(16):
  side=k//4;t=(k%4)/4
  corners=[(0,.55),(.37,0),(0,-.55),(-.37,0),(0,.55)]
  a,b=corners[side],corners[side+1];x=cx+a[0]*(1-t)+b[0]*t;y=a[1]*(1-t)+b[1]*t
  for sign in [-1,1]:tube('Stitch / cross',[(x-.042,y-sign*.044,2.041),(x+.042,y+sign*.044,2.041)],[.009,.009],red,sides=6)
'''+'\n'.join(lines[124:])
s=s.replace('japan.blend','palestine.blend').replace('japan.glb','palestine.glb').replace('JAPAN AUTHORED','PALESTINE AUTHORED').replace('Cedar','Honey wood').replace("(.035,.07,.032)","(.018,.018,.019)")
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=2').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(s)
s=(R/'maps.py').read_text().replace('167*v,87*v,46*v','174*v,121*v,65*v')
s+='\nweave=28+7*np.sin(x*256*6.283)*np.sin(y*256*6.283)+rng.normal(0,2,x.shape)\nImage.fromarray(np.uint8(np.clip(np.stack([weave,weave*.95,weave*.9],-1),0,255))).save(R/"weave.png",optimize=True)\n'
(R/'maps.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n');(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('scoped sources prepared')
