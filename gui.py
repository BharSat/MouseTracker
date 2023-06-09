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
    fpms = 1
    playing = False

    def run(self):
        if self.tracker is None: self.tracker = Tracker("vid.mp4")
        self.tracker.tracking = False
        self.tracker.track(False, start_call=self.start_call, loop_call=self.show_image, end_call=self.deleteLater)

    def show_image(self, im):
        if im is not None:
            self.progress.emit(im)
        return self.playing

    def start_call(self, fpms):
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
        self.startTrackingButton.clicked.connect(self.start_tracking)
        self.pauseTrackingButton.clicked.connect(self.stop_tracking)
        self.pauseTrackingButton.setEnabled(False)
        self.trackingCorrectButton.setText("Select Path")
        self.trackingCorrectButton.setEnabled(False)

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

    def play(self):
        playing = self.trackerThread.playing = not self.trackerThread.playing
        if playing:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")

    def start_tracking(self):
        self.trackerThread.tracker.tracking = True
        self.startTrackingButton.setEnabled(False)
        self.pauseTrackingButton.setEnabled(True)
        self.trackingCorrectButton.setEnabled(True)

    def stop_tracking(self):
        self.trackerThread.tracker.tracking = False
        self.startTrackingButton.setEnabled(True)
        self.pauseTrackingButton.setEnabled(False)

    def select_path(self):
        pass


app = QApplication(sys.argv)
window = UI()
app.exec_()
