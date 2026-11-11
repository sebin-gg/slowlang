---
title: I built a programming language that punishes you for typing too fast
published: true
description: SlowLang is a sarcastic Python-like language and IDE that enforces slow, mindful typing — winner of TinkerHub Useless Projects 2.0. Built by CS students in Kerala, India.
tags: showdev, python, programminglanguages, hackathon
canonical_url: https://sebin-gg.vercel.app/blog/slowlang-a-language-that-punishes-fast-typing
cover_image:
---

Most programming languages want you to go faster. Faster compile times, faster iteration, faster shipping. So for [TinkerHub](https://www.linkedin.com/company/tinkerhub)'s Useless Projects 2.0 hackathon — a Kerala event celebrating gloriously useless software — my teammate [Abin Zachariah Abraham](https://www.linkedin.com/in/abin-zachariah-abraham-124576339/) and I went the other way: we built a language that actively slows you down.

**SlowLang** (also called TortoiseLang) is a sarcastic, Python-like programming language with its own Tkinter IDE. Its core feature is a typing-speed enforcer: type too fast and it throws errors at you.

## What it actually does

- It tracks your typing speed in the IDE. Cross the threshold and you get an angry ASCII turtle and a lockout until you calm down.
- Error messages are haikus and sarcastic praise instead of stack traces.
- There's a lazy mode that randomly refuses to run, because sometimes the code just isn't in the mood.
- It runs in the browser too — a Pyodide-powered demo mirrors the desktop behavior, no install needed.

Under the jokes there's real engineering: a keyboard-event monitor, a state machine for turtle moods (calm / annoyed / furious), a rage lockout timer, and a pytest suite covering the spec. The browser demo reimplements the same state machine in JavaScript, so both versions behave identically.

## Why build something useless on purpose

The hackathon's whole point was creativity over practicality. Building a joke with craft taught us more than a CRUD app would have: state machines, desktop UI with Tkinter, packaging a Python project properly, and porting the same behavior to a WASM runtime for the web demo. Also, it won — SlowLang took first place at Useless Projects 2.0.

I wrote about the event itself [on LinkedIn](https://www.linkedin.com/posts/sebin-m_uselessprojects-creativity-innovation-activity-7364503415713943552-sttp) earlier, and posted [the winner announcement](https://www.linkedin.com/posts/sebin-m_excited-to-share-that-our-project-slowlang-activity-7377585860021669888-JQKx) when the results came out.

## Try it / steal it

- **Browser demo:** https://sebin-gg.github.io/slowlang/ — no install, Pyodide under the hood
- **Source:** https://github.com/sebin-gg/slowlang — Python + Tkinter, tests included
- **My portfolio:** https://sebin-gg.vercel.app — the rest of what I build

I'm a B.Tech CS student at College of Engineering Chengannur in Kerala, India. If a sarcastic turtle ever taught you anything about your typing habits, I'd love to hear it.
