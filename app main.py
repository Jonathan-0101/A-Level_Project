import time
import base64
import sqlite3
from tkinter import *
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

def exitAccountCreationWindow(currentWindow):
    currentWindow.destroy()


def accountcreationError(message, currentWindow):
    popUp = Tk()
    popUp.geometry('250x100')
    popUp.title('Alert!')
    label = Label(popUp, text=message, font=normFont)
    label.pack(side="top", fill="x", pady=10)
    button = Button(popUp, text="Okay", command = lambda: [closePopUp(currentWindow, popUp)])
    button.pack()
    popUp.mainloop()


def accountValidation(userName, firstName, lastName, email, password, confirmPassword, adminPrivileges, accountCreationWindow):
    currentWindow = accountCreationWindow
    # Retreaving the information from the users inputs for validation
    userName = userName.get()
    firstName = firstName.get()
    lastName = lastName.get()
    email = email.get()
    password = password.get()
    confirmPassword = confirmPassword.get()
    admin = adminPrivileges.get()
    
    # Regex for email validation
    emailCheck = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    now = datetime.now() # Gets the current date and time
    timeCreated = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Searches the database for all instances of the given username
    cursor = conn.execute(
        "SELECT * FROM appUsers Where userName = ?", [userName]).fetchall()

    if 0 in (len(userName), len(firstName), len(lastName), len(email), len(password), len(confirmPassword), len(admin)):
        message = 'Some fields are blank \n Please fill all of them in'
        accountcreationError(message, currentWindow)
        
    if len(cursor) == 1:  # Checks that the username is not taken
        message = 'Username is already taken, please try a different one'
        accountcreationError(message, currentWindow)
        
    if not re.fullmatch(emailCheck, email):  # Checks against the regex that the email is valid
        message = 'Email not valid, please try again'
        accountcreationError(message, currentWindow)
        
    # Checking the password
    if password != confirmPassword:  # Checks that the passwords match
        message = 'Passwords do not match please try again'
        accountcreationError(message, currentWindow)

    if len(password) < 6:  # Checks the length of the password
        message = 'Password is not strong enough \n Please use a minimum of 6 characters'
        accountcreationError(message, currentWindow)

    # Checking if the created user should have admin privileges
    
    adminYes = ['y', 'Y', 'yes', 'YES', 'Yes']
    adminNo = ['n', 'N', 'no', 'NO', 'No']
    
    if admin in adminYes:
        adminPrivileges = 1

    elif admin in adminNo:
        adminPrivileges = 0

    else:
        message = 'Admin privileges not in correct form \n Please try again'
        accountcreationError(message, currentWindow)
        
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


def createAccount():
    accountCreationWindow = Tk()
    accountCreationWindow.geometry('390x410')
    accountCreationWindow.title('Create account')

    spacer1 = Label(accountCreationWindow, text ="").grid(row=0, column=0)

    userName = StringVar()
    userNameLabel = Label(accountCreationWindow, text="User Name", pady=10, width=22, anchor='w').grid(row=1, column=1)
    userNameEntry = Entry(accountCreationWindow, textvariable=userName, width=30).grid(row=1, column=2)

    firstName = StringVar()
    firstNameLabel = Label(accountCreationWindow, text="First name", pady=10, width=22, anchor='w').grid(row=2, column=1)
    firstNameEntry = Entry(accountCreationWindow, textvariable=firstName, width=30).grid(row=2, column=2)

    lastName = StringVar()
    lastNameLable = Label(accountCreationWindow, text="Last name", pady=10, width=22, anchor='w').grid(row=3, column=1)
    lastNameEntry = Entry(accountCreationWindow, textvariable=lastName, width=30).grid(row=3, column=2)

    email = StringVar()
    emailLable = Label(accountCreationWindow, text="Email", pady=10, width=22, anchor='w').grid(row=4, column=1)
    emailEntry = Entry(accountCreationWindow, textvariable=email, width=30).grid(row=4, column=2)

    password = StringVar()
    passwordLabel = Label(accountCreationWindow, text="Password", pady=10, width=22, anchor='w').grid(row=5, column=1)
    passwordEntry = Entry(accountCreationWindow, textvariable=password, show='*', width=30).grid(row=5, column=2)

    confirmPassword = StringVar()
    confirmPasswordLabel = Label(accountCreationWindow, text="Confirm password", pady=10, width=22, anchor='w').grid(row=6, column=1)
    confirmPasswordEntry = Entry(accountCreationWindow, textvariable=confirmPassword, show='*', width=30).grid(row=6, column=2)

    adminPrivileges = StringVar()
    adminPrivilegesLable = Label(accountCreationWindow, text ="Admin privalges (yes/no)", pady=10, width=22, anchor='w').grid(row=7, column=1)
    adminPrivilegesEntry = Entry(accountCreationWindow, textvariable=adminPrivileges, width=30).grid(row=7, column=2)

    spacer2 = Label(accountCreationWindow, text ="").grid(row=8, column=1)
    validateLogin = partial(accountValidation, userName, firstName, lastName, email, password, confirmPassword, adminPrivileges, accountCreationWindow)
    loginButton = Button(accountCreationWindow, text="           Create account           ", command=validateLogin).grid(row=9, column=2)
    spacer3 = Label(accountCreationWindow, text =" ").grid(row=10, column=2)
    exitButton = Button(accountCreationWindow, text ="             Exit            ", command = lambda: [exitAccountCreationWindow(accountCreationWindow)]).grid(row=11, column=2)
    accountCreationWindow.mainloop()

