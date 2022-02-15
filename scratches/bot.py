import keyboard
# from pynput import keyboard
import os
import time
from win32gui import GetWindowText, GetForegroundWindow, GetCursorInfo
import win32api

def bot(out_q):

    def set_overlayStatus(status):
        out_q.put(status)

    def check_for_mouseclick():
        state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
        print(state_left)
        if state_left == -128 or state_left == -127:
            keyboard.press("8")
            time.sleep(0.001)
            keyboard.release("8")
            time.sleep(0.001)

    def main():
        print(1)
        time0 = time.time()
        print("----------------------\nBot Activated")
        set_overlayStatus(1)
        while 1:
            if GetCursorInfo()[0] == GetCursorInfo()[1] == 0:
                print("Game Active")
                check_for_mouseclick()
                if time.time() - time0 >= keypress_interval:
                    if keyboard.is_pressed('0'):
                        print("----------------------\nBot Paused")
                        set_overlayStatus(0)
                        return time.time()
            if time.time() - time0 >= keypress_interval:
                if keyboard.is_pressed('0'):
                    print("----------------------\nBot Paused")
                    set_overlayStatus(0)
                    return time.time()

    set_overlayStatus(0)
    keypress_interval = 0.5
    startTime = time.time() - keypress_interval
    while 1:
        if time.time() - startTime >= keypress_interval:
            if keyboard.is_pressed('0'):
                startTime = main()
