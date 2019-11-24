import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QFontDatabase, QFont, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
from PyQL import PyQL
from PyQt5 import uic
from style import style


class QueCashbox(QWidget):
    def __init__(self, parent, cashbox_id):
        super().__init__(parent)
        uic.loadUi("CashboxWidget.ui", self)

        self.cashbox_id = cashbox_id
        self.name = PQLE.select("cashboxes", ["name"], [f"id = {self.cashbox_id}"])[0][0]
        self.cashname_label.setText(self.name)
        
        self.update()
        self.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def update(self):
        data = PQLE.select("cashboxes", ["clicks", "status"],
                           [f"id = {self.cashbox_id}"])
        self.points = data[0][1]
        self.clicks = data[0][0]
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(Qt.white, -1))
        
        if self.points == 0:
            color = (0, 255, 0)
        elif 1 <= self.points <= 3:
            color = (0, 200, 0)
        elif 4 <= self.points <= 6:
            color = (230, 230, 0)
        elif 7 <= self.points <= 8:
            color = (200, 0, 0)
        elif self.points == 9:
            color = (150, 0, 0)
        elif self.points == 10:
            color = (100, 0, 0)
            
        qp.setBrush(QColor(*color))

        qp.drawEllipse(50, 87, 130, 130)
        
        qp.end()
        self.points_label.setText(str(self.points))


class QueVisual(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(850, 280)
        self.setWindowTitle("Визуализация")

        self.data = PQLE.select("cashboxes")

        self.cashboxes = {}
        
        x = 0
        for d in self.data:
            self.cashboxes[d[0]] = QueCashbox(self, d[0])
            self.cashboxes[d[0]].move(x * 200, 10)
            x += 1

        self.show()


def excepthook(type, value, tback):
    sys.__excepthook__(type, value, tback)
sys.excepthook = excepthook


conn = sqlite3.connect("Que.db")
PQLE = PyQL(conn, "Que")

app = QApplication(sys.argv)
app.setStyleSheet(style)

fid = QFontDatabase.addApplicationFont("fonts/Lato-Regular.ttf")  # Replace with your path
fontstr = QFontDatabase.applicationFontFamilies(fid)[0]
font = QFont(fontstr)
app.setFont(font)

ex = QueVisual()

sys.exit(app.exec())
