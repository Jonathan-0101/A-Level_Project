import re
import base64
import sqlite3
import tkinter as tk
from datetime import datetime
from functools import partial

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


largeFont = ("Verdana", 12)
normFont = ("Helvetica", 10)
smallFont = ("Helvetica", 8)

def destroyWindow(currentWindow):
    currentWindow.destroy()


def destroyPopUp(popUpWindow):
    popUpWindow.destroy()


def accountcreationError(message, currentWindow, menuWindow):
    popUp = tk.Toplevel(menuWindow)
    popUp.geometry('250x100')
    popUpWindow = popUp
    popUp.title('Alert!')
    label = tk.Label(popUp, text=message, font=normFont)
    label.pack(side="top", fill="x", pady=10)
    button = tk.Button(popUp, text="Okay", command = lambda: [destroyPopUp(popUpWindow)])
    button.pack()
    popUp.mainloop()

def accountValidation(acUserName, acFirstName, acLastName, acEmail, acPassword, acConfirmPassword, acAdminPrivileges, currentWindow, accountCreationWindow, menuWindow):
    currentWindow = accountCreationWindow
    # Retreaving the information from the users inputs for validation
    userName = acUserName.get()
    firstName = acFirstName.get()
    lastName = acLastName.get()
    email = acEmail.get()
    password = acPassword.get()
    confirmPassword = acConfirmPassword.get()
    adminPrivileges = acAdminPrivileges.get()
    
    # Regex for email validation
    emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    now = datetime.now() # Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if 0 in (len(userName), len(firstName), len(lastName), len(email), len(password), len(confirmPassword), len(adminPrivileges)):
        message = 'Some fields are blank \n Please fill all of them in'
        accountcreationError(message, currentWindow, menuWindow)
        
    if len(cursor) == 1:  # Checks that the username is not taken
        message = 'Username is already taken, please try a different one'
        accountcreationError(message, currentWindow, menuWindow)
        
    if not re.fullmatch(emailCheck, email):  # Checks against the regex that the email is valid
        message = 'Email not valid, please try again'
        accountcreationError(message, currentWindow, menuWindow)
        
    # Checking the password
    if password != confirmPassword:  # Checks that the passwords match
        message = 'Passwords do not match please try again'
        accountcreationError(message, currentWindow, menuWindow)

    if len(password) < 6:  # Checks the length of the password
        message = 'Password is not strong enough \n Please use a minimum of 6 characters'
        accountcreationError(message, currentWindow, menuWindow)

    # Checking if the created user should have admin privileges
    
    adminYes = ['y', 'Y', 'yes', 'YES', 'Yes']
    adminNo = ['n', 'N', 'no', 'NO', 'No']
    
    if adminPrivileges in adminYes:
        adminPrivileges = 1

    elif adminPrivileges in adminNo:
        adminPrivileges = 0

    else:
        message = 'Admin privileges not in correct form \n Please try again'
        accountcreationError(message, currentWindow, menuWindow)
        
    # Making the first letter of the first and last name caplital
    firstName = firstName.capitalize()
    lastName = lastName.capitalize()
    
    # Making the characters of the email lowercase
    email = email.lower()

    # Encrypting the password
    password = password.encode("utf-8")
    password = base64.b64encode(password)
        
    conn.execute("INSERT INTO appUsers(userName, hashedPassword, firstName, lastName, email, adminPrivileges, timeCreated) VALUES (?,?,?,?,?,?,?)", [
                 userName, password, firstName, lastName, email, adminPrivileges, timeCreated])  # Writes the information to the db
    conn.commit()
    currentWindow.destroy()    


