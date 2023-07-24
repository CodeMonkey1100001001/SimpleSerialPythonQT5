import faulthandler

from PyQt5.QtCore import QTimer

faulthandler.enable()

import queue
import threading
import time

from PyQt5 import QtWidgets, uic, QtCore
import sys
import commpanel
import iopanel
from queue import Queue

# globalParentWindow=None
# I will be using the queue instead of QT Signals and Slots so that I can use it with other frameworks
#SERIALQUEUE = Queue(maxsize=100)
SERIALQUEUE = queue.SimpleQueue()

stringToAdd = "test"

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()
        self.theIOPanel = None
        self.theCommPanel = commpanel.CommPanel()
        #subWindow = self.mdiArea.addSubWindow(self.theCommPanel)
        subWindow = self.mdiArea.addSubWindow(self.theCommPanel)
        subWindow.show()
        self.theCommPanel.parentWindow = self
        self.theCommPanel.serialQueue = SERIALQUEUE
        self.processQueue = True

#        oneThing = "a test"
#        SERIALQUEUE.put(oneThing)
#        SERIALQUEUE.get()
        # just to make sure the queue is working

        #self.processQueueThread = threading.Thread(target=self.processIncomingQueue_thread, args=())
        #self.processQueueThread.start()

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.mainTick)
        self.timer.start()

    def mainTick(self):
        #print("mainTick")
        self.processIncomingQueue()

    def shutdownApp(self):
        print("shutting down")
        self.processQueue = False
        print("close the processQueue thread")
        self.theCommPanel.stopSerialReaderThread()
        print("close the serial reader")
        print("main window close")
        # # do stuff
        # if can_exit:
        #     print("can_exit")
        #     event.accept()  # let the window close
        # else:
        #     print("Cannot exit")
        #     event.ignore()

        app.quit()

    def openIOPanel(self):
        print("opening IO Panel")
        self.theIOPanel = iopanel.IOPanel()
        subWindow = self.mdiArea.addSubWindow(self.theIOPanel)
        subWindow.show()
        self.theIOPanel.parentWindow = self

    def sendDataToIOPanel(self, theData):
        if (self.theIOPanel is not None):
            print("inserting",theData)
            #self.theIOPanel.textEdit_Incoming.insertPlainText(theData)
            self.theIOPanel.UpdateTextArea(theData)

    def sendDataToSerial(self, whatToSend):
        print("main windows wants to send", whatToSend)
        self.theCommPanel.sendSerial(whatToSend + "\r")
        # self.sendDataToIOPanel(whatToSend+"\r")

    def addToIncomingQueue(self, theData):
        SERIALQUEUE.put(theData)
    # item = q.get()
    # do_work(item)
    # q.task_done()
    def processIncomingQueue(self):
        if SERIALQUEUE.empty():
            pass
        else:
            try:
                item = SERIALQUEUE.get_nowait()
            except queue.Empty:
                pass
                print('Consumer: gave up waiting...')
            # SERIALQUEUE.task_done()
            print("item=["+str(item.rstrip())+"]")
            stringToAdd = item
            self.sendDataToIOPanel(stringToAdd)
            #SERIALQUEUE.task_done()
        #print("processIncomingQueue_thread ending normally")

    def closeEvent(self, event):
        self.shutdownApp()  # use this function to stop the threads before exiting.


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
window.theCommPanel.stopSerialReaderThread()
print("i can exit now")
