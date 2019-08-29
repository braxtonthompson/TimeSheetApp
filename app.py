from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def button_clicked(self):
        print("clicked")

    def initUI(self):
        self.setGeometry(200, 200, 650, 550)
        self.setWindowTitle("Time Sheet App")

        self.label_username = QtWidgets.QLabel(self)
        self.label_username.setText("Username")
        self.label_username.move(100,100)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Submit")
        self.b1.clicked.connect(self.button_clicked)

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()