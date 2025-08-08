import tkinter as tk
from tkinter import messagebox
from ascii_turtle import show_turtle_rage
from sarcasm_engine import get_sarcastic_message
import time
import random
import os
import keyword

class PythonSyntaxText(tk.Text):
    """A Text widget with basic Python syntax highlighting and smart indentation."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(undo=True, tabs=('1c'))
        self.bind('<KeyRelease>', self._on_key_release)
        self.bind('<Return>', self._on_return)
        self._setup_tags()

    def _setup_tags(self):
        self.tag_configure("keyword", foreground="#0077aa", font=("Consolas", 12, "bold"))
        self.tag_configure("string", foreground="#a31515")
        self.tag_configure("comment", foreground="#008000", font=("Consolas", 12, "italic"))
        self.tag_configure("builtin", foreground="#795E26")
        self.tag_configure("number", foreground="#098658")

    def _on_key_release(self, event=None):
        self.highlight()

    def highlight(self):
        code = self.get("1.0", tk.END)
        self.tag_remove("keyword", "1.0", tk.END)
        self.tag_remove("string", "1.0", tk.END)
        self.tag_remove("comment", "1.0", tk.END)
        self.tag_remove("builtin", "1.0", tk.END)
        self.tag_remove("number", "1.0", tk.END)

        lines = code.split('\n')
        for idx, line in enumerate(lines):
            start = f"{idx+1}.0"
            # Highlight comments
            comment_idx = line.find('#')
            if comment_idx != -1:
                self.tag_add("comment", f"{idx+1}.{comment_idx}", f"{idx+1}.end")
                line = line[:comment_idx]
            # Highlight strings
            pos = 0
            while True:
                s1 = line.find('"', pos)
                s2 = line.find("'", pos)
                if s1 == -1 and s2 == -1:
                    break
                if s1 != -1 and (s2 == -1 or s1 < s2):
                    end = line.find('"', s1+1)
                    if end != -1:
                        self.tag_add("string", f"{idx+1}.{s1}", f"{idx+1}.{end+1}")
                        pos = end+1
                    else:
                        break
                else:
                    end = line.find("'", s2+1)
                    if end != -1:
                        self.tag_add("string", f"{idx+1}.{s2}", f"{idx+1}.{end+1}")
                        pos = end+1
                    else:
                        break
            # Highlight keywords and builtins
            for word in line.split():
                col = line.find(word)
                if word in keyword.kwlist:
                    self.tag_add("keyword", f"{idx+1}.{col}", f"{idx+1}.{col+len(word)}")
                elif word in dir(__builtins__):
                    self.tag_add("builtin", f"{idx+1}.{col}", f"{idx+1}.{col+len(word)}")
                elif word.isdigit():
                    self.tag_add("number", f"{idx+1}.{col}", f"{idx+1}.{col+len(word)}")

    def _on_return(self, event):
        # Smart indentation for Python blocks (for, if, def, class, while, try, except, finally, with)
        line_idx = int(self.index(tk.INSERT).split('.')[0]) - 1
        prev_line = self.get(f"{line_idx}.0", f"{line_idx}.end")
        indent = len(prev_line) - len(prev_line.lstrip(' '))
        # Increase indent after colon (block openers)
        if prev_line.rstrip().endswith(':'):
            indent += 4
        # Decrease indent for dedent keywords
        dedent_keywords = ('return', 'break', 'continue', 'pass', 'raise')
        if any(prev_line.strip().startswith(kw) for kw in dedent_keywords):
            indent = max(0, indent - 4)
        self.insert(tk.INSERT, '\n' + ' ' * indent)
        return "break"

class TortoiseIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("TortoiseLang IDE 🐢")
        self.typing_speed = 0
        self.last_time = time.time()
        self.turtle_angry = False

        self.editor = PythonSyntaxText(root, height=15, width=70, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4")
        self.editor.pack(pady=10)
        self.editor.bind("<Key>", self.track_speed)
        self.editor.bind("<Key>", self.prevent_typing_when_angry, add='+')

        self.output = tk.Label(root, text="Slow and steady...", font=("Consolas", 12), fg="green", bg="#1e1e1e")
        self.output.pack()

        # Turtle rage window (hidden by default)
        self.turtle_win = None

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
        label = tk.Label(self.turtle_win, text=turtle, font=("Consolas", 10), fg="red", justify="left", bg="#1e1e1e")
        label.pack(padx=10, pady=10)
        # Prevent typing while angry
        self.turtle_angry = True
        self.editor.config(state=tk.DISABLED)
        # Auto-close after 2 seconds and re-enable typing
        def calm_turtle():
            if self.turtle_win:
                self.turtle_win.destroy()
            self.turtle_angry = False
            self.editor.config(state=tk.NORMAL)
        self.turtle_win.after(2000, calm_turtle)

    def prevent_typing_when_angry(self, event):
        if self.turtle_angry:
            return "break"

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

    def run_code(self):
        # 10% chance to refuse to run due to laziness
        if random.random() < 0.1:
            messagebox.showwarning("Turtle is Lazy", "🐢 The turtle is feeling lazy and refuses to run your code right now. Try again!")
            return
        # Run code in editor as if it's Python (with please() available)
        text = self.editor.get("1.0", tk.END)
        output_win = tk.Toplevel(self.root)
        output_win.title("Output")
        output_text = tk.Text(output_win, height=15, width=70, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4")
        output_text.pack()
        def please():
            output_text.insert(tk.END, "🙏 The turtle thanks you for your politeness.\n")
        try:
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
    root.configure(bg="#1e1e1e")
    app = TortoiseIDE(root)
    root.mainloop()