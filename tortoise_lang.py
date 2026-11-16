from pathlib import Path
import random
import sys
from emit import _emit
_rng = random.SystemRandom()


def check_pleases(lines, rng=None):
    """Check that 'please()' appears in every random 3-7 line window of the code."""
    rng = rng or _rng
    windows = []
    i = 0
    while i < len(lines):
        step = rng.randint(3, 7)
        windows.append((i, step))
        i += step

    for idx, step in windows:
        window = lines[idx:idx + step]
        if not any('please()' in line.replace(' ', '').replace('\t', '') for line in window):
            _emit(f"😡 Your code is too rude! Please add a 'please()' call near line {idx+1}.")
            return False
    return True

def please():
    _emit("🙏 The turtle thanks you for your politeness.")

def run_slowlang(filename):
    # Constrain file access to .slow/.py files under the current directory (S8707)
    path = Path(filename).resolve()
    if path.suffix not in {".slow", ".py"} or not path.is_relative_to(Path.cwd()):
        _emit("?? TortoiseLang only reads .slow or .py files inside the current folder.")
        return
    filename = str(path)
    # 10% chance to refuse to run due to laziness
    if _rng.random() < 0.1:
        _emit("🐢 The TortoiseLang compiler is feeling lazy and refuses to run your code right now. Try again!")
        return
    with open(filename, encoding="utf-8") as f:
        code = f.read()
    lines = code.splitlines()
    if not check_pleases(lines):
        _emit("🐢 Refusing to run rude code.")
        return
    exec(code, {"please": please})  # noqa: S102 - intentional: language runtime

def main():
    if len(sys.argv) != 2:
        _emit("Usage: slowlang <yourfile.slow>")
    else:
        run_slowlang(sys.argv[1])

if __name__ == "__main__":
    main()

