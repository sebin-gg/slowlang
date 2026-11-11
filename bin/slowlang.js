#!/usr/bin/env node
/* SlowLang joke CLI - checks your .slow file for politeness and laziness.
   Actual execution is Python's job: `pip install slowlang` or use the
   zero-install web demo at https://sebin-gg.github.io/slowlang/ */

"use strict";

const fs = require("fs");
const crypto = require("crypto");

// Lines reused verbatim from demo/app.js (content lives there + sarcasm_engine.py)
const LAZY_TURTLE_LINES = [
  "The turtle is napping. Try again later.",
  "Why rush? The turtle needs a break.",
  "Yawn... too much effort for the turtle."
];
const HAIKU =
  "Zero errors found.\nThe turtle takes full credit.\nYou may thank him now.";
const TURTLE_RAGE = [
  "               _____     ______",
  "             < x   x >  /      \\",
  "              \\  -  /  |  O   O |",
  "              /     \\  |   ∆    |",
  "             |       | \\______/",
  "            /| |   | |\\",
  "           /_|_|___|_|_\\",
  "            /_/     \\_\\"
];

function pick(arr) {
  return arr[crypto.getRandomValues(new Uint32Array(1))[0] % arr.length];
}
function randInt(min, max) {
  return min + (crypto.getRandomValues(new Uint32Array(1))[0] % (max - min + 1));
}
function rand() {
  return crypto.getRandomValues(new Uint32Array(1))[0] / 0xffffffff;
}

function checkPleases(lines) {
  const idx = [];
  for (let i = 0; i < lines.length;) {
    const step = randInt(3, 7);
    idx.push([i, step]);
    i += step;
  }
  for (const [i, step] of idx) {
    const window = lines.slice(i, i + step);
    if (!window.some((l) => l.replace(/ /g, "").includes("please()"))) {
      console.log(TURTLE_RAGE.join("\n"));
      console.log(`Your code is too rude! Please add a 'please()' call near line ${i + 1}.`);
      return false;
    }
  }
  return true;
}

function main() {
  const file = process.argv[2];
  if (!file || !/\.(slow|py)$/.test(file)) {
    console.log("Usage: slowlang <yourfile.slow>");
    process.exit(1);
  }
  if (!fs.existsSync(file)) {
    console.log(`No such file: ${file} - the turtle looked everywhere. Slowly.`);
    process.exit(1);
  }
  if (rand() < 0.1) {
    console.log(pick(LAZY_TURTLE_LINES));
    console.log("The SlowLang compiler refuses to run your code right now. Try again!");
    return;
  }
  const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
  if (!checkPleases(lines)) {
    console.log("Refusing to run rude code.");
    return;
  }
  console.log(HAIKU);
  console.log("\nPoliteness check passed. To actually run it:");
  console.log("  pip install slowlang && slowlang " + file);
  console.log("  or try the zero-install demo: https://sebin-gg.github.io/slowlang/");
}

main();
