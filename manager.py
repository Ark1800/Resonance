
# By: <Your Name Here>
# Date:2024-12-07
# Program Details: <Program Description Here>

import sys, os, contextlib
from PySide6.QtWidgets import (QStackedWidget, QApplication)
import interface.page_game
import interface.page_startscreen
import interface.page_youdied


def start():
    widget.show()
    sys.exit(app.exec())

@contextlib.contextmanager
def image_gui_path():
    try:
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui'))
        yield
    finally:
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))

app = QApplication(sys.argv)
screen_game = interface.page_game.MainWindow()
screen_startscreen = interface.page_startscreen.MainWindow()
screen_youdied = interface.page_youdied.MainWindow()
list_on_screens = list(globals())
widget = QStackedWidget()
for variable_name in list_on_screens:
    if variable_name.startswith('screen'):
        value = globals()[variable_name]
        widget.addWidget(value)
widget.resize(screen_game.size())
widget.setWindowTitle(screen_game.windowTitle());
screen_game.setFocus()
widget.setCurrentWidget(screen_startscreen)
screen_game.pausestate = True