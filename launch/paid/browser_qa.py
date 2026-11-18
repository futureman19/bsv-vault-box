"""Bounded paid integration UI test; real provider adapter, simulated provider and chain."""
import json, subprocess, sys, time, urllib.request, socket
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[1]).resolve(); OUT.mkdir(parents=True,exist_ok=False)
report={'checks':[], 'external':[], 'page_errors':[], 'ports_closed':[]}
with sync_playwright() as pw:
    browser=pw.chromium.launch(channel='msedge',headless=True)
    try:
        for name,width,port in [('desktop',1365,8794),('mobile',390,8795),('ambiguous',390,8796)]:
            log=open(OUT/(name+'-server.txt'),'w')
            proc=subprocess.Popen(['node','launch/paid/cli.js','demo','--dir',str(OUT/(name+'-state')),'--port',str(port)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
            url=f'http://127.0.0.1:{port}'
            context=browser.new_context(viewport={'width':width,'height':900},service_workers='block',reduced_motion='reduce')
            context.route('**/*',lambda route: route.continue_() if route.request.url.startswith(url+'/') else (report['external'].append(route.request.url),route.abort()))
            page=context.new_page();page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
            try:
                for _ in range(100):
                    try:
                        urllib.request.urlopen(url,timeout=1).close();break
                    except OSError: time.sleep(.1)
                page.goto(url);expect(page.locator('#stage')).to_have_text('AVAILABLE')
                initial=page.request.get(url+'/api/state').json()
                page.get_by_role('button',name='Connect public fixture buyer').click()
                expect(page.get_by_role('button',name='Connect public fixture buyer')).to_be_disabled()
                def approve(count):
                    for _ in range(count):
                        button=page.get_by_role('button',name='Approve pending signature')
                        expect(button).to_be_enabled(timeout=30000)
                        pending=page.evaluate('paidFixture.client.pending.id')
                        button.click()
                        expect(page.locator('#wallet-controls pre')).not_to_contain_text(pending,timeout=30000)
                page.screenshot(path=str(OUT/(name+'-initial.png')),full_page=True)
                page.select_option('#mode','reject');page.locator('#next').click();approve(1)
                expect(page.locator('#wallet-controls pre')).to_contain_text('rejected');expect(page.locator('#stage')).to_have_text('AVAILABLE')
                page.select_option('#mode','ok')
                page.get_by_role('button',name='Connect public fixture buyer').click()
                expect(page.get_by_role('button',name='Connect public fixture buyer')).to_be_disabled()
                for stage in ['RESERVED','PACKED','SEALED']:
                    page.locator('#next').click()
                    if stage=='RESERVED':approve(1)
                    expect(page.locator('#stage')).to_have_text(stage,timeout=30000)
                expect(page.locator('#next')).to_be_disabled()
                for scenario in ['partial','shallow','paid']:
                    page.select_option('#scenario',scenario);page.locator('#observe').click()
                    expect(page.locator('#message')).to_have_text('Saved and verified locally.')
                    expect(page.locator('#observe')).to_be_enabled()
                    if scenario!='paid':expect(page.locator('#next')).to_be_disabled()
                expect(page.locator('#next')).to_be_enabled()
                if name=='ambiguous':
                    page.select_option('#mode','ambiguous');page.locator('#next').click()
                    expect(page.locator('#holds')).to_contain_text('AMBIGUOUS_SEND',timeout=30000)
                    before=page.request.get(url+'/api/state').json();page.reload()
                    expect(page.locator('#holds')).to_contain_text('AMBIGUOUS_SEND',timeout=30000)
                    after=page.request.get(url+'/api/state').json();assert before['pending']==after['pending']
                    expect(page.locator('#next')).to_be_disabled()
                    page.screenshot(path=str(OUT/(name+'-held.png')),full_page=True)
                    report['checks'].append('ambiguous exact signed bytes persist across reload')
                else:
                    for stage in ['TRANSFERRED','OPENED','WITHDRAWN']:
                        page.locator('#next').click()
                        if stage in ['OPENED','WITHDRAWN']:approve(3)
                        expect(page.locator('#stage')).to_have_text(stage,timeout=30000)
                        current=page.request.get(url+'/api/state').json();assert current['binding']==initial['binding'];assert all(current['provenance'].values())
                    assert page.evaluate("paidFixture.fixture.calls.filter(x=>x.method==='createSignature').length")==8
                    page.reload();expect(page.locator('#stage')).to_have_text('WITHDRAWN')
                    page.locator('summary').click()
                    with page.expect_download() as dl:page.get_by_text('Download evidence JSON',exact=True).click()
                    dest=OUT/(name+'-download.json');dl.value.save_as(dest)
                    data=json.loads(dest.read_text());assert data==page.request.get(url+'/api/evidence').json();assert data['signatureCalls']==0 # buyer signatures only in browser
                    assert page.evaluate("paidFixture.fixture.calls.filter(x=>x.method==='createSignature').length")==0
                    assert len(data['history'])==5 and data['payment']['qualified'] and not data['chainInclusion']
                    page.locator('summary').click();page.screenshot(path=str(OUT/(name+'-withdrawn.png')),full_page=True)
                    page.select_option('#scenario','excess');page.locator('#observe').click();expect(page.locator('#holds')).to_contain_text('EXCESS_PAYMENT',timeout=30000);expect(page.locator('#stage')).to_have_text('WITHDRAWN')
                    report['checks'].append(name+': reject, partial/depth gate, five transitions, immutable binding, reload, exact download, terminal excess')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert page.locator('img').evaluate('x=>x.complete&&x.naturalWidth>0')
                report['checks'].append(name+': decoded image and no overflow')
            finally:
                context.close();proc.terminate();proc.wait(timeout=15);log.close()
                with socket.socket() as s:assert s.connect_ex(('127.0.0.1',port))!=0
                report['ports_closed'].append(port)
    finally:browser.close()
assert not report['external'] and not report['page_errors']
report['result']='PASS';(OUT/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
