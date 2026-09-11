from feature_popup import show_features_popup

show_features_popup()
import keyword
import random
import time
import tkinter as tk
from tkinter import messagebox
_rng = random.SystemRandom()

from ascii_turtle import show_turtle_just_right, show_turtle_rage, show_turtle_too_slow
from sarcasm_engine import get_loading_quote, get_sarcastic_message
from tortoise_lang import check_pleases
from typing_engine import wpm_from_timestamps

SAMPLE_CODE = '''print("Hello, world!")
for i in range(3):
    print(i)
please()
print("Done!")
'''

RAGE_LOCKOUT_SECONDS = 2


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
        self.key_times = []
        self._rage_remaining = 0

        editor_frame = tk.Frame(root, bg="#1e1e1e")
        editor_frame.pack(pady=10)
        self.gutter = tk.Text(editor_frame, width=4, height=15, font=("Consolas", 12), bg="#252526", fg="#858585", state=tk.DISABLED, wrap=tk.NONE, borderwidth=0, highlightthickness=0, takefocus=0)
        self.gutter.pack(side=tk.LEFT, fill=tk.Y)
        self.editor = PythonSyntaxText(editor_frame, height=15, width=70, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4", borderwidth=0, highlightthickness=0)
        self.editor.pack(side=tk.LEFT)
        self.editor.bind("<Key>", self.track_speed)
        self.editor.bind("<Key>", self.prevent_typing_when_angry, add='+')
        self.editor.bind("<KeyRelease>", lambda e: self.refresh_gutter(), add='+')
        self.editor.config(yscrollcommand=self._sync_gutter_scroll)
        self.refresh_gutter()

        self.output = tk.Label(root, text="Slow and steady...", font=("Consolas", 12), fg="green", bg="#1e1e1e")
        self.output.pack()

        # Turtle rage window (hidden by default)
        self.turtle_win = None

        self.run_btn = tk.Button(root, text="Run (like Python)", command=self.run_code)
        self.run_btn.pack(pady=5)

        self.sample_btn = tk.Button(root, text="Load sample", command=self.load_sample)
        self.sample_btn.pack(pady=5)

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
        self._rage_remaining = RAGE_LOCKOUT_SECONDS
        self.countdown = tk.Label(self.turtle_win, text=f"Typing unlocks in {self._rage_remaining}…", font=("Consolas", 11), fg="red", bg="#1e1e1e")
        self.countdown.pack(pady=(0, 10))
        # Prevent typing while angry
        self.turtle_angry = True
        self.editor.config(state=tk.DISABLED)
        # Closing the popup early still ends the lockout cleanly
        self.turtle_win.protocol("WM_DELETE_WINDOW", self.calm_turtle)
        self.turtle_win.after(1000, self._tick_rage_countdown)
        # Auto-close after the lockout and re-enable typing
        self.turtle_win.after(RAGE_LOCKOUT_SECONDS * 1000, self.calm_turtle)

    def _tick_rage_countdown(self):
        if not self.turtle_angry or self.turtle_win is None or not tk.Toplevel.winfo_exists(self.turtle_win):
            return
        self._rage_remaining -= 1
        if self._rage_remaining > 0:
            self.countdown.config(text=f"Typing unlocks in {self._rage_remaining}…")
            self.turtle_win.after(1000, self._tick_rage_countdown)

    def calm_turtle(self):
        if self.turtle_win:
            self.turtle_win.destroy()
            self.turtle_win = None
        self.turtle_angry = False
        self.editor.config(state=tk.NORMAL)
        self.editor.focus_set()

    def refresh_gutter(self):
        lines = int(self.editor.index("end-1c").split(".")[0])
        self.gutter.config(state=tk.NORMAL)
        self.gutter.delete("1.0", tk.END)
        self.gutter.insert("1.0", "\n".join(str(i) for i in range(1, lines + 1)))
        self.gutter.config(state=tk.DISABLED)
        self._sync_gutter_scroll(*self.editor.yview())

    def _sync_gutter_scroll(self, first, last):
        self.gutter.yview_moveto(first)

    def prevent_typing_when_angry(self, event):
        if self.turtle_angry:
            return "break"

    def track_speed(self, event):
        now = time.time()
        delta = now - self.last_time
        self.last_time = now
        self.key_times.append(now)
        self.key_times = [ts for ts in self.key_times if now - ts <= 10]
        wpm = wpm_from_timestamps(self.key_times, now)
        tag = f" · {wpm:.0f} WPM"

        if self.lazy_mode.get():
            delta *= 2  # Increase delay in lazy mode

        if delta < 0.1:
            self.output.config(text=get_sarcastic_message("lazy_turtle") + tag, fg="red")
            self.show_turtle_rage_window()
        elif delta > 0.5:
            self.output.config(text="You're calm. The turtle is proud 🐢" + tag, fg="green")
        else:
            self.output.config(text="Steady typing..." + tag, fg="blue")

    def load_sample(self):
        if self.editor.get("1.0", tk.END).strip() and not messagebox.askyesno(
            "Load sample", "Replace the editor contents with the sample program?"
        ):
            return
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", SAMPLE_CODE)
        self.editor.highlight()
        self.refresh_gutter()
        self.output.config(text="Sample loaded. Type it gently 🐢", fg="green")

    def run_code(self):
        # 10% chance to refuse to run due to laziness
        if _rng.random() < 0.1 and not self.lazy_mode.get():
            messagebox.showwarning("Turtle is Lazy", "🐢 The turtle is feeling lazy and refuses to run your code right now. Try again!")
            return

        self.run_btn.config(state=tk.DISABLED)
        self.output.config(text="Running your code… the turtle is on it 🐢", fg="blue")
        loading = tk.Toplevel(self.root)
        loading.title("Compiling Slowly...")
        bar = tk.Label(loading, text="Compiling slowly... [          ]", font=("Consolas", 12))
        bar.pack(padx=20, pady=(20, 5))
        quote = tk.Label(loading, text=get_loading_quote(0), font=("Consolas", 11))
        quote.pack(padx=20, pady=(0, 20))
        self._loading_step(loading, bar, quote, 1)

    def _loading_step(self, loading, bar, quote, i):
        if i > 10:
            loading.destroy()
            self._execute_code()
            return
        bar.config(text=f"Compiling slowly... [{'='*i}{' '*(10-i)}]")
        quote.config(text=get_loading_quote(i - 1))
        loading.after(150, lambda: self._loading_step(loading, bar, quote, i + 1))

    def _execute_code(self):

        # Run code in editor as if it's Python (with please() available)
        text = self.editor.get("1.0", tk.END)
        output_win = tk.Toplevel(self.root)
        output_win.title("Output")
        output_text = tk.Text(output_win, height=15, width=70, font=("Consolas", 12), bg="#1e1e1e", fg="#d4d4d4")
        output_text.pack()
        if not check_pleases(text.splitlines()):
            output_text.insert(tk.END, "🐢 Refusing to run rude code. Add more 'please()' calls!\n")
            self.run_btn.config(state=tk.NORMAL)
            return
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
        self.run_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1e1e1e")
    app = TortoiseIDE(root)
    root.mainloop()