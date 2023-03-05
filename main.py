#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton, QMessageBox, QGroupBox, QHBoxLayout, QButtonGroup, QLineEdit, QListWidget, QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance

app = QApplication([])

main_win = QWidget()

main_win.setWindowTitle('')
main_win.resize(600, 400)

Button1 = QPushButton('Папка')
Button2 = QPushButton('Лево')
Button3 = QPushButton('Право')
Button4 = QPushButton('Зеркало')
Button5 = QPushButton('Резкость')
Button6 = QPushButton('Ч/Б')
Button7 = QPushButton('Размытие')

ListPictures = QListWidget()

kartinka = QLabel('картинка')

H1 = QHBoxLayout()
H2 = QHBoxLayout()
V1 = QVBoxLayout()
V2 = QVBoxLayout()

V1.addWidget(Button1 )
V1.addWidget(ListPictures)
H1.addLayout(V1)

H1.addLayout(V2)

V2.addWidget(kartinka)

H2.addWidget(Button2)
H2.addWidget(Button3)
H2.addWidget(Button4)
H2.addWidget(Button5)
H2.addWidget(Button6)
H2.addWidget(Button7)
V2.addLayout(H2)

workdir = ''

def filter(files, extensions):
    result = []
    for i in files:
        for y in extensions:
            if i.endswith(y):
                result.append(i)
    return result
def show_Filename_list():
    extensions = ['jpg','png','bmp']
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    files = filter(os.listdir(workdir),extensions)
    ListPictures.clear()
    for i in files:
        ListPictures.addItem(i)


class Image_Processor():
    def __init__(self):
        self.image = None 
        self.filename = None
        self.save_dir = 'Mod/'
    def Load_Image(self,filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)
    def Show_Image(self,path):
        kartinka.hide()
        pixmapimage = QPixmap(path)
        w,h = kartinka.width(), kartinka.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kartinka.setPixmap(pixmapimage)
        kartinka.show()
    def do_bw(self):
        self.image=self.image.convert("L")
        self.save_Image()
        path=os.path.join(workdir,self.save_dir, self.filename)
        self.Show_Image(path)
    def do_left(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.save_Image()
        path=os.path.join(workdir,self.save_dir, self.filename)
        self.Show_Image(path)
    def do_right(self):
        self.image=self.image.transpose(Image.ROTATE_270)
        self.save_Image()
        path=os.path.join(workdir,self.save_dir, self.filename)
        self.Show_Image(path)
    def do_mirror(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_Image()
        path=os.path.join(workdir,self.save_dir, self.filename)
        self.Show_Image(path)
    def do_rezkostb(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image=self.image.enhance(1.5)
        self.save_Image()
        path=os.path.join(workdir,self.save_dir, self.filename)
        self.Show_Image(path)
    def do_blur(self):
        self.image=self.image.filter(ImageFilter.BLUR)
        self.save_Image()
        path=os.path.join(workdir,self.save_dir, self.filename)
        self.Show_Image(path)
    def save_Image(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        


def ShowChosenImage():
        if ListPictures.currentRow() >= 0:
            filename = ListPictures.currentItem().text()
            workimage.Load_Image(filename)
            image_path = os.path.join(workdir,workimage.filename)
            workimage.Show_Image(image_path)


workimage = Image_Processor()

Button6.clicked.connect(workimage.do_bw)
Button2.clicked.connect(workimage.do_left)
Button3.clicked.connect(workimage.do_right)
Button4.clicked.connect(workimage.do_mirror)
Button5.clicked.connect(workimage.do_rezkostb)
Button7.clicked.connect(workimage.do_blur)
Button1.clicked.connect(show_Filename_list)
ListPictures.currentRowChanged.connect(ShowChosenImage)

main_win.setLayout(H1)
main_win.show()
app.exec_()