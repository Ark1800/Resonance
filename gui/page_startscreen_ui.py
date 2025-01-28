# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_startscreen.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1491, 948)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lbl_player = QLabel(self.centralwidget)
        self.lbl_player.setObjectName(u"lbl_player")
        self.lbl_player.setGeometry(QRect(80, 600, 421, 311))
        self.lbl_player.setPixmap(QPixmap(u"../images/character_bottom_5.png"))
        self.lbl_player.setScaledContents(True)
        self.lbl_backround = QLabel(self.centralwidget)
        self.lbl_backround.setObjectName(u"lbl_backround")
        self.lbl_backround.setGeometry(QRect(0, 0, 1491, 961))
        self.lbl_backround.setPixmap(QPixmap(u"../images/startscreen_backround.png"))
        self.lbl_backround.setScaledContents(True)
        self.lbl_title = QLabel(self.centralwidget)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setGeometry(QRect(170, 20, 1141, 161))
        font = QFont()
        font.setPointSize(120)
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet(u"")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_arrow1 = QLabel(self.centralwidget)
        self.lbl_arrow1.setObjectName(u"lbl_arrow1")
        self.lbl_arrow1.setGeometry(QRect(500, 620, 321, 91))
        self.lbl_arrow1.setPixmap(QPixmap(u"../images/minecraft_arrow.png"))
        self.lbl_arrow1.setScaledContents(True)
        self.lbl_arrow2 = QLabel(self.centralwidget)
        self.lbl_arrow2.setObjectName(u"lbl_arrow2")
        self.lbl_arrow2.setGeometry(QRect(700, 790, 321, 91))
        self.lbl_arrow2.setPixmap(QPixmap(u"../images/minecraft_arrow.png"))
        self.lbl_arrow2.setScaledContents(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(990, 370, 451, 611))
        self.label.setPixmap(QPixmap(u"../images/final_boss.png"))
        self.label.setScaledContents(True)
        self.btn_start = QPushButton(self.centralwidget)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setGeometry(QRect(20, 170, 301, 81))
        font1 = QFont()
        font1.setPointSize(40)
        self.btn_start.setFont(font1)
        self.btn_start.setStyleSheet(u"background-color: rgb(0, 170, 255);")
        self.btn_exit = QPushButton(self.centralwidget)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(20, 260, 301, 81))
        self.btn_exit.setFont(font1)
        self.btn_exit.setStyleSheet(u"background-color: rgb(0, 170, 255);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.lbl_backround.raise_()
        self.lbl_player.raise_()
        self.lbl_title.raise_()
        self.lbl_arrow1.raise_()
        self.lbl_arrow2.raise_()
        self.label.raise_()
        self.btn_start.raise_()
        self.btn_exit.raise_()

        self.retranslateUi(MainWindow)
        self.btn_start.clicked.connect(MainWindow.btn_start_a)
        self.btn_exit.clicked.connect(MainWindow.btn_exit_a)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Resonance", None))
        self.lbl_player.setText("")
        self.lbl_backround.setText("")
        self.lbl_title.setText(QCoreApplication.translate("MainWindow", u"Resonance", None))
        self.lbl_arrow1.setText("")
        self.lbl_arrow2.setText("")
        self.label.setText("")
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
    # retranslateUi

