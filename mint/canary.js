"use strict";
// Hard limits: never read these from config or environment.
const CAPS = Object.freeze({
  pool: 250000,
  prep: 100000,
  fee: 10000,
  price: 10000,
  paymentMultiple: 2,
  inventory: 2,
});
function policy({ chain = "regtest", canary = false } = {}) {
  if (!["regtest", "testnet", "mainnet"].includes(chain))
    throw Error("Invalid chain policy");
  if (chain === "mainnet" && canary !== true)
    throw Error("Mainnet requires canary: true");
  return Object.freeze({
    chain,
    canary: chain === "mainnet",
    network: chain === "mainnet" ? "livenet" : "testnet",
    rpcChain: { regtest: "regtest", testnet: "test", mainnet: "main" }[chain],
  });
}
function bind(target, options) {
  const p = policy(options);
  Object.defineProperty(target, "policy", { value: p, enumerable: true });
  return p;
}
function cap(p, name, n) {
  if (p.canary && (!Number.isSafeInteger(n) || n < 0 || n > CAPS[name]))
    throw Error("Canary " + name + " cap exceeded");
}
function price(p, n) {
  cap(p, "price", n);
  if (p.canary && n < 1) throw Error("Canary price must be positive");
}
function overpaid(p, amount, value) {
  price(p, value);
  return p.canary && amount > CAPS.paymentMultiple * value;
}
function box(p, b) {
  if (!p.canary) return;
  price(p, b.priceSats);
  if (
    b.payment &&
    overpaid(p, b.payment.satoshis, b.priceSats) &&
    !(
      ["EXPIRED", "TRANSFERRED", "OPENED"].includes(b.state) &&
      b.refundRequired === true
    )
  )
    throw Error("Canary payment cap exceeded");
}
function inventory(p, rows) {
  cap(p, "inventory", rows.length);
  for (const b of rows) box(p, b);
}
function match(p, component) {
  if (component?.policy && component.policy.chain !== p.chain)
    throw Error("Component chain policy mismatch");
  if (p.canary && !component?.policy)
    throw Error("Canary component requires explicit chain policy");
}
function chain(p, actual) {
  if (actual !== p.rpcChain) throw Error(p.chain + " only: chain mismatch");
}
// This phase is READ ONLY on mainnet. No config flag can arm broadcasting.
function broadcast(p) {
  if (p.canary)
    throw Error(
      "Mainnet broadcasts disabled in phase 3b; owner-gated funded phase required"
    );
}
module.exports = Object.freeze({
  CAPS,
  policy,
  bind,
  cap,
  price,
  overpaid,
  box,
  inventory,
  match,
  chain,
  broadcast,
});
