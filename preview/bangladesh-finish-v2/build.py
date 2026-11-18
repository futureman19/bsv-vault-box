"""Reproduce the frozen viewer-only correction without recompiling Three."""
from pathlib import Path
R=Path(__file__).resolve().parent
old=b'Math.min(devicePixelRatio,2)'
for src,dest in [('viewer.js','viewer.js'),('viewer.bundle.js','viewer.bundle.js'),('bangladesh-v1.html','bangladesh-finish-v2.html')]:
 raw=(R/'historical-v1'/src).read_bytes();assert raw.count(old)==1
 new=raw.replace(old,b'2');(R/dest).write_bytes(new)
 if dest.endswith('.html'):assert len(new)<5000000
print('Reproduced source, frozen compiled bundle and standalone HTML; models untouched.')
