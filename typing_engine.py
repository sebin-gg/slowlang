import time
import keyboard

class TypingEngine:
    def __init__(self, speed_limit_wpm=30):
        self.speed_limit_wpm = speed_limit_wpm  # max allowed words per minute
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

    def type_listener(self):
        print("🐢 Welcome to TortoiseLang! Type slowly...\n")
        self._reset()

        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name

                # Handle space or enter as a word boundary
                if key == 'space' or key == 'enter':
                    self.buffer += ' '
                elif key == 'backspace':
                    self.buffer = self.buffer[:-1]
                elif len(key) == 1:  # only count alphanumeric keys
                    self.buffer += key

                # Timestamp this key
                self.timestamps.append(time.time())

                # Keep last 10 seconds' timestamps
                self.timestamps = [ts for ts in self.timestamps if time.time() - ts <= 10]

                # Check speed
                speed = self._calculate_speed()
                if speed > self.speed_limit_wpm:
                    self.error_triggered = True
                    raise Exception(
                        f"\n😤 Whoa there, Shakespeare!\n🧠 You're typing at {int(speed)} WPM!\n🐢 Slow down. This is TortoiseLang.\n"
                    )

                if key == 'esc':
                    print("\n👋 Exiting typing engine. Goodbye!")
                    break

if __name__ == "__main__":
    engine = TypingEngine(speed_limit_wpm=30)
    try:
        engine.type_listener()
    except Exception as e:
        print(str(e))
from ascii_turtle import show_turtle_rage
...
if speed > self.speed_limit_wpm:
    self.error_triggered = True
    show_turtle_rage()
    raise Exception(
        f"\n😤 Whoa there, Shakespeare!\n🧠 You're typing at {int(speed)} WPM!\n🐢 Slow down. This is TortoiseLang.\n"
    )