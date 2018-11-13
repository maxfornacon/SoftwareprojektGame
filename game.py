import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.game_widget = Game(parent=self)
        self.setCentralWidget(self.game_widget)

        menubar = self.menuBar()
        settingsMenu = menubar.addMenu('&Settings')
        opt1 = QtWidgets.QAction('3x3', self)
        opt2 = QtWidgets.QAction('4x4', self)
        opt3 = QtWidgets.QAction('reset', self)

        settingsMenu.addAction(opt1)
        settingsMenu.addAction(opt2)
        settingsMenu.addAction(opt3)

        opt1.triggered.connect(lambda: self.game_widget.setupGUI(3))
        opt2.triggered.connect(lambda: self.game_widget.setupGUI(4))
        opt3.triggered.connect(self.game_widget.reset)

        self.setWindowTitle('Game')


class Game(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(self.setupGUI(4))

    def buttonClicked(self):
        button = self.sender()
        idx = self.layout().indexOf(button)
        location = self.layout().getItemPosition(idx)
        self.changeColor(button)
        if location[0] - 1 >= 0:
            buttonAbove = self.layout().itemAtPosition(location[0] - 1, location[1]).widget()
            self.changeColor(buttonAbove)
        if location[0] + 1 <= 2:
            buttonBelow = self.layout().itemAtPosition(location[0] + 1, location[1]).widget()
            self.changeColor(buttonBelow)
        if location[1] - 1 >= 0:
            buttonLeft = self.layout().itemAtPosition(location[0], location[1] - 1).widget()
            self.changeColor(buttonLeft)
        if location[1] + 1 <= 2:
            buttonRight = self.layout().itemAtPosition(location[0], location[1] + 1).widget()
            self.changeColor(buttonRight)
        self.checkWin()

    def changeColor(self, button):
        color = button.palette().button().color().name()
        if color == "#ffffff":
            button.setStyleSheet("background-color: #d3d3d3; border: 2px solid #d3d3d3;")
        elif color == "#d3d3d3":
            button.setStyleSheet("background-color: white; border: 2px solid #d3d3d3;")

    def checkWin(self):
        won = True
        for i in range(9):
            button = self.layout().itemAt(i).widget()
            color = button.palette().button().color().name()
            if color == "#ffffff":
                won = None
                break
        if won:
            QMessageBox.about(self, "Gewonnen", "Du hast gewonnen!")
            self.reset()

    def reset(self):
        for i in range(12):
            button = self.layout().itemAt(i).widget()
            button.setStyleSheet("background-color: #ffffff; border: 2px solid #d3d3d3")

    def setupGUI(self, n):
        grid = QtWidgets.QGridLayout()
        for i in range(n):
            for j in range(n):
                button = QtWidgets.QPushButton(" ")
                button.setFixedSize(100, 100)
                button.setStyleSheet("background-color: white; border: 2px solid #d3d3d3;")
                button.clicked.connect(self.buttonClicked)
                grid.addWidget(button, i, j)
        return grid

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
