"use strict";
const http = require("node:http");
function view(b) {
  if (!b) return null;
  const {
    id,
    state,
    payAddress,
    buyerPubkey,
    priceSats,
    expiresAt,
    refundRequired,
  } = b;
  return {
    id,
    state,
    payAddress,
    buyerPubkey,
    priceSats,
    expiresAt,
    refundRequired,
    transferTxid: b.transfer?.txid || null,
  };
}
function createService({
  store,
  inventory = [],
  host = "127.0.0.1",
  reservationMs = 900000,
  now = Date.now,
} = {}) {
  if (!["127.0.0.1", "::1"].includes(host)) throw Error("Loopback bind only");
  const started = now();
  const server = http.createServer(async (req, res) => {
    const send = (code, obj) => {
      res.writeHead(code, {
        "content-type": "application/json",
        "cache-control": "no-store",
      });
      res.end(JSON.stringify(obj) + "\n");
    };
    try {
      const url = new URL(req.url, "http://localhost"),
        route = url.pathname;
      if (req.headers.origin)
        return send(403, { error: "browser origin not allowed" });
      if (route === "/health")
        return req.method === "GET"
          ? send(200, {
              ok: true,
              service: "boxsv-mint",
              version: "0.2.0-regtest",
              uptimeSec: Math.floor((now() - started) / 1000),
            })
          : send(405, { error: "method not allowed" });
      if (route === "/v1/boxes") {
        if (req.method === "GET")
          return send(200, { boxes: store.all().map(view) });
        if (req.method !== "POST")
          return send(405, { error: "method not allowed" });
        let body = "",
          size = 0;
        for await (const chunk of req) {
          size += chunk.length;
          if (size > 4096) return send(413, { error: "body too large" });
          body += chunk;
        }
        const input = body ? JSON.parse(body) : {};
        if (
          !input ||
          Array.isArray(input) ||
          typeof input !== "object" ||
          Object.keys(input).some((k) => !["id", "buyerPubkey"].includes(k))
        )
          return send(400, { error: "invalid fields" });
        // Empty POST retains skeleton listing contract, but only real configured inventory.
        if (!Object.keys(input).length) {
          const next = inventory.find(
            (i) => !store.all().some((b) => b.inventoryId === i.inventoryId)
          );
          if (!next) return send(409, { error: "inventory empty" });
          return send(201, view(store.list(next)));
        }
        if (
          typeof input.id !== "string" ||
          typeof input.buyerPubkey !== "string"
        )
          return send(400, { error: "id and buyerPubkey required" });
        return send(
          201,
          view(
            store.reserve(input.id, input.buyerPubkey, now() + reservationMs)
          )
        );
      }
      const m = /^\/v1\/boxes\/([\w-]+)$/.exec(route);
      if (m) {
        if (req.method !== "GET")
          return send(405, { error: "method not allowed" });
        let b;
        try {
          b = store.get(m[1]);
        } catch {}
        return b ? send(200, view(b)) : send(404, { error: "not found" });
      }
      return send(404, { error: "not found" });
    } catch {
      if (!res.headersSent)
        send(400, { error: "invalid request or unavailable state" });
      else res.destroy();
    }
  });
  server.requestTimeout = 10000;
  server.headersTimeout = 10000;
  return {
    listen: (port = 8090) =>
      new Promise((resolve, reject) => {
        server.once("error", reject);
        server.listen(port, host, () => {
          server.removeListener("error", reject);
          resolve();
        });
      }),
    address: () => server.address(),
    close: () =>
      new Promise((resolve, reject) =>
        server.close((e) => (e ? reject(e) : resolve()))
      ),
  };
}
module.exports = { createService };
