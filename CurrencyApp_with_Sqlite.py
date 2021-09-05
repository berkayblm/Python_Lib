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
        self.ceviri_alan_1 = QLineEdit()
        self.tl_usd = QRadioButton("TL-USD")
        self.usd_tl = QRadioButton("USD-TR")
        self.tl_eur = QRadioButton("TL-EUR")
        self.eur_tl = QRadioButton("EUR-TL")
        self.tl_str = QRadioButton("TL-STR")
        self.str_tl = QRadioButton("STR-TL")
        self.btc_usd = QRadioButton("BTC-USD")
        self.trans = QPushButton("Çevir")

        self.ceviri_alan_2 = QLineEdit()

        v_box = QVBoxLayout()
        v_box.addWidget(self.ceviri_alan_1)
        v_box.addWidget(self.tl_usd)
        v_box.addWidget(self.usd_tl)
        v_box.addWidget(self.tl_eur)
        v_box.addWidget(self.eur_tl)
        v_box.addWidget(self.tl_str)
        v_box.addWidget(self.str_tl)

        v_box.addWidget(self.trans)

        v_box.addStretch()

        v_box2 = QVBoxLayout()
        v_box2.addWidget(self.ceviri_alan_2)
        v_box2.addStretch()

        h_box = QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addStretch()
        h_box.addLayout(v_box2)
        self.setLayout(h_box)

        self.trans.clicked.connect(lambda : self.click(self.tl_usd.isChecked(),self.usd_tl.isChecked(),self.tl_eur.isChecked(),self.eur_tl.isChecked(),self.tl_str.isChecked(),self.str_tl.isChecked(),self.ceviri_alan_1,self.ceviri_alan_2))


    def click(self,tl_usd,usd_tl,tl_eur,eur_tl,tl_str,str_tl,ceviri_alan_1,ceviri_alan_2):

        url = "https://kur.doviz.com/"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        currency = soup.find_all("span", {"class": "name"})
        value = soup.find_all("span", {"class": "value"})
        self.isim_listesi = []
        self.deger_listesi = []

        for i in currency:
            self.isim_listesi.append(i.text)
        for j in value:
            j = j.text.replace(",", ".")
            self.deger_listesi.append(j)

        if usd_tl:
            result = float(self.deger_listesi[1]) * float(ceviri_alan_1.text())
            ceviri_alan_2.setText(str(result))


        elif tl_usd:
            result = float(ceviri_alan_1.text()) / float(self.deger_listesi[1])
            ceviri_alan_2.setText(str(result))

        elif eur_tl:
            result = float(self.deger_listesi[2]) * float(ceviri_alan_1.text())
            ceviri_alan_2.setText(str(result))

        elif tl_eur:
            result = float(ceviri_alan_1.text()) / float(self.deger_listesi[2])
            ceviri_alan_2.setText(str(result))

        elif str_tl:
            result = float(self.deger_listesi[3]) * float(self.ceviri_alan_1.text())
            ceviri_alan_2.setText(str(result))

        elif tl_str:
            result = float(ceviri_alan_1.text()) / float(self.deger_listesi[3])
            ceviri_alan_2.setText(str(result))

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pencere = Window()
        self.setCentralWidget(self.pencere)
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()
        dosya = menubar.addMenu("Dosya")

        dosya_ac = QAction("Dosya Aç", self)
        dosya_ac.setShortcut("Ctrl+O")

        dosya_kaydet = QAction("Dosya Kaydet",self)
        dosya_kaydet.setShortcut("Ctrl+S")

        temizle = QAction("Satır Sil",self)
        temizle.setShortcut("Ctrl+D")

        cikis = QAction("Çıkış",self)
        cikis.setShortcut("Ctrl+Q")

        dosya.addAction(dosya_ac)
        dosya.addAction(dosya_kaydet)
        dosya.addAction(temizle)
        dosya.addAction(cikis)

        dosya.triggered.connect(self.response)

        self.setWindowTitle("Currency Application")
        self.show()

    def response(self,action):
        if action.text() == "Dosya Aç":
            dosya_ismi = QFileDialog.getOpenFileName(self,"Dosya Aç",os.getenv("HOME"))

            with open(dosya_ismi[0],"r",encoding="utf-8") as file:
                self.pencere.ceviri_alan_1.setText(file.read())

        elif action.text() == "Dosya Kaydet":
            dosya_ismi = QFileDialog.getSaveFileName(self,"Dosya Kaydet",os.getenv("HOME"))

            with open(dosya_ismi[0],"a",encoding="utf-8") as file:
                file.write(self.pencere.ceviri_alan_1.text() + " = " + self.pencere.ceviri_alan_2.text() + "\n")

        elif action.text() == "Satır Sil":
            self.pencere.ceviri_alan_1.clear()
            self.pencere.ceviri_alan_2.clear()

        elif action.text() == "Çıkış":
            qApp.quit()

