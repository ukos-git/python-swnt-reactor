#!/usr/bin/env python
import threading
import time

from MKDatabase import MKDatabase
from MKParser import MKParser
from MKLogFile import MKLogFileHandler
from MKSerial import MKSerial

class MKArduino():
    def __init__(self, port = '/dev/ttyACM0'):
        self.Serial = MKSerial('arduino', port, 9600)
        self.Parser = MKParser()
        self.Database = MKDatabase()
        self.newFile = True
        self.alive = False
        self.debug = False

    def startDebug(self):
        self.debug = True

    def start(self):
        try:
            self.Serial.start()
            self.thread = threading.Thread(target=self.loop)
            self.thread.daemon = True
            self.thread.start()
        except:
            self.stop()
            raise
        else:
            self.alive = True

    def stop(self):
        self.alive = False
        self.Serial.stop()

    def join(self):
        self.thread.join()

    def isAlive(self):
        return self.alive

    def loop(self):
        while self.isAlive():
            time.sleep(0.1)
            if self.Database.isReady():
                self.Serial.send(self.Database.getMessage())
            if self.Serial.isReady():
                self.Parser.input(self.Serial.getMessage())
                oneline = self.Parser.oneline()
                if self.debug:
                    print oneline
                if not self.Parser.isHeadline() and self.Parser.getStatus():
                    self.Database.setData(self.Parser.get(2), self.Parser.get(5), self.Parser.get(8), self.Parser.get(11))
                    self.Database.setSetpoint(self.Parser.get(3), self.Parser.get(6), self.Parser.get(9), self.Parser.get(12))
                if self.Database.isRecording():
                    if self.newFile:
                        self.Logfile = MKLogFileHandler('mkmain','log',True)
                        self.Logfile.open()
                        self.Database.setLogFile(self.Logfile.getLogFile())
                        self.newFile = False
                    self.Logfile.write(oneline)
                else:
                    self.newFile = True