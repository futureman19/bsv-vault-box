from pathlib import Path
import json, hashlib, urllib.request, subprocess, time
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SHA='9709a7a3fd1322a57cc090c97c03f733fed5ccb3'
for attempt in range(30):
    build=json.loads(subprocess.check_output(['gh','api','repos/futureman19/bsv-vault-box/pages/builds/latest']))
    (OUT/'pages-build.json').write_text(json.dumps(build,indent=2))
    print('Pages',attempt,build['status'],build['commit'],flush=True)
    if build['commit']==SHA and build['status']=='built':break
    if build['commit']==SHA and build['status']=='errored':raise RuntimeError(build)
    time.sleep(10)
else:raise RuntimeError('Pages build timeout')
files=['index.html','arcade.css']+[str(p.relative_to(ROOT/'docs')).replace('\\','/') for p in (ROOT/'docs').rglob('*.js')]+[str(p.relative_to(ROOT/'docs')).replace('\\','/') for p in (ROOT/'docs/assets/vault-kit').glob('*.glb')]
report={}
for f in files:
    url='https://boxsv.com/'+('' if f=='index.html' else f)
    with urllib.request.urlopen(url,timeout=30) as r:data=r.read();status=r.status
    worktree=(ROOT/'docs'/f).read_bytes()
    local=subprocess.check_output(['git','show',SHA+':docs/'+f],cwd=ROOT)
    # Pages publishes Git blobs; Windows working-tree text uses CRLF.
    assert worktree==local or (not f.endswith('.glb') and worktree.replace(b'\r\n',b'\n')==local)
    entry={'url':url,'status':status,'bytes':len(data),'live_sha256':hashlib.sha256(data).hexdigest(),'local_sha256':hashlib.sha256(local).hexdigest(),'worktree_sha256':hashlib.sha256(worktree).hexdigest(),'comparison':'approved Git blob; working tree verified with CRLF normalization for text only'}
    entry['match']=entry['live_sha256']==entry['local_sha256'];report[f]=entry
    (OUT/'hash-report.json').write_text(json.dumps(report,indent=2))
    assert entry['match'],entry
print('Hash matches',len(report),flush=True)
runtime={}
def phase(p,s):p.wait_for_function('(s)=>clawGame.state.phase===s',arg=s,timeout=15000)
with sync_playwright() as pw:
    browser=pw.chromium.launch(channel='chrome',headless=False,args=['--use-angle=d3d11','--enable-gpu'])
    try:
        for name,w,h,mobile in [('desktop',1440,1000,False),('mobile',390,844,True)]:
            ctx=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1,is_mobile=mobile,has_touch=mobile,reduced_motion='reduce' if mobile else 'no-preference')
            p=ctx.new_page();errors=[];console=[];bad=[];glbs={}
            p.on('pageerror',lambda e:errors.append(str(e)))
            p.on('console',lambda m:console.append({'type':m.type,'text':m.text}) if m.type in ['warning','error'] else None)
            p.on('response',lambda r:bad.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
            p.on('response',lambda r:glbs.update({r.url:r.status}) if '.glb' in r.url else None)
            p.goto('https://boxsv.com/',wait_until='networkidle')
            p.wait_for_function("window.claw3dHandle?.assets.status==='ready'",timeout=30000)
            assert len(glbs)==4 and all(v==200 for v in glbs.values()),glbs
            assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
            snap=p.evaluate('claw3dHandle.visualSnapshot()')
            assert all(x['authored']==1 for x in snap['prizes']+snap['fingers'])
            p.screenshot(path=str(OUT/(name+'-idle.png')),full_page=True)
            p.locator('#playBtn').click();p.locator('#optDemo').click();phase(p,'armed')
            before=p.evaluate('clawGame.state.x')
            if mobile:
                joy=p.locator('#joystick');joy.scroll_into_view_if_needed();r=joy.bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
                cdp=ctx.new_cdp_session(p)
                cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
                cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+25,'y':y+20}]})
                p.wait_for_timeout(350);cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            else:
                p.keyboard.down('ArrowRight');p.wait_for_timeout(450);p.keyboard.up('ArrowRight')
            assert p.evaluate('clawGame.state.x')>before
            p.locator('#dropBtn').click();phase(p,'grab');p.wait_for_function('clawGame.state.close>.2')
            assert p.evaluate('clawGame.state.drops')==1
            p.screenshot(path=str(OUT/(name+'-grab.png')),full_page=True)
            phase(p,'carry');p.screenshot(path=str(OUT/(name+'-carry.png')),full_page=True)
            phase(p,'reveal');p.wait_for_timeout(800);assert p.locator('#prizeCard').is_visible()
            p.screenshot(path=str(OUT/(name+'-reveal.png')),full_page=True)
            p.screenshot(path=str(OUT/(name+'-reveal-viewport.png')),full_page=False)
            coverage=p.locator('.reveal').evaluate('(el)=>{const r=el.getBoundingClientRect();return {top:r.top,left:r.left,width:r.width,height:r.height,viewportWidth:document.documentElement.clientWidth,viewportHeight:innerHeight,position:getComputedStyle(el).position}}')
            assert coverage['top']==0 and coverage['left']==0 and coverage['height']==coverage['viewportHeight'] and coverage['width']==coverage['viewportWidth'],coverage
            (OUT/(name+'-overlay-coverage.json')).write_text(json.dumps(coverage,indent=2))
            p.locator('#againBtn').click();phase(p,'armed');assert p.evaluate('clawGame.state.selected')==-1
            runtime[name]={'url':p.url,'viewport':[w,h],'assets':snap['assets'],'glbs':glbs,'keyboard_or_touch_move':True,'drop_grab_carry_reveal_reset':True,'pageerrors':errors,'console':console,'http_errors':bad}
            (OUT/'runtime-report.json').write_text(json.dumps(runtime,indent=2))
            # Retain renderer warnings in evidence; errors and unexpected warnings fail.
            known_warning_prefixes=('THREE.WebGLProgram: Program Info Log:', 'THREE.WebGLShadowMap: PCFSoftShadowMap has been removed.')
            unexpected=[m for m in console if m['type']=='error' or not m['text'].startswith(known_warning_prefixes)]
            assert not errors and not bad and not unexpected,(errors,bad,unexpected)
            ctx.close()
    finally:browser.close()
print(json.dumps(runtime,indent=2))
