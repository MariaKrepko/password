from tkinter import*
from tkinter import ttk
import sqlite3
import os.path


global hash

def authorization():
    if os.path.exists('Psswords.db') is False:
        main = Tk()
        main.title('Регистрация')
        main.geometry('400x300+600+150')
        main.resizable(False,False)

        centerFrame = Frame(bg = '#fdfdfe')
        LoginLabel = Label(centerFrame, width=15, text ='login:',  bg = '#fdfdfe')
        LoginLabel.place(relx= 0.33 , rely = 0.1, relwidth=0.3, relheight=0.1)

        LoginField = Entry(centerFrame,width=15,font='TimesNewRoman  14', )
        LoginField.place(relx= 0.2 ,rely = 0.2 , relwidth=0.6, relheight=0.1)

        PasswordLabel = Label(centerFrame, width=15, text = 'Password:', bg = '#fdfdfe')
        PasswordLabel.place(relx= 0.33 ,rely = 0.3 , relwidth=0.3, relheight=0.1)

        PasswordField = Entry(centerFrame, width=15,font='TimesNewRoman  14')
        PasswordField.place(relx= 0.2 ,rely = 0.4 , relwidth=0.6, relheight=0.1)
        '''
        def hashingPassword():
            hash = PasswordField.get()
            print(hash)
        '''
        AuthorizationButton = Button(centerFrame,bg = 'salmon', height = 15, width = 25, text = 'Зарегистрироваться') #, command = hashingPassword)
        AuthorizationButton.place(relx= 0.35 ,rely = 0.65 , relwidth=0.3, relheight=0.1)

        centerFrame.place(relx= 0 ,rely = 0 , relwidth=0.998, relheight=0.998)        



        main.mainloop()
    else:
        main = Tk()
        main.title('Авторизация')
        main.geometry('400x300+600+150')
        main.resizable(False,False)

        centerFrame = Frame(bg = '#fdfdfe')
        LoginLabel = Label(centerFrame, width=15, text ='login:',  bg = '#fdfdfe')
        LoginLabel.place(relx= 0.33 , rely = 0.1, relwidth=0.3, relheight=0.1)

        LoginField = Entry(centerFrame,width=15,font='TimesNewRoman  14', )
        LoginField.place(relx= 0.2 ,rely = 0.2 , relwidth=0.6, relheight=0.1)

        PasswordLabel = Label(centerFrame, width=15, text = 'Password:', bg = '#fdfdfe')
        PasswordLabel.place(relx= 0.33 ,rely = 0.3 , relwidth=0.3, relheight=0.1)

        PasswordField = Entry(centerFrame, width=15,font='TimesNewRoman  14')
        PasswordField.place(relx= 0.2 ,rely = 0.4 , relwidth=0.6, relheight=0.1)

        AuthorizationButton = Button(centerFrame,bg = 'salmon', height = 15, width = 25, text = 'Вход')
        AuthorizationButton.place(relx= 0.35 ,rely = 0.65 , relwidth=0.3, relheight=0.1)

        centerFrame.place(relx= 0 ,rely = 0 , relwidth=0.998, relheight=0.998)      



        main.mainloop()



authorization()

