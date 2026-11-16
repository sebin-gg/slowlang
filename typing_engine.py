import time

from ascii_turtle import show_turtle_rage
from sarcasm_engine import get_sarcastic_remark
from tortoise_lang import check_pleases
from emit import _emit


class TypingSpeedError(Exception):
    """Raised when the user types faster than the configured speed limit."""


def wpm_from_timestamps(timestamps, now, window=10.0):
    """Rolling words-per-minute from keystroke timestamps (5 chars = 1 word)."""
    recent = [ts for ts in timestamps if 0 <= now - ts <= window]
    if len(recent) < 2:
        return 0.0
    span = recent[-1] - recent[0]
    if span <= 0:  # simultaneous timestamps are one burst, not infinite speed
        return 0.0
    return (len(recent) / 5) / (span / 60)


class TypingEngine:
    def __init__(self, speed_limit_wpm=30):
        self.speed_limit_wpm = speed_limit_wpm
        self.timestamps = []
        self.buffer = ''
        self.error_triggered = False

    def _calculate_speed(self):
        """Rolling WPM over the buffered keystrokes (5 characters = 1 word)."""
        if not self.timestamps:
            return 0.0
        return wpm_from_timestamps(self.timestamps, self.timestamps[-1])

    def _reset(self):
        self.timestamps = []
        self.buffer = ''
        self.error_triggered = False

    def type_listener(self):
        import keyboard  # lazy: helpers stay importable without optional deps
        from exporter import export_text

        _emit("🐢 Welcome to TortoiseLang! Type slowly...\n")
        _emit("Shortcuts: [esc]=exit, [ctrl+s]=save, [ctrl+r]=reset, [ctrl+w]=show WPM, [ctrl+e]=export as .slow and check politeness\n")
        self._reset()

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name

                # Handle shortcuts
                if keyboard.is_pressed('ctrl+s'):
                    export_text(self.buffer)
                    _emit("✅ Text exported!\n")
                    continue
                if keyboard.is_pressed('ctrl+r'):
                    self._reset()
                    _emit("🔄 Buffer reset!\n")
                    continue
                if keyboard.is_pressed('ctrl+w'):
                    speed = self._calculate_speed()
                    _emit(f"🐢 Current WPM: {speed:.2f}\n")
                    continue
                if keyboard.is_pressed('ctrl+e'):
                    # Export as .slow and check for please()
                    filename = "tortoise_output.slow"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(self.buffer)
                    lines = self.buffer.splitlines()
                    if not check_pleases(lines):
                        _emit("🐢 Refusing to export rude code. Add more 'please()' calls!")
                    else:
                        _emit(f"✅ Code exported as {filename} and is polite enough!\n")
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
                    _emit(get_sarcastic_remark())
                    raise TypingSpeedError(
                        f"\n?? Whoa there, Shakespeare!\n?? You're typing at {int(speed)} WPM!\n?? Slow down. This is TortoiseLang.\n"
                    )

                if key == 'esc':
                    _emit("\n👋 Exiting typing engine. Goodbye!")
                    break

if __name__ == "__main__":
    engine = TypingEngine(speed_limit_wpm=30)
    try:
        engine.type_listener()
    except TypingSpeedError as e:
        _emit(str(e))
