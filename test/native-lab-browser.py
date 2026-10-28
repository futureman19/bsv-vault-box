"""Local native-token research lab. No production URL or funded wallet."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import subprocess, json, time, urllib.request
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'evidence/native-custody'; OUT.mkdir(parents=True, exist_ok=True)
p = subprocess.Popen(['node', 'scripts/native-lab.js'], cwd=ROOT/'vault', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
try:
 for _ in range(80):
  try:
   urllib.request.urlopen('http://127.0.0.1:4318/api/state'); break
  except OSError: time.sleep(.1)
 else: raise AssertionError('lab did not start')
 with sync_playwright() as pw:
  browser = pw.chromium.launch(channel='chrome', headless=True)
  page = browser.new_page(viewport={'width':1200,'height':900}); errors=[]
  page.on('pageerror', lambda e: errors.append(str(e)))
  page.goto('http://127.0.0.1:4318')
  page.wait_for_function("document.querySelector('#phase').textContent==='FREE'")
  assert page.locator('#deposit').is_disabled()
  for action, phase in [('pack','PACKED'),('remove','FREE'),('pack','PACKED'),('seal','SEALED'),('transfer','SEALED')]:
   page.locator('[data-action='+action+']').click()
   page.wait_for_function('(p)=>document.querySelector("#phase").textContent===p && !document.querySelector("#busy").textContent', arg=phase)
  page.locator('#signer').select_option('alice')
  page.locator('[data-action=open]').click()
  page.wait_for_function("document.querySelector('#result').textContent.includes('REJECTED')")
  page.locator('#signer').select_option('bob')
  page.locator('[data-action=open]').click()
  page.wait_for_function("document.querySelector('#phase').textContent==='OPENED'")
  page.locator('[data-action=withdraw]').click()
  page.wait_for_function("document.querySelector('#phase').textContent==='WITHDRAWN'")
  page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
  controls=page.locator('button').evaluate_all('(es)=>es.map(e=>({text:e.textContent,disabled:e.disabled,x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,parent:e.parentElement.className}))')
  page.set_viewport_size({'width':390,'height':844})
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
  state=page.request.get('http://127.0.0.1:4318/api/state').json()
  assert state['verified']['valid'] and state['verified']['state']['phase']==4
  assert not errors, errors
  (OUT/'browser.json').write_text(json.dumps({'state':state,'errors':errors,'controls':controls},indent=2))
  print('PASS browser: pack/remove/seal/transfer, old-owner rejection, open/withdraw, desktop/mobile, deposits disabled')
  browser.close()
finally:
 p.terminate(); p.wait(timeout=10)
