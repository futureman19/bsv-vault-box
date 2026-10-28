# Three.js 0.186.0 (MIT)

Source: https://registry.npmjs.org/three/-/three-0.186.0.tgz
Tarball SHA256: `61eeff9d7616005c9a481c796f52287d81fbbbc0d55eaca5565322924252c1aa`

This release publishes unminified build/three.module.js and build/three.core.js, not a pre-minified module. The vendored three.module.min.js bundles those two exact files with esbuild 0.28.2:

```
npx --yes esbuild@0.28.2 build/three.module.js --bundle --minify --format=esm --outfile=three.module.min.js
```

Module SHA256: `fba62dfd6f0cdf58c9647d9cfe6e83cec5cf98eb24a7677ad116f4c0fca33902`
RoomEnvironment.js is copied unchanged from examples/jsm/environments/RoomEnvironment.js. LICENSE is copied unchanged. All browser imports are local; no CDN or build tool is required at runtime. Bloom is intentionally omitted to reserve the payload and GPU budget for forms, materials and lighting.

`loaders/GLTFLoader.js`, `utils/BufferGeometryUtils.js`, and `utils/SkeletonUtils.js`
are also copied unchanged from `examples/jsm/` in the same 0.186.0 tarball.
They load the optional authored vault kit; no decoder, CDN, or external texture
requests are required. Core and addons remain pinned to the same release.
