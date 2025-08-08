import time

def typing_speed_tracker():
    text_to_type = "Slow down! Accuracy over speed."
    print("Type this: ", text_to_type)
    
    input("Press Enter to start typing...")
    start = time.time()
    user_input = input("Now type: ")
    end = time.time()

    elapsed = end - start
    wpm = (len(user_input) / 5) / (elapsed / 60)
    
    if user_input != text_to_type:
        print("🐢 ASCII TURTLE: You messed it up. Again.")
        print("🥴 SARCASM: That was... 'impressive'. 🙄")
    else:
        print("👏 Nailed it!")
    
    print(f"⏱️ Your typing speed: {wpm:.2f} WPM")

if __name__ == "__main__":
    typing_speed_tracker()
