import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {pose,validateAsset} from './motion.mjs';
const stage=document.querySelector('#stage'),status=document.querySelector('#status'),open=document.querySelector('#open'),reset=document.querySelector('#reset'),fallback=document.querySelector('#fallback');
let ready=false,failed=false,progress=0,target=0,lid,latch,renderer,scene,camera,controls;
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
window.pilot={ready:false,progress:0,errors:[],rotation:0};
function fail(error){failed=true;ready=false;window.pilot.errors.push(String(error));status.textContent='3D unavailable — showing the rendered poster.';fallback.hidden=false;open.disabled=true;reset.disabled=true;if(renderer)renderer.domElement.hidden=true;}
const timeout=setTimeout(()=>{if(!ready)fail('Asset loading timed out');},15000);
try{
 renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0x10151a,0);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.2;
 stage.prepend(renderer.domElement);renderer.domElement.setAttribute('aria-label','Interactive Lithuania Curonian Dune and Lagoon model. Drag to rotate.');
 scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(36,1,.1,100);camera.position.set(-5,5.3,7);
 controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,.95,0);controls.enablePan=false;controls.enableDamping=false;controls.minDistance=5.5;controls.maxDistance=11;controls.maxPolarAngle=Math.PI*.49;controls.update();controls.saveState();
 const pmrem=new THREE.PMREMGenerator(renderer);const room=new RoomEnvironment();scene.environment=pmrem.fromScene(room,.04).texture;scene.environmentIntensity=.22;room.dispose();pmrem.dispose();
 scene.add(new THREE.HemisphereLight(0xc9e4ff,0x242526,2));
 const key=new THREE.DirectionalLight(0xe3efff,4);key.position.set(-3,6,5);scene.add(key);renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;key.castShadow=true;key.shadow.mapSize.set(1024,1024);Object.assign(key.shadow.camera,{left:-4,right:4,top:5,bottom:-4,near:.1,far:20});key.shadow.bias=-.00015;key.shadow.normalBias=.018;const floor=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.ShadowMaterial({opacity:.26}));floor.rotation.x=-Math.PI/2;floor.position.y=-.29;floor.receiveShadow=true;scene.add(floor);
 const rim=new THREE.DirectionalLight(0xffcc8c,3);rim.position.set(3,4,-3);scene.add(rim);
 const bytes=Uint8Array.from(atob(document.querySelector('#asset').textContent.trim()),c=>c.charCodeAt(0));
 new GLTFLoader().parse(bytes.buffer,'',gltf=>{
  if(failed)return;
  try{
   const root=gltf.scene;lid=root.getObjectByName('Lid_Hinge');latch=root.getObjectByName('Latch_Pivot');
   let triangles=0,meshes=0,nonfinite=0,degenerate=0;const materials=new Set();
   root.updateMatrixWorld(true);root.traverse(o=>{if(!o.isMesh)return;o.castShadow=true;o.receiveShadow=true;meshes++;materials.add(o.material.uuid);let p=o.geometry.attributes.position;for(let i=0;i<p.count;i++)if(![p.getX(i),p.getY(i),p.getZ(i)].every(Number.isFinite))nonfinite++;
    const idx=o.geometry.index;const count=idx?idx.count:p.count;triangles+=count/3;
    const a=new THREE.Vector3(),b=new THREE.Vector3(),c=new THREE.Vector3();for(let i=0;i<count;i+=3){a.fromBufferAttribute(p,idx?idx.getX(i):i);b.fromBufferAttribute(p,idx?idx.getX(i+1):i+1);c.fromBufferAttribute(p,idx?idx.getX(i+2):i+2);if(b.sub(a).cross(c.sub(a)).lengthSq()<1e-18)degenerate++;}
   });
   const bounds=new THREE.Box3().setFromObject(root);validateAsset({lid:!!lid&&!!latch,triangles,bounds:[...bounds.min.toArray(),...bounds.max.toArray()]});if(nonfinite||degenerate)throw Error(`Bad vertices ${nonfinite}, degenerate ${degenerate}`);
   scene.add(root);window.pilot.asset={triangles,meshes,materials:materials.size,bounds:{min:bounds.min.toArray(),max:bounds.max.toArray()},lid:lid.name,latch:latch.name,nonfinite,degenerate,bytes:bytes.length};
   window.pilot.root=root;window.pilot.camera=camera;window.pilot.renderer=renderer;ready=true;window.pilot.ready=true;fallback.hidden=true;open.disabled=false;reset.disabled=false;status.textContent='Drag to rotate · scroll or pinch to zoom';clearTimeout(timeout);
  }catch(e){fail(e);}
 },fail);
 function resize(){const w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}new ResizeObserver(resize).observe(stage);resize();
 let lastFocus=0,lastScale=1;let last=performance.now();function frame(now){requestAnimationFrame(frame);let dt=Math.min((now-last)/1000,.05);last=now;if(ready){progress=reduced.matches?target:THREE.MathUtils.clamp(progress+Math.sign(target-progress)*Math.min(Math.abs(target-progress),dt/.95),0,1);const scale=1+.15*progress;camera.position.sub(controls.target).multiplyScalar(scale/lastScale).add(controls.target);lastScale=scale;const focus=.95*progress;camera.position.y+=focus-lastFocus;controls.target.y+=focus-lastFocus;lastFocus=focus;controls.update();const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.rotation=controls.getAzimuthalAngle();window.pilot.lid=lid.rotation.x;window.pilot.latch=latch.rotation.x;}if(!failed)renderer.render(scene,camera);}requestAnimationFrame(frame);
 // Touch activation is explicit: Edge file previews can deliver pointerup without click.
 function bindAction(button,action){let down=null,lastTouch=-Infinity;button.onpointerdown=e=>{down={id:e.pointerId,x:e.clientX,y:e.clientY};};button.onpointercancel=()=>{down=null;};button.onpointerup=e=>{if(e.pointerType==='touch'&&down?.id===e.pointerId&&Math.hypot(e.clientX-down.x,e.clientY-down.y)<10&&!button.disabled){e.preventDefault();lastTouch=performance.now();action();}down=null;};button.onclick=e=>{if(e.isTrusted&&e.detail>0&&performance.now()-lastTouch<700)return;action();};}
 bindAction(open,()=>{target=target?0:1;open.textContent=target?'Close lid':'Open lid';open.setAttribute('aria-pressed',String(!!target));});
 bindAction(reset,()=>{target=progress=lastFocus=0;lastScale=1;controls.reset();open.textContent='Open lid';open.setAttribute('aria-pressed','false');});
}catch(e){fail(e);}
