import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui,QtCore
import keyboard
import random


class Trans(QWidget):
    closeCutScreenSignal = pyqtSignal()
    def __init__(self):
        super(Trans, self).__init__()
        self.cutPic = False
        self.screen = QApplication.primaryScreen()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        # pal = QPalette()
        # pal.setBrush(QPalette.Highlight, QBrush(QtCore.Qt.green))
        # self.rubberBand.setPalette(pal)

 #       button = QPushButton('Close', self)
 #       self.initUI()

#    def initUI(self):
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
  #      self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
 #       self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


    def cutP(self):
        self.rubberBand.close()
        self.cutPic = True
        self.setCursor(QtCore.Qt.CrossCursor)

    def mousePressEvent(self, event):
        if self.cutPic == True:
            self.old = event.globalPos()
            self.old.x, self.old.y = self.old.x(), self.old.y()
        else:
            self.rubberBand.close()
            self.closeCutScreenSignal.emit()

    def mouseMoveEvent(self, event):
        if self.cutPic == True:
            self.new = event.globalPos()
            self.new.x, self.new.y = self.new.x(), self.new.y()
            self.rect = QtCore.QRect(QPoint(self.old.x, self.old.y), QPoint(self.new.x, self.new.y))
            self.rubberBand.setGeometry(self.rect)
            self.rubberBand.show()

    def mouseReleaseEvent(self, event):
        if self.cutPic == True:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.new = event.globalPos()
            self.new.x, self.new.y = self.new.x(), self.new.y()
            self.cutPic = False
            self.rect = QtCore.QRect(QPoint(self.old.x, self.old.y), QPoint(self.new.x, self.new.y))
            self.setWindowOpacity(0.01)
            self.screenshot = self.screen.grabWindow(QApplication.desktop().winId(), self.rect.x(), self.rect.y(),
                                                     self.rect.width(), self.rect.height())
            self.setWindowOpacity(0.3)
            self.rubberBand.setGeometry(self.rect)
            self.rubberBand.show()
            # save
            dt = 'pic'
            while 1:
                n = random.randint(0, 10)
                dt += str(n)
                if n == 5:
                    break
            self.screenshot.save('cut' + str(dt) + '.png', 'png')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = Trans()
    trans.showFullScreen()
    trans.setWindowOpacity(0.3)
    trans.raise_()
    trans.show()
    sys.exit(app.exec_())