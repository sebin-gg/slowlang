from typing_engine import TypingEngine
from sarcasm_engine import get_sarcastic_message, get_poetic_output

if __name__ == "__main__":
    engine = TypingEngine(speed_limit_wpm=30)
    try:
        engine.type_listener()
    except Exception as e:
        print("\n" + get_sarcastic_message())
        print("\n✨ Poetic wisdom:\n" + get_poetic_output())
