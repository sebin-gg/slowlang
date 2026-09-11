/* TortoiseLang web demo — a faithful port of ui-fakeide.py + sarcasm_engine.py.
   Runs fully client-side. Python executes in-page via Pyodide (lazy-loaded),
   with a tiny fallback runner if the CDN is unreachable. */

"use strict";

var PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";

/* --- Sarcasm + poetry (ported from sarcasm_engine.py — do not “improve”) --- */
var LAZY_TURTLE_LINES = [
  "The turtle is napping. Try again later.",
  "Why rush? The turtle needs a break.",
  "Yawn... too much effort for the turtle."
];

var DEFAULT_LINES = [
  "Oh wow, you're a real keyboard ninja, aren't you?",
  "Slow down! The turtle’s about to sue you for emotional damage.",
  "Your keyboard called. It needs a vacation.",
  "This isn’t a Formula 1 race. It’s TortoiseLang.",
  "Congratulations! You’ve earned the ‘Too Fast, Too Curious’ award.",
  "Nice try, Shakespeare. But the turtle disagrees.",
  "Coding at warp speed? Bold. Wrong, but bold.",
  "You're typing faster than the turtle can think. Rude.",
  "Ever heard of slow food? This is slow code.",
  "Your code has officially outpaced human patience."
];

var HAIKUS = [
  "Code like a whisper,\nSoftly flowing, line by line—\nErrors fear silence.",
  "Slow and steady types,\nWisdom in every keystroke,\nThe bug stays asleep.",
  "Haste is the foe here,\nTurtles preach divine rhythm,\nPause. Now type again.",
  "A line of logic,\nNot rushed but born with meaning,\nLike rain on still ponds.",
  "In slow typing's glow,\nA turtle watches, amused,\nScripting elegance.",
  "Over the keyboard,\nFingers rush, but thoughts delay—\nTurtle shakes his head.",
  "Write one line slowly,\nRead it like a morning breeze—\nThe code flows with peace.",
  "Why do you hurry?\nThe turtle’s still on line two—\nAnd he wrote a gem.",
  "Infinite wisdom—\nLies not in speed, but in pause.\nReflect, type, repeat.",
  "The wind does not rush,\nYet moves mountains patiently.\nSo should your fingers.",
  "Beneath blinking lights,\nFast fingers breed fast errors—\nTurtle sighs again.",
  "A furious tap,\nBrings forth compiler fury—\nPatience is your shield.",
  "Racing through functions,\nSyntax collapses in fear—\nSlow is beautiful.",
  "Shift. Return. Escape.\nNone will help your case here.\nSlow down or regret.",
  "The screen glares at you,\nSilently judging your haste—\nSlow. Compose. Retry.",
  "You typed like thunder,\nthe turtle filed a complaint —\ncase still pending.",
  "Fast fingers falter,\nslow fingers ship on Friday —\nthe turtle nods.",
  "Rubber duck asleep,\nturtle awake and judging —\nexplain it slower.",
  "Zero errors found.\nThe turtle takes full credit.\nYou may thank him now.",
  "A watched pot won't boil;\nwatched code won't ship either.\nType gently anyway.",
  "Your loop ran eleven\ntimes instead of ten. Slow down.\nCount with the turtle."
];

/* --- Loader quotes (ported from sarcasm_engine.py — keep lists identical) --- */
var COMPILE_QUOTES = [
  "Waking the turtle…",
  "Brewing patience…",
  "Counting your keystrokes (slowly)…",
  "Teaching semicolons manners…",
  "Consulting ancient tortoise wisdom…",
  "Polishing haikus…",
  "Asking the compiler for a favor…",
  "Untangling your indentation…",
  "Convincing the turtle you meant that…",
  "Almost there. No rushing."
];

function compileQuote(step) {
  return COMPILE_QUOTES[step % COMPILE_QUOTES.length];
}

/* --- Turtles (ported from ascii_turtle.py) --- */
var TURTLE_RAGE = [
  "               _____     ______",
  "             < x   x >  /      \\",
  "              \\  -  /  |  O   O |",
  "              /     \\  |   ∆    |",
  "             |       | \\______/",
  "            /| |   | |\\",
  "           /_|_|___|_|_\\",
  "            /_/     \\_\\",
  "🐢 RAGE MODE: Turtle is not amused by your speed."
].join("\n");

