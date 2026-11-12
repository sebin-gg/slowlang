// Smoke tests for bin/slowlang.js — the joke politeness-check CLI.
// Requiring (not spawning) keeps V8 coverage mapped back to bin/slowlang.js.
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const require = createRequire(import.meta.url);
const { main, checkPleases } = require("../bin/slowlang.js");

function capture(fn) {
  const out = [];
  const orig = console.log;
  console.log = (s) => out.push(String(s));
  try {
    const code = fn();
    return { code, out: out.join("\n") };
  } finally {
    console.log = orig;
  }
}

function tmpFile(contents, ext = ".slow") {
  const p = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "slowlang-")), "f" + ext);
  fs.writeFileSync(p, contents);
  return p;
}

test("usage error with no file arg", () => {
  const { code, out } = capture(() => main(["node", "slowlang"]));
  assert.equal(code, 1);
  assert.match(out, /Usage: slowlang/);
});

test("usage error on wrong extension", () => {
  const { code } = capture(() => main(["node", "slowlang", "x.txt"]));
  assert.equal(code, 1);
});

test("missing file reports turtle search", () => {
  const { code, out } = capture(() => main(["node", "slowlang", "nope.slow"]));
  assert.equal(code, 1);
  assert.match(out, /No such file/);
});

test("lazy refusal path when rng < 0.1", () => {
  const f = tmpFile("please()\n");
  const { code, out } = capture(() => main(["node", "slowlang", f], () => 0.05));
  assert.equal(code, 0);
  assert.match(out, /refuses to run/);
});

test("rude code gets refused politely", () => {
  const f = tmpFile(Array(20).fill("print('hi')").join("\n"));
  const { code, out } = capture(() => main(["node", "slowlang", f], () => 0.5));
  assert.equal(code, 0);
  assert.match(out, /too rude|Refusing to run rude code/);
});

test("polite code passes the check", () => {
  const f = tmpFile(Array(20).fill("please()").join("\n"));
  const { code, out } = capture(() => main(["node", "slowlang", f], () => 0.5));
  assert.equal(code, 0);
  assert.match(out, /Politeness check passed/);
});

test("checkPleases true on polite, false on rude", () => {
  assert.equal(checkPleases(Array(20).fill("please()")), true);
  assert.equal(checkPleases(Array(20).fill("print('hi')")), false);
});
