from tkinter  import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql
import os
import random
import struct
from bitarray import bitarray
from math import (floor, sin)

import hashlib

global  hash


class MD5():
    bit_add = lambda a, b: (a + b) % pow(2, 32)
    shift_left = lambda x, n: (x << n) | (x >> (32 - n))

    @classmethod
    def R(cls, func, a, b, c, d, x, s, t):
        res = cls.bit_add(func(b, c, d), x)
        res = cls.bit_add(res, t)
        res = cls.bit_add(res, a)
        res = cls.shift_left(res, s)
        res = cls.bit_add(res, b)
        return res

    @classmethod
    def generate_hash(cls, str):
        cls._A = 0x67452301
        cls._B = 0xEFCDAB89
        cls._C = 0x98BADCFE
        cls._D = 0x10325476

        b_array = cls.step_1(str)
        b_array = cls.step_2(len(str), b_array)

        cls.step_4(b_array)

        return cls._step_5()

    @classmethod
    def step_1(cls, str):
        b_array = bitarray()
        b_array.frombytes(str)

        b_array.append(1)

        while b_array.length() % 512 != 448:
            b_array.append(0)

        return bitarray(b_array)

    @classmethod
    def step_2(cls, str_len, s1_array):
        b_len = (str_len * 8) % pow(2, 64)

        b_array_len = bitarray()
        b_array_len.frombytes(struct.pack("<Q", b_len))

        res = s1_array.copy()
        res.extend(b_array_len)

        return res

    # Шаг 3 произведен в объявлении класса

    @classmethod
    def step_4(cls, b_array):
        F = lambda b, c, d: (b & c) | (~b & d)
        G = lambda b, c, d: (b & d) | (c & ~d)
        H = lambda b, c, d: b ^ c ^ d
        I = lambda b, c, d: c ^ (b | ~d)

        T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        N = len(b_array) // 32

        for block_idx in range(0, N // 16, 512):
            a, b, c, d = cls._A, cls._B, cls._C, cls._D

            X = [b_array[block_idx + (x * 32): block_idx + (x * 32) + 32] for x in range(16)]

            X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

            s1 = [7, 12, 17, 22]
            s2 = [5, 9, 14, 20]
            s3 = [4, 11, 16, 23]
            s4 = [6, 10, 15, 21]

            # Раунд 2
            a = cls.R(F, a, b, c, d, X[0], s1[0], T[0])
            d = cls.R(F, d, a, b, c, X[1], s1[1], T[1])
            c = cls.R(F, c, d, a, b, X[2], s1[2], T[2])
            b = cls.R(F, b, c, d, a, X[3], s1[3], T[3])
            a = cls.R(F, a, b, c, d, X[4], s1[0], T[4])
            d = cls.R(F, d, a, b, c, X[5], s1[1], T[5])
            c = cls.R(F, c, d, a, b, X[6], s1[2], T[6])
            b = cls.R(F, b, c, d, a, X[7], s1[3], T[7])
            a = cls.R(F, a, b, c, d, X[8], s1[0], T[8])
            d = cls.R(F, d, a, b, c, X[9], s1[1], T[9])
            c = cls.R(F, c, d, a, b, X[10], s1[2], T[10])
            b = cls.R(F, b, c, d, a, X[11], s1[3], T[11])
            a = cls.R(F, a, b, c, d, X[12], s1[0], T[12])
            d = cls.R(F, d, a, b, c, X[13], s1[1], T[13])
            c = cls.R(F, c, d, a, b, X[14], s1[2], T[14])
            b = cls.R(F, b, c, d, a, X[15], s1[3], T[15])

            # Раунд 2
            a = cls.R(G, a, b, c, d, X[1], s2[0], T[16])
            d = cls.R(G, d, a, b, c, X[6], s2[1], T[17])
            c = cls.R(G, c, d, a, b, X[11], s2[2], T[18])
            b = cls.R(G, b, c, d, a, X[0], s2[3], T[19])
            a = cls.R(G, a, b, c, d, X[5], s2[0], T[20])
            d = cls.R(G, d, a, b, c, X[10], s2[1], T[21])
            c = cls.R(G, c, d, a, b, X[15], s2[2], T[22])
            b = cls.R(G, b, c, d, a, X[4], s2[3], T[23])
            a = cls.R(G, a, b, c, d, X[9], s2[0], T[24])
            d = cls.R(G, d, a, b, c, X[14], s2[1], T[25])
            c = cls.R(G, c, d, a, b, X[3], s2[2], T[26])
            b = cls.R(G, b, c, d, a, X[8], s2[3], T[27])
            a = cls.R(G, a, b, c, d, X[13], s2[0], T[28])
            d = cls.R(G, d, a, b, c, X[2], s2[1], T[29])
            c = cls.R(G, c, d, a, b, X[7], s2[2], T[30])
            b = cls.R(G, b, c, d, a, X[12], s2[3], T[31])

            # Раунд 3
            a = cls.R(H, a, b, c, d, X[5], s3[0], T[32])
            d = cls.R(H, d, a, b, c, X[8], s3[1], T[33])
            c = cls.R(H, c, d, a, b, X[11], s3[2], T[34])
            b = cls.R(H, b, c, d, a, X[14], s3[3], T[35])
            a = cls.R(H, a, b, c, d, X[1], s3[0], T[36])
            d = cls.R(H, d, a, b, c, X[4], s3[1], T[37])
            c = cls.R(H, c, d, a, b, X[7], s3[2], T[38])
            b = cls.R(H, b, c, d, a, X[10], s3[3], T[39])
            a = cls.R(H, a, b, c, d, X[13], s3[0], T[40])
            d = cls.R(H, d, a, b, c, X[0], s3[1], T[41])
            c = cls.R(H, c, d, a, b, X[3], s3[2], T[42])
            b = cls.R(H, b, c, d, a, X[6], s3[3], T[43])
            a = cls.R(H, a, b, c, d, X[9], s3[0], T[44])
            d = cls.R(H, d, a, b, c, X[12], s3[1], T[45])
            c = cls.R(H, c, d, a, b, X[15], s3[2], T[46])
            b = cls.R(H, b, c, d, a, X[2], s3[3], T[47])

            # Раунд 4
            a = cls.R(I, a, b, c, d, X[0], s4[0], T[48])
            d = cls.R(I, d, a, b, c, X[7], s4[1], T[49])
            c = cls.R(I, c, d, a, b, X[14], s4[2], T[50])
            b = cls.R(I, b, c, d, a, X[5], s4[3], T[51])
            a = cls.R(I, a, b, c, d, X[12], s4[0], T[52])
            d = cls.R(I, d, a, b, c, X[3], s4[1], T[53])
            c = cls.R(I, c, d, a, b, X[10], s4[2], T[54])
            b = cls.R(I, b, c, d, a, X[1], s4[3], T[55])
            a = cls.R(I, a, b, c, d, X[8], s4[0], T[56])
            d = cls.R(I, d, a, b, c, X[15], s4[1], T[57])
            c = cls.R(I, c, d, a, b, X[6], s4[2], T[58])
            b = cls.R(I, b, c, d, a, X[13], s4[3], T[59])
            a = cls.R(I, a, b, c, d, X[4], s4[0], T[60])
            d = cls.R(I, d, a, b, c, X[11], s4[1], T[61])
            c = cls.R(I, c, d, a, b, X[2], s4[2], T[62])
            b = cls.R(I, b, c, d, a, X[9], s4[3], T[63])

            cls._A = (a + cls._A) & 0xffffffff
            cls._B = (b + cls._B) & 0xffffffff
            cls._C = (c + cls._C) & 0xffffffff
            cls._D = (d + cls._D) & 0xffffffff

    @classmethod
    def _step_5(cls):
        # Convert the buffers to little-endian.
        A = struct.unpack("<I", struct.pack(">I", cls._A))[0]
        B = struct.unpack("<I", struct.pack(">I", cls._B))[0]
        C = struct.unpack("<I", struct.pack(">I", cls._C))[0]
        D = struct.unpack("<I", struct.pack(">I", cls._D))[0]

        # Output the buffers in lower-case hexadecimal format.
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"



class DB():
    def __init__(self):
        self.ConnectVar = sql.connect('Passwords.db')
        self.CursorVar = self.ConnectVar.cursor()
        self.CursorVar.execute(
        '''CREATE TABLE IF NOT EXISTS passwords (id integer primary key, site text, login text, password text)'''  )
        self.ConnectVar.commit()
        self.a = 5

    def InsertData(self, site, login, password):
        self.CursorVar.execute('''INSERT INTO passwords(site, login, password) VALUES(?, ?, ?)''', (site, login, password))
        self.ConnectVar.commit()

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
   
        generationButton =  Button(RightFrame,  text ='Генерация пароля', command = self.generation)
        generationButton.place(relx = 0.3, rely = 0.55, relwidth = 0.5 , relheight = 0.1)
        

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

    def openChange(self):
        Update()

    def generation(self):
        PasswordGeneration()


class Login(Toplevel, DB ):
    def __init__(self):
        super().__init__()
        #self.db = db
        self.init()
                
    def closing(self):
        if messagebox.askquestion('Выход',"Вы уверены?"):
            mainWindow.destroy()
    

    def entry(self):   
                                                         
        currentHash = MD5.generate_hash(b'self.PasswordFieldd.get()')
        print(currentHash, self.PasswordFieldd.get())

        #если то,что введено с клавиатуры == тому что было записано в файл раньше, то открывается окно
        with open('CurrentHash.txt', 'w') as checkFile:
            checkFile.write(currentHash)
            
        
        with open('CheckHash.txt', 'r') as checkFile:
            with open('CurrentHash.txt', 'r') as currenFile:   
                checkFileList = checkFile.read().splitlines()             
                currenFileList = currenFile.read().splitlines()

                if checkFileList == currenFileList:
                    print('yes')
                    mainWindow.deiconify()
                    print(currenFileList)
                    self.destroy()
                else:                  
                    messagebox.showerror('Ошибка', 'Неправильный пароль')

            os.remove('CurrentHash.txt')

        

    def registering(self):

        checkhash = MD5.generate_hash(b'self.PassworField.get()')
        print(checkhash , '   ', self.PassworField.get())

        with open('CheckHash.txt', 'w') as checkFile:
            checkFile.write(checkhash)

        self.authorization().deiconify()                                                      #тут нужно добавить функцию хэша
        self.withdraw()
        #Создать базу данных
        #и записать то что введено с клавиатуры

        
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

        self.PasswordFieldd = Entry(centerFrame, width=15,font='TimesNewRoman  14')
        self.PasswordFieldd.place(relx= 0.2 ,rely = 0.4 , relwidth=0.6, relheight=0.1)

        self.AuthorizationButton = Button(centerFrame,bg = 'salmon', height = 15, width = 25, text = 'Вход', command = self.entry)
        self.AuthorizationButton.place(relx= 0.35 ,rely = 0.65 , relwidth=0.3, relheight=0.1)

        centerFrame.place(relx= 0 ,rely = 0 , relwidth=0.998, relheight=0.998)      

        self.protocol('WM_DELETE_WINDOW', self.closing)



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

        self.PassworField = Entry(centerFrame, width=15,font='TimesNewRoman  14')
        self.PassworField.place(relx= 0.2 ,rely = 0.4 , relwidth=0.6, relheight=0.1)

        self.AuthorizationButton = Button(centerFrame,bg = 'salmon', height = 15, width = 25, text = 'Зарегистрироваться', command = self.registering)
        self.AuthorizationButton.place(relx= 0.35 ,rely = 0.65 , relwidth=0.3, relheight=0.1)

        centerFrame.place(relx= 0 ,rely = 0 , relwidth=0.998, relheight=0.998)        

        self.protocol('WM_DELETE_WINDOW', self.closing)

    def init(self):
        if os.path.exists('CheckHash.txt') is True:
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
        self.OkButton.place(relx = 0.67,rely = 0.85, relwidth=0.3, relheight=0.08)

        self.grab_set()
        self.focus_set() 

    def CommandGeneration(self):
        chars = '+-/*!&$#?=abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        length = int(self.CharEntry.get())
        password = ''
        for i in range(length):           
            password += random.choice(chars)
        self.PasswordText.insert(1.0, password)




def closing():
    if messagebox.askquestion('Выход',"Вы уверены?"):
        mainWindow.destroy()


if __name__ == '__main__':
    mainWindow = Tk()
    lg = Login()
    db = DB()
    app = Main(mainWindow)
    app.pack()
    mainWindow.title('Manager Passwords')
    mainWindow.geometry('850x500+600+200')
    mainWindow.withdraw()
    mainWindow.protocol('WM_DELETE_WINDOW', closing)
    mainWindow.mainloop()


