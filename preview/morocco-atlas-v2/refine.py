from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'author.py';s=p.read_text();s=s.replace("import bpy,math,random,json","import bpy,math,random,json,os\nPASS=int(os.environ.get('MOROCCO_PASS','3'))")
s=s.replace("stone=mat('Rose ochre / wavy dressed stone'","stone=mat('Rose ochre / irregular mineral strata'")
s=s.replace("rock=mat('Atlas", "tex(stone,'stone-roughness.png','Roughness',True)\nnt=stone.node_tree;im=nt.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(R/'maps/stone-normal.png'));im.image.colorspace_settings.name='Non-Color';im.image.pack();nm=nt.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.22;nt.links.new(im.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs['Normal'],nt.nodes.get('Principled BSDF').inputs['Normal'])\nrock=mat('Atlas")
s=s.replace("co=o.data.vertices[o.data.loops[li].vertex_index].co", "co=o.data.vertices[o.data.loops[li].vertex_index].co\n   if o.name.startswith('Rose stone'):co=co+o.location")
s=s.replace("else:a,b=co.y/2.88+.5,co.z/1.6+.5", "else:a,b=(co.y+1.44+3.72)/3.72+.5,co.z/1.6+.5")
start=s.index('for sy in [-1,1]:\n for i in range(10):module');end=s.index('# Low corner wraps',start)
s=s[:start]+'''if PASS<2:
 for sy in [-1,1]:
  for i in range(10):module(-1.575+i*.35,sy*1.15)
 for sx in [-1,1]:
  for i in range(5):module(sx*1.605,-.70+i*.35)
else:
 # Dense non-overlapping eight-point stars with complementary interstitial kites.
 def rosette(cx,cy,a=.0875):
  pts=[]
  for k in range(16):
   t=k*math.pi/8;rad=a*(1 if k%2==0 else .48)
   pts.append((cx+rad*math.cos(t),cy+rad*math.sin(t)))
  tessera(pts,green)
  for k in range(8):
   t=k*math.pi/4;tn=t+math.pi/4;tm=t+math.pi/8
   tessera([(cx+a*math.cos(t),cy+a*math.sin(t)),(cx+a*1.075*math.cos(tm),cy+a*1.075*math.sin(tm)),(cx+a*math.cos(tn),cy+a*math.sin(tn)),(cx+a*.48*math.cos(tm),cy+a*.48*math.sin(tm))],ivory if k%2 else dark)
 for sy in [-1,1]:
  for j in range(2):
   for i in range(20):rosette(-1.6625+i*.175,sy*1.15+(j-.5)*.175)
 for sx in [-1,1]:
  for j in range(10):
   for i in range(2):rosette(sx*1.605+(i-.5)*.175,-.7875+j*.175)
''' +s[end:]
# tessera bevel without expensive per-piece applied ops; export_apply handles modifier
s=s.replace("me.materials.append(m);parent(o)","me.materials.append(m);parent(o)\n if PASS>=2:\n  be=o.modifiers.new('Ceramic softened arris','BEVEL');be.width=.0014;be.segments=1")
# replace terrain scalar function
s=s.replace("verts=[];faces=[];nx,ny=45,29","verts=[];faces=[];nx,ny=(65,39) if PASS>=3 else (45,29)")
a=s.index('  peaks=.48');b=s.index('\nfor j in range(ny-1)',a)
s=s[:a]+'''  if PASS<3:
   peaks=.48*math.exp(-((u+.10)/.34)**2)+.30*math.exp(-((u+.58)/.25)**2)+.25*math.exp(-((u-.52)/.30)**2)
   ridge=peaks*math.exp(-((v-.15*math.sin(u*7))/.50)**2)
   gullies=(.025*math.sin(u*53+v*9)+.018*math.sin(u*87-v*17))*(1-abs(v))
   z=2.17+edge*(.07+ridge+gullies)
   verts.append((.10+u*.50*math.sqrt(1-v*v*.50),1.04+v*.27*math.sqrt(1-u*u*.50),z))
  else:
   peaks=[(-.48,-.16,.43,.30,.48),(-.13,.17,.74,.32,.56),(.23,-.12,.46,.27,.48),(.54,.23,.35,.31,.53)]
   z=max(h*max(0,1-math.sqrt(((u-px)/wx)**2+((v-py)/wy)**2))**.72 for px,py,h,wx,wy in peaks)
   z+=.10*edge
   drainage=(.027*math.sin(u*71+v*14)+.016*math.sin(u*113-v*21))*min(1,z*5)
   verts.append((.04+u*.68,1.015+v*.30,2.17+max(0,z+drainage)))
''' +s[b:]
# additional pass3 edits run before material cleanup
idx=s.index('for m in list(bpy.data.materials):')
s=s[:idx]+'''if PASS>=3:
 # Front ring retains original size but now lies in the front-face plane.
 mount=bpy.data.objects['Side ring / mount'];mount.location=(-1.25,-1.46,.43);mount.rotation_euler=(math.pi/2,0,0)
 ring=bpy.data.objects['Side ring / hanging brass'];ring.location=(-1.25,-1.50,.30);ring.rotation_euler=(math.pi/2,0,0)
 # Shorten the released hasp around its unchanged bearing anchor, preserving contact.
 for ob in list(bpy.data.objects):
  if ob.parent==latch and ob.type=='MESH' and not any(k in ob.name for k in ['knuckle','bridge']):
   for ve in ob.data.vertices:ve.co.z*=.53
   ob.location.z*=.53
 for ob in list(bpy.data.objects):
  if ob.name.startswith('Corner brass'):
   for ve in ob.data.vertices:
    # Scalloped shoulder with retained wrap seating.
    axis=ve.co.x if 'front' in ob.name else ve.co.y
    if ve.co.z>0:ve.co.z*=.55+.45*math.cos(axis*10)**2
 # Small rounded studs are on the static clasp seat, clear of release path.
 for xx in [-.205,.205]:
  for zz in [1.24,1.47]:disk('Clasp / seated fastener',(xx,-1.502,zz),.022,.013)
''' +s[idx:]
s=s.replace("print('MOROCCO AUTHORED')", "print('MOROCCO AUTHORED PASS',PASS)")
p.write_text(s)
# rewrite version strings in copied tooling
for p in R.glob('*'):
 if p.suffix in ['.py','.js','.html','.json'] and p.name not in ['refine.py']:
  s=p.read_text();p.write_text(s.replace('morocco-atlas-v1','morocco-atlas-v2'))
