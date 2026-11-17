import pathlib,subprocess,json,hashlib
R=pathlib.Path(__file__).resolve().parent
ids='arctic-ocean bahrain bolivia cabo-verde colombia denmark equatorial-guinea gabon guinea indian-ocean japan latvia madagascar mauritius mozambique niger palau portugal saint-vincent-and-the-grenadines sierra-leone south-sudan syria trinidad-and-tobago united-kingdom yemen'.split()
(R/'.gitattributes').write_text('* -text\n')
(R/'assigned.json').write_text(json.dumps(ids,indent=2)+'\n')
b=subprocess.check_output(['git','show','6db6388d04fee0da8e0324a640d5880a5813a39c:launch/launch-01/launch-candidates.json']);assert hashlib.sha256(b).hexdigest()=='28e032084f6bddf80143fd3bfd0e5b06cbdf84dc2343937e7b9bc71734ac3c9c';(R/'parent-ledger.json').write_bytes(b)
for name in ['prepare.py','boards.py','extended_checks.py','smoke_viewers.py','run_motion.py']:
 b=subprocess.check_output(['git','show','c3318e46fe1ac6ba279f99708ae814caa3775db0:launch/art-05/'+name]);(R/name).write_bytes(b)
print('Pinned ART-05 harness copied; only assigned.json differs; no art edits')
