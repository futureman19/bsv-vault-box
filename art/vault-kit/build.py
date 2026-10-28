"""Script-authored BoxSV rigid kit. Blender 5.2; game (x,y,z) -> (x,-z,y).
Regeneration overwrites source and exports; no external textures or addons.
"""
import bpy, math, pathlib, json
from mathutils import Vector
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/assets/vault-kit'
OUT.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != 'Collection': bpy.data.collections.remove(c)
M = {}
for name, color, metallic, rough in [
    ('enamel', (0.035,0.070,0.10,1),.55,.32),
    ('steel', (.24,.31,.38,1),.85,.28),
    ('brass', (.57,.30,.065,1),.75,.3),
    ('dark', (.007,.012,.02,1),.25,.55),
    ('chrome', (.59,.67,.75,1),1,.23),
    ('vault-color', (.19,.32,.43,1),.45,.36)]:
    m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color
    bs.inputs['Metallic'].default_value=metallic;bs.inputs['Roughness'].default_value=rough;M[name]=m

def xyz(v): return Vector((v[0],-v[2],v[1]))
COL=None

def finish(o,name,mat,bevel=0):
    o.name=name
    for c in list(o.users_collection): c.objects.unlink(o)
    COL.objects.link(o);o.data.materials.append(M[mat])
    if bevel:
        mod=o.modifiers.new('Manufactured edge radius','BEVEL');mod.width=bevel;mod.segments=2
        mod=o.modifiers.new('Weighted face normals','WEIGHTED_NORMAL');mod.keep_sharp=True
    return o

