# Real failed observations and bounded corrections

1. Initial build exited 1 because the prescribed baseline dependency directory was empty. Actual Node error:

```
Error: Cannot find module 'C:\Users\futur\Desktop\bsv-vault-box\.worktrees\t_9fab0794\preview\iceland-pilot\node_modules\esbuild\bin\esbuild'
code: 'MODULE_NOT_FOUND'
```

`ln -s` did not yield usable baseline packages; native Python inspection showed an empty directory and the main checkout also lacked esbuild. Fixed by `npm install --prefix preview/vanuatu-v1 --no-audit --no-fund`, which installed the already-declared pinned Three/esbuild dependencies within this new directory only. No dependency upgrade or baseline file modification. Build then passed.

2. Actual initial source poster failed visual acceptance: the narrow crater hid its ember basin and gray ash read as concrete. Preserved `poster-before-visibility-fix.png` and `author-before-visibility-fix.py`. One bounded correction widened rim/bowl, lowered only the front rim, enlarged the basin and increased warm emission; darkened ash maps. Final source and browser checks use the corrected model. This is visual failure-and-fix, not a falsely claimed automated red test.

3. Post-authoring negative controls in verify_theme.py genuinely detach the ember from the lid and lift it above its allowed bowl floor; the unchanged ancestry and depth gates reject both, then source is reloaded and passes. These are deliberate regression controls, not test-first development.

## Declared deviations from initial brief
Crater crown radii grew from .57/.41 to .74/.53; lower bowl .48/.34 and ember .50/.36 instead of approximately .30/.22. Front rim lowered by up to .18; overall summit remains in the original range and crater depth exceeds .40. The basal apron starts at 1.975 so it seats into the slab. Ash map center darkened from about 70 to 48 sRGB. These are intentional visibility/material corrections; no change to hinge/latch pivots or collision exclusions.
