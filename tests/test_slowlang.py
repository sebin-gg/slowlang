"""Smoke tests for TortoiseLang pure helpers."""

from sarcasm_engine import (
    LOADING_QUOTES,
    get_loading_quote,
    get_poetic_output,
    get_sarcastic_message,
    get_sarcastic_remark,
)
from tortoise_lang import check_pleases
from typing_engine import TypingEngine, wpm_from_timestamps


def test_sarcastic_remark_is_string():
    assert isinstance(get_sarcastic_remark(), str)


def test_sarcastic_message_default_theme():
    assert isinstance(get_sarcastic_message(), str)


def test_sarcastic_message_lazy_turtle_theme():
    assert isinstance(get_sarcastic_message("lazy_turtle"), str)


def test_poetic_output_is_string():
    assert isinstance(get_poetic_output(), str)


def test_check_pleases_accepts_polite_code():
    lines = ["please()"] * 20
    assert check_pleases(lines) is True


def test_check_pleases_rejects_rude_code(capsys):
    assert check_pleases(["print('hi')"] * 20) is False
    assert "too rude" in capsys.readouterr().out


class _FixedSteps:
    """Deterministic stand-in for the politeness RNG."""

    def __init__(self, steps):
        self.steps = list(steps)

    def randint(self, a, b):
        return self.steps.pop(0)


def test_check_pleases_respects_each_window_length(capsys):
    # Only the last line is polite, so the first 3-line window must fail.
    lines = ["print('a')", "print('b')", "print('c')", "print('d')", "please()"]
    assert check_pleases(lines, rng=_FixedSteps([3, 7])) is False
    assert "too rude" in capsys.readouterr().out


def test_check_pleases_accepts_when_every_window_has_please():
    lines = ["please()", "print('a')", "print('b')", "please()", "print('c')"]
    assert check_pleases(lines, rng=_FixedSteps([3, 3])) is True


def test_engine_wpm_does_not_grow_with_the_buffer():
    engine = TypingEngine()
    engine.timestamps = [0.0, 0.5, 1.0, 1.5]
    engine.buffer = "a b c"
    first = engine._calculate_speed()
    engine.buffer = "a b c d e f g h i j k l"
    assert engine._calculate_speed() == first


def _cp1252_stdout(monkeypatch):
    """Redirect stdout to a strict cp1252 stream, like a Windows pipe."""
    import io

    raw = io.BytesIO()
    stream = io.TextIOWrapper(raw, encoding="cp1252", errors="strict")
    monkeypatch.setattr("sys.stdout", stream)
    return raw, stream


def test_please_prints_on_a_cp1252_console(monkeypatch):
    from tortoise_lang import please

    raw, stream = _cp1252_stdout(monkeypatch)
    please()  # used to raise UnicodeEncodeError
    stream.flush()
    written = raw.getvalue().decode("cp1252")
    assert "The turtle thanks you for your politeness." in written
    assert "\U0001f64f" not in written  # emoji degraded instead of crashing


def test_rude_message_prints_on_a_cp1252_console(monkeypatch):
    raw, stream = _cp1252_stdout(monkeypatch)
    assert check_pleases(["print('hi')"] * 3, rng=_FixedSteps([3])) is False
    stream.flush()
    assert "too rude" in raw.getvalue().decode("cp1252")


def test_loading_quotes_cycle_deterministically():
    assert len(LOADING_QUOTES) == 10
    assert all(isinstance(q, str) and q for q in LOADING_QUOTES)
    assert get_loading_quote(0) == LOADING_QUOTES[0]
    assert get_loading_quote(10) == LOADING_QUOTES[0]
    assert get_loading_quote(9) == LOADING_QUOTES[9]


def test_poetic_output_varies():
    assert len({get_poetic_output() for _ in range(50)}) > 1


def test_wpm_needs_two_keystrokes():
    assert wpm_from_timestamps([], 100.0) == 0.0
    assert wpm_from_timestamps([99.0], 100.0) == 0.0


def test_wpm_math_and_window():
    stamps = [90.0 + i * 0.2 for i in range(50)]  # 50 keys over 9.8 s
    assert abs(wpm_from_timestamps(stamps, 100.0) - 10 / (9.8 / 60)) < 0.01
    assert wpm_from_timestamps([0.0, 0.1], 100.0) == 0.0  # outside window


def test_main_usage_message(capsys, monkeypatch):
    import sys
    from tortoise_lang import main

    monkeypatch.setattr(sys, "argv", ["slowlang"])
    main()
    assert "Usage: slowlang" in capsys.readouterr().out


def test_main_runs_file(monkeypatch):
    import sys
    from tortoise_lang import main

    called = {}
    monkeypatch.setattr("tortoise_lang.run_slowlang", lambda f: called.setdefault("f", f))
    monkeypatch.setattr(sys, "argv", ["slowlang", "x.slow"])
    main()
    assert called["f"] == "x.slow"


def test_check_pleases_detects_tab_indented_please():
    lines = ["print('a')", "\tplease()", "print('b')"]
    assert check_pleases(lines, rng=_FixedSteps([3])) is True


def test_wpm_simultaneous_timestamps_do_not_rage():
    assert wpm_from_timestamps([5.0, 5.0, 5.0], 5.0) == 0.0


def test_emit_preserves_emoji_on_utf8_stream(monkeypatch):
    import io
    from tortoise_lang import please

    raw = io.BytesIO()
    stream = io.TextIOWrapper(raw, encoding="utf-8", errors="strict")
    monkeypatch.setattr("sys.stdout", stream)
    please()
    stream.flush()
    assert "\U0001f64f" in raw.getvalue().decode("utf-8")  # emoji kept, not replaced
