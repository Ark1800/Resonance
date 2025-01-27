# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_youdied.ui'
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
        MainWindow.resize(1473, 949)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.btn_respawn = QPushButton(self.centralwidget)
        self.btn_respawn.setObjectName(u"btn_respawn")
        self.btn_respawn.setGeometry(QRect(287, 589, 898, 106))
        font = QFont()
        font.setPointSize(40)
        self.btn_respawn.setFont(font)
        self.btn_respawn.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(149, 149, 149);")
        self.lbl_backround = QLabel(self.centralwidget)
        self.lbl_backround.setObjectName(u"lbl_backround")
        self.lbl_backround.setGeometry(QRect(0, 0, 1473, 961))
        self.lbl_backround.setPixmap(QPixmap(u"../images/youdied.png"))
        self.lbl_backround.setScaledContents(True)
        self.btn_title = QPushButton(self.centralwidget)
        self.btn_title.setObjectName(u"btn_title")
        self.btn_title.setGeometry(QRect(287, 730, 898, 106))
        self.btn_title.setFont(font)
        self.btn_title.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(149, 149, 149);")
        self.lbl_score = QLabel(self.centralwidget)
        self.lbl_score.setObjectName(u"lbl_score")
        self.lbl_score.setGeometry(QRect(800, 340, 711, 61))
        font1 = QFont()
        font1.setPointSize(35)
        self.lbl_score.setFont(font1)
        self.lbl_score.setStyleSheet(u"color: rgb(255, 255, 255);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.lbl_backround.raise_()
        self.btn_respawn.raise_()
        self.btn_title.raise_()
        self.lbl_score.raise_()

        self.retranslateUi(MainWindow)
        self.btn_respawn.clicked.connect(MainWindow.btn_respawn_a)
        self.btn_title.clicked.connect(MainWindow.btn_title_a)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Page 1", None))
        self.btn_respawn.setText(QCoreApplication.translate("MainWindow", u"Respawn", None))
        self.lbl_backround.setText("")
        self.btn_title.setText(QCoreApplication.translate("MainWindow", u"Title Screen", None))
        self.lbl_score.setText("")
    # retranslateUi

