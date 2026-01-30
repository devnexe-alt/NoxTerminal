import sys
from PyQt5.QtWidgets import QApplication, QPlainTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont
import winpty
import re
import pyte
from PyQt5.QtGui import QTextCursor

ANSI_ESCAPE = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit BOC
        [@-Z\\-_]
    |     # or [ [vlsqy]| [ (etc) ]
        \[
        [0-?]* # Parameter bytes
        [ -/]* # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)

def clean_ansi(text):
    text = ANSI_ESCAPE.sub('', text)
    return text

class TerminalThread(QThread):
    output_ready = pyqtSignal(str)

    def __init__(self, pty):
        super().__init__()
        self.pty = pty
        self.running = True

    def run(self):
        while self.running:
            try:
                output = self.pty.read(4096)
                if output:
                    self.output_ready.emit(output)
            except EOFError:
                break
            except Exception:
                self.msleep(10)

class NoxTerminal(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoxIDE Terminal")
        self.screen = pyte.Screen(80, 24)
        self.stream = pyte.Stream(self.screen)

        # Стили (Minimalism)
        font = QFont("Consolas", 10)
        self.setFont(font)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0c0c0c;
                color: #cccccc;
                border: none;
                padding: 5px;
            }
        """)
        self.setCursorWidth(2)

        try:
            self.pty = winpty.PtyProcess.spawn('cmd.exe')
        except Exception as e:
            self.insertPlainText(f"Failed to spawn PTY: {e}")
            return

        self.worker = TerminalThread(self.pty)
        self.worker.output_ready.connect(self.on_output)
        self.worker.start()

    def on_output(self, text):
        self.stream.feed(text)
        
        clean_lines = "\n".join(self.screen.display)
        
        self.blockSignals(True)
        self.setPlainText(clean_lines)
        self.blockSignals(False)
        
        self.update_cursor_position()

    def update_cursor_position(self):
        cursor = self.textCursor()

        line = self.screen.cursor.y
        column = self.screen.cursor.x

        cursor.movePosition(QTextCursor.Start)

        for _ in range(line):
            cursor.movePosition(QTextCursor.Down)

        cursor.movePosition(QTextCursor.StartOfLine)
        for _ in range(column):
            cursor.movePosition(QTextCursor.Right)

        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def keyPressEvent(self, event):
        if not self.pty.isalive():
            return

        key = event.key()
        cursor = self.textCursor()
        modifiers = event.modifiers()
        ctrl = modifiers & Qt.ControlModifier
        shift = modifiers & Qt.ShiftModifier
        text = event.text()

        if shift and key in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down, Qt.Key_Home, Qt.Key_End]:
            super().keyPressEvent(event)
            return

        if ctrl and shift:
            if key == Qt.Key_C:
                self.copy()
                return
            if key == Qt.Key_V:
                self.pty.write(QApplication.clipboard().text())
                return

        if ctrl and key == Qt.Key_X and cursor.hasSelection():
            self.copy() 

            selection_length = abs(cursor.selectionEnd() - cursor.selectionStart())
            for _ in range(selection_length):
                self.pty.write('\x7f')
            
            cursor.clearSelection()
            self.setTextCursor(cursor)
            return

        is_printable = text and text.isprintable()
        if cursor.hasSelection() and (key == Qt.Key_Backspace or is_printable):
            selection_length = abs(cursor.selectionEnd() - cursor.selectionStart())
            for _ in range(selection_length):
                self.pty.write('\x7f')
            
            cursor.clearSelection()
            self.setTextCursor(cursor)
            if key == Qt.Key_Backspace:
                return

        if ctrl:
            if key == Qt.Key_V:
                self.pty.write(QApplication.clipboard().text())
                return
            if Qt.Key_A <= key <= Qt.Key_Z:
                ctrl_code = chr(key - ord('A') + 1)
                self.pty.write(ctrl_code)
                return

        key_map = {
            Qt.Key_Up: '\x1b[A',
            Qt.Key_Down: '\x1b[B',
            Qt.Key_Right: '\x1b[C',
            Qt.Key_Left: '\x1b[D',
            Qt.Key_Home: '\x1b[H',
            Qt.Key_End: '\x1b[F',
            Qt.Key_Backspace: '\x7f', 
            Qt.Key_Tab: '\t',
            Qt.Key_Delete: '\x1b[3~',
            Qt.Key_Enter: '\r\n',
            Qt.Key_Return: '\r\n',
        }

        if key in key_map:
            self.pty.write(key_map[key])
        elif text:
            self.pty.write(text)
        
        event.accept()

    def closeEvent(self, event):
        self.worker.running = False
        if self.pty.isalive():
            self.pty.terminate()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    term = NoxTerminal()
    term.resize(900, 500)
    term.show()
    sys.exit(app.exec_())