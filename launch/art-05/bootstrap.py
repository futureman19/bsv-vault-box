import pathlib,subprocess,json,hashlib
R=pathlib.Path(__file__).resolve().parent
ids='angola azerbaijan benin burkina-faso chile cyprus egypt finland grenada iceland italy kyrgyzstan lithuania marshall-islands montenegro new-zealand pacific-ocean philippines saint-kitts-and-nevis serbia south-africa sweden togo ukraine venezuela'.split()
R.mkdir(parents=True,exist_ok=True)
(R/'.gitattributes').write_text('* -text\n')
(R/'assigned.json').write_text(json.dumps(ids,indent=2)+'\n')
b=subprocess.check_output(['git','show','6db6388d04fee0da8e0324a640d5880a5813a39c:launch/launch-01/launch-candidates.json']);assert hashlib.sha256(b).hexdigest()=='28e032084f6bddf80143fd3bfd0e5b06cbdf84dc2343937e7b9bc71734ac3c9c';(R/'parent-ledger.json').write_bytes(b)
for name,branch,source in [('prepare.py','feature/art-04-review','prepare.py'),('boards.py','feature/art-04-review','boards.py'),('extended_checks.py','feature/art-04-review','extended_checks.py'),('smoke_viewers.py','feature/art-03','smoke_viewers.py'),('run_motion.py','feature/art-03','run_motion.py')]:
 folder='art-03' if branch=='feature/art-03' else 'art-04'
 text=subprocess.check_output(['git','show',f'origin/{branch}:launch/{folder}/{source}']).decode()
 text=text.replace("launch-candidates.json","parent-ledger.json")
 if name=='prepare.py':
  lines=text.splitlines();lines[2]='IDS=json.loads((ROOT/\'assigned.json\').read_text())';text='\n'.join(lines)+'\n'
 if name=='run_motion.py':text=text.replace('Algeria contract assertions applied to unchanged Honduras motion module','Reused Algeria contract assertions applied to unchanged selected motion module')
 (R/name).write_text(text)
print('bootstrap complete')