var TURTLE_JUST_RIGHT = [
  "         _____",
  "       < ^   ^ >",
  "        \\  -  /",
  "        /     \\",
  "       |  o o  |",
  "       |   ∆   |",
  "       \\_______/",
  "🐢 Turtle is content with your pace."
].join("\n");

var TURTLE_TOO_SLOW = [
  "         _____",
  "       < -   - >",
  "        \\  _  /",
  "        /     \\",
  "       |  . .  |",
  "       |   -   |",
  "       \\_______/",
  "🐢 Turtle is falling asleep. Type a bit faster!"
].join("\n");

/* --- Python syntax data (mirrors PythonSyntaxText tags) --- */
var PY_KEYWORDS = [
  "False", "None", "True", "and", "as", "assert", "async", "await",
  "break", "class", "continue", "def", "del", "elif", "else", "except",
  "finally", "for", "from", "global", "if", "import", "in", "is",
  "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
  "try", "while", "with", "yield"
];

var PY_BUILTINS = [
  "print", "range", "len", "str", "int", "float", "list", "dict",
  "set", "tuple", "open", "input", "enumerate", "zip", "map",
  "filter", "sum", "min", "max", "abs", "round", "please"
];

/* --- DOM --- */
var editor = document.getElementById("editor");
var highlightCode = document.getElementById("highlight-code");
var highlightPane = document.getElementById("highlight");
var statusEl = document.getElementById("status");
var outputEl = document.getElementById("output");
var runBtn = document.getElementById("run-btn");
var clearBtn = document.getElementById("clear-btn");
var lazyBox = document.getElementById("lazy-mode");
var compileBox = document.getElementById("compile");
var compileLabel = document.getElementById("compile-label");
var compileFill = document.getElementById("compile-fill");
var compileWrap = document.getElementById("compile-bar-wrap");
var rageEl = document.getElementById("rage");
var introEl = document.getElementById("intro");

var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

var lastTime = performance.now() / 1000;
var turtleAngry = false;
var pyodide = null;
var pyodideFailed = false;

