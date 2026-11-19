"""Actual continuous page + browser ProtoWallet/WalletTransport + durable payment delivery."""
import json, subprocess, sys, time, urllib.request, socket
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[1]).resolve();OUT.mkdir(parents=True,exist_ok=False)
report={'checks':[],'external_requests':[],'page_errors':[],'console_errors':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True)
 try:
  for name,width,height,port in [('desktop',1365,1000,8891),('mobile',390,844,8892),('ambiguous',390,844,8893)]:
   url=f'http://127.0.0.1:{port}';log=open(OUT/f'{name}-server.txt','w')
   proc=subprocess.Popen(['node','launch/continuous/paid-cli.js','demo',str(OUT/f'{name}-state'),str(port)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
   context=None
   try:
    for _ in range(100):
     if proc.poll() is not None:raise RuntimeError('server exited')
     try:
      urllib.request.urlopen(url,timeout=1).close();break
     except OSError:time.sleep(.1)
    else:raise RuntimeError('startup timeout')
    context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',service_workers='block')
    def route(r):
     if r.request.url.startswith(url+'/'):r.continue_()
     else:report['external_requests'].append(r.request.url);r.abort()
    context.route('**/*',route)
    page=context.new_page();page.set_default_timeout(120000)
    page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    page.on('console',lambda m:report['console_errors'].append(m.text) if m.type=='error' else None)
    page.goto(url);page.locator('body[data-stage="AVAILABLE"]').wait_for()
    assert page.locator('img').evaluate('i=>i.complete&&i.naturalWidth>0')
    initial=page.request.get(url+'/api/state').json();assert initial['paidIntegration']
    assert initial['policy']['buyer']!=initial['policy']['wallet']['identityKey']
    page.locator('.faults summary').click()
    for mode in (['reject','malicious','wrong-buyer','wrong-network','disconnect'] if name=='desktop' else ['reject']):
     page.select_option('#mode',mode);page.locator('#advance').click();page.locator('#error:not([hidden])').wait_for();page.locator('#advance:not([disabled])').wait_for()
     assert page.locator('body').get_attribute('data-stage')=='AVAILABLE'
     report['checks'].append(name+': '+mode+' rejected before reservation')
    page.locator('.faults summary').click();page.screenshot(path=str(OUT/f'{name}-initial.png'),full_page=True)
    for stage in ['RESERVED','PACKED','SEALED']:
     page.locator('#advance').click();page.locator(f'body[data-stage="{stage}"]').wait_for();page.locator('#advance:not([disabled])').wait_for()
    sealed=page.request.get(url+'/api/state').json();assert sealed['delivery']['status']=='WAITING_PAYMENT'
    assert sealed['reservation']['buyerPubkey']==initial['binding']['buyerPubkey']
    if name=='ambiguous':
     page.locator('.faults summary').click();page.select_option('#mode','ambiguous')
    page.locator('#advance').click()
    if name=='ambiguous':
     page.locator('#advance').filter(has_text='Reconciliation hold').wait_for()
     before=page.request.get(url+'/api/state').json();assert 'AMBIGUOUS_SEND' in before['holds']
     page.reload();page.locator('#advance').filter(has_text='Reconciliation hold').wait_for()
     after=page.request.get(url+'/api/state').json();assert before['delivery']['prepared']==after['delivery']['prepared']
     assert page.locator('#advance').is_disabled();report['checks'].append('ambiguous: exact signed delivery bytes held across reload; no ownership promotion')
    else:
     page.locator('body[data-stage="TRANSFERRED"]').wait_for();page.locator('#advance:not([disabled])').wait_for()
     paid=page.request.get(url+'/api/state').json();assert paid['delivery']['status']=='LOCAL_ACCEPTED';assert paid['binding']==initial['binding'];assert paid['delivery']['binding']==initial['binding']
     page.locator('.controls').screenshot(path=str(OUT/f'{name}-paid.png'))
     for stage in ['OPENED','WITHDRAWN']:
      page.locator('#advance').click();page.locator(f'body[data-stage="{stage}"]').wait_for()
      if stage!='WITHDRAWN':page.locator('#advance:not([disabled])').wait_for()
     page.reload();page.locator('body[data-stage="WITHDRAWN"]').wait_for();page.locator('.evidence summary').click()
     with page.expect_download() as d:page.get_by_text('Download current evidence JSON',exact=True).click()
     dest=OUT/f'{name}-download.json';d.value.save_as(dest);s=json.loads(dest.read_text());assert s==page.request.get(url+'/api/evidence').json()
     assert s['binding']==initial['binding'];assert all(s['provenance'].values());assert len(s['history'])==5
     assert sum(a['status']=='VERIFIED' for a in s['authorizations'])==5
     assert s['realSendingEnabled'] is False and s['chainInclusion'] is False
     report['checks'].append(name+': browser BRC reservation + paid delivery + two-input covenant Open/Withdraw + exact download and reload')
    page.screenshot(path=str(OUT/f'{name}-complete.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');report['checks'].append(name+': image decoded and no horizontal overflow')
   finally:
    if context:context.close()
    proc.terminate();proc.wait(timeout=20);log.close()
    with socket.socket() as s:assert s.connect_ex(('127.0.0.1',port))!=0
 finally:browser.close()
assert not report['external_requests'];assert not report['page_errors']
report['result']='PASS';report['console_note']='Retained expected HTTP 409 errors from explicit negative signature/payment tests; not hidden.'
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
