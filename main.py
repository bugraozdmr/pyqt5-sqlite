import sqlite3
from PyQt5 import QtWidgets
import sys

class pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.baglanti_kur()
        self.ui()

    def baglanti_kur(self):
        self.con = sqlite3.connect("bilgiler.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kullanıcı (ad TEXT,sifre TEXT)")
        self.con.commit()

        # sorgu ilk giriş için
        self.cursor.execute("select * from kullanıcı")
        list = self.cursor.fetchall()
        if len(list) == 0:
            self.ilk_giris()
        else:
            n = input("bilgi güncelleyecek misin ?(e/h) :").lower()
            if n == "e":  # fazla sorgu almadan direkt değiştircem
                self.cursor.execute("select ad from kullanıcı")
                liste = self.cursor.fetchall()
                self.cursor.execute("delete from kullanıcı where ad = ?", (liste[0][0],))
                self.con.cursor()
                s = input("yeni kullanıcı adı :")
                m = input("yeni şifre :")
                self.cursor.execute("insert into kullanıcı values(?,?)", (s, m))
                self.con.commit()
            # else durumunu boşver zaten girmez çıkar

    def ilk_giris(self):
        print("Kullanıcı adı ,parala belirle (Unutma)\n")
        a = input("kullanıcı adı :")   #yukarıdaki sorguda bana kolaylık sağlaması için sildim
        b = input("şifre :")
        self.cursor.execute("insert into kullanıcı values(?,?)", (a,b))
        self.con.commit()
        self.deger = 1      #eğer 1 olmuşsa bilgi güncellemek ister misin diye soracak

    def ui(self):
        self.kadi = QtWidgets.QLineEdit()
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)     #parola girilirken ***** yazıyor
        self.giris = QtWidgets.QPushButton("Giriş yap")
        self.yazi_alani = QtWidgets.QLabel()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.kadi)
        v_box.addWidget(self.password)
        v_box.addStretch()
        v_box.addWidget(self.yazi_alani)
        v_box.addStretch()
        v_box.addWidget(self.giris)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)

        self.setWindowTitle("Kullanıcı girişi")
        self.giris.clicked.connect(self.login)
        self.setGeometry(600,400,300,300)
        self.show()

    def login(self):
        ad = self.kadi.text()
        sifre = self.password.text()

        self.cursor.execute("select * from kullanıcı")
        k = self.cursor.fetchall()

        if ad == k[0][0] and sifre == k[0][1]:      #0.indexin 0. elemanı tek index mevcut
            self.yazi_alani.setText("Girilen bilgiler doğru.")
        elif ad == k[0][0] and sifre != k[0][1]:
            self.yazi_alani.setText("Hatalı şifre !")
        elif ad != k[0][0] and sifre == k[0][1]:
            self.yazi_alani.setText("Hatalı kullanıcı adı !")
        else:
            self.yazi_alani.setText("Her iki bilgide hatalı !")
app = QtWidgets.QApplication(sys.argv)
pencere1 = pencere()
sys.exit(app.exec_())