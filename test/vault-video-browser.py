"""Verify the actual recorded WebM decodes and plays to its end in Chrome."""
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import pathlib,threading,json
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/vault-assets'
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(channel='chrome',headless=False);page=b.new_page(viewport={'width':1440,'height':1000})
  page.goto(f'http://127.0.0.1:{server.server_port}/evidence/vault-assets/gameplay-desktop.webm')
  result=page.evaluate('''async()=>{const v=document.querySelector('video');v.muted=true;v.currentTime=0;
   await new Promise((resolve,reject)=>{v.addEventListener('ended',resolve,{once:true});v.addEventListener('error',reject,{once:true});v.play().catch(reject);});
   const q=v.getVideoPlaybackQuality();return {width:v.videoWidth,height:v.videoHeight,duration:v.duration,ended:v.ended,totalFrames:q.totalVideoFrames,droppedFrames:q.droppedVideoFrames,error:v.error};}''')
  assert result['ended'] and result['width']==1440 and result['height']==1000 and result['duration']>8 and result['totalFrames']>200 and not result['error']
  (OUT/'video-report.json').write_text(json.dumps(result,indent=2)+'\n');print(result);b.close()
finally:server.shutdown()
