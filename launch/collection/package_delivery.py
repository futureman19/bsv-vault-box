"""Build twice identically, recover all files offline, read back every role."""
import hashlib,json,pathlib,shutil,socket,subprocess,zipfile
from unittest.mock import patch
from consolidate import HERE,OUT,sha,enc,save
import check_package

def create(target,files):
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
        for name in files:
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.external_attr=0o100644<<16
            z.writestr(info,(OUT/name).read_bytes())
    with target.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    for name in ['check_package.py','README.md']:
        shutil.copyfile(HERE/name,OUT/name)
    for p in sorted((HERE/'inputs').glob('*.json')):save(OUT/'reviews'/p.name,p.read_bytes())
    save(OUT/'candidate-manifest.json',(HERE/'upstream/candidate-manifest.json').read_bytes())
    names=['index.html','review.html','ledger.json','payload-inventory.json','check_package.py','README.md','candidate-manifest.json']
    names += [p.relative_to(OUT).as_posix() for folder in ['boards','payloads','reviews'] for p in (OUT/folder).rglob('*') if p.is_file()]
    names=sorted(names)
    inventory=[{'path':n,'bytes':(OUT/n).stat().st_size,'sha256':sha((OUT/n).read_bytes())} for n in names]
    save(OUT/'inventory.json',enc(inventory));save(HERE/'delivery-inventory.json',enc(inventory));expected=sha(enc(inventory));names=sorted(names+['inventory.json'])
    full=OUT/'boxsv-201-reviewed-candidates.zip';digest=create(full,names)
    second=OUT/'determinism-check.zip';other=create(second,names);assert other==digest;second.unlink()
    save(HERE/'determinism-report.json',enc({'sha256':digest,'second_sha256':other,'identical':True}))
    dest=OUT/'recovered-final'
    with patch.object(socket,'socket',side_effect=AssertionError('network prohibited')),patch.object(subprocess,'Popen',side_effect=AssertionError('subprocess prohibited')):
        result=check_package.verify(full,expected,dest)
    refs=json.loads((OUT/'payload-inventory.json').read_bytes())
    with zipfile.ZipFile(full) as z:
        for r in refs:
            assert sha(z.read(r['path']))==r['sha256'];assert sha((dest/r['path']).read_bytes())==r['sha256']
    report={'archive':str(full),'archive_bytes':full.stat().st_size,'archive_sha256':digest,'inventory_sha256':expected,'deterministic_double_build':True,'all_role_references_verified':len(refs),'recovery':result,'network_and_subprocess_prohibited':True,'checker_sha256':sha((OUT/'check_package.py').read_bytes()),'note':'Hash integrity is not issuer authentication. Trust checker/archive hash out of band. Historical inner ZIP holds unchanged.'}
    save(HERE/'package-report.json',enc(report));save(OUT/'package-report.json',enc(report));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
