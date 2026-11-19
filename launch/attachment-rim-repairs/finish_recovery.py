from pathlib import Path
from playwright.sync_api import sync_playwright
import json,subprocess,shutil
R=Path(__file__).resolve().parent/'finish';rows=json.loads((R/'packages/package-check.json').read_text());results=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for row in rows:
  out=R/'acceptance'/row['id']
  for mobile,w,h in [(False,1440,1080),(True,390,844)]:
   c=b.new_context(offline=True,reduced_motion='reduce',is_mobile=mobile,has_touch=mobile,viewport={'width':w,'height':h});p=c.new_page();errors=[];external=[]
   p.on('pageerror',lambda e: errors.append(str(e)));p.on('request',lambda q: external.append(q.url) if q.url.startswith(('https:','http:')) else None)
   p.goto(Path(row['recovered_viewer']).as_uri());p.wait_for_function('window.pilot?.ready')
   p.evaluate('''()=>{window.samples=[];let count=0;function sample(){samples.push(pilot.progress);if(++count<120)requestAnimationFrame(sample)}requestAnimationFrame(sample)}''')
   p.locator('#open').tap() if mobile else p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.wait_for_function('samples.includes(1)')
   samples=p.evaluate('samples');assert all(v in [0,1] for v in samples),samples
   p.screenshot(path=str(out/f"recovered-{'mobile' if mobile else 'desktop'}-open.png"))
   p.locator('#reset').tap() if mobile else p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
   assert not errors and not external;assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
   results.append({'id':row['id'],'mobile':mobile,'native_open_reset':True,'reduced_motion_sampled_frames':len(samples),'only_endpoints':True,'page_errors':errors,'external_requests':external,'no_overflow':True});c.close()
  c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto(Path(row['recovered_viewer']).as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');c.close()
  # Run the packaged isolated suites, not mutable working copies.
  viewer=Path(row['recovered_viewer']);base=next(p for p in viewer.parents if p.name.startswith(row['id']+'-') and p.parent.name=='recovered')
  motion=base/'launch/attachment-rim-repairs/finish/acceptance'/row['id']/'motion'
  for test in sorted(motion.glob('*test*.mjs')):
   proc=subprocess.run([shutil.which('node.exe') or shutil.which('node'),'--test','--test-reporter=tap',test.name],cwd=motion,capture_output=True,text=True)
   (out/f'recovered-{test.stem}-output.txt').write_text(proc.stdout+proc.stderr);assert proc.returncode==0 and '# fail 0' in proc.stdout
  print(row['id'],'recovered desktop/mobile/noJS/motion PASS',flush=True)
 b.close()
(R/'acceptance/recovery-check.json').write_text(json.dumps(results,indent=2))
