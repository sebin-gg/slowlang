from feature_popup import show_features_popup

show_features_popup()
import keyword
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox
_rng = random.SystemRandom()

from ascii_turtle import show_turtle_just_right, show_turtle_rage, show_turtle_too_slow
from sarcasm_engine import get_sarcastic_message


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

    def _clear_tags(self):
        for tag in ("keyword", "string", "comment", "builtin", "number"):
            self.tag_remove(tag, "1.0", tk.END)

    def _highlight_line(self, line: str, lineno: int) -> str:
        """Highlight one source line. Returns the code portion (comments stripped)."""
        comment_idx = line.find('#')
        if comment_idx != -1:
            self.tag_add("comment", f"{lineno}.{comment_idx}", f"{lineno}.end")
            line = line[:comment_idx]

        pos = 0
        while True:
            s1 = line.find('"', pos)
            s2 = line.find("'", pos)
            if s1 == -1 and s2 == -1:
                break
            if s1 != -1 and (s2 == -1 or s1 < s2):
                end = line.find('"', s1 + 1)
            else:
                end = line.find("'", s2 + 1)
                s1 = s2
            if end == -1:
                break
            self.tag_add("string", f"{lineno}.{s1}", f"{lineno}.{end + 1}")
            pos = end + 1

        for word in line.split():
            col = line.find(word)
            end_col = col + len(word)
            if word in keyword.kwlist:
                self.tag_add("keyword", f"{lineno}.{col}", f"{lineno}.{end_col}")
            elif word in dir(__builtins__):
                self.tag_add("builtin", f"{lineno}.{col}", f"{lineno}.{end_col}")
            elif word.isdigit():
                self.tag_add("number", f"{lineno}.{col}", f"{lineno}.{end_col}")
        return line

    def highlight(self):
        self._clear_tags()
        for idx, line in enumerate(self.get("1.0", tk.END).split('\n')):
            self._highlight_line(line, idx + 1)

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

        # Lazy mode checkbox
        self.lazy_mode = tk.BooleanVar()
        tk.Checkbutton(root, text="Lazy Mode", variable=self.lazy_mode, bg="#1e1e1e", fg="#d4d4d4", selectcolor="#333").pack()

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

        if self.lazy_mode.get():
            delta *= 2  # Increase delay in lazy mode

        if delta < 0.1:
            self.output.config(text=get_sarcastic_message("lazy_turtle"), fg="red")
            self.show_turtle_rage_window()
        elif delta > 0.5:
            self.output.config(text="You're calm. The turtle is proud 🐢", fg="green")
        else:
            self.output.config(text="Steady typing...", fg="blue")

    def run_code(self):
        # 10% chance to refuse to run due to laziness
        if _rng.random() < 0.1 and not self.lazy_mode.get():
            messagebox.showwarning("Turtle is Lazy", "🐢 The turtle is feeling lazy and refuses to run your code right now. Try again!")
            return

        # In run_code() before executing code
        def fake_loading():
            loading = tk.Toplevel(self.root)
            loading.title("Compiling Slowly...")
            bar = tk.Label(loading, text="Compiling slowly... [          ]", font=("Consolas", 12))
            bar.pack(padx=20, pady=20)
            for i in range(1, 11):
                bar.config(text=f"Compiling slowly... [{'='*i}{' '*(10-i)}]")
                loading.update()
                time.sleep(0.15)
            loading.destroy()
        threading.Thread(target=fake_loading).start()
        time.sleep(1.7)  # Wait for fake loading to finish

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
            exec(text, {"please": please})  # noqa: S102 - editor content is user-authored by design
            sys.stdout = old_stdout
            output_text.insert(tk.END, mystdout.getvalue())
        except Exception as e:  # noqa: BLE001 - GUI must show any error to the user
            output_text.insert(tk.END, f"Error: {e}\n")
        finally:
            sys.stdout = old_stdout

        from sarcasm_engine import get_poetic_output
        output_text.insert(tk.END, "\n✨ Poetic wisdom:\n" + get_poetic_output() + "\n")

        # Show turtle satisfaction or dissatisfaction
        if _rng.random() < 0.2:
            show_turtle_rage()
        elif _rng.random() < 0.5:
            show_turtle_too_slow()
        else:
            show_turtle_just_right()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1e1e1e")
    app = TortoiseIDE(root)
    root.mainloop()