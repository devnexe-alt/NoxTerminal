# 🖥️ NoxTerminal

A lightweight, modern, and minimalist terminal emulator built specifically for **PyQt5** applications. 

`NoxTerminal` provides a seamless way to embed a functional Windows command prompt (via `winpty`) directly into your Python GUI projects with a clean, dark aesthetic.

---

## ✨ Features

* **PyQt5 Native**: Built as a `QPlainTextEdit` subclass, making it easy to drop into any PyQt5 layout.
* **Real-time PTY**: Uses `winpty` for authentic terminal interaction on Windows.
* **Modern Aesthetic**: Minimalist deep-black theme (`#0c0c0c`) with customizable Consolas font.
* **Smart ANSI Handling**: Integrated with `pyte` for proper terminal state emulation (cursor tracking, screen clearing).
* **Key Support**: Handles Tab completion, Arrow keys, Ctrl+C/V, and standard terminal control sequences.
* **Multi-threaded**: Output is handled in a separate `QThread` to keep the UI responsive.

## 🚀 Quick Start

### Prerequisites

You will need Python 3.x and the following dependencies:

```bash
pip install PyQt5 pywinpty pyte
```

## Installation

### 1. Clone the repository:
```
git clone https://github.com/devnexe-alt/NoxTerminal.git
```

### 2. Run the terminal:
```
python main.py
```

## 🛠️ Usage
### To use NoxTerminal in your own PyQt5 app, simply import the class:
```
from nox_terminal import NoxTerminal
from PyQt5.QtWidgets import QApplication

app = QApplication([])
terminal = NoxTerminal()
terminal.show()
app.exec_()
```

## 🎨 Styles & Customization
### The terminal is designed with minimalism in mind. You can easily modify the look in the __init__ method:
```
QPlainTextEdit {
    background-color: #0c0c0c;
    color: #cccccc;
    border: none;
    padding: 5px;
}
```

# 🏗️ Project Structure
NoxTerminal: Main UI component.

* **TerminalThread**: Background worker for PTY communication.

* **ANSI_ESCAPE**: Regex engine for cleaning legacy escape codes.

* **winpty**: Integration layer for the Windows PTY.

Created by DevNexe
