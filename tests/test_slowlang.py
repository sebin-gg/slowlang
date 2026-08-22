"""Smoke tests for TortoiseLang pure helpers."""

from sarcasm_engine import get_poetic_output, get_sarcastic_message, get_sarcastic_remark
from tortoise_lang import check_pleases


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
