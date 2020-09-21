from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui

class alertWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(alertWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(250, 100)
        self.setWindowTitle(appname)
        self.appIcon = QtGui.QIcon(os.path.join(working_directory, 'icon.ico'))
        self.setWindowIcon(self.appIcon)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)


        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.close_window)
        self.btn_close.setFixedSize(25, 20)
        self.btn_close.setObjectName("closeBtn")
        self.btn_close.setFocusPolicy(QtCore.Qt.NoFocus)

        self.closeBtnLayout = QHBoxLayout()
        self.closeBtnLayout.addStretch(1)
        self.closeBtnLayout.addWidget(self.btn_close)

        self.alertMessage = QLabel("App Already Running!")
        self.alertMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.alertMessage.setObjectName("alert")

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.close_window)
        self.okBtn.setFixedWidth(50)
        self.okBtnLay = QHBoxLayout()
        self.okBtnLay.addStretch(1)
        self.okBtnLay.addWidget(self.okBtn)
        self.okBtnLay.addStretch(1)

        self.layout.addLayout(self.closeBtnLayout)
        self.layout.addWidget(self.alertMessage)
        self.layout.addSpacing(8)
        self.layout.addLayout(self.okBtnLay)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def close_window(self):
        self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()