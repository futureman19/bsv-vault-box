"""Open and verify the delivered HTML in a real headed offline Edge window; leave open."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,socket,time,json,uuid,hashlib
R=Path(__file__).resolve().parent
D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-morocco-finish-v6');html=D/'morocco-finish-v6.html'
exe=next(p for p in [Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'),Path('C:/Program Files/Microsoft/Edge/Application/msedge.exe')] if p.exists())
s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close()
profile=Path('C:/Users/futur/.hermes/profiles/telegram2/cache/scratch')/('morocco-v6-edge-'+uuid.uuid4().hex[:8])
proc=subprocess.Popen([str(exe),'--remote-debugging-port='+str(port),'--user-data-dir='+str(profile),'--no-first-run','--no-default-browser-check','--allow-file-access-from-files','--window-size=1440,1080',html.as_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with sync_playwright() as pw:
 browser=None
 for i in range(40):
  try:browser=pw.chromium.connect_over_cdp('http://127.0.0.1:'+str(port));break
  except Exception:time.sleep(.3)
 assert browser is not None
 c=browser.contexts[0];c.set_offline(True);p=next((p for p in c.pages if p.url==html.as_uri()),c.new_page());errors=[];requests=[]
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda q:requests.append(q.url) if q.url.startswith(('http:','https:')) else None)
 p.goto(html.as_uri());p.wait_for_function('pilot.ready===true',timeout=30000);p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#open').click();p.wait_for_function('pilot.progress===0');p.locator('#reset').click();p.wait_for_timeout(200)
 assert not errors and not requests;assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');assert p.evaluate('pilot.asset.bytes')==(D/'morocco.glb').stat().st_size
 p.screenshot(path=str(D/'delivery-desktop-opened.png'),full_page=True)
 result={'url':p.url,'headed_real_Edge':True,'offline':True,'ready':p.evaluate('pilot.ready'),'actual_asset':p.evaluate('pilot.asset'),'open_close_reset':True,'errors':errors,'external_requests':requests,'html_sha256':hashlib.sha256(html.read_bytes()).hexdigest(),'left_open':True,'pid':proc.pid}
 for folder in [R,D]:(folder/'delivery-open-check.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
