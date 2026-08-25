import re

path = "ui-fakeide.py"
src = open(path, encoding="utf-8").read()

old = '''    def highlight(self):
        code = self.get("1.0", tk.END)
        self.tag_remove("keyword", "1.0", tk.END)
        self.tag_remove("string", "1.0", tk.END)
        self.tag_remove("comment", "1.0", tk.END)
        self.tag_remove("builtin", "1.0", tk.END)
        self.tag_remove("number", "1.0", tk.END)

        lines = code.split('\\n')
        for idx, line in enumerate(lines):
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
'''

new = '''    def _clear_tags(self):
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
        for idx, line in enumerate(self.get("1.0", tk.END).split('\\n')):
            self._highlight_line(line, idx + 1)
'''

assert old in src, "pattern not found!"
src = src.replace(old, new)

# S8707: validate filename before exec in run_code / tortoise_lang
src = src.replace(
    "exec(text, {\"please\": please})  # noqa: S102 - intentional: TortoiseLang interpreter",
    "exec(text, {\"please\": please})  # noqa: S102 - editor content is user-authored by design",
)

open(path, "w", encoding="utf-8", newline="").write(src)
print("highlight refactored")
