import * as THREE from 'three';
import { GLTFLoader } from './vendor/three/loaders/GLTFLoader.js';

// All parts use the original renderer's local anchors. No gameplay state is read.
export const parts = ['cabinet', 'claw-hub', 'claw-finger', 'vault-box'];
export async function loadVaultKit() {
  const loader = new GLTFLoader(), resources = new Set();
  const dispose = () => resources.forEach(r => r.dispose());
  // Settle every request before cleanup: failed kits never leak later successes.
  const results = await Promise.allSettled(parts.map(async name => {
    const gltf = await loader.loadAsync(new URL(`./assets/vault-kit/${name}.glb`, import.meta.url).href);
    gltf.scene.traverse(o => {
      if (!o.isMesh) return;
      resources.add(o.geometry);
      for (const m of Array.isArray(o.material) ? o.material : [o.material]) resources.add(m);
    });
    const bounds = new THREE.Box3().setFromObject(gltf.scene), size = bounds.getSize(new THREE.Vector3());
    if (![...bounds.min, ...bounds.max].every(Number.isFinite) || size.length() === 0 || size.length() > 6) throw new Error(`Invalid ${name} bounds`);
    return gltf.scene;
  }));
  if (results.some(r => r.status === 'rejected')) { dispose(); throw new Error('Vault asset kit unavailable'); }
  return { scenes: Object.fromEntries(parts.map((name, i) => [name, results[i].value])), resources, dispose };
}

export function attachVaultPart(source, target, originals, own, color) {
  const visual = source.clone(true);
  visual.name = 'authored-vault-part';
  visual.traverse(o => {
    if (!o.isMesh) return;
    o.castShadow = true; o.receiveShadow = true;
    if (color && o.material.name === 'vault-color') {
      o.material = own(o.material.clone()); o.material.color.copy(color);
    }
  });
  target.add(visual);
  originals.forEach(o => { o.visible = false; });
  return visual;
}
