from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        self.setGeometry(0,0,500,500)
        self.setWindowTitle("Estudo de qtFramework")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Label Simples")
        self.label.move(50,50)

        # Button
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("aperta aqui")
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        # Set state function button
        self.label.setText("clicked")
        self.update()

    def update(self):
        # Responsivity
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = myWindow()   

    win.show()
    sys.exit(app.exec_())
window()