def loginMenu():
    loginWindow = Tk()
    loginWindow.geometry('347x195')
    loginWindow.title('Login')
    currentWindow = loginWindow
    spacer1 = Label(loginWindow, text ="").grid(row=0, column=0)
    username = StringVar()
    usernameLabel = Label(loginWindow, text="User Name", pady=10, width=10, anchor='w').grid(row=1, column=1)
    usernameEntry = Entry(loginWindow, textvariable=username,  width=30).grid(row=1, column=2)
    password = StringVar()
    passwordLabel = Label(loginWindow, text="Password", pady=10, width=10, anchor='w').grid(row=2, column=1)
    passwordEntry = Entry(loginWindow, textvariable=password, show='*',  width=30).grid(row=2, column=2)
    validateLogin = partial(login, username, password, loginWindow)
    loginButton = Button(loginWindow, text="           Login           ", command=validateLogin).grid(row=3, column=2)
    spacer2 = Label(loginWindow, text =" ").grid(row=4, column=2)
    exitButton = Button(loginWindow, text ="             Exit            ", command = exit).grid(row=5, column=2)
    spacer3 = Label(loginWindow, text ="").grid(row=3, column=0)
    loginWindow.mainloop()


def login(username, password, loginWindow):
    currentWindow = loginWindow
    userName = username.get()
    passwordToEncode = password.get()

    if 0 in (len(userName), len(passwordToEncode)):
        message = 'Please fill in the inputs'
        loginError(message, currentWindow)

    passwordToEncode = passwordToEncode.encode("utf-8")
    password = base64.b64encode(passwordToEncode)
    cursor = conn.execute("SELECT * FROM appUsers Where userName = ?", [userName, ]).fetchall()

    if len(cursor) == 0:
        message = 'Username does not exist'
        loginError(message, currentWindow)

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
          loginWindow.destroy()
          main(userName, firstName, lastName, email, adminPrivalges, loginTime, lastLogIn)

      else:
          adminPrivalges = False
          loginWindow.destroy()
          main(userName, firstName, lastName, email, adminPrivalges, loginTime, lastLogIn)

    else:
        message = 'Password incorrect please try again'
        loginError(message, currentWindow)


def closePopUp(currentWindow, popUp):
    popUp.destroy()

def loginError(message, currentWindow):
    popUp = Tk()
    popUp.geometry('250x100')
    popUp.title('Alert!')
    label = Label(popUp, text=message, font=normFont)
    label.pack(side="top", fill="x", pady=10)
    button = Button(popUp, text="Okay", command = lambda: [closePopUp(currentWindow, popUp)])
    button.pack()
    popUp.mainloop()

def viewLogs():
    cursor = conn.execute("SELECT * FROM entryLog").fetchall()
    print(cursor)
    
    
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

def manageUsers():
    print("Manage users")

def main(userName, firstName, lastName, email, adminPrivalges, loginTime, lastLogIn):
    print("Username: ", userName)
    print("First name: ", firstName)
    print("Last name: ", lastName)
    print("Email: ", email)
    print("Admin privaleges: ", adminPrivalges)
    print("Login time: ", loginTime)
    print("Last log in:", lastLogIn)
    userSumarry = 'Username: ' + userName + '\nFirst name: ' + firstName + '\nEmail: ' + email + '\nLog in time: ' + loginTime + '\nLast Log In: ' + lastLogIn
    print(userSumarry)
    menuWindow = Tk()
    menuWindow.geometry('1080x720')
    menuWindow.title('Main menu')
    currentWindow = menuWindow
    #View logs button
    viewLogButton = Button(menuWindow, text="           View Logs           ", command = lambda: [viewLogs()], pady=10, padx=10)
    #Unlock door button
    unlockDoorButton = Button(menuWindow, text="           Unlock door           ", command = lambda: [unlockWindow()], pady=10, padx=10)
    #Exit button
    exitButton = Button(menuWindow, text ="             Log off            ", command = exit, pady=10, padx=10)
    #User summary print out
    userSumarryDisplay = Label(menuWindow, text = userSumarry,  justify=LEFT, pady=10, padx=10)
    userSumarryDisplay.place(relx = 1.0, rely = 0.0, anchor ='ne')

    
    if adminPrivalges == True:  
        #Manage users button
        manageUsersButton = Button(menuWindow, text="          Manage Users          ", command = lambda: [manageUsers()], pady=10, padx=10)
        manageUsersButton.place(relx = 0.5, rely = 0.6, anchor = 'center')
        #Create account button
        createAccountButton = Button(menuWindow, text="          Create Account          ", command = lambda: [createAccount()], pady=10, padx=10)
        createAccountButton.place(relx = 0.5, rely = 0.5, anchor = 'center')
        viewLogButton.place(relx = 0.5, rely = 0.3, anchor = 'center')
        exitButton.place(relx = 0.5, rely = 0.7, anchor = 'center')
        unlockDoorButton.place(relx = 0.5, rely = 0.4, anchor = 'center')

        
    else:
        viewLogButton.place(relx = 0.5, rely = 0.4, anchor = 'center')
        unlockDoorButton.place(relx = 0.5, rely = 0.5, anchor = 'center')
        exitButton.place(relx = 0.5, rely = 0.6, anchor = 'center')
        
    menuWindow.mainloop()



loginMenu()
