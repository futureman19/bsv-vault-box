# Browser WalletInterface integration (parent handoff)

## Build and verified scope

From `launch/paid`: `npm ci --ignore-scripts --no-audit --no-fund`, `npm run build:wallet`, `npm run test:wallet`.
From repo root: `python launch/paid/browser-wallet-qa.py` (Playwright + installed Edge).
Pinned SDK **4.1.1**, esbuild **0.28.2**. Both checked-in `.bundle.js` files are self-contained, no CDN. Live bundle imports existing `wallet.js` unchanged and SDK primitives; the fixture bundle is separate.

The bridge is **one active browser/session per bridge instance**, ephemeral, fail-closed on restart. This is local-app plumbing, not a multi-tenant authentication service. Keep loopback Host / exact Origin / JSON protections and CSP. Public connect metadata is not proof of key possession; successful signatures supply proof. Do not publish or fund based solely on connect.

## Parent server integration (no parent files modified here)

```js
const { SigningBridge } = require('./signing-bridge');
const bridge = new SigningBridge({ network: 'test', timeoutMs: 60000 });
// FIRST in HTTP router, before existing GET/POST fallback:
if (await bridge.handle(req, res, { origin: url })) return;
```

`handle` returns false when route isn't `/api/wallet/*`, otherwise sends a JSON response and returns true. All routes are POST: `/connect` `{session}`; `/pending` `{}`; `/approve` `{envelope}`; `/signature` `{envelope,signature}`; `/disconnect` `{}`. All require exact Origin, Host, `Content-Type: application/json`, `X-BoxSV-Demo: 1`. Except connect, also require `X-BoxSV-Wallet-Session` token. Connect response is `{session,generation,token}`. Never put token into public evidence or persistent state.

After browser Connect, parent must bind `bridge.session.publicKey` (not hardcoded key2) into its trusted policy/binding and rebuild its custody adapter using that public session. Existing buyer-bound persisted state must **not** silently migrate to a different buyer. Do not create or authorize actions until the parent has persisted/validated its binding. If this needs to happen before `/connect` responds, implement that route in parent using `bridge.connect(session)` and perform the trusted binding update before sending the result; mount `bridge.handle` for the remaining routes.

```js
const custody = new CustodyWallet({
  transport: bridge, session: bridge.session,
  binding: trustedBinding, getState, sponsor, getFunding, sellerWallet
});
engine.wallet = {
  request: r => bridge.withRequest(r, () => custody.request(r))
};
```

**Wrap the full `custody.request(r)`**, not a reconstructed `{key,action}`. `withRequest` captures canonical SHA256 of the entire original JSON request and its buyer binding. `signHash` then queues each exact server-generated digest with UUID, generation, action/key, full request, request digest, and session. Existing custody adapter controls hashes; browser cannot submit a new digest. Keep the engine's trusted-state validation and existing custody signature/VM checks. `bridge.session` provides the transport session shape custody expects. `bridge.invalidate(reason)` rejects pending work and clears session. Parent shutdown must call it.

The HTTP action request can remain pending while independent `/pending` polling and explicit Approve clicks finish signatures. Do not disable the wallet approval UI while awaiting the action endpoint. Open/Withdraw require **multiple separate approvals**, one per queued signature, including final response attestation. Do not auto-approve loops. Polling never authenticates or signs.

## Parent browser integration

Serve `/browser-wallet.bundle.js` as same-origin JavaScript, load before parent app initialization. Global:

```js
const ui = BoxSVBrowserWallet.mount({
  root: document.querySelector('#wallet-controls'), network: 'test',
  getWallet: () => explicitlySelectedWalletInterface,
  label: 'Selected WalletInterface'
});
// ui.client.connection = {session,generation,token}; public session only for binding
// ui.client: connect(), poll(), approve(), cancel(), disconnect(), accountChanged()
// ui.dispose(): removes polling/UI and disconnects
```

`mount` supplies distinct Connect and Approve buttons plus Cancel/disconnect, and displays the complete pending envelope. Construction performs **zero provider calls**. `getWallet` is invoked only on Connect. It may return a Promise. Wire an actually supported provider account/network-change event to `ui.client.accountChanged()`; do not guess extension event names. Independently, actual YoursTransport rechecks network + identity + derived self key before and after every signature and rejects late changed-account results.

For custom UI, `new BoxSVBrowserWallet.BrowserWallet({getWallet, network, onChange})`; connect from Connect click, poll while connected, approve only from a **separate explicit click** after rendering pending consent. Errors must be displayed, not converted to success. The class also exposes SDK `verify` through the global for diagnostics.

### Provider compatibility boundary

The adapter consumes a **real WalletInterface object**, including an object supplied by an externally integrated/pinned `@1sat/connect` connection. It does not guess connect-package return shapes or inject a legacy `window.yours` wrapper. For a known CWI-generation extension, parent may explicitly pass `getWallet: () => window.CWI` **only after verifying that installed version supports CWI**. No installed-extension compatibility or actual permissions are claimed here. The supported wire calls are those in existing YoursTransport: `waitForAuthentication({})`, `getNetwork({})`, identity `getPublicKey`, derived `getPublicKey` with `{protocolID:[1,'boxsv covenant'],keyID:'paid-delivery-v1',counterparty:'self',forSelf:true}`, and `createSignature` with the same derivation and exactly 32 `hashToDirectlySign` bytes. No broadcast/createAction/signAction calls.

## Explicit browser fixture mode

Only in explicit fixture mode also serve/load `/browser-wallet-fixture.bundle.js`. Global:

```js
const fixture = BoxSVBrowserWalletFixture.createFixtureProvider();
// fixture.wallet implements exact WalletInterface arguments; scalar 2 is PUBLIC test data
const ui = BoxSVBrowserWallet.mount({root, getWallet:()=>fixture.wallet,
  network:'test', label:'PUBLIC scalar-2 fixture (not extension)'});
```

Fixture never reads any extension global. Its derived fixture key and identity are scalar2's public key by design (not a claim to implement BRC42 derivation). `fixture.calls`, `.control.mode` (`ok`, `reject`, `malicious`, `account-switch`, `wrong-network`) and `.control.delayMs` support fault tests. `browser-wallet-harness.js` offers `BoxSVBrowserWalletHarness.start(root)` returning `{client,dispose,fixture}`; it auto-mounts only if its explicit `[data-boxsv-fixture-harness]` marker exists. **Do not load fixture/harness scripts in live mode.**

`node launch/paid/browser-wallet-harness-server.js` runs a separate loopback-only fixture page on an ephemeral port. This standalone harness does not exercise paid engine/payment orchestration; parent full-app tests remain required. Its only queued digest is the server-fixed public test hash.

## Verification evidence

Nine Node tests execute the actual minified browser bundles in a browser-like VM, use a real loopback HTTP bridge, and verify approval separation, exact envelopes, no replay/unsolicited response, timeout/disconnect, wrong account, malicious DER, and Origin/session guards. Malicious DER is rejected **before any `/signature` POST**, proving browser-local checking rather than server-only verification.

The Playwright helper exercised fresh headless Edge with restrictive CSP, zero installed user-profile extensions, actual Connect and Approve clicks, one scalar2 signature through bundled YoursTransport, successful server verification, then disconnect. External requests and page errors were empty. No real authorization, keys, wallet funds, broadcast, deploy, or commits were used.
