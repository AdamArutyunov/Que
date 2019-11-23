import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QMessageBox
from PyQt5.QtGui import QFontDatabase, QFont
from PyQL import PyQL
from PyQt5 import uic
from style import style


class Cashbox(QMainWindow):
    def __init__(self, cashbox_id):
        super().__init__()
        uic.loadUi("CashboxWindow.ui", self)

        self.cashbox_id = cashbox_id
        self.cashbox_name = PQLE.select("cashboxes", ["name"], [f"id = {self.cashbox_id}"])[0][0]
        self.setWindowTitle(self.cashbox_name)

        self.n = self.parse_n()
        self.update_n()

        self.plus_button.clicked.connect(self.plus)

    def plus(self):
        PQLE.update("cashboxes", "clicks", "clicks + 1", [f"id = {self.cashbox_id}"])
        PQLE.commit()
        self.add_n()

    def parse_n(self):
        n = PQLE.select("cashboxes", ["clicks"], [f"id = {self.cashbox_id}"])[0][0]
        return n

    def add_n(self):
        self.n += 1
        self.update_n()

    def update_n(self):
        self.label.setText(f"Проходов за текущий период: {self.n}")


conn = sqlite3.connect("Que.db")
PQLE = PyQL(conn, "Que")

app = QApplication(sys.argv)
app.setStyleSheet(style)

fid = QFontDatabase.addApplicationFont("fonts/Lato-Regular.ttf")  # Replace with your path
fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
font = QFont(fontstr)
app.setFont(font)


ex = Cashbox(1)
ex.show()

sys.exit(app.exec())
