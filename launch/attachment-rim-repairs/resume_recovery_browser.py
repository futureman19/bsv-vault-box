from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent;rows=json.loads((R/'resume-package-check.json').read_text());results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for row in rows:
  for mobile,w,h in [(False,1440,1080),(True,390,844)]:
   c=b.new_context(offline=True,reduced_motion='reduce',is_mobile=mobile,has_touch=mobile,viewport={'width':w,'height':h});p=c.new_page();p.goto(Path(row['recovered_viewer']).as_uri());p.wait_for_function('window.pilot?.ready')
   p.evaluate('''()=>{window.samples=[];let count=0;function sample(){samples.push(pilot.progress);if(++count<120)requestAnimationFrame(sample)}requestAnimationFrame(sample)}''')
   p.locator('#open').tap() if mobile else p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.wait_for_timeout(250)
   samples=p.evaluate('samples');assert 1 in samples and all(v in [0,1] for v in samples),samples
   p.screenshot(path=str(R/f"{row['id']}-recovered-{'mobile' if mobile else 'desktop'}-open.png"))
   p.locator('#reset').tap() if mobile else p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
   results.append({'id':row['id'],'mobile':mobile,'recovered_file':row['recovered_viewer'],'native_open_reset':True,'reduced_motion_sampled_frames':len(samples),'reduced_motion_only_endpoints':True});c.close()
  c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto(Path(row['recovered_viewer']).as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');c.close()
 b.close()
(R/'resume-recovery-browser-check.json').write_text(json.dumps(results,indent=2));print(results)
