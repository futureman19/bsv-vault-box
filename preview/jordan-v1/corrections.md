# Bounded correction record

Initial actual-source poster showed the arch largely obscured by the east massif. An independently added geometric arch-clearance test also failed on that initial saved source (`initial/theme-source-output.txt`, exit 1): arch and massif surfaces intersected. These were co-moving terrain surfaces, not a failure of the earlier moving-versus-static mechanism check.

Correction 1: shift the arch from rear-right Y=[0.53,0.72] to front-right Y=[-0.62,-0.43], unchanged X, Z and radii. This is an explicit post-authoring deviation from the original brief's rear/right ornament placement for visibility and physical separation. The initial brief is retained unchanged. The same strict source check is rerun; no collision exclusion or threshold changed. Initial poster is retained. No further aesthetic iterations planned.

One browser run failed the inherited fixed 60ms reduced-motion reset assertion; one bounded unchanged rerun passed. The final harness now waits for two actual animation-frame callbacks instead of assuming 60ms contains a rendered frame. Endpoint assertions remain exact, and no viewer behavior changed. The original failure is retained in `initial/reduced-reset-timing-failure.txt`; it is not silently represented as an all-green history.
