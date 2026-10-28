"""Headed actual HTTP/GLTFLoader, rigid anchor and demo-flow acceptance."""
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import pathlib, threading, json, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence/vault-assets';OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
report={}
def phase(page,name):page.wait_for_function('(p)=>clawGame.state.phase===p',arg=name,timeout=12000)
def shot(page,name):page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def arm(page):page.locator('#playBtn').click();page.locator('#optDemo').click();phase(page,'armed')
def state(page):return page.evaluate('clawGame.state')
def visual(page):return page.evaluate('claw3dHandle.visualSnapshot()')
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=False,args=['--use-angle=d3d11','--enable-gpu'])
  for name,w,h,mobile,reduced,reject in [('desktop',1440,1000,False,False,None),('mobile-reduced',390,844,True,True,None),('desktop-rejected',1440,1000,False,False,'vault-box')]+[(f'fallback-{n}',390,844,True,True,n) for n in ['cabinet','claw-hub','claw-finger','vault-box']]:
   opts={'viewport':{'width':w,'height':h},'device_scale_factor':1,'has_touch':mobile,'is_mobile':mobile,'reduced_motion':'reduce' if reduced else 'no-preference'}
   if name=='desktop':opts.update(record_video_dir=str(OUT/'video'),record_video_size={'width':1440,'height':1000})
   context=browser.new_context(**opts);page=context.new_page();errors=[];responses={};rejected=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('response',lambda r:responses.update({r.url.split('/')[-1]:r.status}) if '.glb' in r.url else None)
   if reject:
    def abort(route):rejected.append(route.request.url);route.abort()
    page.route(f'**/{reject}.glb',abort)
   page.goto(url);page.wait_for_function("window.claw3dHandle?.assets.status!=='loading' && !!window.claw3dHandle",timeout=20000)
   snap=visual(page);expected='fallback' if reject else 'ready';assert snap['assets']['status']==expected,snap
   assert snap['primitiveCabinetVisible']==bool(reject)
   if not reject:
    assert all(v==200 for v in responses.values()) and len(responses)==4,responses
    assert all(p['authored']==1 for p in snap['prizes']) and all(f['authored']==1 for f in snap['fingers'])
   else:assert len(rejected)==1
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   page.locator('.machine-wrap').scroll_into_view_if_needed();page.wait_for_timeout(200)
   canvas=page.locator('.claw3d-canvas')
   stability=None
   if reduced:
    code="el=>new Promise(r=>requestAnimationFrame(()=>r(el.toDataURL())))"
    before_visual=visual(page)
    a=canvas.evaluate(code);page.wait_for_timeout(250);b=canvas.evaluate(code)
    assert len(a)>10000 and before_visual==visual(page), 'nonempty, unchanged reduced-motion pose'
    stability={'byte_identical':a==b,'changed_pixels':0,'max_channel_delta':0}
    if a!=b:
     import base64,io
     from PIL import Image,ImageChops
     aa=base64.b64decode(a.split(',')[1]);bb=base64.b64decode(b.split(',')[1])
     (OUT/(name+'-static-a.png')).write_bytes(aa);(OUT/(name+'-static-b.png')).write_bytes(bb)
     diff=ImageChops.difference(Image.open(io.BytesIO(aa)),Image.open(io.BytesIO(bb)))
     pixels=list(diff.getdata());stability.update(changed_pixels=sum(any(v) for v in pixels),max_channel_delta=max(max(v) for v in pixels))
     # Observed D3D11 one-pixel/one-LSB raster variance with identical transforms.
     # This is not a motion tolerance: any second pixel or larger delta fails.
     assert stability['changed_pixels']<=1 and stability['max_channel_delta']<=1,stability
   shot(page,name+'-idle')
   if name=='desktop':
    canvas.screenshot(path=str(OUT/'desktop-model.png'))
    measured=page.evaluate('''async()=>{
      const T=await import('three'), {GLTFLoader}=await import('./vendor/three/loaders/GLTFLoader.js');const loader=new GLTFLoader(),out={};
      for(const name of ['cabinet','claw-hub','claw-finger','vault-box']){
        const response=await fetch('./assets/vault-kit/'+name+'.glb');if(!response.ok)throw Error('HTTP '+response.status);
        const data=await response.arrayBuffer(),hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',data))).map(x=>x.toString(16).padStart(2,'0')).join('');
        const gltf=await loader.parseAsync(data,'');gltf.scene.updateMatrixWorld(true);let triangles=0,meshes=0,minArea=Infinity;
        gltf.scene.traverse(o=>{if(!o.isMesh)return;meshes++;const g=o.geometry,p=g.attributes.position,idx=g.index;const count=idx?idx.count:p.count;triangles+=count/3;
          for(let i=0;i<count;i+=3){const vs=[0,1,2].map(k=>new T.Vector3().fromBufferAttribute(p,idx?idx.getX(i+k):i+k).applyMatrix4(o.matrixWorld));if(!vs.every(v=>v.toArray().every(Number.isFinite)))throw Error('nonfinite');const area=vs[1].sub(vs[0]).cross(vs[2].sub(vs[0])).length()/2;if(area<=1e-12)throw Error('degenerate '+name);minArea=Math.min(area,minArea);}
        });
        const bounds=new T.Box3().setFromObject(gltf.scene);out[name]={http:response.status,bytes:data.byteLength,sha256:hash,triangles,meshes,min:bounds.min.toArray(),max:bounds.max.toArray(),min_triangle_area:minArea};
        gltf.scene.traverse(o=>{if(o.isMesh){o.geometry.dispose();o.material.dispose();}});
      }return out;
    }''')
    source=json.loads((OUT/'source-report.json').read_text())
    for part,m in measured.items():
     assert m['triangles']==source[part]['triangles'],(part,m,source[part])
     for bound in ['min','max']:assert max(abs(a-b) for a,b in zip(m[bound],source[part][bound]))<1e-5,(part,bound)
     assert m['sha256']==hashlib.sha256((ROOT/f'docs/assets/vault-kit/{part}.glb').read_bytes()).hexdigest()
    report['models']=measured
   arm(page)
   before=state(page)
   if mobile:
    page.locator('#joystick').scroll_into_view_if_needed();r=page.locator('#joystick').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
    cdp=context.new_cdp_session(page)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+25,'y':y+20}]})
    page.wait_for_timeout(350);cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:
    page.keyboard.down('ArrowRight');page.wait_for_timeout(450);page.keyboard.up('ArrowRight')
   assert state(page)['x']>before['x']
   page.locator('#dropBtn').click();phase(page,'grab');page.wait_for_function('clawGame.state.close > .2');grab=visual(page);game=state(page)
   assert game['drops']==1
   assert all(f['scale'][0]<1 for f in grab['fingers']),grab
   if not reject:assert all(f['authored']==1 for f in grab['fingers'])
   shot(page,name+'-grab');phase(page,'carry');carry=visual(page);game=state(page)
   assert game['selected']>=0
   selected=carry['prizes'][game['selected']]
   # Same frame inspection of renderer vs state after the render callback.
   alignment=page.evaluate('''()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>{const v=claw3dHandle.visualSnapshot(),s=clawGame.state;const p=v.prizes[s.selected];r({p:p.position,target:s.prize,claw:v.claw});})))''')
   assert max(abs(alignment['p'][i]-alignment['target'][key]) for i,key in enumerate(['x','y','z']))<.03,alignment
   shot(page,name+'-carry');phase(page,'reveal');page.wait_for_timeout(800);shot(page,name+'-reveal')
   assert page.locator('#prizeCard').is_visible();assert visual(page)['prizes'][state(page)['selected']]['visible']==False
   page.locator('#againBtn').click();phase(page,'armed');assert state(page)['selected']==-1
   assert not errors,errors
   report[name]={'status':expected,'http':responses,'rejected':rejected,'errors':errors,'idle':snap,'grab':grab,'carry_alignment':alignment,'input':'CDP touch' if mobile else 'keyboard','reduced_motion_static':stability,'drop_reveal_reset':True}
   if name=='desktop':
    video=page.video;page.close();context.close();video.save_as(str(OUT/'gameplay-desktop.webm'))
   else:context.close()
  browser.close()
finally:
 server.shutdown();(OUT/'browser-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
