"use strict";
const fs = require("node:fs"),
  path = require("node:path");
const { bsv } = require("../vault/src/ordinal-pair");
// Key material only from an owned POSIX file, never argv/env.
function loadKey(file) {
  if (process.platform === "win32")
    throw Error("POSIX 0600 key custody required; use Linux/WSL");
  if (typeof file !== "string" || !path.isAbsolute(file))
    throw Error("Absolute key file path required");
  let fd;
  try {
    fd = fs.openSync(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
    const st = fs.fstatSync(fd);
    if (
      !st.isFile() ||
      (st.mode & 0o777) !== 0o600 ||
      st.uid !== process.getuid() ||
      st.nlink !== 1 ||
      st.size > 128
    )
      throw Error("Key file must be owned, regular, single-link, 0600");
    const text = fs.readFileSync(fd, "utf8").trim();
    let decoded;
    try {
      decoded = bsv.encoding.Base58Check.decode(text);
    } catch {
      throw Error("Invalid key file");
    }
    if (decoded[0] !== 0xef) throw Error("Only testnet-prefix keys accepted");
    if (decoded.length !== 34 || decoded[33] !== 1)
      throw Error("Compressed testnet key required");
    try {
      return bsv.PrivateKey.fromWIF(text);
    } catch {
      throw Error("Invalid key file");
    }
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
  }
}
module.exports = { loadKey };
