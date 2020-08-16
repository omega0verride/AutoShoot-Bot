import os
import sys
import time
import psutil
import winshell
import win32api
import win32com.client
import win32gui
from easysettings import EasySettings
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from queue import Queue
from threading import Thread
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller
import keyboard as keyboardSimulator
import mouse
from modules import bot_overlay
keycodes = {
"code_40": "down",
"code_37": "left",
"code_39": "right",
"code_38": "up",
"code_112": "F1",
"code_113": "F2",
"code_114": "F3",
"code_115": "F4",
"code_116": "F5",
"code_117": "F6",
"code_118": "F7",
"code_119": "F8",
"code_120": "F9",
"code_121": "F10",
"code_122": "F11",
"code_123": "F12",
"code_27": "esc",
"code_34": "Page_Down",
"code_33": "Page_Up",
"code_19": "Pause",
"code_44": "Print_Screen",
"code_145": "Scroll_Lock",
"code_16": "Shift",
"code_32": "Spacebar",
"code_9": "Tab",
"code_8": "Backspace",
"code_13": "Enter",
"code_20":"Caps_Lock",
"code_18": "Alt",
"code_17": "Ctrl",
"code_46": "Delete",
"code_36": "Home",
"code_35": "End",
"code_45": "Insert",
"code_144": "Num_Lock",
"code_109": '-',
"code_106": '*',
"code_110": '.',
"code_111": '/',
"code_107": '+',
"code_96": "num_0",
"code_97": "num_1",
"code_98": "num_2",
"code_99": "num_3",
"code_100": "num_4",
"code_101": "num_5",
"code_12": "num_5",
"code_102": "num_6",
"code_103": "num_7",
"code_104": "num_8",
"code_105": "num_9",
}

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

