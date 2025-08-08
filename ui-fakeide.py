import tkinter as tk
from tkinter import messagebox
from ascii_turtle import show_turtle_rage # This is now using your ascii_turtle file
from exporter import export_to_pdf
from sarcasm_engine import get_sarcastic_message # Using your sarcasm_engine
import time

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

    def track_speed(self, event):
        now = time.time()
        delta = now - self.last_time
        self.last_time = now

        # Use the logic from your files to determine what message to show
        if delta < 0.1:
            self.output.config(text=get_sarcastic_message(), fg="red")
            # Call your turtle rage function in the console
            show_turtle_rage()
        elif delta > 0.5:
            self.output.config(text="You're calm. The turtle is proud 🐢", fg="green")
        else:
            self.output.config(text="Steady typing...", fg="blue")

    def export_pdf(self):
        text = self.editor.get("1.0", tk.END)
        export_to_pdf(text)
        messagebox.showinfo("Export", "PDF exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TortoiseIDE(root)
    root.mainloop()