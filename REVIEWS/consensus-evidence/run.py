"""Run the pinned live Lean column and SV-node harness; no broadcast RPCs."""
import os
import subprocess
from pathlib import Path

home = Path.home()
work = home/'consensus-t_a71c39fc'
lean = work/'bsv-script-lean'
out = Path(__file__).resolve().parent
os.environ['PATH'] = str(home/'.elan/bin')+':'+str(home/'.cargo/bin')+':'+os.environ['PATH']
node = work/'oracle-node'
node.mkdir(exist_ok=True)
conf = (lean/'harness/oracle/bitcoin.conf').read_text().replace('genesisactivationheight=620538','genesisactivationheight=1').replace('chronicleactivationheight=943816','chronicleactivationheight=15000')
(node/'bitcoin.conf').write_text(conf)
cli = [str(home/'bitcoin-sv-1.2.3/bin/bitcoin-cli'), '-datadir='+str(node), '-regtest', '-rpcport=18563']
probe = subprocess.run(cli+['getblockchaininfo'],capture_output=True,text=True)
if probe.returncode:
    start = subprocess.run([str(home/'bitcoin-sv-1.2.3/bin/bitcoind'), '-datadir='+str(node), '-disablewallet', '-connect=0', '-rpcport=18563','-port=18564','-daemon'],capture_output=True,text=True)
    print('oracle start',start.returncode,start.stdout,start.stderr)
    if start.returncode: raise SystemExit(start.returncode)
    import time
    for _ in range(60):
        probe = subprocess.run(cli+['getblockchaininfo'],capture_output=True,text=True)
        if probe.returncode == 0: break
        time.sleep(1)
    if probe.returncode: raise RuntimeError('oracle did not become ready')
commands = [
 [str(lean/'eval/bsvs'),'corpus',str(out/'vault.jsonl'),'--out',str(out/'spec.jsonl'),'--config','sv-regtest','--genesis-height','1','--chronicle-height','15000'],
 [str(lean/'harness/target/release/run_svnode'),'--corpus',str(out/'vault.jsonl'),'--spec',str(out/'spec.jsonl'),'--spec-config','sv-regtest','--genesis-height','1','--chronicle-height','15000','--rpc','http://127.0.0.1:18563','--cookie',str(node/'regtest/.cookie'),'--witnesses',str(out/'node'),'--cells',str(out/'cells.jsonl')]
]
for name,cmd in zip(['spec','node'],commands):
    print('COMMAND',cmd)
    r = subprocess.run(cmd,cwd=lean,capture_output=True,text=True)
    (out/(name+'.log')).write_text(r.stdout+r.stderr)
    print(name,'EXIT',r.returncode, r.stdout[-6000:], r.stderr[-6000:])
    if r.returncode: raise SystemExit(r.returncode)
