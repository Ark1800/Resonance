import random
from PySide6.QtCore import QTimer, QRect, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QListWidget, QLabel, QWidget

class item:
  
  #initialization
  def __init__(self, pixmap, slot_pixmap, type, title, description, stylesheet, attackbuff, rangedbuff, defensebuff, speedbuff, lifeforcebuff):
    self.pixmap = pixmap
    self.slot_pixmap = slot_pixmap
    self.title = title
    self.description = description
    self.stylesheet = stylesheet
    self.attackbuff = attackbuff
    self.rangedbuff = rangedbuff
    self.defensebuff = defensebuff
    self.speedbuff = speedbuff
    self.lifeforcebuff = lifeforcebuff
    self.type = type
  
  def myfunc(self):
    print("Hello my stats are:", self.pixmap, self.slot_pixmap, self.type, self.title, self.description, self.stylesheet, self.attackbuff, self.rangedbuff, self.defensebuff, self.speedbuff, self.lifeforcebuff)
    
  def __str__(self):
    return f"{self.pixmap}, {self.slot_pixmap}, {self.type}, {self.title}, {self.description}, {self.stylesheet}, {self.attackbuff}, {self.rangedbuff}, {self.defensebuff}, {self.speedbuff}, {self.lifeforcebuff}"
  
class healthpot:
  #initialization
  def __init__(self, pixmap, title, description, stylesheet):
    self.pixmap = pixmap
    self.title = title
    self.description = description
    self.stylesheet = stylesheet
  
  def myfunc(self):
    print("Hello my stats are:", self.pixmap, self.title, self.description, self.stylesheet)
    
  def __str__(self):
    return f"{self.pixmap}, {self.title}, {self.description}, {self.stylesheet}"