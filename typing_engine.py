import time
_rng = random.SystemRandom()

import keyboard

from ascii_turtle import show_turtle_rage
from exporter import export_text
from sarcasm_engine import get_sarcastic_remark


class TypingSpeedError(Exception):
    """Raised when the user types faster than the configured speed limit."""


class TypingEngine:
    def __init__(self, speed_limit_wpm=30):
        self.speed_limit_wpm = speed_limit_wpm
        self.timestamps = []
        self.buffer = ''
        self.error_triggered = False

    def _word_count(self):
        return len(self.buffer.strip().split())

    def _calculate_speed(self):
        if len(self.timestamps) < 2:
            return 0
        duration = self.timestamps[-1] - self.timestamps[0]
        if duration == 0:
            return 0
        wpm = (self._word_count() / duration) * 60
        return wpm

    def _reset(self):
        self.timestamps = []
        self.buffer = ''
        self.error_triggered = False

    def _check_please(self, lines):
        """Check that 'please()' appears at random intervals in the code."""
        import random
        required_indices = []
        i = 0
        while i < len(lines):
            step = _rng.randint(3, 7)
            required_indices.append(i)
            i += step

        for idx in required_indices:
            window = lines[idx:idx+step]
            if not any('please()' in line.replace(' ', '') for line in window):
                print(f"😡 Your code is too rude! Please add a 'please()' call near line {idx+1}.")
                return False
        return True

    def type_listener(self):
        print("🐢 Welcome to TortoiseLang! Type slowly...\n")
        print("Shortcuts: [esc]=exit, [ctrl+s]=save, [ctrl+r]=reset, [ctrl+w]=show WPM, [ctrl+e]=export as .slow and check politeness\n")
        self._reset()

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name

                # Handle shortcuts
                if keyboard.is_pressed('ctrl+s'):
                    export_text(self.buffer)
                    print("✅ Text exported!\n")
                    continue
                if keyboard.is_pressed('ctrl+r'):
                    self._reset()
                    print("🔄 Buffer reset!\n")
                    continue
                if keyboard.is_pressed('ctrl+w'):
                    speed = self._calculate_speed()
                    print(f"🐢 Current WPM: {speed:.2f}\n")
                    continue
                if keyboard.is_pressed('ctrl+e'):
                    # Export as .slow and check for please()
                    filename = "tortoise_output.slow"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(self.buffer)
                    lines = self.buffer.splitlines()
                    if not self._check_please(lines):
                        print("🐢 Refusing to export rude code. Add more 'please()' calls!")
                    else:
                        print(f"✅ Code exported as {filename} and is polite enough!\n")
                    continue

                # Handle space or enter as a word boundary
                if key == 'space' or key == 'enter':
                    self.buffer += ' '
                elif key == 'backspace':
                    self.buffer = self.buffer[:-1]
                elif len(key) == 1:
                    self.buffer += key

                # Timestamp this key
                self.timestamps.append(time.time())

                # Keep last 10 seconds' timestamps
                self.timestamps = [ts for ts in self.timestamps if time.time() - ts <= 10]

                # Check speed
                speed = self._calculate_speed()
                if speed > self.speed_limit_wpm:
                    self.error_triggered = True
                    show_turtle_rage()
                    print(get_sarcastic_remark())
                    raise TypingSpeedError(
                        f"\n?? Whoa there, Shakespeare!\n?? You're typing at {int(speed)} WPM!\n?? Slow down. This is TortoiseLang.\n"
                    )

                if key == 'esc':
                    print("\n👋 Exiting typing engine. Goodbye!")
                    break

if __name__ == "__main__":
    engine = TypingEngine(speed_limit_wpm=30)
    try:
        engine.type_listener()
    except TypingSpeedError as e:
        print(str(e))
