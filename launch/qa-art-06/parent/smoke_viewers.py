"""Bounded pilot-interface smoke on unchanged delivered files; not full model acceptance."""
import argparse, hashlib, json, pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser(); parser.add_argument('--ids',nargs='+',default=['afghanistan','arctic-ocean','iceland','japan','morocco','the-moon','united-states']); args=parser.parse_args()
ledger=json.loads((ROOT/'parent-ledger.json').read_text(encoding='utf-8')); entries={e['id']:e for e in ledger['entries']}
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
    for slug in args.ids:
        e=entries[slug]; path=pathlib.Path(e['delivered_viewer']['path']); assert hashlib.sha256(path.read_bytes()).hexdigest()==e['viewer']['sha256']
        dest=ROOT/'smoke'/slug; dest.mkdir(parents=True,exist_ok=True)
        for mobile,width,height in [(False,1440,1080),(True,390,844)]:
            context=browser.new_context(offline=True,viewport={'width':width,'height':height},is_mobile=mobile,has_touch=mobile,device_scale_factor=1)
            page=context.new_page(); errors=[]; requests=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.on('request',lambda r: requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
            row={'id':slug,'mode':'mobile' if mobile else 'desktop','sha256':e['viewer']['sha256'],'scope':'pilot smoke only'}
            try:
                page.goto(path.as_uri()); page.wait_for_function('window.pilot?.ready===true',timeout=30000)
                row['asset']=page.evaluate('pilot.asset')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path=str(dest/(row['mode']+'-closed.png')))
                def press(s):
                    page.locator(s).tap() if mobile else page.locator(s).click()
                start=page.evaluate('pilot.rotation'); b=page.locator('canvas').bounding_box(); x=b['x']+b['width']*.5; y=b['y']+b['height']*.5
                if mobile:
                    c=context.new_cdp_session(page); c.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]}); c.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+75,'y':y+10}]}); c.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
                else:
                    page.mouse.move(x,y); page.mouse.down(); page.mouse.move(x+130,y+20,steps=8); page.mouse.up()
                page.wait_for_function('(s)=>Math.abs(pilot.rotation-s)>.1',arg=start)
                press('#reset'); page.wait_for_function('(s)=>Math.abs(pilot.rotation-s)<1e-6',arg=start)
                press('#open'); page.wait_for_function('pilot.progress===1'); page.screenshot(path=str(dest/(row['mode']+'-open.png')))
                press('#open'); page.wait_for_function('pilot.progress===0')
                press('#open'); page.wait_for_function('pilot.progress>0 && pilot.progress<1'); press('#reset'); page.wait_for_function('pilot.progress===0')
                page.emulate_media(reduced_motion='reduce'); press('#open'); page.wait_for_function('pilot.progress===1'); press('#reset'); page.wait_for_function('pilot.progress===0')
                assert not requests and not errors
                row.update(result='pass',drag=True,open_close=True,interrupted_reset=True,reduced_motion_endpoints=True,no_overflow=True,external_requests=requests,page_errors=errors)
            except Exception as exc:
                row.update(result='fail',error=str(exc),external_requests=requests,page_errors=errors)
            finally: context.close()
            results.append(row); (ROOT/'smoke-results.json').write_text(json.dumps(results,indent=2)+'\n'); print(slug,row['mode'],row['result'],flush=True)
    browser.close()
assert all(r['result']=='pass' for r in results)
