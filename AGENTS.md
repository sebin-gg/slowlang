# Project conventions

slowLang is a joke-with-craft programming language and IDE: Python core,
Tkinter desktop app (`ui-fakeide.py`), and a static browser demo in `demo/`
that mirrors the desktop behavior. Keep the humor; keep the behavior identical
in both.

## Commands

- `python ui-fakeide.py` — desktop IDE (needs Tkinter; on Linux: `sudo apt install python3-tk`)
- `python -m pytest -q` — test gate (install: `python -m pip install -r requirements.txt`)
- `python -m compileall -q .` — syntax gate
- `node --check demo/app.js` — demo syntax gate
- Serve the demo: `python3 -m http.server --directory demo`

## Agent skills (borrowed from the `sebin-gg resume` repo)

Skills live in that repo under `.agents/skills/`. Load the SKILL.md there before
relying on one here. The ones this repo expects:

1. **`designing-beautiful-websites`** — load before any `demo/` UI work.
2. **`unslop`** — audit pass before and after touching user-visible copy
   (README, demo text, haikus). Sarcasm strings are the authors’ jokes:
   never rewrite them, only check new copy around them.
3. **`caveman`** — terse replies. Default mode for agents working here.

## Rules

1. **Desktop and demo stay in sync.** Typing thresholds (0.1 s rage, 0.5 s calm),
   the 2 s rage lockout, the 1-in-10 lazy refusal, Lazy Mode doubling, and the
   20/30/50 turtle-mood split are the spec. Change one, change both.
2. **Sarcasm and haikus are content, not code.** They live in
   `sarcasm_engine.py` (desktop) and `demo/app.js` (web, marked port).
   Add lines to both lists, never to one.
3. **Demo stays static.** No build step, no backend, no images. The only
   runtime dependency is Pyodide, lazy-loaded on Run, with the offline
   fallback runner as backup. Dark theme is the default.
4. **Quality gates stay green:** `pytest`, `compileall`, `node --check`.
   New behavior ships with a test (`tests/` for Python; extend the
   `window.__slowlang` hooks for demo logic).
5. **Semantics/a11y:** real `<button>`/`<dialog>`/`<label>` elements,
   `aria-live` on status and output, visible focus, `prefers-reduced-motion`
   respected. No `target="_blank"` without `rel="noopener noreferrer"`.
6. **Randomness uses `random.SystemRandom`** in Python (never bare `random`
   for user-facing rolls); in JS use `Math.random` only for jokes and
   lockouts, never for anything security-shaped.
7. **`main` ships via small PRs.** Never commit secrets; gitleaks scans every
   commit.
