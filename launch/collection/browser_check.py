import json,pathlib
from playwright.sync_api import sync_playwright
from consolidate import HERE,OUT
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    for mobile in [False,True]:
        context=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 1000},is_mobile=mobile,has_touch=mobile,offline=True)
        page=context.new_page();errors=[];external=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
        for filename in ['index.html','review.html']:
            page.goto((OUT/filename).as_uri());page.wait_for_timeout(600)
            assert page.locator('article').count()==201
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.locator('#hold').select_option('true');assert page.locator('article:visible').count()==73
            page.locator('#hold').select_option('');page.locator('#kind').select_option('Ocean');assert page.locator('article:visible').count()==5
            page.locator('#kind').select_option('');page.locator('#q').fill('the moon');assert page.locator('article:visible').count()==1
            page.locator('#q').fill('');page.screenshot(path=str(HERE/f'{filename}-{ "mobile" if mobile else "desktop"}.png'))
            assert not errors and not external
            results.append({'file':filename,'mobile':mobile,'coverage':201,'hold_filter':73,'ocean_filter':5,'moon_alias':True,'overflow':False,'external_requests':external,'pageerrors':errors})
        context.close()
    browser.close()
(HERE/'browser-report.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
