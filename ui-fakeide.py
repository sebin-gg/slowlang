import tkinter as tk
from tkinter import messagebox, filedialog
from ascii_turtle import show_turtle_rage
from exporter import export_to_pdf
from sarcasm_engine import get_sarcastic_message
import time
import random
import os

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

        # Turtle rage window (hidden by default)
        self.turtle_win = None

        self.export_btn = tk.Button(root, text="Export to PDF", command=self.export_pdf)
        self.export_btn.pack(pady=5)

        self.export_slow_btn = tk.Button(root, text="Export as .slow (politeness check)", command=self.export_slow)
        self.export_slow_btn.pack(pady=5)

        self.run_btn = tk.Button(root, text="Run (like Python)", command=self.run_code)
        self.run_btn.pack(pady=5)

        self.filename = None

    def show_turtle_rage_window(self):
        if self.turtle_win is not None and tk.Toplevel.winfo_exists(self.turtle_win):
            return  # Already open
        self.turtle_win = tk.Toplevel(self.root)
        self.turtle_win.title("🐢 Turtle Rage!")
        self.turtle_win.geometry("400x250")
        turtle = (
            "               _____     ______\n"
            "             < x   x >  /      \\ \n"
            "              \\  -  /  |  O   O |\n"
            "              /     \\  |   ∆    |\n"
            "             |       | \\______/\n"
            "            /| |   | |\\\n"
            "           /_|_|___|_|_\\\n"
            "            /_/     \\_\\\n"
            "🐢 RAGE MODE: Turtle is not amused by your speed."
        )
        label = tk.Label(self.turtle_win, text=turtle, font=("Courier", 10), fg="red", justify="left")
        label.pack(padx=10, pady=10)
        # Auto-close after 2 seconds
        self.turtle_win.after(2000, self.turtle_win.destroy)

    def track_speed(self, event):
        now = time.time()
        delta = now - self.last_time
        self.last_time = now

        if delta < 0.1:
            self.output.config(text=get_sarcastic_message(), fg="red")
            self.show_turtle_rage_window()
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
            # Always export with a different name
            filename = filedialog.asksaveasfilename(defaultextension=".slow", filetypes=[("TortoiseLang Files", "*.slow")], title="Save As")
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                messagebox.showinfo("Export", f"Code exported as {os.path.basename(filename)} and is polite enough!")

    def run_code(self):
        # Run code in editor as if it's Python (with please() available)
        text = self.editor.get("1.0", tk.END)
        output_win = tk.Toplevel(self.root)
        output_win.title("Output")
        output_text = tk.Text(output_win, height=15, width=70, font=("Courier", 12))
        output_text.pack()
        def please():
            output_text.insert(tk.END, "🙏 The turtle thanks you for your politeness.\n")
        try:
            # Redirect print to the output_text widget
            import sys
            from io import StringIO
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            exec(text, {"please": please})
            sys.stdout = old_stdout
            output_text.insert(tk.END, mystdout.getvalue())
        except Exception as e:
            output_text.insert(tk.END, f"Error: {e}\n")
        finally:
            sys.stdout = old_stdout

if __name__ == "__main__":
    root = tk.Tk()
    app = TortoiseIDE(root)
    root.mainloop()