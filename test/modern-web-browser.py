"""Native gallery dialog + forced closedby fallback acceptance (no wallet calls)."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, threading
from playwright.sync_api import sync_playwright, expect
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/modern-web/platform'
OUT.mkdir(parents=True, exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}'
results = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        for mobile, fallback in [(False,False),(True,False),(False,True),(True,True)]:
            context = browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 1000}, has_touch=mobile, is_mobile=mobile, reduced_motion='reduce' if mobile else 'no-preference')
            context.route('**/*', lambda r: r.continue_() if r.request.url.startswith(url) else r.abort())
            if fallback:
                context.add_init_script("delete HTMLDialogElement.prototype.closedBy")
            page = context.new_page(); errors=[]
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(url+'/gallery.html?q=moon')
            if fallback:
                # Removing the reflected property only activates the fallback. Remove
                # the native attribute too, so native light dismiss cannot mask a bug.
                page.locator('#viewer').evaluate("e=>e.removeAttribute('closedby')")
            card=page.locator('[data-id="the-moon"]'); expect(card).to_be_visible()
            card.scroll_into_view_if_needed()
            before=page.evaluate('({width:document.documentElement.clientWidth,x:document.querySelector("#grid").getBoundingClientRect().x})')
            card.tap() if mobile else card.click()
            expect(page.locator('#viewer')).to_be_visible()
            page.locator('#full-image').evaluate('(e)=>e.decode()')
            assert page.locator('#viewer').evaluate('e=>e.matches(":modal")')
            assert before==page.evaluate('({width:document.documentElement.clientWidth,x:document.querySelector("#grid").getBoundingClientRect().x})')
            for key in ['Tab']*4+['Shift+Tab']*4:
                page.keyboard.press(key)
                assert page.evaluate('document.activeElement===document.body || document.querySelector("#viewer").contains(document.activeElement)')
                page.locator('#search').evaluate('(e)=>e.focus()')
                assert not page.locator('#search').evaluate('(e)=>e===document.activeElement')
            r=page.locator('#viewer').bounding_box()
            # Padding belongs to the dialog, not the backdrop.
            page.mouse.click(r['x']+4,r['y']+4)
            expect(page.locator('#viewer')).to_be_visible()
            # A drag from inside to outside must not dismiss.
            page.mouse.move(r['x']+8,r['y']+8);page.mouse.down();page.mouse.move(2,2);page.mouse.up()
            expect(page.locator('#viewer')).to_be_visible()
            y=page.evaluate('scrollY');page.mouse.move(2,2);page.mouse.wheel(0,500);page.wait_for_timeout(250)
            scroll_delta=page.evaluate('scrollY')-y
            assert scroll_delta == 0, 'Backdrop wheel must not scroll the page in this Edge version'
            page.screenshot(path=str(OUT/f'{"mobile" if mobile else "desktop"}-{"fallback" if fallback else "native"}.png'))
            page.touchscreen.tap(2,2) if mobile else page.mouse.click(2,2)
            expect(page.locator('#viewer')).not_to_be_visible()
            expect(card).to_be_focused()
            card.click();page.keyboard.press('Escape');expect(page.locator('#viewer')).not_to_be_visible();expect(card).to_be_focused()
            card.click();page.locator('#close').click();expect(page.locator('#viewer')).not_to_be_visible();expect(card).to_be_focused()
            assert not errors, errors
            results.append({'mobile':mobile,'forcedClosedbyFallback':fallback,'pass':True,'backdropWheelScrollDelta':scroll_delta,'browser':browser.version,'errors':errors})
            context.close()
        browser.close()
finally:
    server.shutdown();server.server_close()
    (OUT/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
