import json
from playwright.sync_api import sync_playwright
from consolidate import HERE,OUT
root=OUT/'recovered-final';results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    for id in ['united-states','morocco','iceland','rwanda']:
        context=browser.new_context(offline=True,viewport={'width':390,'height':844},has_touch=True,is_mobile=True,reduced_motion='reduce');page=context.new_page();errors=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
        page.goto((root/f'payloads/{id}/viewer.html').as_uri());page.locator('#open').wait_for(state='visible');page.wait_for_function("!document.querySelector('#open').disabled")
        page.locator('#open').tap();page.wait_for_function("document.querySelector('#open').textContent.toLowerCase().includes('close')",timeout=15000)
        page.screenshot(path=str(HERE/f'recovered-{id}-open.png'))
        page.locator('#reset').tap();page.wait_for_function("document.querySelector('#open').textContent.toLowerCase().includes('open')",timeout=15000)
        assert not errors and not requests;assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        results.append({'id':id,'offline':True,'touch_open_reset':True,'reduced_motion':True,'external_requests':requests,'pageerrors':errors,'scope':'recovered endpoint smoke, not complete mechanics/fallback QA'})
        context.close()
    page=browser.new_page(viewport={'width':390,'height':844});page.context.set_offline(True);page.goto((root/'index.html').as_uri());assert page.locator('article').count()==201;page.locator('#q').fill('united states');page.locator('article:visible a').first.click();assert '/united-states/viewer.html' in page.url
    browser.close()
(HERE/'recovered-browser-report.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
