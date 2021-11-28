import sys
import sqlite3
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidget, QListWidgetItem
from dialog import Info


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(449, 369)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(50, 20, 91, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 60, 151, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 20, 111, 61))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 449, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Автор"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Название"))
        self.pushButton.setText(_translate("MainWindow", "искать"))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Каталог библиотеки')

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(50, 110, 350, 220)
        self.pushButton.clicked.connect(self.add_button)

    def add_button(self):
        self.listWidget.clear()
        if self.comboBox.currentText() == 'Автор' and len(self.lineEdit.text()) > 0:
            con = sqlite3.connect('books.sqlite')
            cur = con.cursor()
            result = list(cur.execute(f"""
SELECT data.title, data.autor, data.year, genres.title, data.link FROM data
INNER JOIN genres ON data.genre = genres.id
WHERE data.autor LIKE '{str(self.lineEdit.text())}%'
            """).fetchall())
            con.close()
            for elem in map(lambda x: x[0], result):
                newButton = QPushButton(elem)
                newButton.clicked.connect(self.click)
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setSizeHint(newButton.sizeHint())
                self.listWidget.addItem(listWidgetItem)
                self.listWidget.setItemWidget(listWidgetItem, newButton)
                self.listWidget.scrollToItem(listWidgetItem)


        elif self.comboBox.currentText() == 'Название' and len(self.lineEdit.text()) > 0:
            con = sqlite3.connect('books.sqlite')
            cur = con.cursor()
            result = list(cur.execute(f"""
            SELECT data.title, data.autor, data.year, genres.title, data.link FROM data
            INNER JOIN genres ON data.genre = genres.id
            WHERE data.title LIKE '{str(self.lineEdit.text())}%'
                        """).fetchall())
            con.close()
            for elem in map(lambda x: x[0], result):
                newButton = QPushButton(elem)
                newButton.clicked.connect(self.click)
                listWidgetItem = QListWidgetItem()
                listWidgetItem.setSizeHint(newButton.sizeHint())
                self.listWidget.addItem(listWidgetItem)
                self.listWidget.setItemWidget(listWidgetItem, newButton)
                self.listWidget.scrollToItem(listWidgetItem)


    def click(self):
        con = sqlite3.connect('books.sqlite')
        cur = con.cursor()
        a = list(cur.execute(f"""
        SELECT data.title, data.autor, data.year, genres.title, data.link FROM data
        INNER JOIN genres ON data.genre = genres.id
        WHERE data.title = '{self.sender().text()}'
                    """).fetchone())
        self.second = Info(a[0], a[1], a[2], a[3], link=a[4])
        self.second.show()
        con.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
