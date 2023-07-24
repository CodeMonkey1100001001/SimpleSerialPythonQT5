import threading  # to debug segfaults
import time  # to debug segfaults

from PyQt5 import QtWidgets, uic

import serial.tools.list_ports
import serial

class CommPanel(QtWidgets.QMainWindow):
    def __init__(self):
        super(CommPanel, self).__init__()
        uic.loadUi("commpanel.ui", self)
        # instance variables
        self.serialPorts = None
        self.serialPortOpen = False
        self.genericSerialPort = None
        self.serialReaderThread = None
        self.serialReaderThreadNeeded = False
        self.serialReaderThreadRunning = False
        self.parentWindow = None

        self.incomingData = None

        self.serialQueue = None


        self.logToFile = False

        self.serialPorts = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(self.serialPorts):
            self.serialPorts.append(port)
            print("{}: {} [{}]".format(port, desc, hwid))
            self.comboBox_Ports.addItem(port + " - " + desc, port)
            self.comboBox_Ports.setCurrentIndex(0)

        self.serialReaderThreadNeeded = True
        self.serialReaderThread = threading.Thread(target=self.serial_reader_thread, args=())
        self.serialReaderThread.start();


    def stopSerialReaderThread(self):
        self.serialReaderThreadNeeded = False
        # self.stopSerialReaderThread()
        print("stopping serialReaderThread")
        while (self.serialReaderThreadRunning == True):
            print("waiting for comm port to finish")
            time.sleep(0.5)
            pass


    def OpenCommPort(self):
        currentIndex = self.comboBox_Ports.currentIndex()
        userData = self.comboBox_Ports.itemData(currentIndex)
        print("current Index=" + str(currentIndex))
        print("user Data=" + str(userData))
        if (self.serialPortOpen == True):
            self.genericSerialPort.close()
            self.pushButton_Connect.setText("Connect")
            self.serialPortOpen = False
        else:
            self.genericSerialPort = serial.Serial(userData, 115200, timeout=0)
            print(self.genericSerialPort)
            self.pushButton_Connect.setText("Disconnect")
            self.serialPortOpen = True
        self.parentWindow.openIOPanel()


    def sendSerial(self, theData):
        print("this should go into a queue")
        if (self.serialPortOpen == True):
            self.genericSerialPort.write(theData.encode())

    def serial_reader_thread(self):

        c = 0
        seq = []
        print("serial_reader_thread starting ================")
        while (self.serialReaderThreadNeeded == True):
            # thread.sleep(0.1)]
            time.sleep(0.0001)
            if (self.serialPortOpen == True):
                for c in self.genericSerialPort.read():
                    # print("chr="+chr(c))
                    seq.append(chr(c))  # convert from ANSII
                    joined_seq = ''.join(str(v) for v in seq)  # Make a string from array

                if chr(c) == '\n':
                    #print("Line " + str(count) + ': ' + joined_seq)
                    # strToHex(joined_seq)
                    tsSerialPortLine = joined_seq
                    tsSerialPortLineReady = True
                    joined_seq = ""
                    seq = []
                    c = 0
                    self.incomingData = tsSerialPortLine
                    #self.parentWindow.addToIncomingQueue(self.incomingData)
                    #SERIALQUEUE.put(self.incomingData)
                    try:
                        self.serialQueue.put_nowait(self.incomingData)
                    except:
                        print("queproblem)")
                    #print("incomingData",self.incomingData)

        print("Serial Reader thread terminating normally")
        self.serialReaderThreadRunning = False
