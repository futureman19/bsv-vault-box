import * as THREE from 'three';
import { RoomEnvironment } from './vendor/three/RoomEnvironment.js';

// Rendering observes shared deterministic game mechanics; DOM owns input/reveal.
const mounts = new WeakMap();
function mulberry32(seed) {
  return () => { let t = seed += 0x6D2B79F5; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
export function mount(container) {
  if (!(container instanceof HTMLElement)) throw new TypeError('A container element is required');
  if (mounts.has(container)) return mounts.get(container);
  const fallback = container.querySelector('.cabinet');
  const mobile = matchMedia('(max-width: 600px)').matches;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const resources = new Set();
  const assetState = { status: 'loading', parts: 0 };
  let renderer, env, observer, raf = 0, disposed = false, time = 0, last = 0;
  const own = resource => { resources.add(resource); return resource; };
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 40);
  const gold = 0xfbbf24;
  function material(color, metalness = 0, roughness = 0.4, more = {}) {
    return own(new THREE.MeshStandardMaterial({ color, metalness, roughness, ...more }));
  }
  function mesh(geometry, mat, parent, x=0, y=0, z=0) {
    const m = new THREE.Mesh(own(geometry), mat); m.position.set(x,y,z); m.castShadow = true; m.receiveShadow = true; parent.add(m); return m;
  }
  function box(w,h,d,mat,parent,x=0,y=0,z=0) { return mesh(new THREE.BoxGeometry(w,h,d),mat,parent,x,y,z); }
  // Small manufactured bevels catch the studio lights without changing game bounds.
  function shell(w,h,d,r,mat,parent,x=0,y=0,z=0) {
    const shape=new THREE.Shape(), a=w/2-r, b=h/2-r;
    shape.moveTo(-a,-b);shape.lineTo(a,-b);shape.lineTo(a,b);shape.lineTo(-a,b);shape.closePath();
    const geometry=new THREE.ExtrudeGeometry(shape,{depth:d-2*r,bevelEnabled:true,bevelThickness:r,bevelSize:r,bevelSegments:3,steps:1,curveSegments:1});
    geometry.translate(0,0,-d/2+r);
    return mesh(geometry,mat,parent,x,y,z);
  }
  function rod(a,b,r,mat,parent) {
    const v = new THREE.Vector3(...a), end = new THREE.Vector3(...b), delta=end.clone().sub(v);
    const m = mesh(new THREE.CylinderGeometry(r,r,delta.length(),12),mat,parent);
    m.position.copy(v.add(end).multiplyScalar(.5)); m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),delta.normalize()); return m;
  }
  function label(text,w,h,color,bg,parent,x,y,z,size=64) {
    const canvas=document.createElement('canvas'); canvas.width=1024; canvas.height=256;
    const ctx=canvas.getContext('2d'); ctx.fillStyle=bg; ctx.fillRect(0,0,1024,256);
    ctx.fillStyle=color; ctx.font=`700 ${size}px monospace`; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(text,512,132);
    const tex=own(new THREE.CanvasTexture(canvas)); tex.colorSpace=THREE.SRGBColorSpace;
    const mat=own(new THREE.MeshStandardMaterial({map:tex,emissiveMap:tex,emissive:0xffffff,emissiveIntensity:.55,roughness:.3}));
    const m=mesh(new THREE.PlaneGeometry(w,h),mat,parent,x,y,z); m.castShadow=false; return mat;
  }
  function dispose() {
    if(disposed) return; disposed=true; cancelAnimationFrame(raf); observer?.disconnect();
    motion.removeEventListener('change',motionChanged);
    renderer?.domElement.removeEventListener('webglcontextlost',lost);
    resources.forEach(r=>r.dispose()); env?.dispose();
    renderer?.dispose(); renderer?.forceContextLoss(); renderer?.domElement.remove();
    container.classList.remove('claw3d-ready'); if(fallback) fallback.removeAttribute('aria-hidden');
    mounts.delete(container);
  }
  function lost(event) { event.preventDefault(); dispose(); }
  function motionChanged() { last=0; if(motion.matches) { time=0; pose(0); render(); } }
  const game = window.clawMotionHandle || window.ClawMotion.create();
  let prizes=[], claw, marquee, wire, carriage, trolley, chuteLight, cameraDistance=8;
  const prongs=[];
  function pose(t) {
    if(!claw) return;
    const s=game.state, active=s.phase!=='idle';
    const x=active?s.x:.05, z=active?s.z:.04, y=active?s.y:3.08;
    claw.position.set(x,y,z); carriage.position.x=x; trolley.position.set(x,3.16,z);
    const length=3.29-(y-.57); wire.position.set(x,3.29-length/2,z); wire.scale.y=length;
    claw.rotation.z=active?0:Math.sin(t*.8)*.025; claw.rotation.x=active?0:Math.sin(t*.65)*.014;
    prongs.forEach(p=>{p.scale.x=1-s.close*.4;});
    prizes.forEach((p,i)=>{
      const spot=window.ClawMotion.spots[i]; p.visible=!(s.phase==='reveal'&&s.selected===i);
      if(s.selected===i && s.prize) { p.position.set(s.prize.x,s.prize.y,s.prize.z); p.scale.y=s.prize.squash; p.rotation.set(0,0,0); }
      else { p.position.set(spot.x,p.userData.baseY+(motion.matches||active?0:Math.sin(t*1.4+i)*.009),spot.z); p.scale.y=1; p.rotation.copy(p.userData.rotation); }
    });
    marquee.emissiveIntensity=.55+(motion.matches?0:Math.sin(t*1.5)*.07);
    chuteLight.emissiveIntensity=s.flash?5:1.5;
    // Brief restrained camera settle on contact, returning during lift.
    const settle=motion.matches?0:s.phase==='grab'?.035*s.close:s.phase==='lift'?.035*(3.08-s.y)/.475:0;
    camera.position.set(cameraDistance*.27,3.65-settle,cameraDistance-settle); camera.lookAt(0,1.95,0);
  }
  function render() { renderer.render(scene,camera); }
  try {
    // Probe first: unavailable WebGL is an expected fallback, not a console error.
    const canvas=document.createElement('canvas');
    const context=canvas.getContext('webgl2',{alpha:true,antialias:true,powerPreference:'high-performance'});
    if(!context) return null;
    renderer=new THREE.WebGLRenderer({canvas,context,alpha:true,antialias:true});
    renderer.outputColorSpace=THREE.SRGBColorSpace; renderer.toneMapping=THREE.ACESFilmicToneMapping; renderer.toneMappingExposure=1.08;
    renderer.setPixelRatio(Math.min(devicePixelRatio,mobile?1.5:2));
    renderer.shadowMap.enabled=true; renderer.shadowMap.type=THREE.PCFSoftShadowMap;
    canvas.className='claw3d-canvas'; canvas.setAttribute('role','img'); canvas.setAttribute('aria-label','VAULT CLAW: glass arcade cabinet with six wrapped prizes and a metal claw');
    const pmrem=new THREE.PMREMGenerator(renderer), room=new RoomEnvironment();
    try { env=pmrem.fromScene(room,.04); scene.environment=env.texture; scene.environmentIntensity=.85; }
    finally {room.dispose(); pmrem.dispose();}
    const enamel=material(0x243747,.55,.32), edge=material(0x455362,.8,.3), brass=material(0xc79137,.75,.32), chrome=material(0xaebbc9,1,.23), dark=material(0x05090f,.25,.55);
    const light=material(0xffe5a0,.15,.25,{emissive:gold,emissiveIntensity:2});
    const green=material(0x4ade80,.2,.3,{emissive:0x4ade80,emissiveIntensity:1.5}); chuteLight=green;
    const cabinet=new THREE.Group();scene.add(cabinet);
    // Plinth, enamel base, raised sill and tall structural posts.
    shell(2.65,.14,1.8,.035,edge,cabinet,0,.16,0);
    shell(2.48,.75,1.62,.065,enamel,cabinet,0,.59,0);
    box(2.58,.12,1.74,brass,cabinet,0,.99,0);
    box(2.34,.08,1.5,dark,cabinet,0,1.08,0);
    box(2.46,2.34,.09,enamel,cabinet,0,2.23,-.8);
    for(const x of [-1.18,1.18]) for(const z of [-.76,.76]) {
      box(.13,2.6,.13,edge,cabinet,x,2.31,z);
      box(.025,2.35,.025,brass,cabinet,x+(x<0?.07:-.07),2.24,z+.07);
      for(const y of [1.14,3.4]) mesh(new THREE.SphereGeometry(.026,8,6),chrome,cabinet,x,y,z+.075);
    }
    shell(2.62,.46,1.82,.055,enamel,cabinet,0,3.66,0);
    box(2.65,.045,1.84,brass,cabinet,0,3.9,0);
    box(2.43,.31,.03,dark,cabinet,0,3.66,.925);
    const originalCabinet = [...cabinet.children];
    marquee=label('VAULT CLAW',2.26,.28,'#ffdb75','#080d16',cabinet,0,3.66,.945,96);
    label('BOXSV  /  PLAY DEMO',1.5,.24,'#8195ac','#151d29',cabinet,0,2.6,-.742,49);
    // Interior warm strip lights, rear rails and trolley.
    for(const x of [-1.08,1.08]) box(.027,2.15,.025,light,cabinet,x,2.25,-.71);
    box(2.22,.025,.06,light,cabinet,0,3.38,.6);
    for(const z of [-.48,.43]) rod([-1.1,3.29,z],[1.1,3.29,z],.035,chrome,cabinet);
    carriage=box(.48,.12,1.05,edge,cabinet,.05,3.27,0);
    trolley=box(.35,.15,.35,brass,cabinet,.05,3.16,.04);
    claw=new THREE.Group();claw.position.set(.05,3.08,.04);cabinet.add(claw);
    wire=mesh(new THREE.CylinderGeometry(.016,.016,1,12),chrome,cabinet);
    mesh(new THREE.CylinderGeometry(.13,.18,.22,24),chrome,claw,0,-.66,0);
    mesh(new THREE.CylinderGeometry(.19,.19,.045,24),brass,claw,0,-.62,0);
    const originalHub = [...claw.children];
    for(let i=0;i<3;i++) {
      const prong=new THREE.Group();prong.rotation.y=i*Math.PI*2/3;claw.add(prong);prongs.push(prong);
      mesh(new THREE.SphereGeometry(.065,12,8),chrome,prong,.14,-.73,0);
      rod([.14,-.73,0],[.32,-.96,0],.04,chrome,prong);
      rod([.32,-.96,0],[.28,-1.19,0],.035,chrome,prong);
      rod([.28,-1.19,0],[.16,-1.25,0],.029,chrome,prong);
    }
    // Wrapped prizes: separate lids, crossing satin ribbons, two-loop bows.
    const random=mulberry32(210614), colors=[0x973b48,0x21605e,0x3c538b,0x90572a,0x635187,0x327a54];
    const ribbon=material(0xffd674,.5,.28);
    colors.forEach((color,i)=>{
      const p=new THREE.Group(), s=.47;
      p.position.set((i%3-1)*.67,1.12+s/2, i<3?.35:-.33);
      p.rotation.set(0,(random()-.5)*.6,0);p.userData.rotation=p.rotation.clone();p.userData.baseY=p.position.y;cabinet.add(p);prizes.push(p);
      const wrap=material(color,.05,.65);
      p.userData.wrap = wrap;
      shell(s,s,s,.018,wrap,p);shell(s+.035,.075,s+.035,.012,wrap,p,0,s/2,0);
      box(.07,s+.012,s+.014,ribbon,p);box(s+.014,s+.012,.07,ribbon,p);
      box(.075,.012,s+.045,ribbon,p,0,s/2+.044,0);box(s+.045,.012,.075,ribbon,p,0,s/2+.045,0);
      for(const sign of [-1,1]) {
        const bow=mesh(new THREE.TorusGeometry(.085,.015,6,20),ribbon,p,sign*.075,s/2+.1,0);
        bow.scale.set(1,.65,1); bow.rotation.set(-.35,0,sign*.4);
      }
      mesh(new THREE.SphereGeometry(.032,10,8),ribbon,p,0,s/2+.08,.01);
    });
    // Recessed collection port and machined coin fascia.
    box(1.05,.42,.035,brass,cabinet,-.48,.55,.83);box(.94,.32,.045,dark,cabinet,-.48,.55,.857);
    box(.86,.16,.025,edge,cabinet,-.48,.62,.887);box(.82,.018,.02,green,cabinet,-.48,.4,.894);
    label('COLLECT',.63,.1,'#a2b4c4','#05090f',cabinet,-.48,.51,.9,54);
    box(.53,.52,.07,edge,cabinet,.7,.57,.84);box(.065,.19,.02,dark,cabinet,.7,.64,.885);
    label('DEMO',.42,.13,'#ffdb75','#303b49',cabinet,.7,.43,.882,76);
    for(const x of [.49,.91]) for(const y of [.36,.79]) mesh(new THREE.SphereGeometry(.018,8,6),chrome,cabinet,x,y,.885);
    // Side and front glazing retain crisp rims and environment highlights.
    const glass=own(new THREE.MeshPhysicalMaterial({color:0xb8d9e9,metalness:0,roughness:.08,transparent:true,opacity:.12,envMapIntensity:.9,clearcoat:1,clearcoatRoughness:.06,side:THREE.DoubleSide,depthWrite:false}));
    const pane=mesh(new THREE.PlaneGeometry(2.23,2.22),glass,cabinet,0,2.24,.77);pane.castShadow=false;pane.receiveShadow=false;
    for(const x of [-1.18,1.18]) {const m=mesh(new THREE.PlaneGeometry(1.42,2.22),glass,cabinet,x,2.24,0);m.rotation.y=Math.PI/2;m.castShadow=false;m.receiveShadow=false;}
    const gleam=own(new THREE.MeshBasicMaterial({color:0xd5eafa,transparent:true,opacity:.075,depthWrite:false}));
    const reflection=mesh(new THREE.PlaneGeometry(.1,1.8),gleam,cabinet,-.88,2.3,.778);reflection.rotation.z=-.18;reflection.castShadow=false;
    const floor=mesh(new THREE.PlaneGeometry(200,200),own(new THREE.ShadowMaterial({color:0x000000,opacity:.12})),scene);floor.rotation.x=-Math.PI/2;floor.position.y=.01;floor.castShadow=false;
    const contactCanvas=document.createElement('canvas');contactCanvas.width=128;contactCanvas.height=128;
    const contactCtx=contactCanvas.getContext('2d'), gradient=contactCtx.createRadialGradient(64,64,12,64,64,64);
    gradient.addColorStop(0,'rgba(0,0,0,.65)');gradient.addColorStop(1,'rgba(0,0,0,0)');contactCtx.fillStyle=gradient;contactCtx.fillRect(0,0,128,128);
    const contactTexture=own(new THREE.CanvasTexture(contactCanvas));
    const contact=mesh(new THREE.PlaneGeometry(4.1,3.3),own(new THREE.MeshBasicMaterial({map:contactTexture,transparent:true,depthWrite:false})),scene,0,.02,0);
    contact.rotation.x=-Math.PI/2;contact.castShadow=false;contact.receiveShadow=false;
    const key=new THREE.DirectionalLight(0xffe5b1,2.4);key.position.set(-3,7,5);key.castShadow=true;
    key.shadow.mapSize.setScalar(mobile?1024:2048);key.shadow.bias=-.0004;key.shadow.normalBias=.55;
    Object.assign(key.shadow.camera,{left:-3,right:3,top:5,bottom:-2,near:.5,far:16});key.shadow.radius=3;scene.add(key);own(key.shadow);
    const fill=new THREE.DirectionalLight(0x98bdff,2);fill.position.set(4,4,1);scene.add(fill);
    const interior=new THREE.PointLight(0xffd88c,3.5,5,2);interior.position.set(0,3.15,.3);scene.add(interior);
    scene.add(new THREE.HemisphereLight(0xc5d9ff,0x222637,1));
    function resize() {
      const width=container.clientWidth, height=container.clientHeight;
      if(!width||!height) return;
      renderer.setSize(width,height,false);camera.aspect=width/height;
      const distance=Math.max(7.9,4.0/camera.aspect); cameraDistance=distance;
      camera.position.set(distance*.27,3.65,distance);camera.lookAt(0,1.95,0);camera.updateProjectionMatrix();render();
    }
    container.append(canvas);resize();pose(0);render();
    container.classList.add('claw3d-ready');if(fallback) fallback.setAttribute('aria-hidden','true');
    // Replace presentation only after the entire kit validates; retain live anchors,
    // rails, cable, labels, lights, glass and all primitive failure paths.
    import('./vault-assets.js').then(async ({loadVaultKit, attachVaultPart}) => {
      const kit = await loadVaultKit();
      if (disposed || container.dataset.presentation === 'fallback') { kit.dispose(); if (!disposed) assetState.status = 'fallback'; return; }
      kit.resources.forEach(own);
      attachVaultPart(kit.scenes.cabinet, cabinet, originalCabinet, own);
      attachVaultPart(kit.scenes['claw-hub'], claw, originalHub, own);
      prongs.forEach(p => attachVaultPart(kit.scenes['claw-finger'], p, [...p.children], own));
      prizes.forEach(p => attachVaultPart(kit.scenes['vault-box'], p, [...p.children], own, p.userData.wrap.color));
      canvas.setAttribute('aria-label','VAULT CLAW: glass arcade cabinet with six collectible vault boxes and a metal claw');
      assetState.status = 'ready'; assetState.parts = 11; pose(time); render();
      window.clawPresentation?.settle('ready');
    }).catch(() => { if (!disposed) { assetState.status = 'fallback'; window.clawPresentation?.settle('fallback'); } });
    observer=new ResizeObserver(resize);observer.observe(container);
    canvas.addEventListener('webglcontextlost',lost);motion.addEventListener('change',motionChanged);
    function tick(now) {
      if(disposed) return;
      if(!document.hidden) {if(!motion.matches) time+=last?Math.min((now-last)/1000,.05):0;pose(time);render();}
      last=now;raf=requestAnimationFrame(tick);
    }
    raf=requestAnimationFrame(tick);
    const handle={...game,dispose,get disposed(){return disposed;},get assets(){return {...assetState};},
      visualSnapshot(){return {assets:{...assetState},drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,
        claw:claw.position.toArray(),fingers:prongs.map(p=>({scale:p.scale.toArray(),rotation:p.rotation.toArray(),authored:p.children.filter(c=>c.name==='authored-vault-part').length})),
        prizes:prizes.map(p=>({position:p.position.toArray(),visible:p.visible,authored:p.children.filter(c=>c.name==='authored-vault-part').length})),
        primitiveCabinetVisible:originalCabinet.some(o=>o.visible)};}};mounts.set(container,handle);return handle;
  } catch(error) { dispose(); return null; }
}
window.Claw3D={mount};
