from tkinter  import *
from tkinter import ttk
import sqlite3 as sql


class Main(Frame):
    def __init__(self, mainWindow):
       super().__init__(mainWindow)
       
       self.init_main()
       self.db = db
       self.lg = lg
       self.viewRecords()

    def init_main(self):
        RightFrame = Frame( bg = '#fdfdfe')
        RightFrame.place(relx = 0.707 , rely = 0.003, relwidth=0.287, relheight=0.992)

        buttonOpenDialog = Button(RightFrame,  text ='Добавить', command = self.openDialog)
        buttonOpenDialog.place(relx = 0.3, rely = 0.25, relwidth = 0.5 , relheight = 0.1)

        buttonChange =  Button(RightFrame,  text ='Изменить', command = self.openChange)
        buttonChange.place(relx = 0.3, rely = 0.35, relwidth = 0.5 , relheight = 0.1)

        buttonDelete =  Button(RightFrame,  text ='Удалить', command = self.deleteRecords)
        buttonDelete.place(relx = 0.3, rely = 0.45, relwidth = 0.5 , relheight = 0.1)
   
        buttonSearch =  Button(RightFrame,  text ='Поиск', command = self.openSearch)
        buttonSearch.place(relx = 0.3, rely = 0.55, relwidth = 0.5 , relheight = 0.1)
        

        self.tree = ttk.Treeview(columns = ('ID', 'site', 'login', 'password'), height = 15, show = 'headings')
        self.tree.column('ID', width = 15, anchor = CENTER)
        self.tree.column('site', width = 180, anchor = CENTER)
        self.tree.column('login', width = 90, anchor = CENTER)
        self.tree.column('password', width = 90, anchor = CENTER)

        self.tree.heading('ID' , text = 'ID' )
        self.tree.heading('site' , text = 'Сайт' )
        self.tree.heading('login' , text = 'Логин' )
        self.tree.heading('password', text = 'Пароль')
        
        self.tree.place(relx = 0.003, rely = 0.003, relwidth = 0.7 , relheight = 0.992)

    def records(self, site, login, password):
        self.db.InsertData(site, login, password)
        self.viewRecords()


    def updateRecords(self, site, login, password):
        self.db.CursorVar.execute('''UPDATE passwords SET site = ?, login = ?, password = ? WHERE id = ?''', (site, login, password, self.tree.set(self.tree.selection()[0], '#1')))
        self.viewRecords()

    def viewRecords(self):
        self.db.CursorVar.execute('''SELECT * FROM passwords''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row) for row in self.db.CursorVar.fetchall()]


    def deleteRecords(self):
        for selectionItem in self.tree.selection():
            self.db.CursorVar.execute('''DELETE FROM passwords WHERE id = ?''', (self.tree.set(selectionItem, '#1'),))
        self.db.ConnectVar.commit()
        self.viewRecords()


    def openDialog(self):
        Child()

    def openSearch(self):
        Search()

    def openChange(self):
        Update()


class Login(Toplevel):
    def __init__(self):
        super().__init__(mainWindow)

    def authorization(self):
        self.title('Авторизация')
        self.geometry('400x300+600+150')
        self.resizable(False,False)

        centerFrame = Frame(self,bg = '#fdfdfe')
        self.LoginLabel = Label(centerFrame, width=15, text ='login:',  bg = '#fdfdfe')
        self.LoginLabel.place(relx= 0.33 , rely = 0.1, relwidth=0.3, relheight=0.1)

        self.LoginField = Entry(centerFrame,width=15,font='TimesNewRoman  14', )
        self.LoginField.place(relx= 0.2 ,rely = 0.2 , relwidth=0.6, relheight=0.1)

        self.PasswordLabel = Label(centerFrame, width=15, text = 'Password:', bg = '#fdfdfe')
        self.PasswordLabel.place(relx= 0.33 ,rely = 0.3 , relwidth=0.3, relheight=0.1)

        self.PasswordField = Entry(centerFrame, width=15,font='TimesNewRoman  14')
        self.PasswordField.place(relx= 0.2 ,rely = 0.4 , relwidth=0.6, relheight=0.1)

        self.AuthorizationButton = Button(centerFrame,bg = 'salmon', height = 15, width = 25, text = 'Вход')
        self.AuthorizationButton.place(relx= 0.35 ,rely = 0.65 , relwidth=0.3, relheight=0.1)

        centerFrame.place(relx= 0 ,rely = 0 , relwidth=0.998, relheight=0.998)      

    def registration(self):
        self.title('Регистрация')
        self.geometry('400x300+600+150')
        self.resizable(False,False)

        centerFrame = Frame(self, bg = '#fdfdfe')
        self.LoginLabel = Label(centerFrame, width=15, text ='login:',  bg = '#fdfdfe')
        self.LoginLabel.place(relx= 0.33 , rely = 0.1, relwidth=0.3, relheight=0.1)

        self.LoginField = Entry(centerFrame,width=15,font='TimesNewRoman  14', )
        self.LoginField.place(relx= 0.2 ,rely = 0.2 , relwidth=0.6, relheight=0.1)

        self.PasswordLabel = Label(centerFrame, width=15, text = 'Password:', bg = '#fdfdfe')
        self.PasswordLabel.place(relx= 0.33 ,rely = 0.3 , relwidth=0.3, relheight=0.1)

        self.PasswordField = Entry(centerFrame, width=15,font='TimesNewRoman  14')
        self.PasswordField.place(relx= 0.2 ,rely = 0.4 , relwidth=0.6, relheight=0.1)

        self.AuthorizationButton = Button(centerFrame,bg = 'salmon', height = 15, width = 25, text = 'Зарегистрироваться') #, command = hashingPassword)
        self.AuthorizationButton.place(relx= 0.35 ,rely = 0.65 , relwidth=0.3, relheight=0.1)

        centerFrame.place(relx= 0 ,rely = 0 , relwidth=0.998, relheight=0.998)        

    def init(self):
        if os.path.exists('Psswords.db') is True:
            self.authorization()
        else:
            self.registration()



class Child(Toplevel):
    def __init__(self):
        super().__init__(mainWindow)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('добавить данные')
        self.geometry('400x320+890+300')
        self.resizable(False, False)

        ChildFrame = Frame(self, bg = '#fdfdfe')
        ChildFrame.place(relx = 0.008,rely = 0.009, relwidth=0.985, relheight=0.98)

        CenterFrame = Frame(ChildFrame ,bg = '#fdfdfe')
        CenterFrame.place(relx = 0.02, rely = 0.15, relwidth=0.99, relheight=0.65)
        
        self.SiteLabel = Label(CenterFrame, text = 'Сайт:',  anchor = 'w', bg = '#fdfdfe')
        self.SiteLabel.place(relx = 0.01,rely = 0.15, relwidth=0.2, relheight=0.1)

        self.SiteEntry = Entry(CenterFrame)
        self.SiteEntry.place(relx = 0.2,rely = 0.15, relwidth=0.7, relheight=0.1)

        self.LoginLabel = Label(CenterFrame,text = 'Логин:', anchor = 'w',  bg =  '#fdfdfe')
        self.LoginLabel.place(relx = 0.01,rely = 0.3, relwidth=0.2, relheight=0.1)

        self.LoginEntry = Entry(CenterFrame)
        self.LoginEntry.place(relx = 0.2,rely = 0.3, relwidth=0.7, relheight=0.1)

        self.PasswordLabel = Label( CenterFrame,text = 'Пароль:', anchor = 'w', bg =  '#fdfdfe')
        self.PasswordLabel.place(relx = 0.01,rely = 0.45, relwidth=0.2, relheight=0.1)

        self.PasswordEntry = Entry(CenterFrame)
        self.PasswordEntry.place(relx = 0.2,rely = 0.45, relwidth=0.7, relheight=0.1)
        
        #кнопка сгенерировать пароль и добавить в буффер обмена
        
        self.OkayButton = Button(self, bg = '#fdfdfe', text = 'Добавить',command = self.destroy)
        self.OkayButton.bind('<Button-1>' , lambda event: self.view.records(self.SiteEntry.get(), self.LoginEntry.get(), self.PasswordEntry.get()))
        self.OkayButton.place(relx = 0.55, rely = 0.85, relwidth=0.2, relheight=0.08)
        

        self.CancelButton = Button(self, bg = '#fdfdfe', text = 'Отменить', command = self.destroy)
        self.CancelButton.place(relx = 0.77,rely = 0.85, relwidth=0.2, relheight=0.08)

        self.grab_set()
        self.focus_set()        #захват фокуса



class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.view = app
        self.defaultData()

    def init_edit(self):
        self.title('Редактирование данных')
        EditButton = Button(self, text = 'Изменить',command = self.destroy)
        EditButton.place(relx = 0.55, rely = 0.85, relwidth=0.2, relheight=0.08)
        EditButton.bind('<Button-1>' , lambda event: self.view.updateRecords(self.SiteEntry.get(), self.LoginEntry.get(), self.PasswordEntry.get()))

        self.grab_set()
        self.focus_set()

    def defaultData(self):
        self.db.CursorVar.execute('''SELECT * FROM passwords WHERE id = ? ''', (self.view.tree.set(self.view.tree.selection()[0],'#1')))
        
        row = self.db.CursorVar.fetchone()
        self.SiteEntry.insert(0, row[1])
        self.LoginEntry.insert(0, row[2])
        self.PasswordEntry.insert(0, row[3])


class PasswordGeneration(Toplevel):
    def __init__(self):
        super().__init__(mainWindow)
        self.generation()

    def generation(self):
        self.title('Генерация пароля')
        self.geometry('400x320+890+300')

        ChildFrame = Frame(self, bg = '#fdfdfe')
        ChildFrame.place(relx = 0.008,rely = 0.009, relwidth=0.985, relheight=0.98)

        CenterFrame = Frame(ChildFrame ,bg = '#fdfdfe')
        CenterFrame.place(relx = 0.02, rely = 0.15, relwidth=0.99, relheight=0.65)
        
        self.CharLabel = Label(CenterFrame, text = 'Количество\n символов:',  anchor = 'w', bg = '#fdfdfe')
        self.CharLabel.place(relx = 0.01,rely = 0.15, relwidth=0.2, relheight=0.2)

        self.CharEntry = Entry(CenterFrame)
        self.CharEntry.place(relx = 0.2,rely = 0.15, relwidth=0.7, relheight=0.15)

        self.PasswordLabel = Label(CenterFrame,text = 'Пароль:', anchor = 'w',  bg =  '#fdfdfe')
        self.PasswordLabel.place(relx = 0.01,rely = 0.4, relwidth=0.2, relheight=0.2)

        self.PasswordText = Text(CenterFrame, height=1, borderwidth=1)
        self.PasswordText.place(relx = 0.2,rely = 0.4, relwidth=0.7, relheight=0.15)

        self.OkButton = Button(self, bg = '#fdfdfe', text = 'Сгенерировать', command = self.CommandGeneration)
        self.OkButton.place(relx = 0.77,rely = 0.85, relwidth=0.2, relheight=0.08)

        self.grab_set()
        self.focus_set() 

    def CommandGeneration(self):
        chars = '+-/*!&$#?=abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        length = int(self.CharEntry.get())
        password = ''
        for i in range(length):           
            password += random.choice(chars)
        self.PasswordText.insert(1.0,password )


class DB():
    def __init__(self):
        self.ConnectVar = sql.connect('Passwords.db')
        self.CursorVar = self.ConnectVar.cursor()
        self.CursorVar.execute(
        '''CREATE TABLE IF NOT EXISTS passwords (id integer primary key, site text, login text, password text)'''  )
        self.ConnectVar.commit()

    def InsertData(self, site, login, password):
        self.CursorVar.execute('''INSERT INTO passwords(site, login, password) VALUES(?, ?, ?)''', (site, login, password))
        self.ConnectVar.commit()




if __name__ == '__main__':
    mainWindow = Tk()
    db = DB()
    lg = Login()
    app = Main(mainWindow)
    app.pack()
    mainWindow.title('Manager Passwords')
    mainWindow.geometry('850x500+600+200')
    mainWindow.mainloop()
