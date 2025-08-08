<img width="3188" height="1202" alt="frame (3)" src="https://github.com/user-attachments/assets/517ad8e9-ad22-457d-9538-a9e62d137cd7" />

# 🐢 TortoiseLang – Slower is Better

A **sarcastic programming language** that throws errors if you type too fast.  
Complete with a screaming ASCII turtle, fake poetic compiler, and sassy IDE.  
Why rush, when your code can feel... meaningful?

---

## 🧠 Basic Details

### Team Name: XYZ

### Team Members
- Team Lead:  **Sebin Mathew** – College of Engineering Chengannur  
- **Abin Zachariah Abraham** – College of Engineering Chengannur

---

## 🚫 The Problem (that doesn't exist)

Most programming languages focus on speed, efficiency, and productivity,  
leading to stressful coding habits and unrealistic expectations on typing speed.

---

## ✅ The Solution (that nobody asked for)

**TortoiseLang** introduces a language that enforces slow typing.  
Typing too fast results in errors and angry turtle ASCII feedback.  
It promotes *"patience-oriented programming"* with haikus, delays, and sarcastic praise.

---

## 🔧 Technologies / Components Used

### Software:
- Python (for interpreter)
- Tkinter
- PyQt5
- Streamlit *(optional for web showcase)*

### Libraries:
- curses / windows-curses
- keyboard
- time
- fpdf
- rich
- os, sys, re, argparse *(optional)*
- VS Code + Extensions

---

## ⚙️ Installation

```bash
pip install windows-curses keyboard time fpdf rich pyqt5
```

> For Linux/Mac: use `curses` instead of `windows-curses`.

---

## ▶️ How to Run

### 1. **Run the Interpreter (for `.slow` files):**

```bash
python tortoise_lang.py <yourfile.slow>
```

- This will check your code for politeness (`please()` calls at random intervals).
- **10% of the time, the compiler will refuse to run your code due to laziness. Just try again!**
- If polite, your code runs just like Python.
- If not, you'll get a "Your code is too rude!" error.

---

### 2. **Use the Included IDE:**

```bash
python ui-fakeide.py
```

#### **IDE Features:**
- **Live typing speed enforcement:**  
  Type too fast and a turtle rage window will pop up with sarcastic feedback.
- **Politeness check:**  
  Use the "Export as .slow" button to save your code. The IDE will check for `please()` calls at random intervals and refuse to export if your code is "too rude".
- **Run code like Python:**  
  Use the "Run (like Python)" button to execute your code directly in the IDE. The `please()` function is available and prints a polite message.
- **Python color scheme and smart indentation:**  
  The editor highlights Python keywords, strings, comments, and builtins, and auto-indents after colons for blocks.

---

## 🐢 Language Features

- **Python-like syntax:** Write code just like Python.
- **Speed enforcement:** Typing too fast triggers sarcastic errors and turtle rage (in a popup window in the IDE).
- **Politeness required:** You must include `please()` calls at random intervals in your code, or the compiler/IDE refuses to run or export ("Your code is too rude!").
- **Sarcastic feedback:** Get sassy remarks and poetic haikus if you break the rules.
- **Export options:** Save your code as `.slow` (with politeness check).
- **Fake IDE:** Includes a Tkinter-based IDE with live feedback, export, and run buttons, Python color scheme, and smart indentation.

---

## 🧪 How to Test the IDE

1. **Start the IDE:**
   ```bash
   python ui-fakeide.py
   ```

2. **Type your code** in the editor window.  
   - If you type too fast, a turtle rage popup will appear and sarcastic feedback will be shown.
   - If you slow down, the turtle will be happy.
   - Python keywords, comments, and strings are highlighted. Indentation is automatic after colons.

3. **Insert `please()` calls** every few lines (at random intervals) in your code.

4. **Export your code:**
   - Click "Export as .slow (politeness check)" to save your code as a `.slow` file.  
     If you don't have enough `please()` calls, the IDE will refuse to export and show you where to add one.

5. **Run your code:**
   - Click "Run (like Python)" to execute your code in the IDE.  
     Output (including `please()` messages) will appear in a new window.

6. **Test your `.slow` file in the interpreter:**
   ```bash
   python tortoise_lang.py your_exported_file.slow
   ```
   - If your code is polite, it will run (unless the compiler is "lazy"—just try again).
   - If not, you'll get a "too rude" error.

---

## 📝 Example `.slow` File

```python
print("Hello, world!")
please()
for i in range(3):
    print(i)
please()
print("Done!")
```

---

## 🖼️ Screenshots

![Screenshot1](screenshots/ide_window.png)
*A fake IDE window showing turtle ASCII reacting to fast typing.*

![Screenshot2](screenshots/error_message.png)
*Sarcastic error: “Whoa there, Shakespeare. Try again… slower.”*

![Screenshot3](screenshots/final_output.png)
*The “compiled” poetic output of your slow-written program.*

---

## 📊 Diagram

![Workflow](assets/workflow_diagram.png)
*Workflow: Typing input → Typing speed tracker → Syntax validator →
Turtle rage ASCII → Sarcastic error → Poetic output*

---

## 🎥 Project Demo

### 📹 Video

[Demo Video Link](https://example.com/demo-tortoise-lang)
*Demonstrates typing, turtle reactions, and poetic output.*

### 🎭 Additional Demos

* [ASCII Turtle Pack](https://example.com/ascii-turtles)
* [Sample Tortoise Code](https://example.com/sample.tortoise)

---

## 🧑‍🤝‍🧑 Team Contributions

* **Sebin Mathew** – Typing speed engine, sarcasm handler, turtle rage ASCII
* **Abin Zachariah Abraham** – Fake IDE window UI, PDF export module, emoji benchmark spoof

---

Made with ❤️ at TinkerHub Useless Projects
![Badge](https://img.shields.io/badge/TinkerHub-24-black)
![Badge](https://img.shields.io/badge/UselessProjects--25-25)
