Title: SlowLang - a Python-like esolang that punishes you for typing too fast (my project, won TinkerHub Useless Projects 2.0)

Body:

Author here - built this for TinkerHub's Useless Projects 2.0 hackathon (it won).

SlowLang is a Python-based esolang that enforces a per-keystroke speed
floor: type faster than one key every 0.1 seconds and an angry ASCII turtle
rage-locks the editor for 2 seconds amid sarcastic insults, while success
is announced by a smug haiku. There's a mandatory please() token checked as
plain text at random 3-7-line intervals (a comment satisfies it), and a
1-in-10 lazy refusal on valid runs - unless you tick Lazy Mode, which
forgives both that and fast typing.

It's Turing complete - .slow files execute as arbitrary Python under the hood.

Repo: https://github.com/sebin-gg/slowlang
Browser demo: https://sebin-gg.github.io/slowlang/
Esolangs wiki article: https://esolangs.org/wiki/SlowLang
Install: `pip install slowlang` (PyPI) or `npm i -g slowlang` (npm)
