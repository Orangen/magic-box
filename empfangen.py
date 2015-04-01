import time
import json
import binaryhelper
import ButtonListeners
import sys
from twisted.python import log
from twisted.internet import reactor
from subprocess import Popen
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory

# verbindungs protokoll zum server
class ReceiverClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        payload = {"name": "receiverBox", "group":"magic-box"}
        self.listener = ButtonListeners.ButtonListenerReceiverThread(self)
        self.listener.daemon = True;
        self.listener.start()
        self.sendMessage(json.dumps(payload))

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
        print "send icons", icon
        payload = {"icons": icon}    
        self.sendMessage(payload)


class Control():
    import RPi.GPIO as GPIO

    # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
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

    factory = WebSocketClientFactory("ws://109.239.57.147:9910", debug=True,debugCodePaths=True)
    factory.protocol = ReceiverClientProtocol 
    factory.setProtocolOptions(allowHixie76=True)

    reactor.connectTCP("109.239.57.147", 9910, factory)
    reactor.run()