import * as THREE from 'three';
// Presentation only: bounded 3D LineSegments + Points, never included in GLB.
export function fireworks(scene){
 const group=new THREE.Group();group.name='Presentation_fireworks_NOT_collectible';scene.add(group);
 const palette=[0xff334c,0xf5ead6,0x579fff,0xf5d491];
 const bursts=[[-1.6,3.3,-2.0,2],[0,4.0,-2.2,0],[1.6,3.5,-2.2,2]];
 const count=72,tail=3,systems=[];
 for(let j=0;j<bursts.length;j++){
  const positions=new Float32Array(count*tail*6),colors=new Float32Array(positions.length),tips=new Float32Array(count*3),tipColors=new Float32Array(count*3),directions=[];
  for(let i=0;i<count;i++){
   const z=1-2*(i+.5)/count,angle=i*2.3999632297;directions.push(new THREE.Vector3(Math.sqrt(1-z*z)*Math.cos(angle),Math.sqrt(1-z*z)*Math.sin(angle),z));
   const c=new THREE.Color(palette[i%11===0?3:i%5===0?1:bursts[j][3]]);
   c.toArray(tipColors,i*3);for(let k=0;k<tail*2;k++)c.clone().multiplyScalar(.35+.65*k/(tail*2)).toArray(colors,(i*tail*2+k)*3);
  }
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(positions,3));g.setAttribute('color',new THREE.BufferAttribute(colors,3));
  const m=new THREE.LineBasicMaterial({vertexColors:true,transparent:true,opacity:.85,depthWrite:false,blending:THREE.AdditiveBlending,toneMapped:false});const lines=new THREE.LineSegments(g,m);lines.frustumCulled=false;group.add(lines);
  const pg=new THREE.BufferGeometry();pg.setAttribute('position',new THREE.BufferAttribute(tips,3));pg.setAttribute('color',new THREE.BufferAttribute(tipColors,3));const pm=new THREE.PointsMaterial({size:.026,vertexColors:true,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,toneMapped:false});const points=new THREE.Points(pg,pm);points.frustumCulled=false;group.add(points);
  systems.push({g,m,pg,pm,positions,tips,directions,center:new THREE.Vector3(...bursts[j].slice(0,3))});
 }
 function update(seconds,reduced){
  systems.forEach((s,j)=>{
   const age=reduced?.95:((seconds+j*.83)%3.6)/3.6*1.7;
   for(let i=0;i<count;i++){
    function pos(t){return s.directions[i].clone().multiplyScalar((.20+.65*t)*( .88+.12*Math.sin(i*7))).add(s.center).add(new THREE.Vector3(0,-.18*t*t,0));}
    pos(age).toArray(s.tips,i*3);
    for(let k=0;k<tail;k++){pos(Math.max(0,age-k*.10)).toArray(s.positions,(i*tail+k)*6);pos(Math.max(0,age-(k+1)*.10)).toArray(s.positions,(i*tail+k)*6+3);}
   }
   s.m.opacity=s.pm.opacity=reduced?.75:Math.min(1,age*5)*Math.max(0,1-(age-.7));s.g.attributes.position.needsUpdate=true;s.pg.attributes.position.needsUpdate=true;
  });
 }
 update(0,true);return {group,update,systems,particleCount:count*bursts.length,trailSegments:count*bursts.length*tail};
}
