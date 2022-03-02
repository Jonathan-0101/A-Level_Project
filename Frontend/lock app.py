import sqlite3
from tkinter import *


conn = sqlite3.connect('System.db', check_same_thread=False)

def unlock(lockWindow):
    conn.execute("Update doorStatus set lockStatus = 1 where id = 1")
    conn.commit()
    closeUnlockWindow(lockWindow)


def closeUnlockWindow(lockWindow):
    lockWindow.destroy()


def unlockWindow():
    lockWindow = Tk()
    lockWindow.geometry('150x160')
    lockWindow.title('Door lock')
    spacer1 = Label(lockWindow, text="", font=("Arial Bold", 50))
    spacer2 = Label(lockWindow, text="             ").grid(column=0, row=0)
    unlockButton = Button(lockWindow, text="\n  Unlock  \n", command=lambda: [unlock(lockWindow)]).grid(row=1, column=1)
    exitButton = Button(lockWindow, text = "\n     Exit     \n", command =lambda: [closeUnlockWindow(lockWindow)]).grid(row=3, column=1)
    spacer4 = Label(lockWindow, text ="\n").grid(row=4, column=1)
    lockWindow.mainloop()

unlockWindow()
