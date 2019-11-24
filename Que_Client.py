import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QWidget
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import QTimer
from PyQL import PyQL
from PyQt5 import uic
from style import style


class QueCashboxInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("CashboxWindow.ui", self)

        cashboxes_names = map(lambda x: x[0], PQLE.select("cashboxes", ["name"]))

        dialog = QInputDialog(self)
        
        item, OBP = dialog.getItem(self, "Выберите кассу",
                                   "Имя кассы:" + " " * 37, cashboxes_names, 0, False)

        if OBP:
            self.cashbox_id = PQLE.select("cashboxes", ["id"], [f"name = '{item}'"])[0][0]
        else:
            self.hide()
            sys.exit()

        self.cashbox_name = PQLE.select("cashboxes", ["name"], [f"id = {self.cashbox_id}"])[0][0]
        self.setWindowTitle(self.cashbox_name)

        self.parse_n()
        self.update_n()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.parse_n)
        self.timer.start(10)

        self.plus_button.clicked.connect(self.plus)

        self.show()

    def plus(self):
        PQLE.update("cashboxes", "clicks", "clicks + 1", [f"id = {self.cashbox_id}"])
        PQLE.commit()

    def parse_n(self):
        self.n = PQLE.select("cashboxes", ["clicks"], [f"id = {self.cashbox_id}"])[0][0]
        self.update_n()

    def update_n(self):
        self.label.setText(f"Проходов за текущий период: {self.n}")

if __name__ == "__main__":
    conn = sqlite3.connect("Que.db")
    PQLE = PyQL(conn, "Que")

    app = QApplication(sys.argv)
    app.setStyleSheet(style)

    fid = QFontDatabase.addApplicationFont("fonts/Lato-Regular.ttf")  # Replace with your path
    fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
    font = QFont(fontstr)
    app.setFont(font)

    ex = QueCashboxInterface()

    sys.exit(app.exec())
