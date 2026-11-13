"""Independent saved-source theme, pivot and texture assertions, with negatives."""
import bpy,json,math,copy
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
def pivot(o):return {'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale),'parent':o.parent.name if o.parent else None}
base={n:pivot(bpy.data.objects[n]) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'benin.blend'),use_scripts=False);bpy.context.view_layer.update()
objs=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
orn=[o for o in objs if o.name.startswith('Takienta /')]
coords=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
materials={m.name:m for m in bpy.data.materials}
earth=materials['Earth / warm hand-smoothed plaster'];p=earth.node_tree.nodes.get('Principled BSDF')
images={i.name:i for i in bpy.data.images if i.packed_file}
image=images['earth-color.png'];pixels=list(image.pixels);channels=[sorted(pixels[c::4]) for c in range(3)]
median=[a[len(a)//2]*255 for a in channels] # image pixels read as source sRGB for byte image
facts={'pivots':{n:pivot(bpy.data.objects[n]) for n in base},'ornaments':len(orn),'roofed_towers':sum(o.name.startswith('Takienta / tower roofed') for o in orn),'flat_towers':sum(o.name.startswith('Takienta / tower flat') for o in orn),'roofs':sum(o.name.startswith('Takienta / thatched roof') for o in orn),'roof_ribs':sum(o.name.startswith('Takienta / roof rib') for o in orn),'walls':sum(o.name.startswith('Takienta / joining wall') for o in orn),'terrace':sum(o.name=='Takienta / terrace' for o in orn),'wrong_parent':[o.name for o in orn if o.parent.name!='Lid_Hinge'],'feet':sum(o.name.startswith('Earth / foot') and o.parent is None for o in objs),'buttresses':sum(o.name.startswith('Earth / rounded buttress') for o in objs),'bounds':[[min(v[i] for v in coords),max(v[i] for v in coords)] for i in range(3)],'earth_median_srgb':median,'earth_range':(max(pixels[0::4])-min(pixels[0::4]))*255,'maps':{n:list(i.size) for n,i in images.items()},'roughness_linked':p.inputs['Roughness'].is_linked}
def validate(d):
 assert d['pivots']==base,'pivot drift'
 assert d['roofed_towers']==2 and d['flat_towers']==1 and d['roofs']==2,'three tower / two roof contract'
 assert d['roof_ribs']==40 and d['walls']==2 and d['terrace']==1,'architectural forms absent'
 assert d['ornaments']==sum([1,2,2,40,1,1,1,2,1]) and not d['wrong_parent'],'lid ornament parenting' # terrace, towers, roofs, ribs, flat tower, recess, parapet, walls, doorway
 assert d['feet']==4 and d['buttresses']==4,'feet / buttresses'
 assert d['bounds'][0][0]>=-1.35 and d['bounds'][0][1]<=1.35 and d['bounds'][1][0]>=-.85 and d['bounds'][1][1]<=.85,'footprint'
 assert d['bounds'][2][0]<=1.98 and d['bounds'][2][1]<=2.827,'seating / height'
 assert all(lo<=v<=hi for v,(lo,hi) in zip(d['earth_median_srgb'],[(135,185),(65,115),(35,80)])),'earth palette'
 assert d['earth_range']>5 and d['roughness_linked'],'portable variation'
 assert len(d['maps'])==3 and all(max(s)<=512 for s in d['maps'].values()),'map budget'
validate(facts)
negative=[]
for name,key,value in [('missing roof','roofs',1),('detached ornament','wrong_parent',['test']),('bad palette','earth_median_srgb',[0,0,0]),('missing feet','feet',0)]:
 bad=copy.deepcopy(facts);bad[key]=value
 try:validate(bad)
 except AssertionError as e:negative.append({'mutation':name,'rejected':True,'assertion':str(e)})
 else:raise AssertionError('negative accepted: '+name)
facts['status']='PASS';facts['negative_controls']=negative
(R/'theme-check.json').write_text(json.dumps(facts,indent=2));print(json.dumps(facts,indent=2))
