"""Real Edge, file://, offline. No server or node. Run after export.js."""
import hashlib,json,pathlib,os
from playwright.sync_api import sync_playwright
HERE=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-evidence-inspector')
OUT.mkdir(parents=True,exist_ok=True)
HTML=HERE/'boxsv-evidence.html'
assert HTML.exists(), 'generated offline inspector missing'
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    for label,width,height in [('desktop',1440,1100),('mobile',390,844)]:
        context=browser.new_context(viewport={'width':width,'height':height},accept_downloads=True,offline=True,reduced_motion='reduce')
        page=context.new_page();errors=[];requests=[]
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('request',lambda request:requests.append(request.url))
        page.goto(HTML.as_uri());page.wait_for_selector('.item-card')
        assert page.title()=='BoxSV | Inspect the proof'
        assert page.locator('.item-card').count()==4
        assert page.locator('#stage-title').inner_text()=='Withdraw'
        assert '16 accepted' in page.locator('#checks').inner_text()
        assert '20 rejected' in page.locator('#checks').inner_text()
        assert page.locator('button').filter(has_text='Connect wallet').count()==0
        for stage in ['Pack','Seal','Transfer','Open','Withdraw']:
            page.get_by_role('button',name='View recorded '+stage,exact=True).click()
            assert page.locator('#stage-title').inner_text()==stage
            assert len(page.locator('#stage-tx').inner_text())==64
            page.get_by_text('Transaction & ordered outputs',exact=True).click()
            assert page.locator('#stage-details code').count()==6
            assert page.locator('#stage-details code').nth(1).inner_text().endswith(page.locator('#stage-tx').inner_text()+':0')
            assert page.locator('html').evaluate('(e)=>e.scrollWidth<=innerWidth'),stage
            page.get_by_text('Transaction & ordered outputs',exact=True).click()
        for name in ['Collectible Box','Certificate','Object one','Object two']:
            page.get_by_role('button',name='Inspect '+name,exact=True).click()
            assert page.locator('dialog').is_visible()
            assert page.locator('#item-title').inner_text()==name
            assert ':0' in page.locator('#item-origin').inner_text()
            assert '4cd43d140973d410b212f58216a3c9abaed6df35ac8a2cd3a38c7950503f1661:' in page.locator('#item-final').inner_text()
            if name=='Certificate':
                page.get_by_text('Detached signed statement',exact=True).click()
                assert 'BOX4-CERT-1' in page.locator('#certificate-json').inner_text()
                with page.expect_download() as certificate_download:
                    page.get_by_role('button',name='Download signed envelope',exact=True).click()
                certificate_path=OUT/('certificate-'+label+'.json');certificate_download.value.save_as(certificate_path)
                certificate=json.loads(certificate_path.read_text())
                assert json.loads(certificate['statement'])['protocol']=='BOX4-CERT-1'
                page.locator('dialog').evaluate('(e)=>e.scrollTop=0')
                page.screenshot(path=str(OUT/('certificate-'+label+'.png')))
            assert page.locator('dialog').evaluate('(e)=>e.scrollWidth<=e.clientWidth'), 'dialog overflow'
            page.keyboard.press('Tab')
            assert page.locator('dialog').evaluate('(e)=>e.contains(document.activeElement)')
            page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
            assert page.get_by_role('button',name='Inspect '+name,exact=True).evaluate('(e)=>e===document.activeElement')
        button=page.get_by_role('button',name='View recorded Seal',exact=True)
        button.focus();page.keyboard.press('Enter');assert page.locator('#stage-title').inner_text()=='Seal'
        page.get_by_role('button',name='View recorded Withdraw',exact=True).click()
        page.locator('#evidence-disclosure').click()
        with page.expect_download() as d:
            page.get_by_role('button',name='Download raw evidence',exact=True).click()
        target=OUT/('download-'+label+'.json');d.value.save_as(target)
        bundle=json.loads(target.read_text(encoding='utf-8'))
        assert len(bundle['manifest'])==len(bundle['files'])
        for entry in bundle['manifest']:
            raw=bundle['files'][entry['name']].encode()
            assert hashlib.sha256(raw).hexdigest()==entry['sha256'],entry['name']
            assert len(raw)==entry['bytes']
        with page.expect_download() as manifest_download:
            page.get_by_role('button',name='Download hash manifest',exact=True).click()
        manifest_path=OUT/('manifest-'+label+'.json');manifest_download.value.save_as(manifest_path)
        assert json.loads(manifest_path.read_text())==bundle['manifest']
        assert not any('cookie' in f or f.endswith('.conf') for f in bundle['files'])
        page.locator('#evidence-disclosure').click()
        assert page.locator('html').evaluate('(e)=>e.scrollWidth<=innerWidth')
        if label=='mobile':
            assert page.locator('footer span').first.evaluate('(e)=>getComputedStyle(e).display')=='block', 'mobile footer fragments must stack'
        page.evaluate('scrollTo(0,0)');page.screenshot(path=str(OUT/(label+'.png')),full_page=True)
        assert not errors,errors
        assert not [u for u in requests if not u.startswith('file:')],requests
        report.append({'viewport':label,'fileProtocol':True,'offline':True,'stages':5,'items':4,'keyboard':True,'downloadHashes':len(bundle['manifest']),'horizontalOverflow':False,'jsErrors':errors,'externalRequests':0})
        context.close()
    browser.close()
(OUT/'browser-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
