<div align="center">

# NoxTerminal

**A lightweight, modern terminal emulator embedded in PyQt5**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=flat-square&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

*Drop a fully functional terminal right into your PyQt5 app — no compromises.*

</div>

---

## Overview

**NoxTerminal** is a `QPlainTextEdit`-based terminal widget that embeds a real Windows command prompt (`cmd.exe`) directly into any PyQt5 application. Powered by `winpty` for authentic PTY interaction and `pyte` for proper ANSI/VT terminal emulation, it behaves like a real terminal — not a fake text box.

```
┌─────────────────────────────────────────────┐
│  NoxIDE Terminal                        _ □ ✕│
├─────────────────────────────────────────────┤
│                                             │
│  Microsoft Windows [Version 10.0.22631]     │
│  (c) Microsoft Corporation.                 │
│                                             │
│  C:\Users\DevNexe> █                        │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Features

| Feature | Description |
|---|---|
| **PyQt5 Native** | Subclass of `QPlainTextEdit` — drops into any layout |
| **Real PTY** | `winpty` provides authentic `cmd.exe` interaction |
| **ANSI Emulation** | `pyte` handles screen state, cursor tracking, clear sequences |
| **Non-blocking UI** | Output runs in a `QThread` — UI stays responsive |
| **Smart key handling** | Arrow keys, Tab completion, Ctrl+C/V, Delete, Home/End |
| **Selection support** | Select text to copy; typing/backspace replaces selection |
| **Minimalist theme** | Deep black (`#0c0c0c`) with Consolas font, zero clutter |

---

## Installation

### Prerequisites

Python 3.x and the following packages:

```bash
pip install PyQt5 pywinpty pyte
```

### Clone & Run

```bash
git clone https://github.com/devnexe-alt/NoxTerminal.git
cd NoxTerminal
python main.py
```

---

## Usage

Embed `NoxTerminal` in your own PyQt5 application in seconds:

```python
from nox_terminal import NoxTerminal
from PyQt5.QtWidgets import QApplication

app = QApplication([])

terminal = NoxTerminal()
terminal.resize(900, 500)
terminal.show()

app.exec_()
```

No configuration required — it spawns `cmd.exe` automatically on init.

---

## Customization

The terminal is intentionally minimal. Edit the stylesheet in `__init__` to match your app:

```python
self.setStyleSheet("""
    QPlainTextEdit {
        background-color: #0c0c0c;  /* terminal background */
        color: #cccccc;             /* text color          */
        border: none;
        padding: 5px;
    }
""")
```

Change the font family or size:

```python
font = QFont("Consolas", 10)  # any monospace font works
self.setFont(font)
```

---

## Architecture

```
NoxTerminal/
├── main.py              # Entry point + NoxTerminal widget
│
├── NoxTerminal          # QPlainTextEdit subclass (main widget)
│   ├── pyte.Screen      # Virtual terminal screen state
│   ├── pyte.Stream      # ANSI/VT sequence parser
│   └── winpty.PtyProcess# Windows PTY process (cmd.exe)
│
└── TerminalThread       # QThread — reads PTY output asynchronously
```

**Data flow:**

```
[cmd.exe] ──PTY──▶ [TerminalThread] ──signal──▶ [NoxTerminal.on_output]
                                                        │
                                               pyte processes ANSI
                                                        │
                                               setPlainText(screen)
                                                        │
                                               cursor position sync
```

---

## Key Bindings

| Key | Action |
|---|---|
| `↑ ↓ ← →` | Send arrow escape sequences to PTY |
| `Tab` | Send tab (shell completion) |
| `Ctrl+C` | Send interrupt signal |
| `Ctrl+V` | Paste from clipboard into PTY |
| `Ctrl+Shift+C` | Copy selection |
| `Backspace` / `Delete` | Send delete to PTY |
| `Home` / `End` | Move to line start/end |

---

## Requirements

- **OS:** Windows (uses `winpty` and `cmd.exe`)
- **Python:** 3.x
- **Dependencies:** `PyQt5`, `pywinpty`, `pyte`

---

<div align="center">

Made by [DevNexe](https://github.com/devnexe)

</div>