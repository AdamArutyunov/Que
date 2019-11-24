style = '''
QMainWindow {
    background-color: white;
    font-family: “ALato”
}

QInputDialog {
    background-color: white;
    width: 150px;
    height: 50px;
}

QLabel {
    font-size: 25px;
}

QLabel#points_label {
    font-size: 65px;
}

QPushButton {
    background-color: white;
    color: #0084FF;
    border: 2px solid #0084FF;
    border-radius: 15px;
    font-size: 15px;
    min-height: 30px;
    padding: 0 25px;
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

QPushButton#plus_button {
    min-height: 150px;
    font-size: 50px;
    border-radius: 50px;
}

QLayout {
    margin: 20px;
}


QWidget#centralwidget {
    margin: 20px;
}'''
