# Imports tkinter for GUI
from tkinter import *
import os
from clientChat import *



# Global Variables



# The file that stores credentials
credentialsFile = 'credentials.temp' 
 
def NewSignUp():
    global passwordVar
    global nameVar
    global rootSignUp

    rootSignUp = Tk()
    rootSignUp.title('SignUp')
    instructionVar = Label(rootSignUp, text='Please Enter new Credentials\n')
    instructionVar.grid(row=0, column=0, sticky=E)
 
    nameLabel = Label(rootSignUp, text='New Username: ')
    passwordLabel = Label(rootSignUp, text='New Password: ')
    nameLabel.grid(row=1, column=0, sticky=W)
    passwordLabel.grid(row=2, column=0, sticky=W)
 
    nameVar = Entry(rootSignUp)
    passwordVar = Entry(rootSignUp, show='*')
    nameVar.grid(row=1, column=1)
    passwordVar.grid(row=2, column=1)
 
    SignUpButton = Button(rootSignUp, text='SignUp', command=storeCredentialsToFile)
    SignUpButton.grid(columnspan=2, sticky=W)
    rootSignUp.mainloop()


def SignUp():
    global passwordVar
    global nameVar
    global rootSignUp

    rootLogin.destroy()

    rootSignUp = Tk()
    rootSignUp.title('SignUp')
    instructionVar = Label(rootSignUp, text='Please Enter new Credentials\n')
    instructionVar.grid(row=0, column=0, sticky=E)
 
    nameLabel = Label(rootSignUp, text='New Username: ')
    passwordLabel = Label(rootSignUp, text='New Password: ')
    nameLabel.grid(row=1, column=0, sticky=W)
    passwordLabel.grid(row=2, column=0, sticky=W)
 
    nameVar = Entry(rootSignUp)
    passwordVar = Entry(rootSignUp, show='*')
    nameVar.grid(row=1, column=1)
    passwordVar.grid(row=2, column=1)
 
    SignUpButton = Button(rootSignUp, text='SignUp', command=storeCredentialsToFile)
    SignUpButton.grid(columnspan=2, sticky=W)
    rootSignUp.mainloop()
 
def storeCredentialsToFile():
    with open(credentialsFile, 'w') as f:
        f.write(nameVar.get())
        f.write('\n')
        f.write(passwordVar.get())
        f.close()
 
    rootSignUp.destroy()
    Login()
 
def Login():

    global nameVarLogin
    global passwordVarLogin
    global rootLogin

    rootLogin = Tk()
    rootLogin.title('Login')
 
    instructionVar = Label(rootLogin, text='Please Login\n')
    instructionVar.grid(sticky=E)
 
    nameLabel = Label(rootLogin, text='Username: ')
    passwordLabel = Label(rootLogin, text='Password: ')
    nameLabel.grid(row=1, sticky=W)
    passwordLabel.grid(row=2, sticky=W)
 
    nameVarLogin = Entry(rootLogin)
    passwordVarLogin = Entry(rootLogin, show='*')
    nameVarLogin.grid(row=1, column=1)
    passwordVarLogin.grid(row=2, column=1)
 
    loginButton = Button(rootLogin, text='Login', command=checkLogin)
    loginButton.grid(columnspan=2, sticky=W)

    loginButton = Button(rootLogin, text='New User', command=SignUp)
    loginButton.grid(columnspan=3, sticky=W)
 
    deleteButton = Button(rootLogin, text='Delete User', fg='red', command=delUser)
    deleteButton.grid(columnspan=2, sticky=W)
    rootLogin.mainloop()
 
def checkLogin():
    with open(credentialsFile) as f:
        data = f.readlines()
        username = data[0].rstrip()
        password = data[1].rstrip()
 
    if nameVarLogin.get() == username and passwordVarLogin.get() == password:
        rootLogin.destroy()
        cl = client()
        cl.client_program()

    else:
        invalidDetailsWindow = Tk()
        invalidDetailsWindow.title('Invalid Details')
        invalidDetailsWindow.geometry('150x50')
        invalidDetailsWindowLabel = Label(r, text='\n[!] Invalid Login')
        invalidDetailsWindowLabel.pack()
        invalidDetailsWindow.mainloop()
 
def delUser():
    # Deletes the credentials File, i.e. all the users
    os.remove(credentialsFile)
    rootLogin.destroy()
    NewSignUp()


if __name__ == '__main__':
    if os.path.isfile(credentialsFile):
        Login()
    else:
        NewSignUp()
