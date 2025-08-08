from typing_engine import TypingEngine
from sarcasm_engine import get_sarcastic_message, get_poetic_output
import random
import sys

def check_pleases(lines):
    """Check that 'please()' appears at random intervals in the code."""
    required_indices = []
    i = 0
    while i < len(lines):
        step = random.randint(3, 7)
        required_indices.append(i)
        i += step

    for idx in required_indices:
        window = lines[idx:idx+step]
        if not any('please()' in line.replace(' ', '') for line in window):
            print(f"😡 Your code is too rude! Please add a 'please()' call near line {idx+1}.")
            return False
    return True

def please():
    # The magic function required by the language
    print("🙏 The turtle thanks you for your politeness.")

def run_slowlang(filename):
    with open(filename, encoding="utf-8") as f:
        code = f.read()
    lines = code.splitlines()
    if not check_pleases(lines):
        print("🐢 Refusing to run rude code.")
        return
    # Provide 'please' in the global namespace
    exec(code, {"please": please})

if __name__ == "__main__":
    engine = TypingEngine(speed_limit_wpm=30)
    try:
        engine.type_listener()
    except Exception as e:
        print("\n" + get_sarcastic_message())
        print("\n✨ Poetic wisdom:\n" + get_poetic_output())
