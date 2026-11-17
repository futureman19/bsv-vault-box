import pathlib,json,hashlib
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
entries={e['id']:e for e in json.loads((R/'parent-ledger.json').read_text())['entries']}
out=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for slug in ['venezuela','chile','saint-kitts-and-nevis']:
  e=entries[slug]; f=pathlib.Path(e['delivered_viewer']['path']);assert hashlib.sha256(f.read_bytes()).hexdigest()==e['viewer']['sha256']
  c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();errors=[];p.on('pageerror',lambda err:errors.append(str(err)))
  p.goto(f.as_uri());p.wait_for_function('pilot.ready');p.locator('#open').click();p.wait_for_function('pilot.progress===1')
  d=R/'resume-runtime'/slug;d.mkdir(parents=True,exist_ok=True)
  p.screenshot(path=str(d/'open.png'))
  nodes=p.evaluate('''()=>{let a=[];pilot.root.traverse(o=>{if(/hinge|latch|clasp|pivot|keeper/i.test(o.name))a.push({name:o.name,parent:o.parent?.name,position:o.position.toArray(),world:o.getWorldPosition(o.position.clone()).toArray()})});return a}''')
  box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
  p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+450,y+50,steps=25);p.mouse.up();p.wait_for_timeout(600);p.screenshot(path=str(d/'rotated-open.png'))
  p.locator('#reset').click();p.wait_for_function('pilot.progress===0');assert not errors
  out.append({'id':slug,'viewer_sha256':e['viewer']['sha256'],'open_reset':'pass','hardware_nodes':nodes,'page_errors':errors});c.close()
 b.close()
(R/'resume-runtime.json').write_text(json.dumps(out,indent=2)+'\n')
print('3 immutable runtime investigations passed open/reset; captures saved')
