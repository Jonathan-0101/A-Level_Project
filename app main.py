import re
import os
import time
import hashlib
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from datetime import datetime

conn = sqlite3.connect('System.db', check_same_thread=False)

conn.execute('''CREATE TABLE if not exists appUsers
  (userName VARCHAR PRIMARY KEY,
  hashedPassword INTEGER,
  firstName TEXT,
  lastName TEXT,
  email VARCHAR,
  adminPrivileges INTEGER,
  timeCreated DATETIME);''')
conn.commit()


def closeWindow(currentWindow):
    currentWindow.destroy()


def popUpWindow(title, message, menuWindow):
    popUp = tk.Toplevel(menuWindow)
    popUp.geometry('250x100')
    currentWindow = popUp
    popUp.title(title)
    label = Label(popUp, text=message, font=normfont)
    label.pack(side="top", fill="x", pady=10)
    button = Button(popUp, text="Okay", command=lambda:[closeWindow(currentWindow)])
    button.pack()
    popUp.mainloop()


def accountValidation(acUserName, acFirstName, acLastName, acEmail, acPassword, acConfirmPassword, acAdminPrivileges, accountCreationWindow, menuWindow):
    # Retreaving the information from the users inputs for validation
    userName = acUserName.get()
    firstName = acFirstName.get()
    lastName = acLastName.get()
    email = acEmail.get()
    password = acPassword.get()
    confirmPassword = acConfirmPassword.get()
    adminPrivileges = acAdminPrivileges.get()
    title = "Account Creation Error"

    # Regex for email validation
    emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    now = datetime.now() # Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")
    logInTimeForDB = now.strftime("%d/%m/%Y")

    # Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if 0 in (len(userName), len(firstName), len(lastName), len(email), len(password), len(confirmPassword)):
        message = 'Some fields are blank \n Please fill all of them in'
        popUpWindow(title, message, menuWindow)

    if len(cursor) == 1:  # Checks that the username is not taken
        message = 'Username is already taken, please try a different one'
        popUpWindow(title, message, menuWindow)

    if not re.fullmatch(emailCheck, email):  # Checks against the regex that the email is valid
        message = 'Email not valid, please try again'
        popUpWindow(title, message, menuWindow)

    # Checking the password
    if password != confirmPassword:  # Checks that the passwords match
        message = 'Passwords do not match please try again'
        popUpWindow(title, message, menuWindow)

    if len(password) < 6:  # Checks the length of the password
        message = 'Password is not strong enough \n Please use a minimum of 6 characters'
        popUpWindow(title, message, menuWindow)

    else:
        message = 'Admin privileges not in correct form \n Please try again'
        popUpWindow(title, message, menuWindow)

    # Making the first letter of the first and last name caplital
    firstName = firstName.capitalize()
    lastName = lastName.capitalize()

    # Making the characters of the email lowercase
    email = email.lower()

    # Encrypting the password
    password = password.encode()
    password = hashlib.sha3_512(password).hexdigest()

    conn.execute("INSERT INTO appUsers(userName, hashedPassword, firstName, lastName, email, adminPrivileges, timeCreated, lastLogIn) VALUES (?,?,?,?,?,?,?,?)", [
                 userName, password, firstName, lastName, email, adminPrivileges, timeCreated, logInTimeForDB])  # Writes the information to the db
    conn.commit()
    title = "Alert!"
    message = "User created successfully"
    popUpWindow(title, message, menuWindow)
    accountCreationWindow.destroy()    


