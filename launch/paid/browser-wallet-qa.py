"""Isolated Edge fixture UI: no installed profile, extension, funds or broadcast."""
import json, subprocess, time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT = Path(__file__).resolve().parent
proc = subprocess.Popen(['node', str(ROOT/'browser-wallet-harness-server.js')], stdout=subprocess.PIPE, text=True)
try:
    url = proc.stdout.readline().strip()
    assert url.startswith('http://127.0.0.1:')
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(service_workers='block')
        external, errors = [], []
        context.route('**/*', lambda r: r.continue_() if r.request.url.startswith(url+'/') else (external.append(r.request.url), r.abort()))
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(url)
        assert page.evaluate('walletHarness.fixture.calls.length') == 0
        page.get_by_role('button', name='Connect PUBLIC', exact=False).click()
        try:
            expect(page.get_by_role('button', name='Connect PUBLIC', exact=False)).to_be_disabled()
        except Exception:
            print(page.locator('body').inner_text(), errors)
            raise
        page.evaluate("fetch('/fixture/request', {method:'POST'})")
        approve = page.get_by_role('button', name='Approve pending signature')
        expect(approve).to_be_enabled()
        assert page.evaluate("walletHarness.fixture.calls.filter(c=>c.method==='createSignature').length") == 0
        approve.click()
        for _ in range(100):
            if page.request.get(url+'/fixture/state').json()['result']:
                break
            time.sleep(.05)
        state = page.request.get(url+'/fixture/state').json()
        assert state['result']['signature'].startswith('30'), state
        assert page.evaluate("walletHarness.fixture.calls.filter(c=>c.method==='createSignature').length") == 1
        page.get_by_role('button', name='Cancel / disconnect').click()
        for _ in range(100):
            if page.request.get(url+'/fixture/state').json()['session'] is None:
                break
            time.sleep(.05)
        assert page.request.get(url+'/fixture/state').json()['session'] is None
        assert not external and not errors, (external, errors)
        print(json.dumps({'passed': True, 'browser': 'fresh headless Edge', 'actual_wallet_js': True, 'local_sdk_der_verification': True, 'signatures': 1, 'external_requests': external, 'page_errors': errors}))
        browser.close()
finally:
    proc.terminate()
    proc.wait(timeout=10)
