"""Verify the shipped report offline; not a collectible runtime test."""
import json,pathlib,hashlib
from playwright.sync_api import sync_playwright
R=pathlib.Path(__file__).resolve().parent
out=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(channel='msedge',headless=True)
    for width,height in [(1440,1080),(390,844)]:
        c=b.new_context(offline=True,viewport={'width':width,'height':height})
        p=c.new_page(); errors=[]; requests=[]
        p.on('pageerror',lambda e:errors.append(str(e)))
        p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('https:','http:')) else None)
        p.goto((R/'review.html').as_uri())
        assert p.locator('article').count()==25
        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert p.locator('img').evaluate_all('(xs)=>xs.length===25&&xs.every(x=>x.complete&&x.naturalWidth>0)')
        assert not errors and not requests
        out.append({'viewport':[width,height],'articles':25,'images':25,'no_overflow':True,'external_requests':requests,'errors':errors,'result':'pass'})
        c.close()
    b.close()
(R/'report-browser-results.json').write_text(json.dumps({'html_sha256':hashlib.sha256((R/'review.html').read_bytes()).hexdigest(),'cases':out},indent=2)+'\n')
print('PASS two offline report viewports, 25 images/articles each')
