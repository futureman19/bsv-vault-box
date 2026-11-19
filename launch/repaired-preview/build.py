"""Export immutable selected viewers; build an independently hostable review folder."""
import base64,hashlib,io,json,re,subprocess,zipfile
from collections import Counter
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from discover import ROOT,PINS,blob
REPO=ROOT.parents[1]
OUT=REPO/'preview/repaired-collection-v1'
MASTER='536af22c22f9f9edaf0fb53709e1a511184e87b4'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def unique(rows):
 assert len(rows)==len({e['id'] for e in rows})
 return {e['id']:e for e in rows}
def meta(ref,path,data):return {'commit':ref,'path':path,'bytes':len(data),'sha256':sha(data)}
def load(name):return json.loads((ROOT/'inputs'/f'{name}.json').read_bytes())
def extract(ref,path,target,expected=None):
 data=blob(ref,path)
 if expected:assert sha(data)==expected,(path,sha(data),expected)
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 return data,meta(ref,path,data)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'.gitattributes').write_text('* -text\n',encoding='utf-8')
 base=load('baseline'); entries=unique(base['entries']); ordinary=unique(load('ordinary')['entries']); structural=unique(load('structural')['records']); repairs=load('repairs')
 gallery=unique(json.loads(blob(MASTER,'docs/assets/gallery/manifest.json'))['entries'])
 assert set(entries)==set(gallery) and len(entries)==201
 assert Counter(e['category'] for e in entries.values())=={'Country':195,'Ocean':5,'Moon':1}
 decisions={}; duplicate_reviews=[]
 for lane in ['visual-a','visual-b']:
  for e in json.loads((ROOT/lane/'decisions.json').read_bytes()):
   if e['id'] in decisions:
    duplicate_reviews.append(e['id']);assert e['disposition']==decisions[e['id']]['disposition']
   decisions[e['id']]=e
 special={'united-states':('united-states-flag-v10','USA stars continue across skirt/rim, not onto the main wall; explicit requested continuation remains unmet.'),'cabo-verde':('cabo-verde-view-v2','Caldera opening remains only partly readable at mobile size.'),'saint-vincent-and-the-grenadines':('saint-vincent-and-the-grenadines-view-v2','Crater depression remains difficult to read at mobile size.')}
 substantive={'iceland':'Glacier still lacks convincing glassy depth; river and moss remain graphic. No demonstrated unsupported trim defect.','lithuania':'Pale corner blocks still differ from the requested/promotional black-corner treatment.','malta':'Linear bastion miniature does not reproduce the branching reference silhouette.','mozambique':'Channel texture offsets remain visible; geological/water finish differs from the reference.'}
 artifact_reports={}
 for key,ref,path in [('art-delivery',PINS['repairs'][0],'launch/collection-repairs/art-delivery.json'),('package-repairs',PINS['repairs'][0],'launch/collection-repairs/packages-02/report.json')]:
  data=blob(ref,path);(ROOT/'inputs'/f'{key}.json').write_bytes(data);artifact_reports[key]=json.loads(data)
 packages={}
 for p in artifact_reports['package-repairs']['packages']:
  packages[p['id']]=(PINS['repairs'][0],'launch/collection-repairs/packages-02/'+p['archive'],p['archive_sha256'])
 for p in artifact_reports['art-delivery']:
  packages[p['id']]=(PINS['repairs'][0],'launch/collection-repairs/deliveries/'+p['folder']+'-source.zip',p['source_zip_sha256'])
 for report in ['package-check.json','resume-package-check.json']:
  data=blob(PINS['structural'][0],'launch/attachment-rim-repairs/'+report);(ROOT/'inputs'/report).write_bytes(data)
  for p in json.loads(data):packages[p['id']]=(PINS['structural'][0],'launch/attachment-rim-repairs/'+p['zip'],p['zip_sha256'])
 for id,s in structural.items():
  if 'final_acceptance' in s:
   p=s['final_acceptance']['source_package'];packages[id]=(PINS['structural'][0],p['zip'].replace('\\','/'),p['zip_sha256'])
 packages['bangladesh']=(PINS['ordinary'][0],'launch/ordinary-finish-20/bangladesh-finish-v2-source.zip','260943cb81ab875cc0d469c2c56665fe439c4c667161321be1f686b166c41c64')
 result=[]
 for id,e in entries.items():
  ref,path,expected=e['viewer']['commit'],e['viewer']['path'],e['viewer']['sha256']; change='unchanged'; resolved=[]; notes='Stylized materials and miniature detail; promotional rendering is not exact model equivalence.'; disposition='preview-accepted-with-limitations'
  model=next(f for f in e['files'] if f['role']=='model')
  modelref,modelpath,modelhash=model['source']['commit'],model['source']['path'],model['sha256']
  source=next(f for f in e['files'] if f['role']=='editable-source' and not Path(f['source']['path']).name.startswith('baseline'))
  sourceref,sourcepath,sourcehash=source['source']['commit'],source['source']['path'],source['sha256']
  history={'baseline_record':e,'repair_record':next(x for x in repairs['records'] if x['id']==id)}
  if id in decisions:notes=decisions[id]['issue'];disposition=decisions[id]['disposition'];history['visual_decision']=decisions[id]
  if id in ordinary:
   history['ordinary_record']=ordinary[id];notes=ordinary[id]['remaining_visual_limitations'];resolved.append('Ordinary finish adjudicated within existing stylized design; no broad repaint requested.')
  if id=='bangladesh':
   ref=PINS['ordinary'][0];path='preview/bangladesh-finish-v2/bangladesh-finish-v2.html';expected=None;change='presentation';resolved.append('Higher internal render resolution selected; original model bytes retained.')
  if id in special:
   folder,notes=special[id];ref=PINS['repairs'][0];path=f'preview/{folder}/{folder}.html';expected=None;change='geometry' if id=='united-states' else 'camera';disposition='substantive-feature-hold'
   if id=='united-states':modelref=sourceref=ref;modelpath=f'preview/{folder}/{id}.glb';sourcepath=f'preview/{folder}/{id}.blend';modelhash=sourcehash=None;resolved.append('V10 skirt/rim stars, lid and feet treatment selected; main-wall feature NOT resolved.')
  if id in structural:
   s=structural[id];history['structural_record']=s
   if id!='iceland':
    ref=PINS['structural'][0];path=s.get('final_acceptance',{}).get('candidate',s.get('candidate',{}).get('path',f'preview/{id}-repair-v2/{id}-repair-v2.html'));expected=s.get('final_acceptance',{}).get('html_sha256',s.get('candidate',{}).get('sha256'));change='geometry+camera' if id=='panama' else 'geometry'
    modelref=sourceref=ref;modelpath=str(Path(path).parent/f'{id}.glb').replace('\\','/');sourcepath=str(Path(path).parent/f'{id}.blend').replace('\\','/');modelhash=s.get('final_acceptance',{}).get('source_export',{}).get('glb');sourcehash=s.get('final_acceptance',{}).get('source_export',{}).get('blend')
    resolved.append('Demonstrated static trim/support gaps repaired; inherited sampled collision and source/export reports retained, not rerun.')
   else:resolved.append('Suspicious projections identified as supported original geometry; no trim repair needed. Clean dependency-pinned rebuild remains unestablished.')
   notes=s.get('final_acceptance',{}).get('limitations','Small seam repair; stylized surfaces and intentional corner contrast retained.')
  if id in substantive:notes=substantive[id];disposition='substantive-feature-hold'
  if id in repairs['repaired_packages']:resolved.append('New canonical exact-byte source package supersedes the historical packaging defect; old archive record retained unchanged.')
  html,viewer=extract(ref,path,OUT/'viewers'/f'{id}.html',expected)
  assert len(html)<5000000,(id,len(html));viewer['url']=f'viewers/{id}.html';viewer['version']=Path(path).stem
  mb=blob(modelref,modelpath);sb=blob(sourceref,sourcepath)
  if modelhash:assert sha(mb)==modelhash
  if sourcehash:assert sha(sb)==sourcehash
  assert base64.b64encode(mb) in html,(id,'selected GLB not embedded')
  modelmeta=meta(modelref,modelpath,mb);sourcemeta=meta(sourceref,sourcepath,sb)
  package_meta=None
  if id in packages:
   pref,ppath,phash=packages[id];pb=blob(pref,ppath);assert sha(pb)==phash,(id,'package hash')
   with zipfile.ZipFile(io.BytesIO(pb)) as z:
    names=z.namelist();assert len(names)==len(set(names))
    matched={}
    for role,hash_,suffix in [('viewer',viewer['sha256'],'.html'),('model',modelmeta['sha256'],'.glb'),('editable_source',sourcemeta['sha256'],'.blend')]:
     candidates=[n for n in names if n.endswith(suffix)]
     matches=[n for n in candidates if sha(z.read(n))==hash_];assert matches,(id,role,'missing selected payload in new package');matched[role]=matches
   package_meta=meta(pref,ppath,pb);package_meta['selected_payloads_readback']=matched;package_meta['scope']='New archive hash and selected payload bytes verified now; full inner inventory and geometry QA reused from immutable handoff.'
  # The source poster must occur in this selected viewer; do not reuse stale gallery previews.
  matches=re.findall(rb'data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=]+)',html)
  assert matches,id
  mime,encoded=matches[0];poster=base64.b64decode(encoded);im=Image.open(io.BytesIO(poster)).convert('RGB');im.thumbnail((440,350));buf=io.BytesIO();im.save(buf,format='WEBP',quality=77);thumb=buf.getvalue()
  (OUT/'models').mkdir(exist_ok=True);(OUT/'models'/f'{id}.webp').write_bytes(thumb)
  marketing=gallery[id]['image'];promodata,promo=extract(MASTER,'docs/'+marketing['src'],OUT/'art'/f'{id}.webp',marketing['sha256']);promo['url']=f'art/{id}.webp'
  tiny=Image.open(io.BytesIO(promodata)).convert('RGB');tiny.thumbnail((320,260));buf=io.BytesIO();tiny.save(buf,format='WEBP',quality=65);promo['inline']='data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()
  poster_meta={'url':f'models/{id}.webp','sha256':sha(thumb),'bytes':len(thumb),'embedded_poster_sha256':sha(poster),'selected_viewer_sha256':viewer['sha256'],'transform':'Pillow thumbnail within 440x350, RGB WebP quality 77','inline':'data:image/webp;base64,'+base64.b64encode(thumb).decode()}
  # Preserve historical records in a separate immutable evidence envelope, not in the UI payload.
  (ROOT/'history').mkdir(exist_ok=True);dump(ROOT/'history'/f'{id}.json',history)
  result.append({'id':id,'name':e['name'],'category':e['category'],'viewer':viewer,'model':modelmeta,'editable_source':sourcemeta,'marketing':promo,'poster':poster_meta,'change':change,'disposition':disposition,'issue':notes,'resolved':resolved,'final_user_approved':e['final_user_approved'],'launch_ready':False,'history':f'../../launch/repaired-preview/history/{id}.json','current_source_package':package_meta,'packaging_status':'superseded-by-verified-new-envelope' if package_meta else 'inherited-package-evidence-not-rerun','historical_archive_holds':e.get('package_missing_gates',[])})
  print(id,viewer['version'],len(html),flush=True)
 assert len(result)==201
 payload={'schema':'boxsv-repaired-preview-v1','production_base':MASTER,'inputs':PINS,'counts':dict(Counter(e['category'] for e in result)),'entries':result,'minted':False,'sale_active':False,'status':'Collection preview; not launch approval','duplicate_visual_reviews_reconciled':duplicate_reviews}
 # Portable manifest uses no machine-local paths or dangling history link.
 for e in result:e['history']='Evidence in source branch: launch/repaired-preview/history/'+e['id']+'.json'
 manifest=json.loads(json.dumps(payload))
 for e in manifest['entries']:e['poster'].pop('inline');e['marketing'].pop('inline')
 dump(OUT/'manifest.json',manifest)
 template=(ROOT/'template.html').read_text(encoding='utf-8')
 for offline,name in [(False,'index.html'),(True,'review.html')]:
  rows=json.loads(json.dumps(result))
  for e in rows:
   if offline:e['poster']['url']=e['poster']['inline'];e['marketing']['url']=e['marketing']['inline']
   e['poster'].pop('inline');e['marketing'].pop('inline')
  page=template.replace('__OFFLINE__',json.dumps(offline)).replace('__DATA__',json.dumps(rows,ensure_ascii=False).replace('</','<\\/'))
  (OUT/name).write_text(page,encoding='utf-8')
 dump(ROOT/'build-report.json',{'coverage':payload['counts'],'changed':{e['id']:e['change'] for e in result if e['change']!='unchanged'},'dispositions':dict(Counter(e['disposition'] for e in result)),'standalone_bytes':(OUT/'review.html').stat().st_size,'max_viewer_bytes':max(e['viewer']['bytes'] for e in result),'input_hashes':{p.name:sha(p.read_bytes()) for p in (ROOT/'inputs').iterdir()},'duplicate_visual_reviews_reconciled':duplicate_reviews})
 # Actual-model / marketing contact sheets for bounded parent inspection.
 ids=list(dict.fromkeys(list(structural)+list(ordinary)+list(special)))
 for start in range(0,len(ids),6):
  group=ids[start:start+6];sheet=Image.new('RGB',(1000,len(group)*250),(18,22,27));draw=ImageDraw.Draw(sheet)
  for n,id in enumerate(group):
   draw.text((10,n*250+5),id+' | selected model / existing promotional art',fill='white')
   for col,folder in enumerate(['models','art']):
    im=Image.open(OUT/folder/f'{id}.webp').convert('RGB');im.thumbnail((480,220));sheet.paste(im,(col*500+(500-im.width)//2,n*250+25))
  sheet.save(ROOT/f'current-comparison-{start//6}.jpg',quality=88)
if __name__=='__main__':main()
