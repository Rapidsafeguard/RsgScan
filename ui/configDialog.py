#!/usr/bin/env python

'''
Company name : Rapidsafeguard
Author  : Punit Darji
Linked-in : punit-darji-5500
Twitter  : rapidsafeguard
instagram : Rapidsafeguard
Blog : www.easyhack.in

'''

import os
from PyQt5.QtGui import *                                               # for filters dialog
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from app.auxiliary import *                                             # for timestamps
from six import u as unicode
from ui.ancillaryDialog import flipState

class Config(QtWidgets.QPlainTextEdit):
    def __init__(self, qss, parent = None):
        super(Config, self).__init__(parent)
        self.setMinimumHeight(550)
        self.setStyleSheet(qss)
        self.setPlainText(open('rsgscan.conf','r').read())
        self.setReadOnly(False)

    def getText(self):
        return self.toPlainText()

class ConfigDialog(QtWidgets.QDialog):
    def __init__(self, controller, qss, parent = None):
        super(ConfigDialog, self).__init__(parent)
        self.controller = controller
        self.qss = qss
        self.setWindowTitle("Config")
        self.Main = QtWidgets.QVBoxLayout()
        self.frm = QtWidgets.QFormLayout()
        self.setGeometry(0, 0, 800, 600)
        self.center()
        self.Qui_update()
        self.setStyleSheet(self.qss)

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def Qui_update(self):
        self.form = QtWidgets.QFormLayout()
        self.form2 = QtWidgets.QVBoxLayout()
        self.tabwid = QtWidgets.QTabWidget(self)
        self.TabConfig = QtWidgets.QWidget(self)
        self.cmdSave = QtWidgets.QPushButton("Save")
        self.cmdSave.setFixedWidth(90)
        self.cmdSave.setIcon(QtGui.QIcon('images/save.png'))
        self.cmdSave.clicked.connect(self.save)
        self.cmdClose = QtWidgets.QPushButton("Close")
        self.cmdClose.setFixedWidth(90)
        self.cmdClose.setIcon(QtGui.QIcon('images/close.png'))
        self.cmdClose.clicked.connect(self.close)

        self.formConfig = QtWidgets.QFormLayout()

        # Config Section
        self.configObj = Config(qss = self.qss)
        self.formConfig.addRow(self.configObj)
        self.TabConfig.setLayout(self.formConfig)

        self.tabwid.addTab(self.TabConfig,'Config')
        self.form.addRow(self.tabwid)
        self.form2.addWidget(QtWidgets.QLabel('<br>'))
        self.form2.addWidget(self.cmdSave, alignment = Qt.AlignCenter)
        self.form2.addWidget(self.cmdClose, alignment = Qt.AlignCenter)
        self.form.addRow(self.form2)
        self.Main.addLayout(self.form)
        self.setLayout(self.Main)

    def save(self):
        fileObj = open('rsgscan.conf','w')
        fileObj.write(self.configObj.getText())
        fileObj.close()
        self.controller.loadSettings()
