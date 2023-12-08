import argparse
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QTextEdit, QHBoxLayout
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import QSize, Qt
import html

import difflib
import pyperclip


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=None)
    parser.add_argument("-c", "--corrected", default=None)
    parser.add_argument("-x", "--xpos", default=0)
    parser.add_argument("-y", "--ypos", default=0)
    return parser.parse_args()


def get_colored(original_str, modified_str):
    d = difflib.Differ()
    diff = list(d.compare(original_str, modified_str))
    original = []
    modified = []
    for char in diff:
        if char.startswith("-"):
            original.append([char[-1], "red"])
        elif char.startswith(" "):
            original.append([char[-1], None])
            modified.append([char[-1], None])
        elif char.startswith("+"):
            modified.append([char[-1], "green"])
    return original, modified


class CopyButton(QWidget):
    def __init__(self, modified_str=''):
        super(CopyButton, self).__init__()
        button = QPushButton(self)
        lightness = self.palette().color(QPalette.Window).lightnessF()
        theme = "dark_theme" if lightness < 0.5 else "light_theme"
        icon = QIcon(f"./resources/copy_{theme}.svg")
        button.setIcon(icon)
        icon_size = QSize(64, 64)
        button.setIconSize(icon_size)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setSizeIncrement(10, 10)
        self.setMinimumSize(100, 50)
        self.setMaximumSize(30000, 120)
        button.resizeEvent = lambda event: self.on_resize(button, icon)
        button.clicked.connect(lambda event: pyperclip.copy(modified_str))
        layout = QVBoxLayout(self)
        layout.addWidget(button)

    def on_resize(self, button, icon):
        size = QSize(button.width(), button.height())
        icon.actualSize(size)
        button.setIconSize(size)


class ArrowLabel(QWidget):
    def __init__(self):
        super(ArrowLabel, self).__init__()
        label = QLabel(self)
        lightness = self.palette().color(self.palette().Window).lightnessF()
        theme = "dark_theme" if lightness < 0.5 else "light_theme"
        icon = QIcon(f"./resources/arrow_{theme}.svg")
        pixmap = icon.pixmap(QSize(64, 64))
        label.setPixmap(pixmap)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(200, 10000)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.resizeEvent = lambda event: self.on_resize(label, icon)
        layout = QVBoxLayout(self)
        layout.addWidget(label)

    def on_resize(self, label, icon):
        size = QSize(label.width(), label.height())
        pixmap = icon.pixmap(size)
        label.setPixmap(pixmap)


class DisplayResult(QWidget):
    def __init__(self, original_str='', modified_str=''):
        super().__init__()
        self.original_str = original_str
        self.modified_str = modified_str
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.te_input = QTextEdit()
        self.te_corrected = QTextEdit()
        self.te_input.setReadOnly(True)
        self.te_corrected.setReadOnly(True)
        original, modified = get_colored(self.original_str, self.modified_str)
        self.set_colored_text(self.te_input, original)
        self.set_colored_text(self.te_corrected, modified)
        right_area = QWidget()
        right_layout = QVBoxLayout()
        self.te_input.setStyleSheet('QTextEdit { white-space: break-spaces; }')
        self.te_corrected.setStyleSheet('QTextEdit { white-space: break-spaces; }')
        right_area.setLayout(right_layout)

        right_layout.addWidget(self.te_corrected)
        right_layout.addWidget(CopyButton(modified_str=self.modified_str))
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.te_input)
        splitter.addWidget(ArrowLabel())
        splitter.addWidget(right_area)
        splitter.setStretchFactor(0, 1)
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setWindowTitle("Spell checker")

        self.setGeometry(100, 100, 600, 200)

    def set_colored_text(self, text_edit, colored_str):
        cursor = text_edit.textCursor()
        for char in colored_str:
            color = char[1]
            escaped = "&nbsp;" if char[0] == ' ' else html.escape(char[0])
            if color:
                cursor.insertHtml(
                    f'<font style="color: white; background-color: {color}">{escaped}</font>'
                )
            else:
                cursor.insertHtml(f'<font>{escaped}</font>')


if __name__ == "__main__":
    args = get_args()
    app = QApplication(sys.argv)
    window = DisplayResult(original_str=args.input, modified_str=args.corrected)
    window.show()
    sys.exit(app.exec_())
