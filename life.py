import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GameScene(QGraphicsScene):
    def __init__(self):
        QObject.__init__(self)

        # Create instance of GameField and QTimer objects
        self.gameField = GameField()
        self.timer = QTimer()

        # Connect timer ticking to a slot
        self.timer.timeout.connect(self.timerTick)

        # Create a two-dimensional 150000 unit graphic item array corresponding
        # each cell
        self.cellIcons = [[QGraphicsRectItem()] * 100 for i in range(150)]

        # Set background as grey and apply over it a light gray rectangle
        self.setBackgroundBrush(Qt.gray)
        self.addRect(0, 0, 600, 400, QPen(Qt.black), QBrush(Qt.lightGray))

        # Default cell width
        self.cW = 4
        # Default cell height
        self.cH = 4

        # Fill all graphical data for each cell to the two-dimensional array
        for x in range(150):
            for y in range(100):
                icon = QGraphicsRectItem()
                icon.setRect(x * self.cW, y * self.cH, self.cW, self.cH)
                icon.setPen(QPen(Qt.black))
                icon.setBrush(QBrush(Qt.darkGray))
                icon.setVisible(False)
                self.cellIcons[x][y] = icon
                self.addItem(self.cellIcons[x][y])

        print("Scene created")

    def mousePressEvent(self, event):
        # Mouse coordinates have to be divided with cell width and height in
        # order to get them correctly
        x = int(event.lastScenePos().x() / self.cW)
        y = int(event.lastScenePos().y() / self.cH)

        # Check if mouse coordinates are out of bounds
        if (x > 0 and x < 149 and y > 0 and y < 99):
            # Check if the cell is alive
            if (self.gameField.isAliveAt(x, y) == False):
                # Set cell icon alive & visible
                self.setVisible(x, y, True)
                self.gameField.cells[x][y] = True
                print(f"Cell X: {x}, Y: {y}, Z: 1")
            else:
                # Set cell icon dead & hidden
                self.setVisible(x, y, False)
                self.gameField.cells[x][y] = False
                print(f"Cell X: {x}, Y: {y}, Z: 0")

    def mouseMoveEvent(self, event):
        # See event mousePressEvent. This event applies while mouse is moving

        x = int(event.lastScenePos().x() / self.cW)
        y = int(event.lastScenePos().y() / self.cH)

        if (x > 0 and x < 149 and y > 0 and y < 99):
            if (self.gameField.isAliveAt(x, y) == False):
                self.setVisible(x, y, True)
                self.gameField.cells[x][y] = True
                print(f"Cell X: {x}, Y: {y}, Z: 1")

    def setVisible(self, x, y, visible):
        self.cellIcons[x][y].setVisible(visible)

    def timerTick(self):
        # This method is called when the timer "ticks"

        # Call for method calculating live and dead cells
        self.gameField.calculateCells()

        # "Drawing" all the dead and alive cells corrensponding each coordinate
        for x in range(150):
            for y in range(100):
                if (self.gameField.isAliveAt(x, y)):
                    self.setVisible(x, y, True)
                else:
                    self.setVisible(x, y, False)

    def clearScene(self):
        # Set all alive cells dead
        for x in range(150):
            for y in range(100):
                self.setVisible(x, y, False)

        # Clear the alive cells from the array containing states for each cell
        self.gameField.cells = [[False] * 100 for i in range(150)]
        print("Scene cleared")


