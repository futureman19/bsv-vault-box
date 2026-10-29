"use strict";
const fs = require("node:fs"),
  path = require("node:path"),
  os = require("node:os"),
  { spawnSync } = require("node:child_process");
if (process.platform === "win32") {
  const file = __filename
    .replaceAll("\\", "/")
    .replace(/^([A-Za-z]):/, (_, d) => "/mnt/" + d.toLowerCase());
  const r = spawnSync(
    "wsl.exe",
    ["-e", "bash", "-lc", 'exec node "$@"', "mint-tests", file],
    { stdio: "inherit", timeout: 60000 }
  );
  process.exit(r.status ?? 1);
}
const base = path.join(os.homedir(), ".cache", "boxsv-mint-tests");
fs.mkdirSync(base, { recursive: true });
const dir = fs.mkdtempSync(path.join(base, "run-"));
try {
  const files = fs
    .readdirSync(__dirname)
    .filter((n) => n.endsWith(".test.js"))
    .sort()
    .map((n) => path.join(__dirname, n));
  const r = spawnSync(process.execPath, ["--test", ...files], {
    stdio: "inherit",
    timeout: 60000,
    env: { ...process.env, TMPDIR: dir },
  });
  process.exitCode = r.status ?? 1;
} finally {
  fs.rmSync(dir, { recursive: true, force: true });
}
