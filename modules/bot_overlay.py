import tkinter
import win32api, win32con, pywintypes

def createOverlay(in_q):
    root = tkinter.Tk()

    screen_width = root.winfo_screenwidth()

    def update_label():
        if len(list(in_q.queue)):
            retCode = in_q.get()
            if retCode[1]:
                if retCode[0]:
                    text = "Bot: Active"
                else:
                    text = "Bot: Disabled"
                #print(text)
            else:
                text = ''
            overlay_text.set(text)
            label.update_idletasks()
            top = 0
            left = str(screen_width - label.winfo_reqwidth())
            label.master.geometry("+%s+%s" % (left, top))
        root.after(500, update_label)

    overlay_text = tkinter.StringVar()
    overlay_text.set("Bot: Disabled")
    label = tkinter.Label(textvariable=overlay_text, font=('Arial','12'), fg='white', bg='black')
    top = 0
    left = str(screen_width - label.winfo_reqwidth())
    label.master.geometry("+%s+%s" % (left, top))
    label.master.overrideredirect(True)
    label.master.lift()
    label.master.wm_attributes('-transparentcolor','black')
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
    # The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
    label.pack()

    update_label()
    root.mainloop()