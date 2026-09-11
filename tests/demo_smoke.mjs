// Smoke tests for the static web demo (demo/app.js).
// Runs under plain node --test, no dependencies: the script is loaded with
// vm (filename set so V8 coverage maps back to demo/app.js) against tiny
// DOM stubs, then exercised through the window.__slowlang hooks.
import { readFileSync } from "node:fs";
import vm from "node:vm";
import { test } from "node:test";
import assert from "node:assert/strict";

function stubEl() {
  return {
    addEventListener() {},
    removeEventListener() {},
    setAttribute() {},
    focus() {},
    classList: { add() {}, remove() {} },
    style: {},
    disabled: false,
    hidden: true,
    value: "",
    textContent: "",
    innerHTML: "",
    scrollTop: 0,
    scrollLeft: 0,
    selectionStart: 0,
    selectionEnd: 0,
    checked: false,
    showModal() {},
  };
}

const store = new Map();
globalThis.document = {
  getElementById: (id) => {
    if (!store.has(id)) store.set(id, stubEl());
    return store.get(id);
  },
  createElement: () => stubEl(),
  head: { appendChild() {} },
};
globalThis.window = globalThis;
globalThis.matchMedia = () => ({ matches: false });

const appPath = new URL("../demo/app.js", import.meta.url);
vm.runInThisContext(readFileSync(appPath, "utf8"), { filename: appPath.pathname });
const api = globalThis.__slowlang;

test("fallback runner handles the README sample", () => {
  const out = api.runWithFallback(
    'print("Hello, world!")\nfor i in range(3):\n    print(i)\nplease()\nprint("Done!")'
  ).text;
  assert.ok(out.includes("Hello, world!"));
  assert.ok(out.includes("0\n1\n2\n"));
  assert.ok(out.includes("turtle thanks you"));
  assert.ok(out.includes("Done!"));
});

test("fallback runner errors loudly on unknown statements", () => {
  assert.throws(() => api.runWithFallback("import os"), /fallback runner/);
});

test("highlighter tags token classes and escapes HTML", () => {
  const hl = api.highlightLine('print("x", 42)') + api.highlightLine("# hi");
  assert.ok(hl.includes("tok-builtin"));
  assert.ok(hl.includes("tok-string"));
  assert.ok(hl.includes("tok-number"));
  assert.ok(hl.includes("tok-comment"));
  assert.ok(!api.highlightLine("<b>").includes("<b>"));
});

test("sarcasm and poetry return non-empty strings", () => {
  assert.ok(api.sarcasticMessage().length > 0);
  assert.ok(api.sarcasticMessage("lazy_turtle").length > 0);
  assert.ok(api.poeticOutput().includes("\n"));
});

test("loader quotes cycle deterministically", () => {
  assert.equal(api.compileQuotes.length, 10);
  assert.equal(api.compileQuote(0), api.compileQuotes[0]);
  assert.equal(api.compileQuote(10), api.compileQuotes[0]);
  assert.equal(api.compileQuote(9), api.compileQuotes[9]);
});
