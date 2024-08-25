from PyQt5 import QtWidgets, QtCore
from form import Ui_MainWindow
from os import listdir
from os.path import isfile, join
import math
import os
import numpy
import cv2
import sys

SYSTEM = "Linux"

class EnCrypter(QtCore.QThread):
    updated = QtCore.pyqtSignal(int)
    running = False
    def __init__(self, *args, **kwargs):
        super(EnCrypter, self).__init__(*args, **kwargs)
        self.rus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.symbols = " .,?!:~0123456789"
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui
    
    def run(self):
        text = self.ui.plainTextEdit.toPlainText().upper()
        text = "_" + text + "_"
        text = text.replace("–", "-")

        type_encrypt = self.ui.comboBox.currentText()
        letters = []

        if type_encrypt == "Ничего":
            letters = list(text)
        elif type_encrypt == "Цезарь":
            key = self.ui.lineEdit.text()
            key_set = set(key)
            sum_errors = sum(list([0 if x in "0123456789" else 1 for x in key_set]))
            if sum_errors > 0: 
                return self.ui.plainTextEdit.setPlainText("Некорректный ключ!")
            key = int(key)
            for letter_id in range(len(text)):
                if text[letter_id] in self.rus:
                    letters.append(self.rus[(self.rus.index(text[letter_id]) + key) % len(self.rus)])
                elif text[letter_id] in self.eng:
                    letters.append(self.eng[(self.eng.index(text[letter_id]) + key) % len(self.eng)])
                elif text[letter_id] in self.symbols:
                    letters.append(self.symbols[(self.symbols.index(text[letter_id]) + key) % len(self.symbols)])
                else:
                    letters.append(text[letter_id])
        elif type_encrypt == "Вижинер":
            key = self.ui.lineEdit.text().upper()
            key_count = 0
            key_set = set(key)
            sum_errors = sum(list([0 if x in self.rus + self.eng else 1 for x in key_set]))
            if sum_errors > 0: 
                return self.ui.plainTextEdit.setPlainText("Некорректный ключ! Должен состоять из русского и английского алфавитов")
            for letter_id in range(len(text)):

                key_value = self.rus.index(key[key_count]) if key[key_count] in self.rus else self.eng.index(key[key_count])
                if text[letter_id] in self.rus:
                    letters.append(self.rus[(self.rus.index(text[letter_id]) + key_value) % len(self.rus)])
                elif text[letter_id] in self.eng:
                    letters.append(self.eng[(self.eng.index(text[letter_id]) + key_value) % len(self.eng)])
                elif text[letter_id] in self.symbols:
                    letters.append(self.symbols[(self.symbols.index(text[letter_id]) + key_value) % len(self.symbols)])
                else:
                    letters.append(text[letter_id])
                key_count = (key_count + 1) % len(key)
        elif type_encrypt == "XOR":
            key = self.ui.lineEdit.text()
            key_set = set(key)
            sum_errors = sum(list([0 if x in "0123456789" else 1 for x in key_set]))
            if sum_errors > 0: 
                return self.ui.plainTextEdit.setPlainText("Некорректный ключ!")
            key = int(key)
            for letter_id in range(len(text)):
                if text[letter_id] in self.rus:
                    letters.append(self.rus[(self.rus.index(text[letter_id]) ^ (key % len(self.rus))) % len(self.rus)])
                elif text[letter_id] in self.eng:
                    letters.append(self.eng[(self.eng.index(text[letter_id]) ^ (key % len(self.eng))) % len(self.eng)])
                elif text[letter_id] in self.symbols:
                    letters.append(self.symbols[(self.symbols.index(text[letter_id]) ^ (key % len(self.symbols))) % len(self.symbols)])
                else:
                    letters.append(text[letter_id])
        else:
            letters = list(text)
        

        self.updated.emit(0)
        
        wrap = self.ui.spinBox.value()
        string_wrap = wrap if wrap > 0 else len(letters)
        size_w = 40
        size_h = 50
        size_gap = 5
        break_start = cv2.imread("./alphabet/break.png", cv2.IMREAD_GRAYSCALE)
        break_start = cv2.resize(break_start, (size_w, size_h))
        size = math.ceil(len(letters) / string_wrap)

        vis = numpy.zeros((size_gap + size * (size_h + size_gap), (size_gap + size_w) * string_wrap + size_gap), numpy.float32)
        vis = numpy.where(vis == 0, 255.0, vis)

        files = self.load_letters(f"./alphabet/")

        for let_id in range(0, len(letters)):
            if letters[let_id] == "_":
                temp_let = break_start
            elif letters[let_id] == " ":
                temp_let = cv2.imread(f"./alphabet/space.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == ".":
                temp_let = cv2.imread(f"./alphabet/dot.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == ",":
                temp_let = cv2.imread(f"./alphabet/comma.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == ":":
                temp_let = cv2.imread(f"./alphabet/double_dot.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == "\'":
                temp_let = cv2.imread(f"./alphabet/apos.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == "~":
                temp_let = cv2.imread(f"./alphabet/tilda.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == "!":
                temp_let = cv2.imread(f"./alphabet/scream.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == "?":
                temp_let = cv2.imread(f"./alphabet/quest.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == "\"":
                temp_let = cv2.imread(f"./alphabet/ddapos.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif letters[let_id] == "-":
                temp_let = cv2.imread(f"./alphabet/dash.png", cv2.IMREAD_GRAYSCALE)
                temp_let = cv2.resize(temp_let, (size_w, size_h))
            elif os.path.exists(f"./alphabet/{letters[let_id]}.png"):
                temp_let = files[letters[let_id]]
            else:
                temp_let = break_start
            new_y1 = size_gap + let_id//string_wrap * size_h
            new_y2 = (let_id//string_wrap + 1) * size_h + size_gap
            new_x1 = size_gap + (let_id % string_wrap)*(size_w+size_gap)
            new_x2 = (let_id % string_wrap + 1)*(size_w+size_gap)
            vis[new_y1:new_y2, new_x1:new_x2] = temp_let
            self.updated.emit(int(100*let_id/len(letters)))
        cv2.imwrite("result.png", vis)
        self.updated.emit(100)

    def load_letters(self, path):
        size_w = 40
        size_h = 50

        files = list([f for f in listdir(path) if isfile(join(path, f))])
        break_png = cv2.imread(f"./alphabet/break.png", cv2.IMREAD_GRAYSCALE)
        break_png = cv2.resize(break_png, (size_w, size_h))
        img_to_str = {"_": break_png}

        for f in files:
            with open(f"./alphabet/{f}", "rb") as File:
                png_chunk = File.read()
                png_chunk = numpy.frombuffer(png_chunk, dtype=numpy.uint8)
            letter = cv2.imdecode(png_chunk, cv2.IMREAD_GRAYSCALE)
            letter = cv2.resize(letter, (size_w, size_h))
            img_to_str[f.split(".")[0]] = letter

        return img_to_str
    

class DeCrypter(QtCore.QThread):
    updated = QtCore.pyqtSignal(int)
    running = False

    def __init__(self, *args, **kwargs):
        super(DeCrypter, self).__init__(*args, **kwargs)
        self.rus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.symbols = " .,?!:~0123456789"
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def set_win(self, win):
        self.win = win

    def run(self):
        size_w = 40
        size_h = 50
        size_gap = 5

        file_to_img = self.load_letters(f"./alphabet/")

        if SYSTEM == "WINDOWS":
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.win, 'Load the picture', r"", "")
        else:
            file_name = "result.png"

        image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
        (width, height) = image.shape
        string_wrap = (width - size_gap) // (size_h + size_gap)
        size_letter = (height - size_gap) // (size_gap + size_w)
        result = string_wrap * size_letter
        index_ = 0
        string = ""
        self.updated.emit(0)

        for y in range(string_wrap):
            for x in range(size_letter):
                new_y1 = size_gap + y * size_h
                new_y2 = (y + 1) * size_h + size_gap
                new_x1 = size_gap + x*(size_w+size_gap)
                new_x2 = (x + 1)*(size_w+size_gap)
                img = image[new_y1:new_y2, new_x1:new_x2]
                symbol = [0, "_"]
                add_is = True

                for fname in file_to_img:

                    if numpy.sum(img) == 50*40*255:
                        add_is = False
                        break 

                    number_of_equal_elements = numpy.sum(file_to_img[fname]==img)
                    total_elements = numpy.multiply(*img.shape)
                    percentage = number_of_equal_elements/total_elements
                    
                    if percentage > symbol[0]:
                        symbol[0] = percentage
                        if fname == "space":
                            symbol[1] = " "
                        elif fname == "dot":
                            symbol[1] = "."
                        elif fname == "comma":
                            symbol[1] = ","
                        elif fname == "double_dot":
                            symbol[1] = ":"
                        elif fname == "tilda":
                            symbol[1] = "~"
                        elif fname == "apos":
                            symbol[1] = "\'"
                        elif fname == "quest":
                            symbol[1] = "?"
                        elif fname == "scream":
                            symbol[1] = "!"
                        elif fname == "ddapos":
                            symbol[1] = "\""
                        elif fname == "dash":
                            symbol[1] = "-"
                        else:
                            symbol[1] = fname
                    
                if add_is:
                    string += symbol[1]
                self.updated.emit(int(100*index_/result))
                index_ += 1

        type_encrypt = self.ui.comboBox.currentText()
        letters = []
        
        if type_encrypt == "Ничего":
            letters = list(string)
        elif type_encrypt == "Цезарь":
            key = self.ui.lineEdit.text()
            key_set = set(key)
            sum_errors = sum(list([0 if x in "0123456789" else 1 for x in key_set]))
            if sum_errors > 0: 
                return self.ui.plainTextEdit.setPlainText("Некорректный ключ!")
            key = int(key)
            for letter_id in range(len(string)):
                if string[letter_id] in self.rus:
                    letters.append(self.rus[(self.rus.index(string[letter_id]) - key) % len(self.rus)])
                elif string[letter_id] in self.eng:
                    letters.append(self.eng[(self.eng.index(string[letter_id]) - key) % len(self.eng)])
                elif string[letter_id] in self.symbols:
                    letters.append(self.symbols[(self.symbols.index(string[letter_id]) - key) % len(self.symbols)])
                else:
                    letters.append(string[letter_id])
        elif type_encrypt == "Вижинер":
            key = self.ui.lineEdit.text().upper()
            key_count = 0
            key_set = set(key)
            sum_errors = sum(list([0 if x in self.rus + self.eng else 1 for x in key_set]))
            if sum_errors > 0: 
                return self.ui.plainTextEdit.setPlainText("Некорректный ключ! Должен состоять из русского и английского алфавитов")
            for letter_id in range(len(string)):

                key_value = self.rus.index(key[key_count]) if key[key_count] in self.rus else self.eng.index(key[key_count])
                if string[letter_id] in self.rus:
                    letters.append(self.rus[(self.rus.index(string[letter_id]) - key_value) % len(self.rus)])
                elif string[letter_id] in self.eng:
                    letters.append(self.eng[(self.eng.index(string[letter_id]) - key_value) % len(self.eng)])
                elif string[letter_id] in self.symbols:
                    letters.append(self.symbols[(self.symbols.index(string[letter_id]) - key_value) % len(self.symbols)])
                else:
                    letters.append(string[letter_id])
                key_count = (key_count + 1) % len(key)
        elif type_encrypt == "XOR":
            key = self.ui.lineEdit.text()
            key_set = set(key)
            sum_errors = sum(list([0 if x in "0123456789" else 1 for x in key_set]))
            if sum_errors > 0: 
                return self.ui.plainTextEdit.setPlainText("Некорректный ключ!")
            key = int(key)
            for letter_id in range(len(string)):
                if string[letter_id] in self.rus:
                    letters.append(self.rus[(self.rus.index(string[letter_id]) ^ (key % len(self.rus))) % len(self.rus)])
                elif string[letter_id] in self.eng:
                    letters.append(self.eng[(self.eng.index(string[letter_id]) ^ (key % len(self.eng))) % len(self.eng)])
                elif string[letter_id] in self.symbols:
                    letters.append(self.symbols[(self.symbols.index(string[letter_id]) ^ (key % len(self.symbols))) % len(self.symbols)])
                else:
                    letters.append(string[letter_id])
        else:
            letters = list(string)
        
        string = "".join(letters)

        self.ui.plainTextEdit_2.setPlainText(string.replace("_", "▮"))
        self.updated.emit(100)

    def load_letters(self, path):
        size_w = 40
        size_h = 50

        files = list([f for f in listdir(path) if isfile(join(path, f))])
        break_png = cv2.imread(f"./alphabet/break.png", cv2.IMREAD_GRAYSCALE)
        break_png = cv2.resize(break_png, (size_w, size_h))
        img_to_str = {"_": break_png}

        for f in files:
            with open(f"./alphabet/{f}", "rb") as File:
                png_chunk = File.read()
                png_chunk = numpy.frombuffer(png_chunk, dtype=numpy.uint8)
            letter = cv2.imdecode(png_chunk, cv2.IMREAD_GRAYSCALE)
            letter = cv2.resize(letter, (size_w, size_h))
            img_to_str[f.split(".")[0]] = letter

        return img_to_str

 
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.rus = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.eng = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        self.ui.comboBox_3.addItems(list(self.rus+self.eng+" 0123456789"))
        
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_6.clicked.connect(self.encrypt)
        self.ui.pushButton_5.clicked.connect(self.decrypt)
    
    def on_update(self, data):
        self.ui.progressBar.setValue(data)

    def encrypt(self):
        self.encrypt_task = EnCrypter(self)
        self.encrypt_task.set_ui(self.ui)
        self.encrypt_task.updated.connect(self.on_update)
        self.encrypt_task.start()
    
    def decrypt(self):
        self.decrypt_task = DeCrypter(self)
        self.decrypt_task.set_ui(self.ui)
        self.decrypt_task.set_win(self)
        self.decrypt_task.updated.connect(self.on_update)
        self.decrypt_task.start()



app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())
