import random
from PySide6.QtCore import QTimer, QRect, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QListWidgetItem, QListWidget, QLabel, QWidget

class Slime:
  
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed

  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}"
  
class HauntedArmor:
  
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed
  
  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}"
  
class Mage:
  
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed, rangedattack):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed
    self.rangedattack = rangedattack
    
  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed, self.rangedattack)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}, {self.rangedattack}"

class Sonic:
  
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed
    
  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}"

class Tangela:
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed
    
  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}"

class Miniboss:
  
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed, rangedattack):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed
    self.rangedattack = rangedattack
    
  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed, self.rangedattack)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}, {self.rangedattack}"

class Boss:
  
  #initialization
  def __init__(self, health, attack, defense, pixmap, speed, rangedattack):
    self.health = health
    self.attack = attack
    self.defense = defense
    self.pixmap = pixmap
    self.speed = speed
    self.rangedattack = rangedattack
    
  def myfunc(self):
    print("Hello my stats are:", self.health, self.attack, self.defense, self.speed, self.rangedattack)
    
  def __str__(self):
    return f"{self.health}, {self.attack}, {self.defense}, {self.pixmap}, {self.speed}, {self.rangedattack}"

    