class MainWindow(QtWidgets.QWidget):

    def __init__(self, queue, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle(appname)
        self.shortcutName = appname
        self.appIcon = QtGui.QIcon(os.path.join(working_directory, 'icon.ico'))
        self.setWindowIcon(self.appIcon)
        self.setFixedSize(550, 300)
        self.center()
        self.queue = queue

        self.config = EasySettings('config.conf')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel(appname)
        self.title.setFixedSize(200, 20)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("windowTitle")

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.close_window)
        self.btn_close.setFixedSize(25, 20)
        self.btn_close.setObjectName("closeBtn")
        self.btn_close.setFocusPolicy(QtCore.Qt.NoFocus)

        self.btn_minimise = QPushButton("-")
        self.btn_minimise.clicked.connect(self.btn_minimise_clicked)
        self.btn_minimise.setFixedSize(25, 20)
        self.btn_minimise.setObjectName("minimiseBtn")
        self.btn_minimise.setFocusPolicy(QtCore.Qt.NoFocus)

        self.titleLayout.addWidget(self.btn_close)
        self.titleLayout.addStretch(1)
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addStretch(1)
        self.titleLayout.addWidget(self.btn_minimise)

        # --------------------------------------------------------------------------------------------------------------
        global onoffLabel
        onoffLabel = QLabel("OFF")
        onoffLabel.setObjectName("onoffLabel")
        onoffLabel.setFixedWidth(65)
        onoffLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.currentOnOffShortcutLabel = QLabel("On/Off Keyboard Shortcut")
        self.currentOnOffShortcutLabel.setObjectName("currentOnOffShortcutLabel")
        self.currentOnOffShortcutLabel.setFixedWidth(200)
        # self.currentOnOffShortcutLabel.setToolTip("Note: The shortcut does not support combinations!")
        # implementmessagebox

        global currentOnOffShortcutLabel1
        with open(os.path.join(working_directory, 'shortcutRegisters', 'OnOff_Shortcut_Key.txt'), 'r') as file:
            on_off_shortcut_key_name = file.readlines()[1]
        currentOnOffShortcutLabel1 = QLabel(on_off_shortcut_key_name)
        currentOnOffShortcutLabel1.setObjectName("currentOnOffShortcutLabel1")
        currentOnOffShortcutLabel1.setAlignment(QtCore.Qt.AlignCenter)
        currentOnOffShortcutLabel1.setFixedWidth(140)

        global recordOnOffShortcut
        recordOnOffShortcut = QPushButton("Record New")
        recordOnOffShortcut.setObjectName("recordOnOffshortcutButton")
        recordOnOffShortcut.pressed.connect(self.disableBotWhileRecording)
        recordOnOffShortcut.released.connect(self.set_OnOff_shortcut_key)
        recordOnOffShortcut.setFixedSize(80, 26)
        recordOnOffShortcut.setStyleSheet(
            "QPushButton#recordOnOffshortcutButton{color: white; border: 1px solid grey;}QPushButton#recordOnOffshortcutButton:hover{border: 1px solid khaki;color: grey;}")
        recordOnOffShortcut.setFocusPolicy(QtCore.Qt.NoFocus)

        self.onoffLay = QHBoxLayout()
        self.onoffLay.addSpacing(10)
        self.onoffLay.addWidget(onoffLabel)
        self.onoffLay.addSpacing(5)
        self.onoffLay.addWidget(self.currentOnOffShortcutLabel)
        self.onoffLay.addWidget(currentOnOffShortcutLabel1)
        self.onoffLay.addStretch(1)
        self.onoffLay.addWidget(recordOnOffShortcut)
        self.onoffLay.addSpacing(30)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        global onoffButton
        onoffButton = OnOffslideButton(self, 0)
        onoffButton.setObjectName("onoffSlideButton")

        self.currentShootShortcutLabel = QLabel("Game Shoot Keybind")
        self.currentShootShortcutLabel.setObjectName("currentOnOffShortcutLabel")
        self.currentShootShortcutLabel.setFixedWidth(200)
        self.currentShootShortcutLabel.setAlignment(QtCore.Qt.AlignCenter)

        global currentShootShortcutLabel1
        with open(os.path.join(working_directory, 'shortcutRegisters', 'Game_Shoot_Shortcut_Key.txt'), 'r') as file:
            shoot_shortcut_key_name = file.readlines()[1]
        currentShootShortcutLabel1 = QLabel(shoot_shortcut_key_name)
        currentShootShortcutLabel1.setObjectName("currentOnOffShortcutLabel1")
        currentShootShortcutLabel1.setAlignment(QtCore.Qt.AlignCenter)
        currentShootShortcutLabel1.setFixedWidth(140)

        global recordShootShortcut
        recordShootShortcut = QPushButton("Record New")
        recordShootShortcut.setObjectName("recordShootshortcutButton")
        recordShootShortcut.pressed.connect(self.disableBotWhileRecording)
        recordShootShortcut.released.connect(self.set_Shoot_shortcut_key)
        recordShootShortcut.setFixedSize(80, 26)
        recordShootShortcut.setStyleSheet(
            "QPushButton#recordShootshortcutButton{color: white; border: 1px solid grey;}QPushButton#recordShootshortcutButton:hover{border: 1px solid khaki;color: grey;}")
        recordShootShortcut.setFocusPolicy(QtCore.Qt.NoFocus)

        self.keybindLay = QHBoxLayout()
        self.keybindLay.addSpacing(10)
        self.keybindLay.addWidget(onoffButton)
        self.keybindLay.addSpacing(50)
        self.keybindLay.addWidget(self.currentShootShortcutLabel)
        self.keybindLay.addWidget(currentShootShortcutLabel1)
        self.keybindLay.addStretch(1)
        self.keybindLay.addWidget(recordShootShortcut)
        self.keybindLay.addSpacing(30)
        # --------------------------------------------------------------------------------------------------------------

        self.startOnStartupCheckBox = QCheckBox("Start On Boot")
        self.startOnStartupCheckBox.clicked.connect(self.setStartOnStartup)
        self.startOnStartupCheckBox.setObjectName("checkboxes")
        self.startOnStartupCheckBox.setChecked(self.config.get('startOnBoot'))
        self.startOnStartupCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.startActiveCheckBox = QCheckBox("Start Active")
        self.startActiveCheckBox.clicked.connect(self.setStartActive)
        self.startActiveCheckBox.setObjectName("checkboxes")
        self.startActiveCheckBox.setChecked(self.config.get('startActive'))
        self.startActiveCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.overlayCheckBox = QCheckBox("Show Overlay")
        self.overlayCheckBox.clicked.connect(self.setShowOverlay)
        self.overlayCheckBox.setObjectName("checkboxes")
        self.overlayCheckBox.setChecked(self.config.get('showOverlay'))
        self.overlayCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.gamesOnlyCheckBox = QCheckBox("Active InGame Only")
        self.gamesOnlyCheckBox.clicked.connect(self.setGamesOnly)
        self.gamesOnlyCheckBox.setToolTip("If checked, bot works only in games (when the mouse icon is hidden).")
        self.gamesOnlyCheckBox.setToolTipDuration(4000)
        self.gamesOnlyCheckBox.setObjectName("checkboxes")
        self.gamesOnlyCheckBox.setChecked(self.config.get('gamesOnly'))
        self.gamesOnlyCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.checkBoxLay = QHBoxLayout()

        self.checkBoxLay.addSpacing(10)
        self.checkBoxLay.addStretch(1)
        self.checkBoxLay.addWidget(self.overlayCheckBox)
        self.checkBoxLay.addSpacing(5)
        self.checkBoxLay.addWidget(self.startOnStartupCheckBox)
        self.checkBoxLay.addSpacing(5)
        self.checkBoxLay.addWidget(self.startActiveCheckBox)
        self.checkBoxLay.addSpacing(5)
        self.checkBoxLay.addWidget(self.gamesOnlyCheckBox)
        self.checkBoxLay.addStretch(1)
        self.checkBoxLay.addSpacing(10)

        # --------------------------------------------------------------------------------------------------------------

        self.layout.addLayout(self.titleLayout)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.onoffLay)
        self.layout.addSpacing(5)
        self.layout.addLayout(self.keybindLay)
        self.layout.addStretch(1)
        self.layout.addLayout(self.checkBoxLay)
        self.layout.addSpacing(10)

        self.setLayout(self.layout)
        self.oldPos = self.pos()

        menu = QMenu()
        menu.setStyleSheet(
            open(os.path.join(working_directory, 'systemTray', 'system_tray_menu_stylesheet.css')).read())

        showAction = menu.addAction("Show")
        showAction.triggered.connect(self.show_window)
        try:
            showAction.setIcon(
                QtGui.QIcon(os.path.join(working_directory, 'systemTray', 'tray_menu_show_app_icon.png')))
        except Exception as e:
            log("Error: " + e)

        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.close_window)
        try:
            exitAction.setIcon(
                QtGui.QIcon(os.path.join(working_directory, 'systemTray', 'tray_menu_exit_app_icon.png')))
        except Exception as e:
            log("Error:" + e)

        self.tray = QSystemTrayIcon()
        self.tray_icon = QtGui.QIcon(os.path.join(working_directory, 'systemTray', 'tray_icon.png'))
        self.tray.setIcon(self.tray_icon)
        self.tray.setToolTip(appname)
        self.tray.setVisible(1)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.system_tray_icon_clicked_or_doubleclicked)

        global overlayStatus
        overlayStatus = self.config.get("showOverlay")
        global work_on_games_with_hidden_mouse_only
        work_on_games_with_hidden_mouse_only = self.config.get('gamesOnly')
        if self.config.get("startActive"):
            onoffButton.click()
            if not onoffButton.isChecked():
                self.turnBotOn()
            else:
                self.turnBotOff()

    def turnBotOn(self):
        onoffLabel.setText("ON")
        log("Set Bot: Active")
        self.queue.put([1, overlayStatus])
        global bot_active
        bot_active = 1

    def turnBotOff(self):
        onoffLabel.setText("OFF")
        log("Set Bot: Disabled")
        self.queue.put([0, overlayStatus])
        global bot_active
        bot_active = 0

    def setStartOnStartup(self):
        checked = self.startOnStartupCheckBox.isChecked()
        self.config.set("startOnBoot", checked)
        self.config.save()
        if checked:
            self.addToStartUp()
        else:
            self.removeFromStartup()

    def setStartActive(self):
        checked = self.startActiveCheckBox.isChecked()
        self.config.set("startActive", checked)
        self.config.save()

    def setShowOverlay(self):
        checked = self.overlayCheckBox.isChecked()
        self.config.set("showOverlay", checked)
        self.config.save()
        global overlayStatus
        if checked:
            overlayStatus = 1
            self.queue.put([int(not onoffButton.isChecked()), overlayStatus])
        else:
            overlayStatus = 0
            self.queue.put([2, overlayStatus])

    def setGamesOnly(self):
        checked = self.gamesOnlyCheckBox.isChecked()
        self.config.set("gamesOnly", checked)
        self.config.save()
        global work_on_games_with_hidden_mouse_only
        work_on_games_with_hidden_mouse_only = checked

    def addToStartUp(self):
        self.exe_name = os.path.basename(sys.argv[0])
        self.target_exe = (os.path.abspath(sys.argv[0]))
        self.working_directory = (os.path.abspath(sys.argv[0])).split("\\" + self.exe_name)[0]

        log("Add to startup" + str(self.exe_name) + str(self.target_exe) + str(self.working_directory))

        try:
            windowsStartupFolder = winshell.startup()
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(windowsStartupFolder + '\%s.lnk' % self.shortcutName)
            shortcut.Targetpath = r'%s' % self.target_exe
            shortcut.WorkingDirectory = r'%s' % self.working_directory
            shortcut.save()
        except Exception as error:
            log("Error adding shortcut to startup folder. --> " + str(error))

    def removeFromStartup(self):
        windowsStartupFolder = winshell.startup()
        try:
            if os.path.exists(windowsStartupFolder + '\%s.lnk' % self.shortcutName):
                os.remove(windowsStartupFolder + '\%s.lnk' % self.shortcutName)
                log("--------------> Successfully removed from startup")
            else:
                pass
        except Exception as error:
            log("Error removing shortcut from startup folder. --> " + str(error))

    def disableBotWhileRecording(self):
        global bot_active
        bot_active = 0

    def set_OnOff_shortcut_key(self):
        recordShootShortcut.setDisabled(1)
        onoffButton.setDisabled(1)
        recordOnOffShortcut.setText("Recording")
        recordOnOffShortcut.setStyleSheet(
            "QPushButton#recordOnOffshortcutButton{color: red; border: 1px solid grey;}QPushButton#recordOnOffshortcutButton:hover{border: 1px solid khaki;color: grey;}")
        log('--------------> Recording OnOff Shortcut...')
        global Shortcut_Function
        Shortcut_Function = 'OnOff_Shortcut_Key'

    def set_Shoot_shortcut_key(self):
        recordOnOffShortcut.setDisabled(1)
        onoffButton.setDisabled(1)
        recordShootShortcut.setText("Recording")
        recordShootShortcut.setStyleSheet(
            "QPushButton#recordShootshortcutButton{color: red; border: 1px solid grey;}QPushButton#recordShootshortcutButton:hover{border: 1px solid khaki;color: grey;}")
        log('--------------> Recording Shoot Shortcut...')
        global Shortcut_Function
        Shortcut_Function = 'Game_Shoot_Shortcut_Key'

    def system_tray_icon_clicked_or_doubleclicked(self, reason):
        if reason == QSystemTrayIcon.Trigger or reason == QSystemTrayIcon.DoubleClick:
            self.show_window()

    def show_window(self):
        self.show()
        self.tray.show()
        self.activateWindow()
        self.center()

    def btn_minimise_clicked(self):
        self.hide()

    def close_window(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

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
        self.okBtn.clicked.connect(self.close)
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


class KeyboardListenerClass:

    def on_press(self, key):
        pass

    def set_on_off_shortcut_key(self, key, key_name):
        global Shortcut_Function
        with open(os.path.join(working_directory, 'shortcutRegisters', Shortcut_Function) + '.txt', 'w+') as file:
            file.write(key + '\n' + key_name)
        Shortcut_Function = ''
        log('Set %s as new OnnOff shortcut key.' % key)
        recordOnOffShortcut.setStyleSheet(
            'QPushButton#recordOnOffshortcutButton{color: white; border: 1px solid grey;}QPushButton#recordOnOffshortcutButton:hover{border: 1px solid khaki;color: grey;}')
        recordOnOffShortcut.setText("Record New")
        currentOnOffShortcutLabel1.setText(str(key_name))
        recordShootShortcut.setEnabled(1)
        onoffButton.setEnabled(1)
        global bot_active
        bot_active = 1

    def set_game_shoot_shortcut_key(self, key, key_name):
        global Shortcut_Function
        with open(os.path.join(working_directory, 'shortcutRegisters', Shortcut_Function) + '.txt', 'w+') as file:
            file.write(key + '\n' + key_name)
        global shoot_shortcut_key_for_Simulator
        shoot_shortcut_key_for_Simulator = key
        Shortcut_Function = ''
        log('--------------> Set %s as new Shoot shortcut key.' % key)
        recordShootShortcut.setStyleSheet(
            'QPushButton#recordShootshortcutButton{color: white; border: 1px solid grey;}QPushButton#recordShootshortcutButton:hover{border: 1px solid khaki;color: grey;}')
        recordShootShortcut.setText("Record New")
        currentShootShortcutLabel1.setText(str(key_name))
        recordOnOffShortcut.setEnabled(1)
        onoffButton.setEnabled(1)
        global bot_active
        bot_active = 1

    def on_release(self, key):
        with open(os.path.join(working_directory, 'shortcutRegisters', 'OnOff_Shortcut_Key.txt'), 'r') as file:
            content = file.readlines()
            on_off_shortcut_key = content[0].replace('\n', '')
        with open(os.path.join(working_directory, 'shortcutRegisters', 'Game_Shoot_Shortcut_Key.txt'), 'r') as file:
            content = file.readlines()
            shoot_shortcut_key = content[0].replace('\n', '')
        key = str(key)
        key_name = key
        try:
            if 'Key.' in key:
                key = key.replace('Key.', '')
                if '_l' == key[-2:] or '_r' == key[-2:]:
                    key = key.replace('_l', '').replace('_r', '')
            elif '<' in key:
                key = 'code_' + key.replace('<', '').replace('>','')
                key = keycodes[key]
                key_name = key
            else:
                key = key.replace('\'', '')
        except:
            key = ''
            print("Key Not Supported")
        # print(key)
        print(len(key))
        if len(key):
            if Shortcut_Function == "OnOff_Shortcut_Key":
                if key is not on_off_shortcut_key:
                    if key != shoot_shortcut_key:
                        self.set_on_off_shortcut_key(key, key_name)
                    else:
                        # implementmessagebox
                        pass
            elif Shortcut_Function == "Game_Shoot_Shortcut_Key":
                if key is not shoot_shortcut_key:
                    if key != on_off_shortcut_key:
                        self.set_game_shoot_shortcut_key(key, key_name)
                    else:
                        # implementmessagebox
                        pass
            elif on_off_shortcut_key == key:
                global bot_active
                onoffButton.click()
                if not onoffButton.isChecked():
                    onoffLabel.setText("ON")
                    # print("Bot: Active")
                    self.queue.put([1, overlayStatus])
                    bot_active = 1
                else:
                    onoffLabel.setText("OFF")
                    # print("Bot: Disabled")
                    self.queue.put([0, overlayStatus])
                    bot_active = 0

    def run(self, q):
        self.queue = q
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


class ClickBot:
    def check_for_mouseclick(self):
        state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
        # print(state_left)
        if state_left == -128 or state_left == -127:
            print(shoot_shortcut_key_for_Simulator)
            try:
                keyboardSimulator.press(shoot_shortcut_key_for_Simulator)
                time.sleep(0.001)
                keyboardSimulator.release(shoot_shortcut_key_for_Simulator)
                time.sleep(0.001)
            except:
                print("Key Not Supported")

    def bot_loop(self):
        while 1:
            time.sleep(0.001)
            if bot_active:
                if work_on_games_with_hidden_mouse_only:
                    if win32gui.GetCursorInfo()[0] == win32gui.GetCursorInfo()[1] == 0:
                        # print("Game Active")
                        self.check_for_mouseclick()
                else:
                    self.check_for_mouseclick()

def alert_already_running():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(os.path.join(working_directory, 'style', 'alertWindowStylesheet.css')).read())
    appIcon = QtGui.QIcon(os.path.join(working_directory, 'icon.png'))
    app.setWindowIcon(appIcon)
    window = alertWindow()
    window.show()
    app.exec_()