function pick(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function sarcasticMessage(theme) {
  if (theme === "lazy_turtle") return pick(LAZY_TURTLE_LINES);
  return pick(DEFAULT_LINES);
}

function poeticOutput() {
  return pick(HAIKUS);
}

/* --- Syntax highlighting (ports PythonSyntaxText._highlight_line) --- */
function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function highlightLine(line) {
  var commentAt = line.indexOf("#");
  var comment = "";
  var code = line;
  if (commentAt !== -1) {
    comment = line.slice(commentAt);
    code = line.slice(0, commentAt);
  }
  var re = /("[^"\n]*"|'[^'\n]*'|\b\d+\b|\b[A-Za-z_][A-Za-z0-9_]*)/g;
  // Walk the code once, wrapping tokens and escaping everything else.
  var rebuilt = "";
  var last = 0;
  re.lastIndex = 0;
  var m2;
  while ((m2 = re.exec(code)) !== null) {
    rebuilt += escapeHtml(code.slice(last, m2.index));
    var t = m2[0];
    var c = null;
    if (/^["']/.test(t)) c = "tok-string";
    else if (/^\d+$/.test(t)) c = "tok-number";
    else if (PY_KEYWORDS.indexOf(t) !== -1) c = "tok-keyword";
    else if (PY_BUILTINS.indexOf(t) !== -1) c = "tok-builtin";
    rebuilt += c
      ? '<span class="' + c + '">' + escapeHtml(t) + "</span>"
      : escapeHtml(t);
    last = m2.index + t.length;
  }
  rebuilt += escapeHtml(code.slice(last));
  if (comment) rebuilt += '<span class="tok-comment">' + escapeHtml(comment) + "</span>";
  return rebuilt || " ";
}

function refreshHighlight() {
  var lines = editor.value.split("\n").map(highlightLine);
  highlightCode.innerHTML = lines.join("\n");
  highlightPane.scrollTop = editor.scrollTop;
  highlightPane.scrollLeft = editor.scrollLeft;
}

function setStatus(text, mood) {
  statusEl.textContent = text;
  statusEl.classList.remove("is-rage", "is-calm", "is-steady");
  if (mood) statusEl.classList.add(mood);
}

/* --- Turtle rage lockout (ports show_turtle_rage_window) --- */
var rageTimer = null;

function showRage() {
  if (!rageEl.hidden) return;
  rageEl.hidden = false;
  turtleAngry = true;
  editor.disabled = true;
  clearTimeout(rageTimer);
  rageTimer = setTimeout(calmTurtle, 2000);
}

function calmTurtle() {
  rageEl.hidden = true;
  turtleAngry = false;
  editor.disabled = false;
  editor.focus();
}

/* --- Typing-speed enforcement (ports TortoiseIDE.track_speed) --- */
editor.addEventListener("keydown", function () {
  if (turtleAngry) return;
  var now = performance.now() / 1000;
  var delta = now - lastTime;
  lastTime = now;
  if (lazyBox.checked) delta *= 2; // lazy mode forgives, like the desktop IDE

  if (delta < 0.1) {
    setStatus(sarcasticMessage("lazy_turtle"), "is-rage");
    showRage();
  } else if (delta > 0.5) {
    setStatus("You’re calm. The turtle is proud 🐢", "is-calm");
  } else {
    setStatus("Steady typing…", "is-steady");
  }
});

editor.addEventListener("input", refreshHighlight);
editor.addEventListener("scroll", function () {
  highlightPane.scrollTop = editor.scrollTop;
  highlightPane.scrollLeft = editor.scrollLeft;
});

/* Smart indent on Enter (ports _on_return, simplified for the web). */
editor.addEventListener("keydown", function (ev) {
  if (ev.key !== "Enter" || turtleAngry) return;
  ev.preventDefault();
  var pos = editor.selectionStart;
  var text = editor.value;
  var lineStart = text.lastIndexOf("\n", pos - 1) + 1;
  var prevLine = text.slice(lineStart, pos);
  var indent = (prevLine.match(/^ */) || [""])[0].length;
  if (/:\s*$/.test(prevLine)) indent += 4;
  var insert = "\n" + " ".repeat(indent);
  editor.setRangeText(insert, pos, editor.selectionEnd, "end");
  refreshHighlight();
  // Count the inserted newline as a calm keystroke, not a rage spike.
  lastTime = performance.now() / 1000;
});

/* --- Fake compile bar (ports fake_loading) --- */
function fakeCompile() {
  compileBox.hidden = false;
  if (reduceMotion) {
    compileFill.style.width = "100%";
    compileWrap.setAttribute("aria-valuenow", "10");
    compileLabel.textContent = compileQuote(COMPILE_QUOTES.length - 1);
    return Promise.resolve();
  }
  return new Promise(function (resolve) {
    var i = 0;
    compileFill.style.width = "0%";
    compileLabel.textContent = compileQuote(0);
    var tick = setInterval(function () {
      i += 1;
      compileFill.style.width = (i * 10) + "%";
      compileWrap.setAttribute("aria-valuenow", String(i));
      compileLabel.textContent = compileQuote(i - 1);
      if (i >= 10) {
        clearInterval(tick);
        resolve();
      }
    }, 150);
  });
}

/* --- Code execution --- */
function loadScript(src) {
  return new Promise(function (resolve, reject) {
    var s = document.createElement("script");
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

async function runWithPyodide(code) {
  if (!window.loadPyodide) await loadScript(PYODIDE_URL);
  if (!pyodide) pyodide = await window.loadPyodide();
  var out = "";
  pyodide.setStdout({ batched: function (s) { out += s + "\n"; } });
  pyodide.setStderr({ batched: function (s) { out += s + "\n"; } });
  pyodide.globals.set("please", function () {
    out += "🙏 The turtle thanks you for your politeness.\n";
  });
  await pyodide.runPythonAsync(code);
  return out;
}

/* Minimal fallback when Pyodide/the CDN is unreachable: handles the
   constructs used in the sample (print, for i in range(n), please). */
function runWithFallback(code) {
  var lines = code.split("\n");
  var out = "";
  var vars = { please: function () { out += "🙏 The turtle thanks you for your politeness.\n"; } };

  function evalPrint(expr, scope) {
    expr = expr.trim();
    var str = expr.match(/^["'](.*)["']$/);
    if (str) return str[1];
    if (/^-?\d+$/.test(expr)) return expr;
    if (Object.prototype.hasOwnProperty.call(scope, expr)) return String(scope[expr]);
    throw new Error("the fallback runner only understands print(\"…\"), print(number) and print(variable). Connect to the net for full Python.");
  }

  function execBlock(block, scope) {
    for (var k = 0; k < block.length; k++) {
      var raw = block[k];
      var line = raw.trim();
      if (!line || line.startsWith("#")) continue;
      var pr = line.match(/^print\((.*)\)$/);
      if (pr) {
        out += evalPrint(pr[1], scope) + "\n";
        continue;
      }
      if (line === "please()") {
        vars.please();
        continue;
      }
      var loop = line.match(/^for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+range\((\d+)\):$/);
      if (loop) {
        var name = loop[1];
        var n = parseInt(loop[2], 10);
        var indent = raw.match(/^ */)[0].length;
        var body = [];
        k++;
        while (k < block.length && (/^\s*$/.test(block[k]) || block[k].match(/^ */)[0].length > indent)) {
          body.push(block[k].replace(new RegExp("^ {0," + (indent + 4) + "}"), ""));
          k++;
        }
        k--;
        for (var i = 0; i < n; i++) {
          var child = Object.create(scope);
          child[name] = i;
          execBlock(body, child);
        }
        continue;
      }
      throw new Error("the fallback runner got stuck on: " + line);
    }
  }

  execBlock(lines, Object.create(vars));
  return { text: out, fallback: true };
}

runBtn.addEventListener("click", async function () {
  if (turtleAngry) return;
  // 10% lazy refusal, unless Lazy Mode is on (ports run_code).
  if (Math.random() < 0.1 && !lazyBox.checked) {
    outputEl.textContent = "🐢 The turtle is feeling lazy and refuses to run your code right now. Try again!";
    outputEl.classList.add("output-error");
    return;
  }
  outputEl.classList.remove("output-error");
  runBtn.disabled = true;
  runBtn.textContent = "Running…";
  setStatus("Running your code… the turtle is on it 🐢", "is-steady");
  try {
    await fakeCompile();
    var code = editor.value;
    var result = "";
    var usedFallback = false;
    if (!pyodideFailed) {
      try {
        result = await runWithPyodide(code);
      } catch (err) {
        pyodideFailed = true;
        var fb = runWithFallback(code);
        result = fb.text;
        usedFallback = true;
      }
    } else {
      result = runWithFallback(code).text;
      usedFallback = true;
    }
    var text = result || "(no output — the turtle heard nothing)\n";
    text += "\n✨ Poetic wisdom:\n" + poeticOutput() + "\n";
    // Turtle mood roll (ports run_code’s 20/30/50 split).
    var roll = Math.random();
    text += "\n" + (roll < 0.2 ? TURTLE_RAGE : roll < 0.5 ? TURTLE_TOO_SLOW : TURTLE_JUST_RIGHT) + "\n";
    if (usedFallback) {
      text += "\n(note: full Python couldn’t load, so the tiny offline runner stepped in)\n";
    }
    outputEl.textContent = text;
  } catch (err) {
    var msg = err && err.message ? err.message : String(err);
    // Mirror the desktop IDE: show the error, then the wisdom anyway.
    outputEl.textContent = "Error: " + msg + "\n\n✨ Poetic wisdom:\n" + poeticOutput() + "\n";
    outputEl.classList.add("output-error");
  } finally {
    compileBox.hidden = true;
    compileFill.style.width = "0%";
    compileWrap.setAttribute("aria-valuenow", "0");
    compileLabel.textContent = "Compiling slowly…";
    runBtn.disabled = false;
    runBtn.textContent = "Run (like Python)";
  }
});

clearBtn.addEventListener("click", function () {
  outputEl.textContent = "Slow and steady… output lands here.";
  outputEl.classList.remove("output-error");
  editor.focus();
});

/* --- Init --- */
refreshHighlight();
if (typeof introEl.showModal === "function") {
  introEl.showModal();
}

/* Test hooks (harmless in the browser; lets future agents unit-test the port). */
if (typeof window !== "undefined") {
  window.__slowlang = {
    runWithFallback: runWithFallback,
    highlightLine: highlightLine,
    sarcasticMessage: sarcasticMessage,
    poeticOutput: poeticOutput,
    compileQuote: compileQuote,
    compileQuotes: COMPILE_QUOTES
  };
}
