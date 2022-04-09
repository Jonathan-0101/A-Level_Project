import re
import os
import time
import string
import random
import hashlib
import sqlite3
import sv_ttk
import smtplib
import pyttsx3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime
from dotenv import load_dotenv

conn = sqlite3.connect('database.db', check_same_thread=False)

def closeWindow(currentWindow):
    currentWindow.destroy()

def deleteAccount(tree, userList):
    print("Delete account")
    rowId = tree.selection()
    if len(rowId) == 0:
        return
    rowId = str(rowId[0])
    rowId = int(rowId.strip("I"))
    rowId = rowId - 1
    print(rowId)
    if rowId == 0:
        print("Can not delete the admin account")
        return
    userName = userList[rowId][0]
    # ---------------------------
    #ADD CONFORMATION
    '''
    Ask user to confirm deletion 
    '''
    #ADD CONFORMATION
    # ---------------------------
    conn.execute("DELETE FROM appUsers WHERE userName = ?", (userName,))
    conn.commit()
  
def manageUsers(window):
    #Creating the windiow for the event display
    viewWindow = tk.Toplevel(window)
    viewWindow.geometry("1020x690")

    currentWindow = viewWindow

    #Creating frame layer fo the tkinter tree view window
    frame = Frame(viewWindow)
    frame.pack(pady=20)

    #Fixing headings to the top of the table
    tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), show='headings', height=25)
    tree.pack(side=LEFT)

    #Adding the scroll bar for events
    sb = Scrollbar(frame, orient=VERTICAL)
    sb.pack(side=RIGHT, fill=Y)

    #Attatching the scrollbar to the side fo the table
    tree.config(yscrollcommand=sb.set)
    sb.config(command=tree.yview)

    #Creating headings for the table
    tree["columns"] = ("1", "2", "3", "4", "5")
    tree['show'] = 'headings'
    tree.column("1", width=100, anchor='c')
    tree.column("2", width=100, anchor='c')
    tree.heading("1", text="Username")
    tree.heading("2", text="First name")
    tree.heading("3", text="Last Name")
    tree.heading("4", text="Email")
    tree.heading("5", text="Admin privlages")

    #Retriving information from the database
    entryLog = conn.execute("SELECT * FROM appUsers").fetchall()
    userList = []

    #Populating the table with events, with most recent events at the top
    loopNum = 0
    for event in entryLog:
        userName = event[0]
        firstName = event[2]
        lastName = event[3]
        email = event[4]
        adminPrivlages = event[5]
        logInfo = [userName, firstName, lastName, email, adminPrivlages]
        userList.append(logInfo)
        loopNum += 1 
        pos = ("L",(loopNum))
        tree.insert("", "end", text=pos, values = (userName, firstName, lastName, email, adminPrivlages))

    style = ttk.Style(viewWindow)
    style.theme_use("default")
    style.map("Treeview")
    #Creating button to view video and exit when done
    Button(viewWindow, text="          Delete user        ", command=lambda:[deleteAccount(tree, userList)], pady=10, padx=10).pack()
    Label(viewWindow, text=" ").pack()
    Button(viewWindow, text="              Exit              ", command=lambda:[closeWindow(currentWindow)], pady=10, padx=10).pack()
    viewWindow.mainloop()


window = tk.Tk() # Creating window for login system
window.geometry('347x275')
window.title('Login') # Setting the title for window
manageUsers(window)
window.mainloop()