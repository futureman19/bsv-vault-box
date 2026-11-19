import subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PINS={'baseline':('f0a54d9b3e80338fbe34c869987a45d6d23ae25c','launch/collection/ledger.json'),'repairs':('3952a4eb1c57ca921c21d0aa774ab8b8752e3df7','launch/collection-repairs/dispositions.json'),'ordinary':('ece254fb70859e63dbd80b76631a32eb01455df6','launch/ordinary-finish-20/dispositions.json'),'structural':('7a59667e5ab40bc6cf58fd30b57974621cb30d9b','launch/attachment-rim-repairs/finish/final-ledger.json')}
def blob(ref,path):return subprocess.check_output(['git','show',f'{ref}:{path}'])
def main():
 (ROOT/'inputs').mkdir(exist_ok=True)
 for key,(ref,path) in PINS.items():
  data=blob(ref,path);(ROOT/'inputs'/f'{key}.json').write_bytes(data)
  obj=json.loads(data)
  print(key, list(obj))
  if key=='structural':
   for e in obj['records']:
    print(e['id'],json.dumps({k:v for k,v in e.items() if k not in ['original_record','source_scripts','viewer','final_acceptance']})[:3500]);print('acceptance',json.dumps(e.get('final_acceptance',{}))[:1000])
 if True:
  data=blob(PINS['structural'][0],'launch/attachment-rim-repairs/finish/OWNER-PACKET.md');(ROOT/'inputs'/'OWNER-PACKET.md').write_bytes(data)
if __name__=='__main__':main()
