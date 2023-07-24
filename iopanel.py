from PyQt5 import QtWidgets, uic

class IOPanel(QtWidgets.QMainWindow):

    def __init__(self):
        super(IOPanel, self).__init__()
        uic.loadUi("iopanel.ui", self)
        # instance variables
        self.serialPorts = None
        self.serialPortOpen = False
        self.tsSerialPort = None
        self.serialReaderThread = None
        self.serialReaderThreadNeeded = False
        self.serialReaderThreadRunning = False
        self.parentWindow = None

    def sendLine(self):
        print("sending one line")
        whatToSend = self.lineEdit_WTS.text() # self.line.text()
        print("what to send",whatToSend)
        self.parentWindow.sendDataToSerial(whatToSend)

    def UpdateTextArea(self,whatToAdd):
        print("whatToAdd",whatToAdd)
        # self.theIOPanel.textEdit_Incoming.insertPlainText(theData)
        self.textEdit_Incoming.insertPlainText(whatToAdd)