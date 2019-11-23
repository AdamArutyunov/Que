style = '''
QMainWindow {
    background-color: white;
    font-family: “ALato”
}

QDialog {
    background-color: white;
}

QLabel {
    font-size: 25px;
}

QPushButton {
    background-color: white;
    color: #0084FF;
    border: 2px solid #0084FF;
    border-radius: 30px;
    font-size: 50px;
    min-height: 150px;
}

QPushButton:!enabled {
    opacity: 0.5;
    filter: alpha(opacity=50);
    color: #80c1ff;
    border-color: #80c1ff;
}

QPushButton:pressed {
    background-color: #0084FF;
    color: white;
}

QLayout {
    margin: 20px;
}


QWidget#centralwidget {
    margin: 20px;
}'''
