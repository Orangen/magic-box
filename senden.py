import time
import json
import binaryhelper
import ButtonListeners
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientFactory

# verbindungs protokoll zum server
class SendenClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        payload = {"name": "receiverBox", "group":"magic-box"}
        self.listener = ButtonListeners.ButtonListenerSenderThread(self)
        self.listener.daemon = True;
        self.listener.start()
        self.sendMessage(json.dumps(payload))

    def onMessage(self, payload, isBinary):
        print "Received Data"
        json_dict = json.loads(payload)    
        if json_dict.get("icons",None) is not None:
            print "Received Data icons"
            showIcons(json_dict.get("icons",None))


    def sendImage(self, fileName):
        print "Sending image", fileName
        payload = binaryhelper.file_to_json(fileName, {})
        self.sendMessage(payload, isBinary = False)


class Control():
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)

    def showIcons(self, icons):
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)

        # XD LED an
        if json_dict.get("icons",None) is "grinsSmilie":
            GPIO.output(16, GPIO.HIGH)
        # Herz LED an
        if json_dict.get("icons",None) is "herz":
            GPIO.output(18, GPIO.HIGH)
        # Stern LED an
        if json_dict.get("icons",None) is "stern":
            GPIO.output(19, GPIO.HIGH)
        # Tele LED an
        if json_dict.get("icons",None) is "tele":
            GPIO.output(21, GPIO.HIGH)
        # :) LED an
        if json_dict.get("icons",None) is "Smilie":
            GPIO.output(22, GPIO.HIGH)


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://109.239.57.147:9910", debug=True,debugCodePaths=True)
    factory.protocol = SendenClientProtocol
    factory.setProtocolOptions(allowHixie76=True)

    reactor.connectTCP("109.239.57.147", 9910, factory)
    reactor.run()