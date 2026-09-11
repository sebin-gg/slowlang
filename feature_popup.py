import tkinter as tk
from tkinter import scrolledtext

FEATURES_TEXT = """
🐢 TortoiseLang – Slower is Better

Features:
• if you close the angry popup you will lose your right to code 
• Python-like syntax: Write code just like Python.
• Speed enforcement: Typing too fast triggers sarcastic errors and turtle rage.
• Sarcastic feedback: Get sassy remarks and poetic haikus if you break the rules.
• Fake IDE: Tkinter-based IDE with live feedback, export, and run buttons, Python color scheme, and smart indentation.
• Live typing speed enforcement: Type too fast and a turtle rage window will pop up.
• Run code like Python: Use the "Run (like Python)" button to execute your code directly in the IDE.
• Rude code is refused: add please() calls or the turtle won't run it.
• Live WPM readout, line numbers, and a countdown on the rage lockout.
• Load sample button and a gentle streak for rage-free runs.
• The compiler will sometimes pop words of wisdom after execution.
• Python color scheme and smart indentation: Editor highlights Python keywords, strings, comments, and builtins, and auto-indents after colons for blocks.
• Sarcastic errors and poetic output: Enjoy haikus and sassy remarks if you break the rules.
• The compiler will sometimes pop words of wisdom after execution.
"""

def show_features_popup():
    popup = tk.Tk()
    popup.title("Welcome to TortoiseLang!")
    popup.geometry("600x400")
    popup.resizable(False, False)

    label = tk.Label(popup, text="Welcome to TortoiseLang!", font=("Arial", 16, "bold"))
    label.pack(pady=10)

    text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=("Consolas", 11), height=18, width=70)
    text_area.insert(tk.END, FEATURES_TEXT)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    btn = tk.Button(popup, text="Continue to IDE", font=("Arial", 12), command=popup.destroy)
    btn.pack(pady=10)

    popup.mainloop()

if __name__ == "__main__":
    show_features_popup()