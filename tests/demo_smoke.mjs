// Smoke tests for the static web demo (demo/app.js).
// Runs under plain node --test, no dependencies: the browser script is
// loaded with require() against tiny DOM stubs, then exercised through the
// window.__slowlang hooks. Requiring (not vm-evaluating) keeps the file a
// plain static script and lets V8 coverage map back to demo/app.js.
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

function stubEl() {
  const handlers = {};
  const kids = [];
  return {
    __handlers: handlers,
    addEventListener: (type, fn) => {
      (handlers[type] ||= []).push(fn);
    },
    removeEventListener() {},
    setAttribute() {},
    focus() {},
    click: async function () {
      for (const fn of handlers.click || []) await fn();
    },
    appendChild: (c) => {
      kids.push(c);
      return c;
    },
    removeChild: (c) => {
      const i = kids.indexOf(c);
      if (i !== -1) kids.splice(i, 1);
      return c;
    },
    get firstChild() {
      return kids[0] || null;
    },
    get childCount() {
      return kids.length;
    },
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

const windowListeners = {};
globalThis.addEventListener = (type, fn) => {
  (windowListeners[type] ||= []).push(fn);
};
globalThis.removeEventListener = () => {};
globalThis.dispatchTestEvent = (type) => {
  for (const fn of windowListeners[type] || []) fn();
};

let copied = null;
Object.defineProperty(globalThis, "navigator", {
  value: {
    onLine: true,
    clipboard: {
      writeText: async (t) => {
        copied = t;
      },
    },
  },
  configurable: true,
});

const require = createRequire(import.meta.url);
require("../demo/app.js");
const api = globalThis.__slowlang;
const el = (id) => store.get(id);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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

test("run quotes pick four valid quotes", () => {
  const q = api.pickRunQuotes();
  assert.equal(q.length, 4);
  for (const line of q) assert.ok(api.compileQuotes.includes(line));
});

test("status sets mood faces", () => {
  api.setStatus("boom", "is-rage");
  assert.equal(el("status").textContent, "boom");
  assert.equal(el("mood-face").textContent, "🐢💢");
  api.setStatus("calm", "is-calm");
  assert.equal(el("mood-face").textContent, "🐢💚");
});

test("rage lockout disables the editor, counts down, then recovers", async () => {
  api.showRage();
  assert.equal(el("editor").disabled, true);
  assert.equal(el("rage").hidden, false);
  assert.ok(el("rage-count").textContent.includes("2"));
  await sleep(1100);
  assert.ok(el("rage-count").textContent.includes("1"));
  await sleep(1200);
  assert.equal(el("rage").hidden, true);
  assert.equal(el("editor").disabled, false);
});

test("run executes code, shows wisdom and restores the button", async () => {
  // Fake Pyodide: capture stdout through the real batched() callback.
  globalThis.loadPyodide = async () => ({
    setStdout: () => {},
    setStderr: () => {},
    globals: { set: () => {} },
    runPythonAsync: async () => {},
  });
  // Drive output through please(): the app wires it to write a thank-you.
  const realGlobals = { please: null };
  globalThis.loadPyodide = async () => ({
    setStdout: ({ batched }) => batched("hello from python"),
    setStderr: () => {},
    globals: { set: (name, fn) => { realGlobals[name] = fn; } },
    runPythonAsync: async () => { realGlobals.please(); },
  });
  el("editor").value = 'print("hi")';
  el("lazy-mode").checked = true; // skip the 1-in-10 lazy refusal
  await el("run-btn").click();
  assert.equal(el("run-btn").disabled, false);
  assert.equal(el("run-btn").textContent, "Run (like Python)");
  assert.ok(el("output").textContent.includes("hello from python"));
  assert.ok(el("output").textContent.includes("turtle thanks you"));
  assert.ok(el("output").textContent.includes("Poetic wisdom"));
  assert.ok(el("output").textContent.includes("🐢"));
  // A rage happened earlier in this suite, so this run resets the streak…
  assert.ok(el("streak").textContent.includes("build your gentle streak"));
  // …and a second calm run starts one.
  await el("run-btn").click();
  assert.ok(el("streak").textContent.includes("Gentle streak: 1"));
  delete globalThis.loadPyodide;
});

test("offline note toggles", () => {
  api.updateNetNote(false);
  assert.equal(el("net-note").hidden, false);
  api.updateNetNote(true);
  assert.equal(el("net-note").hidden, true);
  globalThis.dispatchTestEvent("online");
  assert.equal(el("net-note").hidden, true);
});

test("copy buttons hand text to the clipboard", async () => {
  await el("copy-btn").__handlers.click[0]();
  assert.ok(copied.includes("hello from python"));
  assert.ok(el("status").textContent.includes("witnessed it"));
  await el("haiku-btn").__handlers.click[0]();
  assert.ok(copied.includes("\n"));
  assert.ok(el("status").textContent.includes("Haiku copied"));
});

test("diary records rages and runs", () => {
  assert.ok(el("diary-summary").textContent.includes("Rage diary (3)"));
  assert.equal(el("diary-list").childCount, 3);
});