def createAccount(menuWindow):
    accountCreationWindow = tk.Toplevel(menuWindow)
    accountCreationWindow.geometry('390x410')
    accountCreationWindow.title('Create account')
    currentWindow = accountCreationWindow

    spacer1 = Label(accountCreationWindow, text="").grid(row=0, column=0)

    acUserName = StringVar()
    userNameLabel = Label(accountCreationWindow, text="User Name", pady=10, width=22, anchor='w').grid(row=1, column=1)
    userNameEntry = Entry(accountCreationWindow, textvariable=acUserName, width=30).grid(row=1, column=2)

    acFirstName = StringVar()
    firstNameLabel = Label(accountCreationWindow, text="First name", pady=10, width=22, anchor='w').grid(row=2, column=1)
    firstNameEntry = Entry(accountCreationWindow, textvariable=acFirstName, width=30).grid(row=2, column=2)

    acLastName = StringVar()
    lastNameLable = Label(accountCreationWindow, text="Last name", pady=10, width=22, anchor='w').grid(row=3, column=1)
    lastNameEntry = Entry(accountCreationWindow, textvariable=acLastName, width=30).grid(row=3, column=2)

    acEmail = StringVar()
    emailLable = Label(accountCreationWindow, text="Email", pady=10, width=22, anchor='w').grid(row=4, column=1)
    emailEntry = Entry(accountCreationWindow, textvariable=acEmail, width=30).grid(row=4, column=2)

    acPassword = StringVar()
    passwordLabel = Label(accountCreationWindow, text="Password", pady=10, width=22, anchor='w').grid(row=5, column=1)
    passwordEntry = Entry(accountCreationWindow, textvariable=acPassword, show='*', width=30).grid(row=5, column=2)

    acConfirmPassword = StringVar()
    confirmPasswordLabel = Label(accountCreationWindow, text="Confirm password", pady=10, width=22, anchor='w').grid(row=6, column=1)
    confirmPasswordEntry = Entry(accountCreationWindow, textvariable=acConfirmPassword, show='*', width=30).grid(row=6, column=2)

    adminPrivileges = IntVar()
    adminLable = Label(accountCreationWindow, text="Admin privlages", pady=10, width=22, anchor='w').grid(row=7, column=1)
    Checkbutton(accountCreationWindow, text="                                                       ", variable=adminPrivileges).grid(row=7, column=2)

    spacer2 = Label(accountCreationWindow, text="").grid(row=8, column=1)
    loginButton = Button(accountCreationWindow, text="           Create account           ", command=lambda:[accountValidation(acUserName, acFirstName, acLastName, acEmail, acPassword, acConfirmPassword, acAdminPrivileges, accountCreationWindow, menuWindow)]).grid(row=9, column=2)
    spacer3 = Label(accountCreationWindow, text=" ").grid(row=10, column=2)
    exitButton = Button(accountCreationWindow, text="             Exit            ", command=lambda:[closeWindow(currentWindow)]).grid(row=11, column=2)
    accountCreationWindow.mainloop()


def showSelected(tree, entryLogList):
    #Retriving the row id of the event
    rowId = tree.selection()
    if len(rowId) == 0:
        return
    rowId = str(rowId[0])
    rowId = int(rowId.strip("I"))
    videoId = str(entryLogList[rowId-1][0])
    #Getting path to the file as will differ per computer
    path = os.getcwd()
    #Add the requiered video to the end of the path
    path = (path + "\\Recordings\\" + videoId + ".h264")
    #Start the video file in computers player
    os.startfile(path)
    #Add timeout to allow the file to open
    time.sleep(2)


def viewLogs(menuWindow):
    #Creating the windiow for the event display
    viewWindow = tk.Toplevel(menuWindow)
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
        if entry == 1:
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
        tree.insert("", "end", text=pos, values = (eventId, entry, firstName, lastName, dateTime))

    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")

    #Creating button to view video and exit when done
    Button(viewWindow, text="Display event video", command=lambda:[showSelected(tree, entryLogList)], pady=10, padx=10).pack()
    Label(viewWindow, text=" ").pack()
    Button(viewWindow, text="              Exit              ", command=lambda:[closeWindow(currentWindow)], pady=10, padx=10).pack()

    viewWindow.mainloop()


def unlock(lockWindow, menuWindow):
    conn.execute("Update doorStatus set lockStatus = 1")
    conn.commit()
    title = "Alert!"
    message = "Door unlocked for 30 seconds"
    popUpWindow(title, message, menuWindow)
    time.sleep(10)
    lockWindow.destroy()


def unlockWindow(menuWindow):
    #Creating lock window
    lockWindow = tk.Toplevel(menuWindow)
    currentWindow = lockWindow
    #Sizeing the window
    lockWindow.geometry('150x160')
    lockWindow.title('Door lock')
    spacer1 = Label(lockWindow, text="", font=("Arial Bold", 50))
    spacer2 = Label(lockWindow, text="             ").grid(column=0, row=0)
    #Creating unlock button
    unlockButton = Button(lockWindow, text="\n  Unlock  \n", command=lambda:[unlock(lockWindow, menuWindow)]).grid(row=1, column=1)
    #Creating exit button
    exitButton = Button(lockWindow, text="\n     Exit     \n", command=lambda:[closeWindow(currentWindow)]).grid(row=3, column=1)
    spacer4 = Label(lockWindow, text="\n").grid(row=4, column=1)
    lockWindow.mainloop()


def manageUsers(menuWindow):
    print("Manage users")


