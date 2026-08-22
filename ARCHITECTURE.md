# Architecture & Execution Runtime

## Overview
`slowlang` (TortoiseLang) is an intentional, patience-oriented programming runtime that throttles typing velocity and enforces mindfulness through interactive execution feedback, sarcastic telemetry, and delay penalties.

```mermaid
graph LR
    subgraph "Input Layer"
        K[Keystroke Stream] --> E[Typing Engine]
    end

    subgraph "Telemetry & Cadence Analysis"
        E --> V[Velocity Calculator - WPM / CPM]
        V --> T{Speed > Threshold?}
        T -- Yes --> P[Penalty Engine: Delay Throttling & ASCII Rage]
        T -- No --> H[Patience Reward: Zen Haiku & Flow State]
    end

    subgraph "Execution Pipeline"
        P --> AST[AST Parser / Tokenizer]
        H --> AST
        AST --> R[Interpreter Runtime]
        R --> OUT[Console Output Buffer]
    end
```

---

## Architectural Decision Records (ADRs)

### ADR-001: Real-Time Event-Driven Keystroke Interceptor
* **Status**: Accepted
* **Context**: Traditional linters only analyze code post-edit; patience enforcement requires live rhythm monitoring.
* **Decision**: Build an event-driven `TypingEngine` calculating rolling average intervals between consecutive keypresses (`delta_ms`).
* **Consequences**: Immediate behavioral feedback with zero perceivable rendering latency.

### ADR-002: Modular Penalty & Sarcasm State Machine
* **Status**: Accepted
* **Context**: Feedback must scale dynamically with developer impatience.
* **Decision**: Implement state machine with 4 escalations: `Zen` -> `Warning` -> `Sarcastic Intervention` -> `Angry Turtle ASCII Lockout`.
* **Consequences**: Humorous, gamified feedback loop that enforces typing rate limits cleanly.
