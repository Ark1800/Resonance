from PySide6.QtCore import QTimer
from PySide6.QtCore import Qt
from PySide6.QtCore import QRect
from PySide6.QtCore import QTimer, QRect, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QListWidget

def collision(object1, object2):
    # Get the global coordinates of the top-left corner of object1
    object1_global_top_left = object1.mapToGlobal(object1.rect().topLeft())

    # Get the global coordinates of the top-left corner of object2
    object2_global_top_left = object2.mapToGlobal(object2.rect().topLeft())
    
    # Check for collision
    return QRect(object1_global_top_left, object1.rect().size()).intersects(QRect(object2_global_top_left, object2.rect().size()))