def main(userName, firstName, email, adminPrivalges, loginTime, lastLogIn):
    userSumarry = 'Username: ' + userName + '\nFirst name: ' + firstName + '\nEmail: ' + email + '\nLog in time: ' + loginTime + '\nLast Log In: ' + lastLogIn
    menuWindow = tk.Tk()
    menuWindow.geometry('360x500')
    menuWindow.title('Main menu')
    #View logs button
    viewLogButton = Button(menuWindow, text ="           View Logs           ", command=lambda:[viewLogs(menuWindow)], pady=10, padx=10)
    #Unlock door button
    unlockDoorButton = Button(menuWindow, text ="         Unlock door         ", command=lambda:[unlockWindow(menuWindow)], pady=10, padx=10)
    #Exit button
    exitButton = Button(menuWindow, text ="              Log off             ", command=exit, pady=10, padx=10)
    #User summary print out
    userSumarryDisplay = Label(menuWindow, text=userSumarry,  justify="left", pady=10, padx=10)
    userSumarryDisplay.place(relx=1.0, rely=0.0, anchor='ne')


    if adminPrivalges is True:  
        #Create account button
        createAccountButton = Button(menuWindow, text="      Create Account      ", command=lambda:[createAccount(menuWindow)], pady=10, padx=10)
        #Manage users button
        manageUsersButton = Button(menuWindow, text="       Manage Users       ", command=lambda:[manageUsers(menuWindow)], pady=10, padx=10)
        #Placing the buttons
        createAccountButton.place(relx=0.5, rely=0.5, anchor='center')
        manageUsersButton.place(relx=0.5, rely=0.6, anchor='center')
        viewLogButton.place(relx=0.5, rely=0.3, anchor='center')
        exitButton.place(relx=0.5, rely=0.7, anchor='center')
        unlockDoorButton.place(relx=0.5, rely=0.4, anchor='center')


    else:
        viewLogButton.place(relx=0.5, rely=0.4, anchor='center')
        unlockDoorButton.place(relx=0.5, rely=0.5, anchor='center')
        exitButton.place(relx=0.5, rely=0.6, anchor='center')

    menuWindow.mainloop()


def login(username, password, window):
    userName = username.get()
    passwordToEncode = password.get()

    if 0 in (len(userName), len(passwordToEncode)):
        message = 'Please fill in the inputs'
        loginError(message, window)

    passwordToEncode = passwordToEncode.encode()
    password = hashlib.sha3_512(passwordToEncode).hexdigest()
    cursor = conn.execute("SELECT * FROM appUsers Where userName = ?", [userName, ]).fetchall()

    if len(cursor) == 0:
        message = 'Username or password incorrect'
        loginError(message, window)

    passwordToCheck = cursor[0][1]

    if password == passwordToCheck:
      firstName = cursor[0][2]
      lastName = cursor[0][3]  
      email = cursor[0][4]
      adminPrivalges = cursor[0][5]
      lastLogIn = cursor[0][7]
      now = datetime.now()
      logInTimeForDB = now.strftime("%d/%m/%Y")
      conn.execute("UPDATE appUsers SET lastLogIn = ? WHERE userName = ?", (logInTimeForDB, userName))
      conn.commit()
      loginTime = now.strftime("%H:%M")

      if adminPrivalges == 1:
          adminPrivalges = True
          window.destroy()
          main(userName, firstName, email, adminPrivalges, loginTime, lastLogIn)

      else:
          adminPrivalges = False
          window.destroy()
          main(userName, firstName, email, adminPrivalges, loginTime, lastLogIn)

    else:
        message = 'Username or password incorrect'
        loginError(message, window)


def loginError(message, window):
    popUp = tk.Toplevel(window)
    popUp.geometry('250x100')
    currentWindow = popUp
    popUp.title('Alert!')
    label = Label(popUp, text=message, font=normfont)
    label.pack(side="top", fill="x", pady=10)
    button = Button(popUp, text="Okay", command=lambda:[closeWindow(currentWindow)])
    button.pack()
    popUp.mainloop()

largefont=("Verdana", 12)
normfont=("Helvetica", 10)
smallfontd=("Helvetica", 8)

window = tk.Tk()
window.geometry('347x195')
window.title('Login')
spacer1 = Label(window, text="").grid(row=0, column=0)
username = StringVar()
usernameLabel = Label(window, text="User Name", pady=10, padx=10, width=10, anchor='w').grid(row=1, column=1 )
usernameEntry = Entry(window, textvariable=username,  width=30).grid(row=1, column=2)
password = StringVar()
passwordLabel = Label(window, text="Password", pady=10, padx=10, width=10, anchor='w').grid(row=2, column=1)
passwordEntry = Entry(window, textvariable=password, show='*', width=30).grid(row=2, column=2)
loginButton = Button(window, text="           Login           ", command=lambda:[login(username, password, window)]).grid(row=3, column=2)
spacer2 = Label(window, text=" ").grid(row=4, column=2)
exitButton = Button(window, text="             Exit            ", command=exit).grid(row=5, column=2)
spacer3 = Label(window, text="").grid(row=3, column=0)
window.mainloop()
