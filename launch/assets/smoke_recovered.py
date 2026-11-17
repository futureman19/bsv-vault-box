"""Offline smoke of recovered bytes, not renewed collection art acceptance."""
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parent
inventory = json.loads((ROOT / 'recovered-final/recovery-inventory.json').read_bytes())
results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge', headless=True, args=['--allow-file-access-from-files'])
    for slug in ('iceland', 'morocco', 'rwanda', 'united-states'):
        row = next(r for r in inventory if r['path'].startswith(slug + '/viewer-'))
        path = ROOT / 'recovered-final' / row['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        context = browser.new_context(offline=True, viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        page = context.new_page()
        errors, requests = [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: requests.append(r.url) if r.url.startswith(('http:', 'https:')) else None)
        page.goto(path.as_uri())
        page.wait_for_function('window.pilot?.ready===true', timeout=30000)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        page.screenshot(path=str(ROOT / (slug + '-recovered.png')))
        page.locator('#open').tap()
        page.wait_for_function('pilot.progress===1')
        page.locator('#open').tap()
        page.wait_for_function('pilot.progress===0')
        page.locator('#reset').tap()
        assert not errors and not requests
        results.append({'slug': slug, 'sha256': row['sha256'], 'offline_mobile_open_close_reset': True, 'page_errors': errors, 'external_requests': requests})
        context.close()
    browser.close()
(ROOT / 'recovered-browser-report.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
