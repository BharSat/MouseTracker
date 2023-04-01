from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys, time
from contour import *
import numpy as np

# sys.stdout = open("Out.txt", "at")
sys.stderr = sys.__stderr__ = sys.stdout
sys._excepthook = sys.excepthook


def exception_hook(*args):
    print(args)
    sys._excepthook(*args)
    sys.exit(1)


sys.excepthook = exception_hook


class Worker(QThread):
    progress = pyqtSignal(np.ndarray)
    tracker = None
    fpms=1
    playing = False
    def run(self):
        if self.tracker == None: self.tracker = Tracker("vid.mp4")
        self.tracker.tracking=True
        self.tracker.track(False, self.startCall, self.show_image, self.deleteLater)
    
    def show_image(self, im):
        if im is not None:
            self.progress.emit(im)
        return self.playing
    
    def startCall(self, fpms):
        self.fpms = fpms


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("main.ui", self)
        cw = self.centralwidget
        print("loaded ui")
        
        self.trackerThread = Worker()
        
        self.trackerThread.progress.connect(self.show_image)
        
        self.playButton.clicked.connect(self.play)
        
        self.show()
        self.trackerThread.start()
    
    @pyqtSlot(np.ndarray)
    def show_image(self, im):
        self.image = im
        self.image_ = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_Grayscale8)
        try:
            p = QPixmap.fromImage(self.image_)
            self.imageShow.setPixmap(p)
        except Exception as e:
            print(e)
    
    def play():
        self.playButton.setText("Pause")



app = QApplication(sys.argv)
window = UI()
app.exec_()