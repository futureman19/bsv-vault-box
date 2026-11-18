"""Bounded local web acceptance; no chain, signing or external services."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, threading
from playwright.sync_api import sync_playwright, expect
ROOT = Path(__file__).resolve().parents[1]
import os
OUT = ROOT / os.environ.get('BOXSV_EVIDENCE_DIR', 'evidence/launch-web/interaction')
OUT.mkdir(parents=True, exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}'
checks = []
result = 'FAIL'
failure = None
def passed(name):
    checks.append(name)
    print('PASS', name, flush=True)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width':390,'height':844}, reduced_motion='reduce')
        context.route('**/*', lambda r: r.continue_() if r.request.url.startswith(url) else r.abort())
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(url+'/gallery.html?q=ocean&category=Ocean')
        expect(page.locator('.design:visible')).to_have_count(5)
        page.locator('[data-id="arctic-ocean"]').click()
        page.reload()
        expect(page.locator('#viewer')).to_be_visible()
        expect(page.locator('#image-title')).to_have_text('Arctic Ocean')
        page.keyboard.press('Escape')
        expect(page.locator('.design:visible')).to_have_count(5)
        expect(page.locator('#search')).to_have_value('ocean')
        page.wait_for_function("location.hash === ''")
        passed('shareable combined search/category and selected design survive reload')
        # Full-image network failure retains provenance, exposes recovery and recovers.
        page.route('**/arctic-ocean.webp', lambda r: r.abort())
        page.goto(url+'/gallery.html?q=ocean&category=Ocean')
        page.locator('[data-id="arctic-ocean"]').click()
        expect(page.locator('#image-load')).to_contain_text('Image unavailable')
        expect(page.locator('#image-note')).to_contain_text('not a model screenshot')
        page.screenshot(path=str(OUT/'image-failure-mobile.png'))
        page.keyboard.press('Escape')
        page.unroute('**/arctic-ocean.webp')
        page.locator('[data-id="arctic-ocean"]').click()
        page.locator('#full-image').evaluate('(e)=>e.decode()')
        expect(page.locator('#image-load')).to_have_text('')
        passed('full-image failure preserves disclosure and reopening retries successfully')
        page.route('**/china-thumb.webp', lambda r: r.abort())
        page.goto(url+'/gallery.html?q=china')
        expect(page.locator('[data-id="china"]')).to_have_class('design art image-unavailable')
        page.locator('[data-id="china"]').click()
        page.locator('#full-image').evaluate('(e)=>e.decode()')
        passed('thumbnail failure remains named, accessible and opens available full image')
        page.route('**/manifest.json', lambda r: r.fulfill(status=503,body='unavailable'))
        page.goto(url+'/gallery.html')
        expect(page.locator('#load-retry')).to_be_visible()
        page.unroute('**/manifest.json')
        page.locator('#load-retry').click()
        expect(page.locator('.design')).to_have_count(201)
        passed('manifest failure has working retry')
        page.unroute('**/china-thumb.webp')
        # Initial load must not fetch full art or interactive collection viewers.
        loaded=[]
        page.on('request', lambda r: loaded.append(r.url))
        page.goto(url+'/gallery.html')
        expect(page.locator('.design')).to_have_count(201)
        page.wait_for_timeout(500)
        art=[u for u in loaded if '/assets/gallery/' in u and u.endswith('.webp')]
        assert art and all('-thumb.webp' in u for u in art)
        assert len(art)<201
        assert not any('.glb' in u for u in loaded)
        passed(f'lazy initial mobile load: {len(art)} thumbnails; no full art or model payloads')
        for motion, surface in [('reduce','box-demo.html'),('no-preference','box-demo.html'),('reduce','index.html'),('no-preference','index.html')]:
            page.emulate_media(reduced_motion=motion)
            page.goto(url+'/'+surface)
            box=page.locator('box-inspector') if surface=='index.html' else page.locator('body')
            def b(id): return box.locator('#'+id)
            def settled(phase):
                expect(b('stage')).to_have_attribute('data-phase',phase)
                expect(b('stage')).not_to_have_attribute('aria-busy','true')
            b('inspect').focus();page.keyboard.press('Enter')
            expect(b('open')).to_be_focused()
            page.keyboard.press('Escape');expect(b('inspect')).to_be_focused()
            for cycle in [1,2]:
                b('inspect').click();b('transfer').click();settled('sealed')
                assert b('sealLabel').inner_text()==f'SEAL #{cycle} · INTACT'
                b('inspect').click()
                if cycle==2: expect(b('sealCopy')).to_contain_text('earlier seal')
                b('open').click();settled('opened')
                expect(b('itemDescription')).to_contain_text('still inside')
                expect(b('itemDescription')).to_contain_text('Star collectible' if cycle==1 else 'Blue constellation')
                if cycle==1:
                    page.screenshot(path=str(OUT/f'box-open-{surface}-{motion}.png'))
                b('withdraw').click();settled('empty')
                assert b('lid').evaluate('(e)=>getComputedStyle(e).transform')!='none'
                b('repack').click();settled('sealed')
                assert b('sealLabel').inner_text()==f'SEAL #{cycle+1} · INTACT'
            history=b('history').text_content()
            assert 'Seal #1 · Star collectible · broken by Bob' in history
            assert 'Seal #2 · Blue constellation collectible · broken by Alice' in history
            assert 'Seal #3 · Star collectible · intact' in history
            b('inspect').click();b('open').click();b('reset').click()
            page.wait_for_timeout(2200);settled('sealed')
            assert b('history').locator('li').count()==1
            assert b('sealLabel').inner_text()=='SEAL #1 · INTACT'
            passed(f'{surface}/{motion}: keyboard/focus, transfer, two reuse cycles, contents/history, persistent lid, interrupted reset')
        for width in [320,390,768,1440]:
            page.set_viewport_size({'width':width,'height':844})
            page.goto(url+'/box-demo.html')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.locator('#inspect').click()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.screenshot(path=str(OUT/f'box-inspect-{width}.png'))
        passed('standalone Box no overflow at 320/390/768/1440')
        assert not errors, errors
        browser.close()
        result = 'PASS'
except Exception as error:
    failure = str(error)
    raise
finally:
    server.shutdown()
    (OUT/'report.json').write_text(json.dumps({'result':result,'failure':failure,'checks':checks,'count':len(checks),'scope':'Local Edge; viewport emulation, no physical phone or chain proof'},indent=2)+'\n')
