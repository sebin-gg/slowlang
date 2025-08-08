import time

def calculate_wpm(start_time, end_time, typed_text):
    words = len(typed_text.split())
    duration = end_time - start_time
    wpm = (words / duration) * 60
    return round(wpm, 2)

prompt = "The quick brown fox jumps over the lazy dog."

print("Type this sentence:")
print(prompt)
input("Press Enter to start...")

start = time.time()
typed = input("\nStart typing:\n")
end = time.time()

wpm = calculate_wpm(start, end, typed)
print(f"\nYour typing speed: {wpm} WPM")
