# Independent rehearsal review

Reviewer: `deleg_9e60f944`; read-only review at integrated HEAD c03e292, with new rehearsal evidence and browser output-path change. No node startup or external network, keys, funds or board mutations by reviewer.

**Verdict: bounded layered rehearsal PASS, with visual/evidence qualifications. Production launch HOLD.** Not third-party certification or proof of a continuous production mint.

Independently reran `node evidence/rehearsal/audit-regtest.js`: PASS. Five custody transactions, six sponsor preparations, exact RPC bytes, VM validation, block membership and final UTXO snapshots; old-owner mandatory Script rejection. Fees 2,500 custody sats plus 3,000 preparation sats. Other test logs reviewed, not rerun independently.

Reviewed actual images with vision: web/box-inspect-320.png, web/image-failure-mobile.png, claw/mobile-reveal.png (also full-resolution crop), claw/desktop-reveal.png, claw/no-webgl.png, wallet-success.png.

Required integration holds:
- Allocation -> actual collectible NFT binding is unimplemented/unproven. Uganda simulation has serializedTransaction:null, unsigned detached certificate and custody verification false. Regtest generic text ordinal and separate signed Iceland VM proof are different fixtures.
- Real wallet signing is unimplemented/unproven. Four identity-only mocks do not prove extension compatibility or transaction authorization.

Visual limitations:
- Narrow Box and failure dialogs retain readable simulation/promotional-art disclosures; no obvious clipped action controls.
- Dimmed game text shows through behind mobile prize disclosure, reducing clarity.
- desktop-reveal.png is overwritten by later race-test capture before delayed prize card settles; it is not proof of settled desktop reveal.
- Full-page screenshots contain blank lazy-gallery areas; these screenshots alone cannot distinguish lazy capture timing from asset failures. Do not claim gallery completeness from them.
- Desktop/emulated mobile only, not physical-phone acceptance.

Preserve 73 art/package review holds, 128 limited candidates, zero final approvals; USA star continuation unresolved/unapproved. Sale terms, fair production randomness, integrated custody/wallet flow, storage, public-chain compatibility, independent security and release authorization remain held. Reuse remains UI-only.
