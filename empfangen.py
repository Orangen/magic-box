import time
import json
import binaryhelper
import ButtonListeners
import threading
import sys
import RPi.GPIO as GPIO
from subprocess import Popen
from twisted.python import log
from twisted.internet import reactor
from subprocess import Popen
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

# verbindungs protokoll zum server
class ReceiverClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        payload = {"name": "receiverBox", "group": "magic-box"}
        self.listener = ButtonListeners.ButtonListenerReceiverThread(self)
        self.listener.daemon = True;
        self.listener.start()

    def onMessage(self, payload, isBinary):
        print "onMessage"
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            json_dict = json.loads(payload)
            if json_dict.get("data",None) is not None:
                print "Received Data image"
                binaryhelper.dict_to_file(json_dict, "test.jpg")
                Control.printImage("image.jpg")

    def sendIcon(self, icon):
        print "send icons"
        self.sendMessage(icon)



class Control():

    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)
    # Pins auf Output setzen
    GPIO.setup(11, GPIO.OUT)


    def printImage(self, imageName):
        # Bild drucken
        Popen(["lp", imageName])
        print "Received Data image"
        time.sleep(0.1)
        # signalleuchte an
        GPIO.output(11, GPIO.HIGH) 




if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://109.239.57.147:9910", debug=True)
    factory.protocol = ReceiverClientProtocol

    reactor.connectTCP("109.239.57.147", 9910, factory)
    reactor.run()