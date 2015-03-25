import time
import json
import binaryhelper
import ButtonListeners
import threading
import sys
from twisted.python import log
from twisted.internet import reactor
from subprocess import Popen
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

# verbindungs protokoll zum server
class SendenClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        payload = {"name": "sendenBox", "group": "magic-box"}
        self.listener = ButtonListeners.ButtonListenerSenderThread(self)
        self.listener.daemon = True;
        self.listener.start()


    def onMessage(self, payload, isBinary):
        # here be dragons
        pass

    def sendImage(self, fileName):
        print "Sending image", fileName
        payload = binaryhelper.file_to_json(fileName, {"group":"magic-box"})
        self.sendMessage(payload)



if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://109.239.57.147:9910", debug=False)
    factory.protocol = SendenClientProtocol

    reactor.connectTCP("109.239.57.147", 9910, factory)
    reactor.run()