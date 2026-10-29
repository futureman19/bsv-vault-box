"use strict";
const fs = require("node:fs"),
  path = require("node:path"),
  os = require("node:os"),
  crypto = require("node:crypto"),
  net = require("node:net");
const { spawn, execFileSync } = require("node:child_process");
const { createRpc } = require("../node-rpc");
const HASH = "13f222f5b466fe4af2bb867628354e4ae9711a10019e89fc7bf018b90e30b3c8";
const delay = (ms) => new Promise((r) => setTimeout(r, ms));
async function startNode(evidence) {
  if (process.platform !== "linux" || !path.isAbsolute(evidence))
    throw Error("Linux and absolute evidence path required");
  if (fs.existsSync(evidence)) throw Error("Refusing to overwrite evidence");
  const base = path.join(os.homedir(), ".cache", "boxsv-mint-regtest");
  fs.mkdirSync(base, { recursive: true, mode: 0o700 });
  const data = fs.mkdtempSync(path.join(base, "run-"));
  fs.chmodSync(data, 0o700);
  const archive = path.join(data, "node.tar.gz"),
    url = "https://download.bitcoinsv.io/bitcoinsv/1.2.3/";
  execFileSync(
    "curl",
    [
      "--fail",
      "--location",
      "--silent",
      "--show-error",
      "--max-time",
      "120",
      url + "bitcoin-sv-1.2.3-x86_64-linux-gnu.tar.gz",
      "-o",
      archive,
    ],
    { timeout: 125000 }
  );
  const hash = crypto
    .createHash("sha256")
    .update(fs.readFileSync(archive))
    .digest("hex");
  if (hash !== HASH) throw Error("Archive checksum mismatch");
  execFileSync("tar", ["-xzf", archive, "-C", data], { timeout: 30000 });
  const binary = path.join(data, "bitcoin-sv-1.2.3/bin/bitcoind");
  const port = await new Promise((resolve, reject) => {
    const s = net.createServer();
    s.on("error", reject);
    s.listen(0, "127.0.0.1", () => {
      const p = s.address().port;
      s.close(() => resolve(p));
    });
  });
  const config = `regtest=1\nserver=1\nlisten=0\nconnect=0\ndnsseed=0\ndns=0\ndiscover=0\nupnp=0\ndisablewallet=1\ntxindex=1\nassumevalid=0\ngenesisactivationheight=1\nchronicleactivationheight=2\nrpcbind=127.0.0.1\nrpcallowip=127.0.0.1\nrpcport=${port}\nexcessiveblocksize=100000000\nblockmaxsize=10000000\nmaxstackmemoryusageconsensus=100000000\ncoinsdbcache=32\ndbcache=16\nminminingtxfee=0.00000001\nacceptnonstdtxn=0\nacceptnonstdoutputs=1\n`;
  fs.mkdirSync(evidence, { recursive: true });
  fs.writeFileSync(path.join(data, "bitcoin.conf"), config);
  fs.writeFileSync(path.join(evidence, "bitcoin.conf"), config);
  const guard = path.resolve(
    __dirname,
    "../../vault/scripts/bitcoind-guard.sh"
  );
  const args = [
    guard,
    binary,
    "-regtest",
    `-datadir=${data}`,
    `-conf=${data}/bitcoin.conf`,
  ];
  fs.writeFileSync(
    path.join(evidence, "provenance.json"),
    JSON.stringify(
      {
        archiveUrl: url + "bitcoin-sv-1.2.3-x86_64-linux-gnu.tar.gz",
        archiveSha256: hash,
        binarySha256: crypto
          .createHash("sha256")
          .update(fs.readFileSync(binary))
          .digest("hex"),
        guard,
        args,
        timeoutSeconds: 180,
        platform: os.platform(),
        data,
      },
      null,
      2
    ) + "\n"
  );
  const stdout = fs.openSync(path.join(evidence, "node-stdout.log"), "wx");
  const child = spawn("bash", args, {
    detached: true,
    stdio: ["ignore", stdout, stdout],
    env: { ...process.env, BOXSV_NODE_TIMEOUT: "180" },
  });
  fs.closeSync(stdout);
  let spawnError;
  child.on("error", (e) => {
    spawnError = e;
  });
  const exited = new Promise((resolve) => child.once("exit", resolve));
  const rpc = createRpc({
    url: `http://127.0.0.1:${port}`,
    cookiePath: path.join(data, "regtest/.cookie"),
    journalPath: path.join(evidence, "rpc.jsonl"),
    timeoutMs: 5000,
  });
  async function stop() {
    if (child.exitCode === null && !spawnError) {
      try {
        await rpc("stop");
      } catch {}
      await Promise.race([exited, delay(5000)]);
    }
    if (child.exitCode === null && child.pid) {
      try {
        process.kill(-child.pid, "SIGTERM");
      } catch {}
      await Promise.race([exited, delay(3000)]);
    }
    if (child.exitCode === null && child.pid) {
      try {
        process.kill(-child.pid, "SIGKILL");
      } catch {}
      await Promise.race([exited, delay(1000)]);
    }
    const nodeLog = path.join(data, "regtest/bitcoind.log");
    if (fs.existsSync(nodeLog))
      fs.copyFileSync(nodeLog, path.join(evidence, "bitcoind.log"));
    const key = path.join(data, "fixture.key");
    if (fs.existsSync(key)) fs.unlinkSync(key);
    fs.writeFileSync(
      path.join(evidence, "shutdown.json"),
      JSON.stringify({
        exitCode: child.exitCode,
        signalCode: child.signalCode,
        ownedPid: child.pid,
      }) + "\n"
    );
  }
  try {
    let ready = false;
    for (let i = 0; i < 100; i++) {
      if (spawnError || child.exitCode !== null)
        throw Error("Owned regtest node exited before ready");
      try {
        const info = await rpc("getblockchaininfo");
        if (info.chain !== "regtest") throw Error("Wrong chain");
        ready = true;
        break;
      } catch {}
      await delay(200);
    }
    if (!ready) throw Error("Regtest startup deadline");
    const network = await rpc("getnetworkinfo");
    if (!network.subversion.includes("1.2.3"))
      throw Error("Unexpected node version");
    fs.writeFileSync(
      path.join(evidence, "network.json"),
      JSON.stringify(network, null, 2) + "\n"
    );
    return { rpc, data, stop };
  } catch (e) {
    await stop();
    throw e;
  }
}
module.exports = { startNode };
