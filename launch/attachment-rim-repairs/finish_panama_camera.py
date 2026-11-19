"""Second/final Panama pass: camera only; retain all prior capture evidence."""
from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[2];p=R/'preview/panama-repair-v2';old=p/'pass1';old.mkdir()
for name in ['panama-repair-v2.html','browser-check.json','finish-browser-output.txt','finish-build-output.txt','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','mobile-fallback.png']:
 shutil.copyfile(p/name,old/name)
for name in ['viewer.js','viewer.bundle.js']:
 text=(p/name).read_text();assert text.count('.position.set(-5,3.7,7)')==1
 (p/name).write_text(text.replace('.position.set(-5,3.7,7)','.position.set(-5,5.7,7)'))
text=(p/'build.py').read_text();text=text.replace("assert (R/'viewer.bundle.js').read_bytes()==(R/'historical-v1/viewer.bundle.js').read_bytes()", "assert (R/'viewer.bundle.js').read_text()==(R/'historical-v1/viewer.bundle.js').read_text().replace('.position.set(-5,3.7,7)', '.position.set(-5,5.7,7)')")
(p/'build.py').write_text(text)
(p/'presentation-check.json').write_text(json.dumps({'total_correction_passes':2,'geometry_passes':1,'camera_only_passes':1,'old_camera':[-5,3.7,7],'new_camera':[-5,5.7,7],'three_trunks_confirmed_in_source':True,'limitation':'Three canopy forms now discernible, two still overlap in projection. No missing tree was invented; landmarks and source camera unchanged. Pass1 preserves same-camera rim comparison.'},indent=2))
