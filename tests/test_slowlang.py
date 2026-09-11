"""Smoke tests for TortoiseLang pure helpers."""

from sarcasm_engine import (
    LOADING_QUOTES,
    get_loading_quote,
    get_poetic_output,
    get_sarcastic_message,
    get_sarcastic_remark,
)
from tortoise_lang import check_pleases
from typing_engine import wpm_from_timestamps


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