#------------------DATABASE -------------------------------------

class Window_Database(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.baglanti_olustur()

    def baglanti_olustur(self):
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()

        self.cursor.execute("Create Table If Not Exists kullanicilar(kullanici_adi TEXT,parola TEXT)")

        self.con.commit()
    def initUI(self):
        self.kullanici_adi = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.kayit_ol = QtWidgets.QPushButton("Kayıt Ol")
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.giris = QtWidgets.QPushButton("Giriş Yap")
        self.yazi_alani = QtWidgets.QLabel("")
        self.yazi_alani_2 = QtWidgets.QLabel("")
        self.kayit_isim = QtWidgets.QLineEdit()
        self.kayit_parola = QtWidgets.QLineEdit()
        self.kayit_parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.kayit_parola_2 = QtWidgets.QLineEdit()
        self.kayit_parola_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.picture = QtWidgets.QLabel()
        self.picture.setPixmap(QtGui.QPixmap("../Python-Logo-Free-PNG-Image.png"))

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.kullanici_adi)
        v_box.addWidget(self.parola)
        v_box.addWidget(self.yazi_alani)
        v_box.addWidget(self.giris)
        v_box.addStretch()
        v_box.addWidget(self.picture)
        v_box.addWidget(self.kayit_ol)
        v_box.addWidget(self.kayit_isim)
        v_box.addWidget(self.kayit_parola)
        v_box.addWidget(self.kayit_parola_2)
        v_box.addWidget(self.yazi_alani_2)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)

        self.giris.clicked.connect(self.login)
        self.kayit_ol.clicked.connect(self.signup)

        self.show()

    def login(self):
        ad = self.kullanici_adi.text()
        par = self.parola.text()

        self.cursor.execute("Select * from kullanicilar Where kullanici_adi = ? and parola = ?",(ad,par))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.yazi_alani.setText("Böyle bir kullanıcı yok")
        else:
            self.yazi_alani.setText("Hoşgeldiniz " + ad)

            if self.yazi_alani.text() == f"Hoşgeldiniz {self.kullanici_adi.text()}":
                time.sleep(1.2)
                self.w = Menu()
                self.w.show()

    def signup(self):
        isim = self.kayit_isim.text()
        parola_1 = self.kayit_parola.text()
        parola_2 = self.kayit_parola_2.text()

        self.cursor.execute("Select * From kullanicilar Where kullanici_adi = ?",(isim,))
        liste = self.cursor.fetchall()

        if len(liste) == 0:

            if len(parola_1) and len(parola_2) < 8:
                self.yazi_alani_2.setText("Parola en az 8 karakterden oluşmalı.")
            elif parola_1 != parola_2:
                self.yazi_alani_2.setText("İki parola da aynı olmalı.")
            else:
                self.yazi_alani_2.setText("Başarıyla Kayıt Olundu!")
                self.cursor.execute("Insert into kullanicilar VALUES(?,?)",(isim, parola_1))
                self.con.commit()

        else:
            self.yazi_alani_2.setText("Kullanıcı adı alınmış.")


app = QApplication(sys.argv)
window = Window_Database()
window.setGeometry(300,300,600,600)
sys.exit(app.exec_())