def create_GUI(q):
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet((open(os.path.join(working_directory, 'style', 'guiStylesheet.css')).read()))
    appIcon = QtGui.QIcon(os.path.join(working_directory, 'icon.png'))
    app.setWindowIcon(appIcon)
    window = MainWindow(q)
    window.show()
    app.exec_()


def log(log):
    with open('log.txt', 'a+') as logfile:
        logfile.write(str(log) + '\n')
def setup_log():
    with open('log.txt', 'w+') as logfile:
        logfile.write(str('Start Logging --> %s' %time.strftime('%H:%M:%S, %d/%m/%Y')) + '\n')

if __name__ == '__main__':
    setup_log()
    appname = "AutoShoot Bot"
    working_directory = os.path.dirname(os.path.realpath(__file__))
    processes = list(p.name() for p in psutil.process_iter())
    log('\n----------------------Running Processes----------------------\n' + str(processes) + '\n----------------------Running Processes----------------------')
    log('Number of %s App Running: '%appname + str(processes.count(appname + '.exe')))
    if processes.count(appname + '.exe') < 2:
        Shortcut_Function = ''
        bot_active = 0
        work_on_games_with_hidden_mouse_only = 1

        with open(os.path.join(working_directory, 'shortcutRegisters', 'Game_Shoot_Shortcut_Key.txt'), 'r') as file:
            content = file.readlines()
            global shoot_shortcut_key_for_Simulator
            shoot_shortcut_key_for_Simulator = content[0].replace('\n', '')

        q = Queue()
        keyboardSimulator = Controller()
        keyboard_listener = KeyboardListenerClass()
        bot = ClickBot()

        gui_process = Thread(target=create_GUI, args=(q,))
        keyboard_listener_process = Thread(target=keyboard_listener.run, args=(q,))
        bot_overlay_process = Thread(target=bot_overlay.createOverlay, args=(q,))
        bot_process = Thread(target=bot.bot_loop, args=())

        gui_process.start()
        keyboard_listener_process.setDaemon(gui_process)
        bot_overlay_process.setDaemon(gui_process)
        bot_process.setDaemon(gui_process)
        keyboard_listener_process.start()
        bot_overlay_process.start()
        bot_process.start()
    else:
        log('............App Already Running............')
        alert_already_running()
