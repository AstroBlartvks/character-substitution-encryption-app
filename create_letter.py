
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import sys
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        """
        Если хотите нарисовать для 
        пробела: space.png
        запятой: comma.png
        точки: dot.png
        двоеточия: double_dot.png
        тильды: tilda.png
        апострофа/одинарной кавычки: apos.png
        двойные кавыычки: ddapos.png
        восклицательный знак: scream.png
        вопросительный знак: quest.png
        тире: dash.png
        """

        title = "Для зарисовки символов"
        top = 200
        left = 200
        width = 400
        height = 500
 
        self.rus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
 
        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.setMinimumSize(width, height)

        self.comboBox_1 = QComboBox(self)
        self.comboBox_1.setGeometry(0, 20, width, 30)
        self.comboBox_1.setObjectName("comboBox_1")
        self.comboBox_1.addItems(["Русский", "Английский"])
        self.comboBox_1.setStyleSheet("font-size: 14pt;")

        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setGeometry(0, 50, width, 30)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(list(self.rus))
        self.comboBox_2.setStyleSheet("font-size: 14pt;")
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.comboBox_1.currentIndexChanged.connect(self.change_it)
 
        self.drawing = False
        self.brushSize = 15
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
 
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
 
        saveAction = QAction(QIcon("icons/save.png"), "Save",self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)
 
        clearAction = QAction(QIcon("icons/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
 
    def change_it(self):
        self.comboBox_2.clear()
        self.comboBox_2.addItems([list(self.rus), list(self.eng)][self.comboBox_1.currentIndex()])
 
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
 
    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
 
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
 
    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawImage(self.rect(),self.image, self.image.rect() )
 
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", f"{self.comboBox_2.currentText()}.png", "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
 
        if filePath == "":
            return
        self.image.save(filePath)
 
    def clear(self):
        self.image.fill(Qt.white)
        self.update()
 
    def threePixel(self):
        self.brushSize = 3
 
    def fivePixel(self):
        self.brushSize = 5
 
    def sevenPixel(self):
        self.brushSize = 7
 
    def ninePixel(self):
        self.brushSize = 9
 
    def blackColor(self):
        self.brushColor = Qt.black
 
    def whiteColor(self):
        self.brushColor = Qt.white
 
    def redColor(self):
        self.brushColor = Qt.red
 
    def greenColor(self):
        self.brushColor = Qt.green
 
    def yellowColor(self):
        self.brushColor = Qt.yellow
        
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
