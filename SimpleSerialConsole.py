import queue
import threading
import time

from PyQt5 import QtWidgets, uic
import sys
import commpanel
import iopanel
from queue import Queue

# globalParentWindow=None
# I will be using the queue instead of QT Signals and Slots so that I can use it with other frameworks
SERIALQUEUE = Queue()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()
        self.theIOPanel = None
        self.theCommPanel = commpanel.CommPanel()
        subWindow = self.mdiArea.addSubWindow(self.theCommPanel)
        subWindow = self.mdiArea.addSubWindow(self.theCommPanel)
        subWindow.show()
        self.theCommPanel.parentWindow = self
        self.processQueue = True

        oneThing = "a test"
        SERIALQUEUE.put(oneThing)
        SERIALQUEUE.get()
        # just to make sure the queue is working

        self.processQueueThread = threading.Thread(target=self.processIncomingQueue_thread, args=())
        self.processQueueThread.start()

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
            # print("inserting",theData)
            self.theIOPanel.textEdit_Incoming.insertPlainText(theData)

    def sendDataToSerial(self, whatToSend):
        print("main windows wants to send", whatToSend)
        self.theCommPanel.sendSerial(whatToSend + "\r")
        # self.sendDataToIOPanel(whatToSend+"\r")

    def addToIncomingQueue(self, theData):
        SERIALQUEUE.put(theData)

    def processIncomingQueue_thread(self):
        while self.processQueue is True:
            try:
                item = SERIALQUEUE.get(timeout=0.5)
            except queue.Empty:
                pass
                # print('Consumer: gave up waiting...')
                continue
            print("item=["+str(item.rstrip())+"]")
            self.sendDataToIOPanel(item)

            time.sleep(0.0001)
        print("processIncomingQueue_thread ending normally")

    def closeEvent(self, event):
        self.shutdownApp()  # use this function to stop the threads before exiting.


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
window.theCommPanel.stopSerialReaderThread()
print("i can exit now")
