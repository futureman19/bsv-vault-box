import json,pathlib,hashlib,collections
R=pathlib.Path(__file__).resolve().parent
notes={
'afghanistan':('needs-decision','Smooth pale mountain peaks versus craggy promotional relief; bright cobalt winding veins versus dark granular lapis.'),
'armenia':('pass','Arches and hardware retained; broad banding and repeating interior stone mottling look less natural than promotion.'),
'barbados':('pass','Terraces and turquoise coast retained; regular tiers and simplified erosion versus richer promotional stone.'),
'botswana':('pass','Delta channels become subtle on mobile; weave is graphic rather than tactile. No demonstrated structural failure.'),
'cameroon':('needs-decision','Warm taupe diagonal streaks versus cool granular volcanic stone in marketing; rounded canopy and simplified rocky terrain.'),
'costa-rica':('pass','Faceted volcano and rounded canopy retain identity; cloudy green-gray material is stylized in both representations.'),
'dominica':('pass','Angular ridges and stepped pale basin versus softened promotional terrain; reduced mobile detail.'),
'estonia':('pass','Bog pools and path retained; flatter water and simpler banks than promotional moss and depth shading.'),
'georgia':('needs-decision','Tower retained but broad faceted mountains and repeated geometric vegetation differ materially from craggy promotional landscape.'),
'guyana':('needs-decision','Waterfall retained; block-like escarpment and rounded canopy versus irregular cliff and layered promotional rainforest.'),
'iran':('pass','Star motifs and hardware retained; graphic blue/turquoise surfaces lack promotional glaze variation and apparent relief.'),
'kazakhstan':('pass','Scrolls and circular ornament retained; cream panels do not resolve as fibrous felt and wood reads as regular stripes.'),
'lesotho':('pass','Compact mountain cluster; pale stone streaks and graphic indigo stripes rather than tactile textile. Framing affects perceived terrain size.'),
'malaysia':('needs-decision','Consistent crimson body and bronze-brown top versus marketing mauve and charcoal. Viewer copy explicitly says crimson; direction decision, not proven renderer bug.'),
'micronesia':('needs-decision','Regular platforms and smooth masonry versus tactile basalt and stronger sculptural promotional relief.'),
'namibia':('needs-decision','Compact yellow-gold dunes and narrower apparent playa versus elongated peach marketing ridges. Parent full archive inventory hold remains.'),
'north-korea':('needs-decision','Compact caldera and smaller visible lake; regular diagonal/wavy stone texture versus subtler promotional finish.'),
'panama':('needs-decision','Three visible trees in promotion versus two in both closed runtime views. Sparser canopy, flatter banks and narrower channel; confirmed visual inconsistency, not proven functional bug.'),
'republic-of-the-congo':('needs-decision','Flatter shoreline and smaller segmented canopies versus fuller promotional wetland; darker warmer grain.'),
'san-marino':('needs-decision','Low-severity hold from delegated review: three towers retained but compact ridge and brighter uniformly mottled stone. Minor illustration enhancement, not a mechanical correction.'),
'slovakia':('needs-decision','Uniform timber and low apparent white ornament relief versus tactile promotional wood and raised decoration.'),
'spain':('needs-decision','Recognizable cobalt/ivory motifs; smoother terracotta and ceramic finish versus granular clay and nuanced promotional glaze.'),
 'tanzania':('needs-decision','Regular green mountain footprint and simplified summit; conspicuous repeated diagonal/crosshatched wood, especially open interior.'),
 'turkey':('needs-decision','Tulip composition retained but graphic relief and uniform blue/ivory finish differ from richer promotional glaze and metal.'),
 'uruguay':('needs-decision','Shallower landscape and less pronounced gorge impression; regular checked/diagonal shell texture versus stronger promotional terrain depth.'),
 'zimbabwe':('needs-decision','Compact regularly tiered boulders and flatter tan base versus broad irregular promotional rocks; cleaner repetitive masonry.')}
ids=json.loads((R/'assigned.json').read_text()); p=json.loads((R/'packaging-results.json').read_text()); smoke=json.loads((R/'smoke-results.json').read_text()); motion=json.loads((R/'motion-results.json').read_text())
assert set(notes)==set(ids) and len(p)==26 and len(smoke)==52 and len(motion)==26
assert all(x['result']=='pass' for x in smoke) and all(x['passed'] for x in motion)
rows=[]
for e in p:
 s=e['id']; status,note=notes[s]; captures=[f'smoke/{s}/{m}-{pose}.png' for m in ['desktop','mobile'] for pose in ['closed','open']];assert all((R/c).exists() for c in captures)
 rows.append(dict(id=s,status=status,user_final_approved=False,launch_ready=False,polish_iterations=0,model_changed=False,selection=e['selection'],viewer=e['viewer'],glb_bytes=e['glb_bytes'],source_archives=e['archives'],captures=captures,comparison=f'boards/{s}.jpg',visual_findings=note,hardware='Principal fittings retained. Open interiors/hinges visible; screenshots establish no collision or contact proof.',decision='Accept stylized candidate or authorize scoped alignment; no automatic substantial redesign.' if status=='needs-decision' else 'No observed defect warrants model regeneration; retain finish caveats and final approval hold.',technical_scope='Fresh exact-byte packaging/CRC/required payloads, motion unit checks and offline desktop/mobile controls; no fresh Blender source parity, sampled collision or corrupt/no-JS fallback rerun.',browser=[x for x in smoke if x['id']==s],motion=[x for x in motion if x['id']==s][0],inherited_missing_gates=e['missing_gates']))
result={'schema':'boxsv-art-review/1','task':'t_e669e48c','parent_commit':'6db6388d04fee0da8e0324a640d5880a5813a39c','parent_ledger_sha256':hashlib.sha256((R/'launch-candidates.json').read_bytes()).hexdigest(),'assigned':ids,'reviewed':len(rows),'unreviewed':[],'counts':dict(collections.Counter(x['status'] for x in rows)),'changed_designs':[],'entries':rows}
(R/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'counts':result['counts'],'html_min':min(x['viewer']['bytes'] for x in rows),'html_max':max(x['viewer']['bytes'] for x in rows),'reviewed':len(rows)},indent=2))
