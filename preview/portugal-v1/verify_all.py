from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[[sys.executable,str(R/'build.py')],['C:/Program Files/nodejs/node.exe','--test',str(R/'tests.mjs')]]
commands += [[B,'--background','--factory-startup','--python-exit-code','1','--python',str(R/f)] for f in ['verify_source.py','verify_parity.py','verify_theme.py']]
commands += [[sys.executable,str(R/f)] for f in ['verify_browser.py','verify_extended.py']]
for i,cmd in enumerate(commands):
 result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace');log=R/f'verify-{i}.log'
 if log.exists() and 'Traceback' in log.read_text():log.rename(R/f'verify-{i}-failed.log')
 log.write_text(result.stdout+'\n'+result.stderr,encoding='utf8');print(result.stdout,result.stderr,flush=True);assert result.returncode==0,(cmd,result.returncode)
print('ALL VERIFICATION PASS')
