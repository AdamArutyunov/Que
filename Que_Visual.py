import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
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

        self.resize(850, 350)
        self.setWindowTitle("Визуализация")

        self.data = PQLE.select("cashboxes")
        self.warning_label = QLabel(self)
        self.warning_label.setGeometry(10, 275, 800, 100)

        self.cashboxes = {}
        
        x = 0
        for d in self.data:
            self.cashboxes[d[0]] = QueCashbox(self, d[0])
            self.cashboxes[d[0]].move(x * 200, 10)
            x += 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_warning)
        self.timer.start(100)

        self.min_x = -1
        self.max_x = -1

        self.show()

    def check_warning(self):
        self.data = PQLE.select("cashboxes")
        min_value = min(self.data, key=lambda x: x[2])
        max_value = max(self.data, key=lambda x: x[2])
        if max_value[2] - min_value[2] >= 5:
            max_name = max_value[3]
            min_name = min_value[3]
            max_id = max_value[0]
            min_id = min_value[1]
            max_i = list(self.data).index(max_value)
            min_i = list(self.data).index(min_value)

            text = f"""Покупатели с {max_name}! Перейдите на {min_name}."""
            self.warning_label.setText(text)

            self.min_x = 200 * min_i + 118
            self.max_x = 200 * max_i + 118
        else:
            self.warning_label.setText("")
            self.min_x = -1
            self.max_x = -1

        self.repaint()


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(Qt.red, 3))
        if self.min_x == self.max_x == -1:
            return

        h = 250
        qp.drawLine(self.max_x, h, self.min_x, h)
        if self.max_x < self.min_x:
            qp.drawLine(self.min_x, h, self.min_x - 30, h - 10)
            qp.drawLine(self.min_x, h, self.min_x - 30, h + 10)
        else:
            qp.drawLine(self.min_x, h, self.min_x + 30, h - 10)
            qp.drawLine(self.min_x, h, self.min_x + 30, h + 10)
        qp.end()
        

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