def createAccount(menuWindow):
    accountCreationWindow = tk.Toplevel(menuWindow)
    accountCreationWindow.geometry('390x410')
    accountCreationWindow.title('Create account')
    currentWindow = accountCreationWindow

    spacer1 = tk.Label(accountCreationWindow, text ="").grid(row=0, column=0)

    acUserName = tk.StringVar()
    userNameLabel = tk.Label(accountCreationWindow, text="User Name", pady=10, width=22, anchor='w').grid(row=1, column=1)
    userNameEntry = tk.Entry(accountCreationWindow, textvariable=acUserName, width=30).grid(row=1, column=2)

    acFirstName = tk.StringVar()
    firstNameLabel = tk.Label(accountCreationWindow, text="First name", pady=10, width=22, anchor='w').grid(row=2, column=1)
    firstNameEntry = tk.Entry(accountCreationWindow, textvariable=acFirstName, width=30).grid(row=2, column=2)

    acLastName = tk.StringVar()
    lastNameLable = tk.Label(accountCreationWindow, text="Last name", pady=10, width=22, anchor='w').grid(row=3, column=1)
    lastNameEntry = tk.Entry(accountCreationWindow, textvariable=acLastName, width=30).grid(row=3, column=2)

    acEmail = tk.StringVar()
    emailLable = tk.Label(accountCreationWindow, text="Email", pady=10, width=22, anchor='w').grid(row=4, column=1)
    emailEntry = tk.Entry(accountCreationWindow, textvariable=acEmail, width=30).grid(row=4, column=2)

    acPassword = tk.StringVar()
    passwordLabel = tk.Label(accountCreationWindow, text="Password", pady=10, width=22, anchor='w').grid(row=5, column=1)
    passwordEntry = tk.Entry(accountCreationWindow, textvariable=acPassword, show='*', width=30).grid(row=5, column=2)

    acConfirmPassword = tk.StringVar()
    confirmPasswordLabel = tk.Label(accountCreationWindow, text="Confirm password", pady=10, width=22, anchor='w').grid(row=6, column=1)
    confirmPasswordEntry = tk.Entry(accountCreationWindow, textvariable=acConfirmPassword, show='*', width=30).grid(row=6, column=2)

    acAdminPrivileges = tk.StringVar()
    adminPrivilegesLable = tk.Label(accountCreationWindow, text ="Admin privalges (yes/no)", pady=10, width=22, anchor='w').grid(row=7, column=1)
    adminPrivilegesEntry = tk.Entry(accountCreationWindow, textvariable=acAdminPrivileges, width=30).grid(row=7, column=2)

    spacer2 = tk.Label(accountCreationWindow, text ="").grid(row=8, column=1)
    validateAc = partial(accountValidation, acUserName, acFirstName, acLastName, acEmail, acPassword, acConfirmPassword, acAdminPrivileges, currentWindow, accountCreationWindow, menuWindow)
    loginButton = tk.Button(accountCreationWindow, text="           Create account           ", command = validateAc).grid(row=9, column=2)
    spacer3 = tk.Label(accountCreationWindow, text =" ").grid(row=10, column=2)
    exitButton = tk.Button(accountCreationWindow, text ="             Exit            ", command = lambda: [destroyWindow(currentWindow)]).grid(row=11, column=2)
    accountCreationWindow.mainloop()
    


def viewLogs(menuWindow):
    cursor = conn.execute("SELECT * FROM entryLog").fetchall()
    print(cursor)
    
    
def unlock(lockWindow):
    conn.execute("Update doorStatus set lockStatus = 1 where id = 1")
    conn.commit()
    closeUnlockWindow(lockWindow)


def closeUnlockWindow(lockWindow):
    lockWindow.destroy()


def unlockWindow(menuWindow):
    lockWindow = tk.Toplevel(menuWindow)
    lockWindow.geometry('150x160')
    lockWindow.title('Door lock')
    spacer1 = tk.Label(lockWindow, text="", font=("Arial Bold", 50))
    spacer2 = tk.Label(lockWindow, text="             ").grid(column=0, row=0)
    unlockButton = tk.Button(lockWindow, text="\n  Unlock  \n", command=lambda: [unlock(lockWindow)]).grid(row=1, column=1)
    exitButton = tk.Button(lockWindow, text = "\n     Exit     \n", command =lambda: [closeUnlockWindow(lockWindow)]).grid(row=3, column=1)
    spacer4 = tk.Label(lockWindow, text ="\n").grid(row=4, column=1)
    lockWindow.mainloop()


def manageUsers(menuWindow):
    print("Manage users")


