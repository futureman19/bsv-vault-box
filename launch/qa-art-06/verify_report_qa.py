import pathlib,json
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
out=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 for w,h in [(1440,1080),(390,844)]:
  c=b.new_context(offline=True,viewport={'width':w,'height':h});page=c.new_page();errors=[];requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
  page.goto((R/'review.html').as_uri());assert page.locator('article').count()==25
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert page.evaluate('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
  assert not errors and not requests
  out.append({'viewport':[w,h],'articles':25,'images_loaded':25,'overflow':False,'page_errors':errors,'external_requests':requests});c.close()
 b.close()
(R/'report-browser-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS two offline report viewports')