class GameField:
    def __init__(self):
        print("Field created")

        # Create two two-dimensional arrays for the current cells and the cells
        # which are about to come alive
        self.cells = [[False] * 100 for i in range(150)]

        # A "glider" For testing purposes
        '''
        self.cells[50][50] = True
        self.cells[51][50] = True
        self.cells[51][48] = True
        self.cells[52][49] = True
        self.cells[52][50] = True
        '''

    def isAliveAt(self, x, y):
        return self.cells[x][y] == True

    def calculateCells(self):
        # This method contains all the actual game logic
        neighbours = 0

        newCells = [[False] * 100 for i in range(150)]

        for x in range(149):
            for y in range(99):

                ''' Check if the cell is alive and then
                    check the count of neighbour of each cell
                    _______________________
                    |x-1,y+1|x,y+1|x+1,y+1|
                    |_______|_____|_______|
                    |x-1,y  |x,y  |x+1,y  |
                    |_______|_____|_______|
                    |x-1,y-1|x,y-1|x+1,y-1|
                    |_______|_____|_______|
                '''

                # Set the count of neighbours of each cell as zero at start
                neighbours = 0

                if (x > 0 and y > 0):

                    if (self.cells[x - 1][y - 1] == True):
                        neighbours += 1
                    if (self.cells[x - 1][y] == True):
                        neighbours += 1
                    if (self.cells[x - 1][y + 1] == True):
                        neighbours += 1

                    if (self.cells[x][y - 1] == True):
                        neighbours += 1
                    if (self.cells[x][y + 1] == True):
                        neighbours += 1
                    if (self.cells[x + 1][y - 1] == True):
                        neighbours += 1

                if (self.cells[x + 1][y] == True):
                    neighbours += 1
                if (self.cells[x + 1][y + 1] == True):
                    neighbours += 1

                # If the count of cells neigbours is less than two,
                # mark the cell as dead due to underpopulation
                if (neighbours < 2):
                    newCells[x][y] = False
                    continue

                # If cell has more than three neigbours, mark the cell
                # as dead due to overpopulation
                if (neighbours > 3):
                    newCells[x][y] = False
                    continue

                # If the cell is alive and it has two or three neighbours keep
                # the cell alive
                if ((neighbours == 2 or neighbours == 3) and
                        self.cells[x][y] == True):
                    newCells[x][y] = True
                    continue

                # If the cell is dead and it has three neighbours mark
                # the cell alive
                if (neighbours == 3 and self.cells[x][y] == False):
                    newCells[x][y] = True
                    continue

        # Set the newborn and killed cells to the array
        # containing the cells for the game logic
        self.cells = newCells


class LifeWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Set the LifeWindow widget to the middle of the screen and set default
        # width and height
        self.setGeometry(
            QApplication.desktop().width() / 2,
            QApplication.desktop().height() / 2,
            655,
            525)

        # Add title
        self.setWindowTitle("PyQt Conway's Game of Life (c) visuve 2011")

        self.graphicsView = QGraphicsView()

        # Create pushbuttons
        self.pushButtonStart = QPushButton("Start", self)
        self.pushButtonPause = QPushButton("Pause", self)
        self.pushButtonNew = QPushButton("New", self)

        # Enable and disable the pushbuttons suitable for the situation
        self.pushButtonStart.setEnabled(True)
        self.pushButtonPause.setDisabled(True)
        self.pushButtonNew.setDisabled(True)

        # Connect pushbutton clicks to their slots
        self.pushButtonStart.clicked.connect(self.pushButtonStart_clicked)
        self.pushButtonPause.clicked.connect(self.pushButtonPause_clicked)
        self.pushButtonNew.clicked.connect(self.pushButtonNew_clicked)

        # Create a gridlaoyt for the pushbuttons and the graphicsview
        gridLayout = QGridLayout(self)
        gridLayout.addWidget(self.graphicsView, 0, 0, 1, 3, Qt.Alignment(0))
        gridLayout.addWidget(self.pushButtonStart, 1, 0)
        gridLayout.addWidget(self.pushButtonPause, 1, 1)
        gridLayout.addWidget(self.pushButtonNew, 1, 2)

        # Create an instance of graphicsscene object called gamescene and set
        # it as the
        # current scene of the graphicsview
        self.gameScene = GameScene()
        self.graphicsView.setScene(self.gameScene)

        # Enable graphicsview antialiasing and disable scrollbars
        self.graphicsView.setRenderHints(QPainter.Antialiasing)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        print("Window created")

    def resizeEvent(self, event):
        # Allways upon user resizing the window the aspect ratio is kept at 3:2
        self.graphicsView.fitInView(0, 0, 600, 400, Qt.KeepAspectRatio)

    def pushButtonStart_clicked(self):
        # Start the graphicsscenes own timer and start the whole game and its
        # logic
        self.gameScene.timer.start(50)
        print("Timer started")

        self.pushButtonStart.setDisabled(True)
        self.pushButtonPause.setEnabled(True)
        self.pushButtonNew.setDisabled(True)

    def pushButtonPause_clicked(self):
        # Stop the graphicsscenes own timer to "pause" the game
        self.gameScene.timer.stop()
        print("Timer stopped")

        self.pushButtonStart.setEnabled(True)
        self.pushButtonPause.setDisabled(True)
        self.pushButtonNew.setEnabled(True)

    def pushButtonNew_clicked(self):
        # Stop the timer and call the graphicsscenes method clearScene for a
        # new start
        self.gameScene.timer.stop()
        self.gameScene.clearScene()
        print("New scene created")

        self.pushButtonStart.setEnabled(True)
        self.pushButtonPause.setDisabled(True)
        self.pushButtonNew.setEnabled(True)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    application_window = LifeWindow()
    application_window.show()
    application_window.resizeEvent(None)
    application.exec_()