def box(name,loc,size,mat,bevel=.01):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz(loc));o=bpy.context.object
    o.dimensions=(size[0],size[2],size[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    return finish(o,name,mat,min(bevel,min(size)*.35))

def cyl(name,a,b,r,mat,vertices=16,r2=None):
    delta=xyz(b)-xyz(a)
    bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r,radius2=r if r2 is None else r2,depth=delta.length,location=(xyz(a)+xyz(b))*.5)
    o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=delta.to_track_quat('Z','Y')
    return finish(o,name,mat)

def plate(name,points,thickness,mat):
    # Profile in game XY, extruded through Z. Named editable solid linkage.
    verts=[xyz((x,y,z)) for z in [-thickness/2,thickness/2] for x,y in points];n=len(points)
    faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    o=bpy.data.objects.new(name,data);COL.objects.link(o);o.data.materials.append(M[mat])
    # Recalculate closed mesh normals independently of profile winding.
    bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
    mod=o.modifiers.new('Linkage edge bevel','BEVEL');mod.width=.006;mod.segments=2
    return o

def collection(name):
    global COL
    COL=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(COL)
    return COL

collection('cabinet')
box('Lower floating plinth',(0,.16,0),(2.65,.14,1.8),'steel',.035)
box('Stepped armored pedestal',(0,.59,0),(2.48,.75,1.62),'enamel',.065)
box('Front inset access panel',(0,.60,.819),(2.19,.55,.03),'dark',.025)
for x in [-1.02,1.02]:
    for z in [-.62,.62]:
        box('Isolation foot',(x,.08,z),(.38,.12,.4),'dark',.03)
    box('Base shoulder',(x,.61,.848),(.11,.58,.07),'steel',.02)
box('Bed brass sill',(0,.99,0),(2.58,.12,1.74),'brass',.025)
box('Prize tray',(0,1.08,0),(2.34,.08,1.5),'dark',.018)
box('Rear enclosure',(0,2.23,-.8),(2.46,2.34,.09),'enamel',.025)
for x in [-.78,0,.78]:
    box('Pressed rear panel',(x,2.19,-.741),(.71,1.93,.024),'steel',.025)
    box('Rear panel recess',(x,2.19,-.725),(.64,1.84,.016),'enamel',.022)
for x in [-1.18,1.18]:
    for z in [-.76,.76]:
        box('Structural chamfered upright',(x,2.31,z),(.15,2.6,.15),'steel',.027)
        box('Inlaid brass upright',(x+( .081 if x<0 else -.081),2.24,z+.04),(.018,2.35,.065),'brass',.005)
        for y in [1.22,3.30]:
            box('Corner reinforced socket',(x,y,z),(.215,.25,.20),'enamel',.025)
            cyl('Hex socket bolt',(x,y,z+.10),(x,y,z+.12),.032,'chrome',6)
box('Machined header',(0,3.66,0),(2.62,.46,1.82),'enamel',.055)
box('Layered crown',(0,3.91,0),(2.65,.065,1.84),'brass',.018)
box('Crown top inset',(0,3.956,0),(2.40,.035,1.61),'steel',.012)
box('Marquee recessed bezel',(0,3.66,.925),(2.43,.31,.03),'dark',.012)
for x in [-1.245,1.245]:
    box('Side service panel',(x,.58,0),(.03,.48,1.23),'steel',.01)
    for z in [-.42,-.28,-.14,0,.14,.28,.42]:
        box('Side cooling louver',(x*1.015,.61,z),(.025,.28,.065),'dark',.008)
for x in [-1.10,1.10]:
    box('Header corner guard',(x,3.66,.95),(.12,.32,.065),'brass',.018)

collection('claw-hub')
cyl('Actuator neck',(0,-.55,0),(0,-.64,0),.09,'steel',16)
cyl('Actuator upper collar',(0,-.61,0),(0,-.65,0),.19,'brass',24)
cyl('Tapered actuator housing',(0,-.65,0),(0,-.77,0),.16,'chrome',24,r2=.115)
cyl('Lower actuator collar',(0,-.755,0),(0,-.79,0),.125,'steel',24)
for i in range(6):
    a=i*math.tau/6;x=.145*math.cos(a);z=.145*math.sin(a)
    cyl('Housing rib',(x,-.655,z),(x*.84,-.74,z*.84),.013,'dark',8)
for i in range(3):
    a=i*math.tau/3;x=.13*math.cos(a);z=.13*math.sin(a)
    cyl('Hydraulic piston',(x,-.57,z),(x,-.69,z),.02,'brass',12)

collection('claw-finger')
plate('Forged hooked jaw',[(.105,-.72),(.17,-.715),(.355,-.95),(.32,-1.205),(.16,-1.28),(.145,-1.235),(.26,-1.165),(.28,-.965)],.067,'chrome')
plate('Inset linkage spine',[(.164,-.78),(.314,-.962),(.287,-1.151),(.271,-1.142),(.293,-.968),(.147,-.792)],.078,'dark')
for x,y in [(.14,-.73),(.317,-.96)]:
    cyl('Hinge barrel',(x,y,-.055),(x,y,.055),.057,'steel',16)
    cyl('Brass pivot pin',(x,y,-.061),(x,y,.061),.028,'brass',12)
box('Grip tooth',(.19,-1.242,0),(.065,.025,.087),'brass',.006)

collection('vault-box')
box('Recolorable vault shell',(0,0,0),(.47,.47,.47),'vault-color',.029)
box('Lid separation gasket',(0,.195,0),(.483,.023,.483),'dark',.006)
box('Armored vault lid',(0,.242,0),(.50,.072,.50),'vault-color',.018)
box('Lid inlay',(0,.282,0),(.30,.012,.29),'steel',.005)
for x in [-.203,.203]:
    for z in [-.203,.203]:
        box('Protective corner shoe',(x,-.17,z),(.092,.125,.092),'brass',.015)
        box('Riveted upper corner',(x,.13,z),(.065,.075,.065),'brass',.01)
        cyl('Lid security bolt',(x,.276,z),(x,.29,z),.018,'chrome',8)
box('Recessed lock plate',(0,-.015,.241),(.32,.31,.025),'dark',.017)
cyl('Octagonal lock escutcheon',(0,-.015,.25),(0,-.015,.273),.138,'brass',8)
cyl('Inset rotary door',(0,-.015,.274),(0,-.015,.287),.112,'steel',16)
cyl('Rotary lock center',(0,-.015,.288),(0,-.015,.316),.041,'brass',16)
for a in [0,math.tau/3,2*math.tau/3]:
    cyl('Vault wheel spoke',(0,-.015,.309),(.082*math.cos(a),-.015+.082*math.sin(a),.309),.012,'chrome',8)
for x in [-.245,.245]:
    for y in [-.08,.09]:
        box('Side hinge',(x,y,-.17),(.026,.061,.085),'steel',.008)
box('Sealed top strap',(0,.292,-.085),(.10,.013,.06),'brass',.004)

# Save editable named parts before creating material-batched export copies.
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene['coordinate_contract']='game +Y up; rigid parts stay at existing animation anchors'
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene['provenance']='Custom script-authored BoxSV geometry, no external models or textures'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/vault-kit/vault-kit.blend'))
summary={}
for col in [c for c in bpy.data.collections if c.name in ['cabinet','claw-hub','claw-finger','vault-box']]:
    bpy.ops.object.select_all(action='DESELECT');copies=[]
    for src in list(col.objects):
        cp=src.copy();cp.data=src.data.copy();bpy.context.scene.collection.objects.link(cp)
        cp.select_set(True);bpy.context.view_layer.objects.active=cp
        for mod in list(cp.modifiers): bpy.ops.object.modifier_apply(modifier=mod.name)
        cp.select_set(False);copies.append(cp)
    batches={material:[o for o in copies if o.data.materials[0].name==material] for material in M}
    for material, batch in batches.items():
        if not batch: continue
        bpy.ops.object.select_all(action='DESELECT')
        for o in batch: o.select_set(True)
        bpy.context.view_layer.objects.active=batch[0];bpy.ops.object.join()
        joined=bpy.context.object;joined.name=f'{col.name}__{material}'
        bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    # Only surviving export copies (source collection membership is unchanged).
    bpy.ops.object.select_all(action='DESELECT')
    exported=[o for o in bpy.context.scene.collection.objects if o.type=='MESH']
    for o in exported:o.select_set(True)
    path=OUT/f'{col.name}.glb'
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_extras=False)
    summary[col.name]={'bytes':path.stat().st_size,'editable_parts':len(col.objects),'material_batches':len(exported)}
    for o in exported:bpy.data.objects.remove(o,do_unlink=True)
(OUT/'source-manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
