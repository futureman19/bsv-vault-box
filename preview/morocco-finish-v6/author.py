"""Paint-only finish on approved geometry. Export target primitives for GLB graft."""
import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline/morocco.blend'),use_scripts=False)
# Body: uniform linear-light multiplier; original map and registration untouched.
m=bpy.data.materials['Reference / Morocco reddish mineral strata'];nt=m.node_tree;p=next(n for n in nt.nodes if n.type=='BSDF_PRINCIPLED');socket=p.inputs['Base Color'];old=socket.links[0].from_socket;nt.links.remove(socket.links[0]);mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.90,.90,.90,1);nt.links.new(old,mul.inputs[1]);nt.links.new(mul.outputs[0],socket)
def mapped(name,file,roughness):
 m=bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;p=nt.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=roughness;im=bpy.data.images.load(str(R/'maps'/file));im.pack();n=nt.nodes.new('ShaderNodeTexImage');n.image=im;nt.links.new(n.outputs['Color'],p.inputs['Base Color']);return m
wood=mapped('Cedar / warm reference-grained vertical edges','cedar-edge.jpg',.57)
ceramic=mapped('Ceramic / reference emerald ivory rosette','ceramic-atlas.png',.48)
lid=bpy.data.objects['Lid / polished slab'];lid.data.materials.append(wood)
# Original top UV/map untouched. Dedicated named UV for edge faces only.
uv=lid.data.uv_layers.new(name='EdgeGrain');nt=wood.node_tree;n=next(n for n in nt.nodes if n.type=='TEX_IMAGE');uvnode=nt.nodes.new('ShaderNodeUVMap');uvnode.uv_map='EdgeGrain';nt.links.new(uvnode.outputs['UV'],n.inputs['Vector'])
for p in lid.data.polygons:
 edge=abs(p.normal.z)<.7
 if edge:p.material_index=1
 for li in p.loop_indices:
  v=lid.matrix_world@lid.data.vertices[lid.data.loops[li].vertex_index].co
  u=(v.x+1.86)/3.72 if abs(p.normal.y)>=abs(p.normal.x) else (v.y+1.39)/3.72
  uv.data[li].uv=(u,(v.z-1.678)/.48)
targets=[lid]
# The one integrated correction: the old tiny raised tessera fragmented the
# reference rosette under grazing light. Replace ONLY these three carriers with
# contiguous thin ceramic panels. Existing bed, hardware and lid stay untouched.
def prism(x0,x1,y0,y1):
 z0,z1=2.1711,2.185
 verts=[(x,y,z) for z in (z0,z1) for y in (y0,y1) for x in (x0,x1)]
 faces=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 return verts,faces
panels={
 'Ceramic tessera / deep green glaze':[(-1.785,1.785,-1.33,-.97)],
 'Ceramic tessera / ivory glaze':[(-1.785,1.785,.97,1.33)],
 'Ceramic tessera / near black green accents':[(-1.785,-1.425,-.97,.97),(1.425,1.785,-.97,.97)]}
for name,rects in panels.items():
 o=bpy.data.objects[name];verts=[];faces=[]
 for bounds in rects:
  v,f=prism(*bounds);off=len(verts);verts.extend(v);faces.extend([tuple(i+off for i in face) for face in f])
 mesh=bpy.data.meshes.new('Reference continuous ceramic carrier');mesh.from_pydata(verts,[],faces);mesh.update();o.data=mesh
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith(('Ceramic tessera','Tile bed')):continue
 targets.append(o);o.data.materials.clear();o.data.materials.append(ceramic)
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='UVMap')
 for loop in o.data.loops:
  v=o.matrix_world@o.data.vertices[loop.vertex_index].co;layer.data[loop.index].uv=((v.x+1.785)/3.57,(v.y+1.33)/2.66)
 for p in o.data.polygons:p.material_index=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'morocco.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in targets:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(R/'target-export.glb'),export_format='GLB',use_selection=True,export_animations=False)
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('V6 saved, target primitives exported, actual model poster rendered')
