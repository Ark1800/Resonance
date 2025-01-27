# By: Andrew C.
# Date: 2024-12-07
# Program Details: This Program is a fully functional wave based attack game WITH a miniboss and a final boss it is called resonance and you collect music discs and items for power

#
import os, sys, ULTIMATE_DEFS, random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import manager
from PySide6.QtWidgets import QMainWindow
from gui.page_youdied_ui import Ui_MainWindow
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QListWidget, QLabel, QWidget


if __name__ == "__main__":    
    manager.start()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        with manager.image_gui_path():
            self.setupUi(self)
    
    def btn_respawn_a(self):
        manager.screen_game.setup()
        manager.screen_game.pausestate = False
        manager.widget.setCurrentWidget(manager.screen_game)
    
    def btn_title_a(self):
        manager.widget.setCurrentWidget(manager.screen_startscreen)