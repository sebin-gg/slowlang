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
    print("🙏 The turtle thanks you for your politeness.")

def run_slowlang(filename):
    with open(filename, encoding="utf-8") as f:
        code = f.read()
    lines = code.splitlines()
    if not check_pleases(lines):
        print("🐢 Refusing to run rude code.")
        return
    exec(code, {"please": please})

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tortoise_lang.py <yourfile.slow>")
    else:
        run_slowlang(sys.argv[1])
