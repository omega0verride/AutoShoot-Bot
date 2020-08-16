from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui

class OnOffslideButton(QCheckBox):
    def __init__(self, parent, value):
        super(QCheckBox, self).__init__(parent)
        self.setEnabled(True)
        self._enable = 0
        self.setChecked(not value)

    def mousePressEvent(self, *args, **kwargs):

        if self.isChecked():
            self.setChecked(False)
            self.parent().turnBotOn()
        else:
            self.setChecked(True)
            self.parent().turnBotOff()
        return QCheckBox.mousePressEvent(self, *args, **kwargs)

    def paintEvent(self, event):

        self.setMinimumHeight(10)
        self.setMinimumWidth(20)
        self.setMaximumHeight(30)
        self.setMaximumWidth(70)

        self.resize(self.parent().width(), self.parent().height())
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.isChecked():
            brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
            painter.setBrush(brush)

            painter.drawRoundedRect(0, 0, self.width() - 2, self.height() - 2,
                                    self.height() / 2, self.height() / 2)

            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            painter.setBrush(brush)
            painter.drawEllipse(0, 0, self.height(), self.height())

        else:
            brush = QtGui.QBrush(QtGui.QColor(66, 149, 244))
            painter.setBrush(brush)

            painter.drawRoundedRect(0, 0, self.width() - 2, self.height() - 2,
                                    self.height() / 2, self.height() / 2)

            brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
            painter.setBrush(brush)
            painter.drawEllipse(self.width() - self.height(), 0, self.height(), self.height())