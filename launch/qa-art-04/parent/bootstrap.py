import pathlib,subprocess,json,hashlib
R=pathlib.Path(__file__).resolve().parent
ref='d6a689fd19cfddcc5fef52606f4e581938a8a004'
for n in ['prepare.py','smoke_viewers.py','motion_checks.py','extended_checks.py','boards.py','finalize.py']:
 b=subprocess.check_output(['git','show',ref+':launch/qa-art-02/parent/'+n]);(R/n).write_bytes(b)
b=subprocess.check_output(['git','show','6db6388d04fee0da8e0324a640d5880a5813a39c:launch/launch-01/launch-candidates.json'])
assert hashlib.sha256(b).hexdigest()=='28e032084f6bddf80143fd3bfd0e5b06cbdf84dc2343937e7b9bc71734ac3c9c'
(R/'parent-ledger.json').write_bytes(b)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('*.zip\n__pycache__/\n')
print('Harness source and ledger pinned')
