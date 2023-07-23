from PyQt5 import QtWidgets, uic
import sys
import commpanel
import iopanel
import serial

#globalParentWindow=None


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()

        self.theCommPanel = commpanel.CommPanel()
        subWindow = self.mdiArea.addSubWindow(self.theCommPanel)
        subWindow.show()
        self.theCommPanel.parentWindow = self

        # self.theIOPanel = iopanel.IOPanel()
        # subWindow2 = self.mdiArea.addSubWindow(self.theIOPanel)
        # subWindow2.show()
        # self.theIOPanel.parentWindow = self


        #globalParentWindow=self


    def shutdownApp(self):
        print("shutting down")
        app.quit()

    def openIOPanel(self):
        print("opening IO Panel")
        self.theIOPanel = iopanel.IOPanel()
        subWindow = self.mdiArea.addSubWindow(self.theIOPanel)
        subWindow.show()
        self.theIOPanel.parentWindow = self

        #globalParentWindow=self

    def sendDataToIOPanel(self,theData):
        print("inserting")
        self.theIOPanel.textEdit_Incoming.insertPlainText(theData)

    def sendDataToSerial(self,whatToSend):
        print("main windows wants to send",whatToSend)
        self.theCommPanel.sendSerial(whatToSend+"\r")
        #self.sendDataToIOPanel(whatToSend+"\r")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
window.theCommPanel.stopSerialReaderThread()
print("i can exit now")
