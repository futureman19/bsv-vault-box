"""Bounded independent verification of the saved final deliverable.
Authoring is separate. BLENDER may override the installed executable path.
"""
from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
steps=[('build',[sys.executable,'build.py']),('motion',['node','--test','tests.mjs'])]
for label,file in [('source','verify_source.py'),('parity','verify_parity.py'),('theme-source','verify_theme_source.py')]:
 steps.append((label,[blender,'--background','--factory-startup','--python-exit-code','1','--python',file]))
steps.extend([('browser',[sys.executable,'verify_browser.py']),('theme',[sys.executable,'verify_theme.py']),('delivery',[sys.executable,'verify_delivery.py'])])
transcript=[]
for label,command in steps:
 proc=subprocess.run(command,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
 text=proc.stdout;(R/(label+'-output.txt')).write_text(text,encoding='utf8') if label!='delivery' else None
 transcript.append('$ '+' '.join(command)+'\n'+text+'\nEXIT_CODE '+str(proc.returncode))
 print(label.upper(), 'PASS' if proc.returncode==0 else 'FAIL',flush=True)
 (R/'verification-output.txt').write_text('\n\n'.join(transcript),encoding='utf8')
 if proc.returncode:print(text);raise SystemExit(proc.returncode)
print('ALL ACCEPTANCE CHECKS PASS')
