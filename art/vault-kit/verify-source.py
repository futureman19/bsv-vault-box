"""Independent saved-source reopening, evaluated topology and anchor checks."""
import bpy, pathlib, json, math
ROOT=pathlib.Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/vault-kit/vault-kit.blend'))
report={}
for name in ['cabinet','claw-hub','claw-finger','vault-box']:
    col=bpy.data.collections[name];vertices=[];triangles=0;min_area=math.inf
    for obj in col.objects:
        ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
        for v in m.vertices:
            p=obj.matrix_world@v.co;vertices.append([p.x,p.z,-p.y])
        for t in m.loop_triangles:
            a,b,c=[m.vertices[i].co for i in t.vertices];area=(b-a).cross(c-a).length/2
            min_area=min(min_area,area);assert area>1e-12,(name,obj.name,area)
        triangles+=len(m.loop_triangles);ev.to_mesh_clear()
    report[name]={'parts':len(col.objects),'triangles':triangles,'min_triangle_area':min_area,
        'min':[min(v[i] for v in vertices) for i in range(3)],'max':[max(v[i] for v in vertices) for i in range(3)]}
assert report['cabinet']['min'][1]>=0
assert report['claw-finger']['min'][1]<-1.2 and report['claw-hub']['max'][1]<-.5
assert abs(report['vault-box']['min'][1]+.235)<1e-5
out=ROOT/'evidence/vault-assets';out.mkdir(exist_ok=True,parents=True)
(out/'source-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