def main(userName, firstName, lastName, email, adminPrivalges, loginTime, lastLogIn):
    userSumarry = 'Username: ' + userName + '\nFirst name: ' + firstName + '\nEmail: ' + email + '\nLog in time: ' + loginTime + '\nLast Log In: ' + lastLogIn
    print(userSumarry)
    menuWindow = tk.Tk()
    menuWindow.geometry('360x500')
    menuWindow.title('Main menu')
    #View logs button
    viewLogButton = tk.Button(menuWindow, text="           View Logs           ", command = lambda: [viewLogs(menuWindow)], pady=10, padx=10)
    #Unlock door button
    unlockDoorButton = tk.Button(menuWindow, text="         Unlock door         ", command = lambda: [unlockWindow(menuWindow)], pady=10, padx=10)
    #Exit button
    exitButton = tk.Button(menuWindow, text ="              Log off             ", command = exit, pady=10, padx=10)
    #User summary print out
    userSumarryDisplay = tk.Label(menuWindow, text = userSumarry,  justify="left", pady=10, padx=10)
    userSumarryDisplay.place(relx = 1.0, rely = 0.0, anchor ='ne')

    
    if adminPrivalges is True:  
        #Create account button
        createAccountButton = tk.Button(menuWindow, text="      Create Account      ", command = lambda: [createAccount(menuWindow)], pady=10, padx=10)
        #Manage users button
        manageUsersButton = tk.Button(menuWindow, text="       Manage Users       ", command = lambda: [manageUsers(menuWindow)], pady=10, padx=10)
        #Placing the buttons
        createAccountButton.place(relx = 0.5, rely = 0.5, anchor = 'center')
        manageUsersButton.place(relx = 0.5, rely = 0.6, anchor = 'center')
        viewLogButton.place(relx = 0.5, rely = 0.3, anchor = 'center')
        exitButton.place(relx = 0.5, rely = 0.7, anchor = 'center')
        unlockDoorButton.place(relx = 0.5, rely = 0.4, anchor = 'center')

        
    else:
        viewLogButton.place(relx = 0.5, rely = 0.4, anchor = 'center')
        unlockDoorButton.place(relx = 0.5, rely = 0.5, anchor = 'center')
        exitButton.place(relx = 0.5, rely = 0.6, anchor = 'center')
        
    menuWindow.mainloop()


def login(username, password, window):
    currentWindow = window
    userName = username.get()
    passwordToEncode = password.get()

    if 0 in (len(userName), len(passwordToEncode)):
        message = 'Please fill in the inputs'
        loginError(message, currentWindow, window)

    passwordToEncode = passwordToEncode.encode("utf-8")
    password = base64.b64encode(passwordToEncode)
    cursor = conn.execute("SELECT * FROM appUsers Where userName = ?", [userName, ]).fetchall()

    if len(cursor) == 0:
        message = 'Username or password incorrect'
        loginError(message, currentWindow, window)

    passwordToCheck = cursor[0][1]

    if password == passwordToCheck:
      print("Authorised")
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
          main(userName, firstName, lastName, email, adminPrivalges, loginTime, lastLogIn)

      else:
          adminPrivalges = False
          window.destroy()
          main(userName, firstName, lastName, email, adminPrivalges, loginTime, lastLogIn)

    else:
        message = 'Username or password incorrect'
        loginError(message, currentWindow, window)


def loginError(message, currentWindow, window):
    popUp = tk.Toplevel(window)
    popUp.geometry('250x100')
    popUpWindow = popUp
    popUp.title('Alert!')
    label = tk.Label(popUp, text=message, font=normFont)
    label.pack(side="top", fill="x", pady=10)
    button = tk.Button(popUp, text="Okay", command = lambda: [destroyPopUp(popUpWindow)])
    button.pack()
    popUp.mainloop()
    
    
window = tk.Tk()
window.geometry('347x195')
window.title('Login')
currentWindow = window
spacer1 = tk.Label(window, text ="").grid(row=0, column=0)
username = tk.StringVar()
usernameLabel = tk.Label(window, text="User Name", pady=10, width=10, anchor='w').grid(row=1, column=1)
usernameEntry = tk.Entry(window, textvariable=username,  width=30).grid(row=1, column=2)
password = tk.StringVar()
passwordLabel = tk.Label(window, text="Password", pady=10, width=10, anchor='w').grid(row=2, column=1)
passwordEntry = tk.Entry(window, textvariable=password, show='*',  width=30).grid(row=2, column=2)
loginButton = tk.Button(window, text="           Login           ", command = lambda: [login(username, password, window)]).grid(row=3, column=2)
spacer2 = tk.Label(window, text =" ").grid(row=4, column=2)
exitButton = tk.Button(window, text ="             Exit            ", command = exit).grid(row=5, column=2)
spacer3 = tk.Label(window, text ="").grid(row=3, column=0)
window.mainloop()
