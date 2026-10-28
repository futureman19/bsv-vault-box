"""Headed, local static-site presentation checks; no payments or chain writes."""
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import pathlib, threading, json, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / os.environ.get('BOXSV_EVIDENCE_DIR', 'evidence/arcade-polish')
OUT.mkdir(parents=True, exist_ok=True)
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(ROOT / 'docs')))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}/'
report = {}
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=False)
        for name, width, height in [('desktop',1440,1000), ('mobile',390,844), ('narrow',320,740), ('tablet',768,1024)]:
            page = browser.new_page(viewport={'width':width,'height':height}, reduced_motion='reduce')
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.goto(url)
            page.wait_for_function('!!window.claw3dHandle')
            page.wait_for_function("claw3dHandle.assets.status !== 'loading'")
            page.wait_for_timeout(400)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), name
            canvas = page.locator('.claw3d-canvas')
            canvas.scroll_into_view_if_needed()
            page.wait_for_timeout(200)  # settle viewport scrolling before pixel comparison
            # Compare backing-store pixels, not fractional CSS clip boundaries after scrolling.
            snapshot = "el=>new Promise(resolve=>requestAnimationFrame(()=>resolve(el.toDataURL())))"
            frozen = canvas.evaluate(snapshot)
            page.wait_for_timeout(300)
            assert len(frozen) > 10000, 'nonempty canvas pixels'
            assert frozen == canvas.evaluate(snapshot), 'reduced-motion idle must be static'
            page.emulate_media(reduced_motion='no-preference')
            page.wait_for_timeout(400)
            assert frozen != canvas.evaluate(snapshot), 'ordinary idle motion remains active'
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_timeout(100)
            page.screenshot(path=str(OUT / f'{name}.png'), full_page=True)
            page.locator('#playBtn').focus()
            assert page.locator('#playBtn').evaluate("el=>getComputedStyle(el).outlineStyle") != 'none'
            page.keyboard.press('Enter')
            assert page.locator('#walletModal').is_visible()
            page.locator('#optCancel').click()
            assert page.evaluate("clawGame.state.phase === 'idle'")
            assert not errors, errors
            landing_errors = list(errors)
            page.locator('.proof-link').click()
            assert page.url.endswith('/check.html')
            assert page.locator('h1').is_visible()
            page.wait_for_timeout(300)
            report[name] = {'overflow':False,'reduced_motion_static':True,'keyboard_play_cancel':True,'checker_navigation':True,'landing_errors':landing_errors,'checker_console':list(errors)}
            page.close()
        browser.close()
        browser = p.chromium.launch(channel='chrome', headless=False, args=['--disable-webgl'])
        page = browser.new_page(viewport={'width':390,'height':844}, reduced_motion='reduce')
        page.goto(url)
        page.wait_for_timeout(600)
        assert page.locator('#cabinet').is_visible()
        assert page.locator('.claw3d-canvas').count() == 0
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.screenshot(path=str(OUT / 'fallback.png'), full_page=True)
        report['webgl_disabled'] = 'CSS cabinet visible, no overflow'
        browser.close()
finally:
    server.shutdown()
    (OUT / 'visual-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
