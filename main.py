import time
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWidgets import qApp,QMainWindow,QAction
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from PyQt5 import QtWidgets,QtGui

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.transform_area_1 = QLineEdit()
        self.tl_usd = QRadioButton("TL-USD")
        self.usd_tl = QRadioButton("USD-TR")
        self.tl_eur = QRadioButton("TL-EUR")
        self.eur_tl = QRadioButton("EUR-TL")
        self.tl_str = QRadioButton("TL-STR")
        self.str_tl = QRadioButton("STR-TL")
        self.btc_usd = QRadioButton("BTC-USD")
        self.trans = QPushButton("Convert")

        self.transform_area_2 = QLineEdit()

        v_box = QVBoxLayout()
        v_box.addWidget(self.transform_area_1)
        v_box.addWidget(self.tl_usd)
        v_box.addWidget(self.usd_tl)
        v_box.addWidget(self.tl_eur)
        v_box.addWidget(self.eur_tl)
        v_box.addWidget(self.tl_str)
        v_box.addWidget(self.str_tl)

        v_box.addWidget(self.trans)

        v_box.addStretch()

        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.transform_area_2)
        v_box2.addStretch()

        h_box = QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addStretch()
        h_box.addLayout(v_box2)
        self.setLayout(h_box)

        self.trans.clicked.connect(lambda : self.click(self.tl_usd.isChecked(), self.usd_tl.isChecked(), self.tl_eur.isChecked(), self.eur_tl.isChecked(), self.tl_str.isChecked(), self.str_tl.isChecked(), self.transform_area_1, self.transform_area_2))


    def click(self,tl_usd,usd_tl,tl_eur,eur_tl,tl_str,str_tl,transform_area_1,transform_area_2):

        url = "https://kur.doviz.com/"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        currency = soup.find_all("span", {"class": "name"})
        value = soup.find_all("span", {"class": "value"})
        self.name_list = []
        self.value_list = []

        for i in currency:
            self.name_list.append(i.text)
        for j in value:
            j = j.text.replace(",", ".")
            self.value_list.append(j)

        if usd_tl:
            result = float(self.value_list[1]) * float(transform_area_1.text())
            transform_area_2.setText(str(result))

        elif tl_usd:
            result = float(transform_area_1.text()) / float(self.value_list[1])
            transform_area_2.setText(str(result))

        elif eur_tl:
            result = float(self.value_list[2]) * float(transform_area_1.text())
            transform_area_2.setText(str(result))

        elif tl_eur:
            result = float(transform_area_1.text()) / float(self.value_list[2])
            transform_area_2.setText(str(result))

        elif str_tl:
            result = float(self.value_list[3]) * float(self.transform_area_1.text())
            transform_area_2.setText(str(result))

        elif tl_str:
            result = float(transform_area_1.text()) / float(self.value_list[3])
            transform_area_2.setText(str(result))

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = Window()
        self.setCentralWidget(self.w)
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        file = menubar.addMenu("File")

        open_file = QAction("Open File", self)
        open_file.setShortcut("Ctrl+O")

        save_file = QAction("Save File", self)
        save_file.setShortcut("Ctrl+S")

        clear = QAction("CLear Lines", self)
        clear.setShortcut("Ctrl+D")

        exit = QAction("Exit", self)
        exit.setShortcut("Ctrl+Q")

        file.addAction(open_file)
        file.addAction(save_file)
        file.addAction(clear)
        file.addAction(exit)

        file.triggered.connect(self.response)

        self.setWindowTitle("Currency Application")
        self.show()

    def response(self,action):
        if action.text() == "Open File":
            file_name = QFileDialog.getOpenFileName(self,"Open File",os.getenv("HOME"))

            with open(file_name[0],"r",encoding="utf-8") as file:
                self.w.transform_area_1.setText(file.read())

        elif action.text() == "Save File":
            file_name = QFileDialog.getSaveFileName(self,"Save File",os.getenv("HOME"))

            with open(file_name[0],"a",encoding="utf-8") as file:
                file.write(self.w.transform_area_1.text() + " = " + self.w.transform_area_2.text() + "\n")

        elif action.text() == "Clear Lines":
            self.w.transform_area_1.clear()
            self.w.transform_area_2.clear()

        elif action.text() == "Exit":
            qApp.quit()

#------------------DATABASE -------------------------------------

class Window_Database(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_connection()

    def create_connection(self):
        self.con = sqlite3.connect("../database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("Create Table If Not Exists users(user_name TEXT,password TEXT)")
        self.con.commit()
    def initUI(self):
        self.username = QtWidgets.QLineEdit()
        self.passwrd = QtWidgets.QLineEdit()
        self.sign_up = QtWidgets.QPushButton("Sing up")
        self.passwrd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.log_in = QtWidgets.QPushButton("Log in")
        self.text_area_1 = QtWidgets.QLabel("")
        self.text_area_2 = QtWidgets.QLabel("")
        self.signup_name = QtWidgets.QLineEdit()
        self.signup_pwd = QtWidgets.QLineEdit()
        self.signup_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup_pwd_2 = QtWidgets.QLineEdit()
        self.signup_pwd_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(QtGui.QPixmap("../Python-Logo-Free-PNG-Image.png"))

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.username)
        v_box.addWidget(self.passwrd)
        v_box.addWidget(self.text_area_1)
        v_box.addWidget(self.log_in)
        v_box.addStretch()
        v_box.addWidget(self.picture)
        v_box.addWidget(self.sign_up)
        v_box.addWidget(self.signup_name)
        v_box.addWidget(self.signup_pwd)
        v_box.addWidget(self.signup_pwd_2)
        v_box.addWidget(self.text_area_2)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        self.log_in.clicked.connect(self.login)
        self.sign_up.clicked.connect(self.signup)

        self.show()

    def login(self):
        ad = self.username.text()
        par = self.passwrd.text()

        self.cursor.execute("Select * from users Where user_name = ? and password = ?",(ad,par))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.text_area_1.setText("No such user found")
        else:
            self.text_area_1.setText("Welcome " + ad)

            if self.text_area_1.text() == f"Welcome {self.username.text()}":
                time.sleep(1.2)
                self.w = Menu()
                self.w.show()

    def signup(self):
        name = self.signup_name.text()
        pw_1 = self.signup_pwd.text()
        pw_2 = self.signup_pwd_2.text()

        self.cursor.execute("Select * From users Where user_name = ?",(name,))
        liste = self.cursor.fetchall()

        if len(liste) == 0:

            if len(pw_1) and len(pw_2) < 8:
                self.text_area_2.setText("Password must contain at least 8 characters.")
            elif pw_1 != pw_2:
                self.text_area_2.setText("Both passwords must be the same.")
            else:
                self.text_area_2.setText("Successfully signed up!")
                self.cursor.execute("Insert into users VALUES(?,?)",(name, pw_1))
                self.con.commit()

        else:
            self.text_area_2.setText("This username had already been taken.")


app = QApplication(sys.argv)
window = Window_Database()
window.setGeometry(300,300,600,600)
sys.exit(app.exec_())


