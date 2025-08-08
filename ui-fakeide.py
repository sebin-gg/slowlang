import tkinter as tk
from tkinter import messagebox
from ascii_turtle import show_turtle_rage
from exporter import export_to_pdf
from sarcasm_engine import get_sarcastic_message
import time
import random

class TortoiseIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("TortoiseLang IDE 🐢")
        self.typing_speed = 0
        self.last_time = time.time()

        self.editor = tk.Text(root, height=15, width=70, font=("Courier", 12))
        self.editor.pack(pady=10)
        self.editor.bind("<Key>", self.track_speed)

        self.output = tk.Label(root, text="Slow and steady...", font=("Courier", 12), fg="green")
        self.output.pack()

        self.export_btn = tk.Button(root, text="Export to PDF", command=self.export_pdf)
        self.export_btn.pack(pady=5)

        self.export_slow_btn = tk.Button(root, text="Export as .slow (politeness check)", command=self.export_slow)
        self.export_slow_btn.pack(pady=5)

    def track_speed(self, event):
        now = time.time()
        delta = now - self.last_time
        self.last_time = now

        if delta < 0.1:
            self.output.config(text=get_sarcastic_message(), fg="red")
            show_turtle_rage()
        elif delta > 0.5:
            self.output.config(text="You're calm. The turtle is proud 🐢", fg="green")
        else:
            self.output.config(text="Steady typing...", fg="blue")

    def _check_please(self, lines):
        required_indices = []
        i = 0
        while i < len(lines):
            step = random.randint(3, 7)
            required_indices.append(i)
            i += step

        for idx in required_indices:
            window = lines[idx:idx+step]
            if not any('please()' in line.replace(' ', '') for line in window):
                return False, idx+1
        return True, None

    def export_pdf(self):
        text = self.editor.get("1.0", tk.END)
        export_to_pdf(text)
        messagebox.showinfo("Export", "PDF exported successfully!")

    def export_slow(self):
        text = self.editor.get("1.0", tk.END)
        lines = text.splitlines()
        ok, line = self._check_please(lines)
        if not ok:
            messagebox.showerror("Politeness Error", f"Your code is too rude! Please add a 'please()' call near line {line}.")
        else:
            with open("tortoise_output.slow", "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Export", "Code exported as tortoise_output.slow and is polite enough!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TortoiseIDE(root)
    root.mainloop()