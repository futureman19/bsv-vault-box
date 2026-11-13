from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'author.py';s=p.read_text()
a=s.index("stone('Terrain / granite'");b=s.index('def tube(',a);s=s[:a]+s[b:]
a=s.index('trunk=[');b=s.index('# Medallion',a)
s=s[:a]+'''# Three stylized sculptural roses, seated on a continuous green carrier.
pink=mat('Rose / dusty pink',(.56,.16,.24),.48)
blush=mat('Rose / inner blush',(.72,.28,.36),.43)
cube('Rose carrier',(0,.1,1.993),(2.7,1.35,.035),moss,lid,.012)
for j,(cx,cy) in enumerate([(-.85,.10),(0,.30),(.85,.10)]):
 tube('Rose stem '+str(j),[(cx,-.45,2.025),(cx+.08,-.10,2.035),(cx,cy,2.055)],[.025,.022,.022],moss)
 for ring in range(2):
  for k in range(6):
   a=k*math.tau/6+ring*.45;r=.20 if ring==0 else .095
   o=stone('Rose petal '+str(j)+' '+str(ring)+' '+str(k),(cx+r*math.cos(a),cy+r*math.sin(a),2.09+ring*.07),(.16 if ring==0 else .105,.10 if ring==0 else .07,.065),lid,pink if ring==0 else blush,2)
   o.rotation_euler.z=a+.6
 stone('Rose center '+str(j),(cx,cy,2.19),(.07,.07,.055),lid,blush,2)
 for k in range(4):
  a=k*math.tau/4+.7
  o=stone('Rose leaf '+str(j)+' '+str(k),(cx+.34*math.cos(a),cy+.34*math.sin(a),2.045),(.18,.07,.035),lid,moss,1);o.rotation_euler.z=a
''' + s[b:]
s=s.replace("'Cedar /", "'Wine timber /").replace("'Cedar tree /", "'Rose /")
s=s.replace("scene.cycles.samples=32", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False")
s=s.replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800').replace("location=(-5.6,-7.8,4.5)","location=(-5.6,-7.8,6.5)")
p.write_text(s)
p=R/'maps.py';s=p.read_text().replace('167*v,87*v,46*v','132*v,52*v,64*v');p.write_text(s)
p=R/'template.html';s=p.read_text().replace('Yakushima cedar. Mossed granite. Quiet brass.','Rose Valley pink. Wine timber. Quiet brass.').replace('inspired by the original Bulgaria concept','inspired by the rose-growing tradition of Kazanlak').replace('JAPAN','BULGARIA');p.write_text(s)
p=R/'viewer.js';s=p.read_text().replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.2,7)');p.write_text(s)
p=R/'verify_browser.py';s=p.read_text().replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=3000);assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=3000);assert page.evaluate('pilot.progress')==0")
s=s.replace('context.close();browser.close()', '''context.close()
 context=browser.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844})
 page=context.new_page();page.goto((ROOT/'bulgaria-v1.html').as_uri());assert page.locator('#fallback').is_visible();page.screenshot(path=str(ROOT/'mobile-nojs.png'));results.append({'case':'no-JS','poster':True});context.close();browser.close()''');p.write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('adapted scoped source')
