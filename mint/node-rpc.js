"use strict";
const fs = require("node:fs"),
  path = require("node:path");
function createRpc({ url, cookiePath, journalPath, timeoutMs = 30000 }) {
  const target = new URL(url);
  if (
    target.protocol !== "http:" ||
    !["127.0.0.1", "[::1]"].includes(target.hostname) ||
    target.username ||
    target.password ||
    target.pathname !== "/" ||
    target.search ||
    target.hash
  )
    throw Error("Loopback HTTP RPC only");
  if (!path.isAbsolute(cookiePath))
    throw Error("Absolute cookie path required");
  if (!Number.isSafeInteger(timeoutMs) || timeoutMs < 1)
    throw Error("Invalid RPC timeout");
  let id = 0;
  return async function rpc(method, params = []) {
    const requestId = ++id;
    const cookie = fs.readFileSync(cookiePath, "utf8").trim();
    const response = await fetch(target, {
      method: "POST",
      redirect: "error",
      headers: {
        Authorization: "Basic " + Buffer.from(cookie).toString("base64"),
        "content-type": "application/json",
      },
      body: JSON.stringify({ jsonrpc: "1.0", id: requestId, method, params }),
      signal: AbortSignal.timeout(timeoutMs),
    });
    const body = await response.json();
    if (body.id !== requestId) throw Error("RPC response id mismatch");
    if (journalPath)
      fs.appendFileSync(
        journalPath,
        JSON.stringify({ method, params, response: body }) + "\n"
      );
    if (body.error) {
      const e = Error("RPC " + method + " failed (" + body.error.code + ")");
      e.code = body.error.code;
      throw e;
    }
    if (!response.ok) throw Error("RPC HTTP failure");
    return body.result;
  };
}
module.exports = { createRpc };
