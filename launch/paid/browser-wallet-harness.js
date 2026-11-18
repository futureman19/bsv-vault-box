'use strict';
// Test-only page helper. Load AFTER both self-contained bundles, never in live mode.
window.BoxSVBrowserWalletHarness={start(root){
 const fixture=window.BoxSVBrowserWalletFixture.createFixtureProvider();
 const ui=window.BoxSVBrowserWallet.mount({root,getWallet:()=>fixture.wallet,network:'test',label:'PUBLIC scalar-2 fixture (not extension)'});
 return {...ui,fixture};
}};
if(document.querySelector('[data-boxsv-fixture-harness]'))window.walletHarness=window.BoxSVBrowserWalletHarness.start(document.querySelector('[data-boxsv-fixture-harness]'));
