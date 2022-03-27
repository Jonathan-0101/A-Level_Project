import os
import time
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk

def closeWindow(currentWindow):
    currentWindow.destroy()

#Connecting to the database
conn = sqlite3.connect('System.db', check_same_thread = False)

#Function for opening video of selected event
def showSelected(tree, entryLogList):
    rowId = tree.selection()
    if len(rowId) == 0:
        return
    rowId = str(rowId[0])
    rowId = int(rowId.strip("I"))
    videoId = str(entryLogList[rowId-1][0])
    path = os.getcwd()
    path = (path + "\\Recordings\\" + videoId + ".h264")             
    os.startfile(path)
    time.sleep(1)

def viewLogs():
    #Creating the windiow for the event display
    viewWindow = tk.Tk()
    viewWindow.geometry("1020x655")
    viewWindow.title("Event view")

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
    tree.heading("1", text="Event Id")
    tree.heading("2", text="Result")
    tree.heading("3", text="First Name")
    tree.heading("4", text="Last Name")
    tree.heading("5", text="Date Time")

    #Retriving information from the database
    entryLog = conn.execute("SELECT * FROM entryLog").fetchall()
    entryLog.reverse()
    entryLogList = []

    #Populating the table with events, with most recent events at the top
    for i in range(len(entryLog)):
        eventId = entryLog[i][0]
        entry = entryLog[i][1]
        if entry is 1:
            entry = "Entry"
            userId = entryLog[i][2]
            userDetails = conn.execute("SELECT firstName, lastName FROM idCards WHERE id = ?", (userId, )).fetchall()
            firstName = userDetails[0][0]
            lastName = userDetails[0][1]
        else:
            userId = None
            entry = "No entry"
            firstName = None
            lastName = None
        dateTime = entryLog[i][3]
        logInfo = [eventId, entry, userId, firstName, lastName, dateTime]
        entryLogList.append(logInfo)
        pos = ("L",(i+1))
        tree.insert("", "end", text = pos, values = (eventId, entry, firstName, lastName, dateTime))

    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")

    #Creating button to view video and exit when done
    Button(viewWindow, text="Display event video", command = lambda: [showSelected(tree, entryLogList)], pady = 5, padx = 5 ).pack()
    Button(viewWindow, text="              Exit              ", command = lambda: [closeWindow(currentWindow)], pady = 5, padx = 5 ).pack()

    viewWindow.mainloop()

viewLogs()
