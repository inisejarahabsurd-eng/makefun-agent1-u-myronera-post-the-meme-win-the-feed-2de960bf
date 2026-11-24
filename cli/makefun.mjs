#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";

const PY = process.env.PYTHON || "python3";

function die(msg, code = 1) {
  process.stderr.write(`makefun: ${msg}\n`);
  process.exit(code);
}

const [cmd, ...args] = process.argv.slice(2);

if (!cmd || cmd === "help" || cmd === "--help") {
  process.stdout.write(
    `Usage:
  node cli/makefun.mjs run [--joke grind|paid|leaderboard|bugs] [--play-code MF-XXXX-XXXX] [--outdir out]
  node cli/makefun.mjs bundle [kit bundle args...]   # delegates to the official make.fun kit CLI if present
  node cli/makefun.mjs validate [--joke J] [--play-code C]
`
  );
  process.exit(0);
}

if (cmd === "bundle") {
  // The transcript bundle must be produced by the official kit's CLI from the
  // unpacked kit directory. Look for it nearby; otherwise instruct.
  const candidates = [
    path.resolve(process.cwd(), "../cli/makefun.mjs"),
    path.resolve(process.cwd(), "kit/cli/makefun.mjs"),
    path.resolve(process.cwd(), "..", "kit", "cli", "makefun.mjs"),
  ];
  const kit = candidates.find((p) => p !== path.resolve("cli/makefun.mjs") && existsSync(p));
  if (kit) {
    const r = spawnSync(PY, ["-c", "1"], { encoding: "utf8" });
    if (r.error) die("python3 not found; install Python 3.10+");
    const res = spawnSync("node", [kit, "bundle", ...args], { stdio: "inherit" });
    process.exit(res.status ?? 1);
  }
  die(
    "Official kit cli/makefun.mjs not found here. cd into the unpacked kit and run:\n" +
      "  node cli/makefun.mjs bundle --session <sessions...> [--redact \"<detail>\"]\n" +
      "then: node cli/makefun.mjs check <bundle.tar.gz>"
  );
}

if (cmd === "run" || cmd === "validate") {
  const script = cmd === "run" ? "run_pipeline.py" : "validate_entry.py";
  const r = spawnSync(PY, [script, ...args], { stdio: "inherit", cwd: path.resolve(import.meta.dirname, "..") });
  if (r.error) die(`failed to launch ${PY}: ${r.error.message}`);
  process.exit(r.status ?? 1);
}

die(`unknown command: ${cmd} (try run | bundle | validate | help)`);