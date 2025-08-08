import time
import random
import os

# Sarcasm responses
sarcasm_lines = [
    "Wow. That was... something.",
    "Impressive. If we were timing snails.",
    "You're typing like it's 1995 dial-up.",
    "My grandma types faster—and she's imaginary.",
    "That was... slow. Even for this language."
]

# ASCII turtle rage frames
turtle_frames = [
    r"""
        (\_/)
        (•_•)  ...
        / >🐢
    """,
    r"""
        (\_/)
        (•_•)  😠
        / >💢
    """,
    r"""
        (\_/)
        (ง •̀_•́)ง  😡
        / >🔥
    """,
    r"""
        (\_/)
        (╯°□°)╯︵ ┻━┻
        / >💥
    """
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_turtle_rage():
    for frame in turtle_frames:
        clear_screen()
        print(frame)
        time.sleep(0.4)

def typing_session():
    clear_screen()
    print("⌨️ Welcome to SlowLang Typing Challenge")
    prompt = "The quick brown fox jumps over the lazy dog"
    print(f"\n📝 Type this:\n{prompt}\n")

    input("Press ENTER when you're ready...")
    clear_screen()
    print(f"\n📝 Type this:\n{prompt}\n")

    start_time = time.time()
    user_input = input("Your input: ")
    end_time = time.time()

    elapsed = end_time - start_time
    accuracy = sum(1 for a, b in zip(prompt, user_input) if a == b) / len(prompt) * 100
    wpm = (len(user_input) / 5) / (elapsed / 60)

    print("\n⏱️  Results:")
    print(f"   Time Taken: {elapsed:.2f} sec")
    print(f"   Typing Speed: {wpm:.2f} WPM")
    print(f"   Accuracy: {accuracy:.2f}%")

    if accuracy < 80 or wpm < 20:
        print(f"\n🥴 SARCASM: {random.choice(sarcasm_lines)} 🙄")
        display_turtle_rage()
    else:
        print("\n👏 Great job, you beat the turtle!")

if __name__ == "__main__":
    typing_session()
