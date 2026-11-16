"""Local HTTP + Chromium acceptance. Requires Pillow and Python Playwright.
python scripts/test-gallery.py --review PATH --output PATH
"""
import argparse
from collections import Counter
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--review', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT / 'docs/assets/gallery/manifest.json').read_text(encoding='utf-8'))
source = json.loads((args.review / 'manifest.json').read_text(encoding='utf-8'))
assert {(e['id'], e['name'], e['category']) for e in manifest['entries']} == {(e['id'], e['name'], e['category']) for e in source['entries']}
assert len(manifest['entries']) == len({e['id'] for e in manifest['entries']}) == 201
assert Counter(e['imageType'] for e in manifest['entries']) == {'Promotional art': 201}
assert Counter(e['category'] for e in manifest['entries']) == {'Country': 195, 'Ocean': 5, 'Moon': 1}
for entry in manifest['entries']:
    for kind in ('image', 'thumbnail'):
        meta = entry[kind]
        path = ROOT / 'docs' / meta['src']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == meta['sha256']
        with Image.open(path) as image:
            assert image.size == (meta['width'], meta['height'])
            image.verify()
print('PASS exact source roster: 201 unique designs / 195 countries / 5 oceans / 1 Moon; 402 image hashes and dimensions')
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT / 'docs')))
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f'http://127.0.0.1:{server.server_port}'
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: errors.append(f'{response.status} {response.url}') if response.status >= 400 else None)
    page.goto(url + '/gallery.html')
    page.wait_for_function("document.querySelector('#status').textContent === '201 of 201 designs'")
    assert page.locator('.design').count() == 201
    assert page.locator('.design.art').count() == 201
    assert 'All 201 designs' in page.locator('.disclosure').inner_text()
    assert 'Illustrated detail can differ' in page.locator('.disclosure').inner_text()
    # Decode every published full image and thumbnail through the browser, not just disk checks.
    loaded = page.evaluate('''async () => {
      const {entries} = await (await fetch('assets/gallery/manifest.json')).json();
      let count = 0;
      for (const e of entries) for (const kind of ['thumbnail','image']) {
        const image = new Image(); image.src = e[kind].src;
        try { await image.decode(); } catch (error) { throw new Error(`${e.id}/${kind}: ${error}`); }
        if (!image.naturalWidth) throw new Error(e.id); count++;
      }
      return count;
    }''')
    assert loaded == 402
    print('PASS browser decoded all 402 published images')
    for category, count in [('Country', 195), ('Ocean', 5), ('Moon', 1), ('All', 201)]:
        page.locator(f'[data-category="{category}"]').click()
        assert page.locator('.design:visible').count() == count
    for query, expected in [('iceland', 'iceland'), ('JAPAN', 'japan'), ('the moon', 'the-moon'), ('moon', 'the-moon'), ('the-moon', 'the-moon'), ('cote d ivoire', 'cote-d-ivoire')]:
        page.locator('#search').fill(query)
        assert page.locator('.design:visible').count() == 1
        assert page.locator('.design:visible').get_attribute('data-id') == expected
    page.locator('[data-category="Country"]').click()
    assert page.locator('.design:visible').count() == 1  # Côte d’Ivoire
    page.locator('#search').fill('moon')
    assert page.locator('.design:visible').count() == 0
    page.locator('#reset').click()
    page.locator('#search').fill('not-a-design-xyz')
    assert page.locator('#empty').is_visible()
    page.locator('#reset').click()
    print('PASS categories, combined filters, normalized search, Moon aliases, empty/reset')
    # Keyboard entry, native focus containment, escape and focus restoration.
    card = page.locator('[data-id="afghanistan"]')
    card.focus(); page.keyboard.press('Enter')
    assert page.locator('#viewer').is_visible()
    assert page.locator('#close').evaluate('(e) => e === document.activeElement')
    for key in ['Tab', 'Shift+Tab']:
        page.keyboard.press(key)
        assert page.evaluate("document.querySelector('#viewer').contains(document.activeElement)")
    page.keyboard.press('Escape')
    assert not page.locator('#viewer').is_visible()
    assert card.evaluate('(e) => e === document.activeElement')
    card.click(); page.locator('#close').click()
    assert not page.locator('#viewer').is_visible()
    card.click(); page.mouse.click(2, 2)
    assert not page.locator('#viewer').is_visible()
    print('PASS dialog Enter, Tab/Shift+Tab containment, Escape, close button, backdrop, focus restoration')
    for width in [1440, 1024, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 900})
        page.evaluate('scrollTo(0,0)')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        assert page.locator('.design img').first.evaluate('(e) => Math.abs(e.getBoundingClientRect().width - e.getBoundingClientRect().height) < 1'), width
        if width in [1440, 390]:
            page.screenshot(path=str(args.output / f'gallery-{width}.png'))
            page.locator('#grid').scroll_into_view_if_needed()
            page.locator('.design img').first.evaluate('(e) => e.decode()')
            page.screenshot(path=str(args.output / f'cards-{width}.png'))
        page.locator('#search').fill('moon')
        page.locator('[data-id="the-moon"]').click()
        page.locator('#full-image').evaluate('(e) => e.decode()')
        assert page.locator('#viewer').evaluate('(e) => e.scrollWidth <= e.clientWidth')
        if width in [1440, 390]: page.screenshot(path=str(args.output / f'dialog-{width}.png'))
        page.keyboard.press('Escape')
        page.locator('#search').fill('')
    print('PASS no overflow at 1440, 1024, 768, 390, 320; desktop/mobile screenshots')
    featured = [('china', 'China'), ('canada', 'Canada'), ('united-states', 'United States'), ('egypt', 'Egypt'), ('the-moon', 'Moon'), ('iceland', 'Iceland')]
    for width in [1440, 1024, 768, 390, 320]:
        page.set_viewport_size({'width': width, 'height': 900})
        page.goto(url + '/index.html')
        assert page.locator('nav a[href="gallery.html"]').count() == 1
        assert page.locator('#collection a[href="gallery.html"]').count() == 1
        assert 'Six worlds to start' in page.locator('#collection').inner_text()
        assert page.locator('.showcase a').evaluate_all('(links) => links.map(a => a.getAttribute("href"))') == ['gallery.html#' + slug for slug, _ in featured]
        assert page.locator('.showcase img').evaluate_all('(images) => images.map(image => image.getAttribute("src"))') == [next(e for e in manifest['entries'] if e['id'] == slug)['thumbnail']['src'] for slug, _ in featured]
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.screenshot(path=str(args.output / f'homepage-{width}.png'))
        page.locator('#collection').scroll_into_view_if_needed()
        page.locator('.showcase img').evaluate_all('(images) => Promise.all(images.map(image => image.decode()))')
        page.locator('#collection').screenshot(path=str(args.output / f'showcase-{width}.png'))
        if width in [1440, 390]:
            for slug, name in featured:
                page.locator(f'.showcase a[href="gallery.html#{slug}"]').click()
                page.wait_for_selector('#viewer[open]')
                assert page.locator('#image-title').inner_text() == name
                expected = next(e for e in manifest['entries'] if e['id'] == slug)
                assert page.locator('#full-image').get_attribute('src') == expected['image']['src']
                page.locator('#full-image').evaluate('(e) => e.decode()')
                assert page.locator('#viewer').evaluate('(e) => e.scrollWidth <= e.clientWidth')
                assert page.locator('#close').evaluate('(e) => e === document.activeElement')
                if slug == 'iceland':
                    page.screenshot(path=str(args.output / f'iceland-dialog-{width}.png'))
                if slug == 'united-states':
                    assert 'model is unchanged' in page.locator('#image-note').inner_text()
                    page.screenshot(path=str(args.output / f'usa-dialog-{width}.png'))
                page.keyboard.press('Escape')
                page.wait_for_function('(slug) => document.activeElement?.dataset.id === slug && !document.querySelector("#viewer").open', arg=slug)
                assert page.evaluate('location.hash') == ''
                page.go_back()
                page.wait_for_selector('.showcase')
        page.locator('nav a[href="gallery.html"]').click()
        page.wait_for_function("document.querySelector('#status').textContent === '201 of 201 designs'")
    page.goto(url + '/gallery.html#unknown-artwork')
    page.wait_for_function("document.querySelector('#status').textContent === '201 of 201 designs'")
    assert not page.locator('#viewer').is_visible()
    page.locator('#search').fill('egypt')
    page.evaluate("location.hash = 'china'")
    page.wait_for_selector('#viewer[open]')
    assert page.locator('#image-title').inner_text() == 'China'
    page.keyboard.press('Escape')
    page.wait_for_function('document.activeElement?.dataset.id === "china" && !document.querySelector("#viewer").open')
    print('PASS six ordered showcase links and thumbnails, exact dialog artwork, deep-link focus/Escape, invalid hash, hashchange with filters')
    print('PASS homepage links, homepage mobile/desktop overflow and gallery navigation')
    assert not errors, errors
    browser.close()
server.shutdown()
report = {'result': 'PASS', 'designs': 201, 'imagesDecoded': loaded, 'browserErrors': errors, 'screenshots': sorted(p.name for p in args.output.glob('*.png'))}
(args.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
