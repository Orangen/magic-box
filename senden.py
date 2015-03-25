import time
import json
import binaryhelper
import ButtonListeners
import threading
from subprocess import Popen
from autobahn.twisted.websocket import WebSocketClientProtocol
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

# verbindungs protokoll zum server
class SendenClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        payload = {"name": "sendenBox", "group": "magic-box"}
        self.listener = ButtonListeners.ButtonListenerSenderThread(self)
        self.listener.start()


    def onMessage(self, payload, isBinary):
        # here be dragons
        pass

    def sendImage(self, fileName):
        print "Sending image", fileName
        payload = binaryhelper.file_to_json(fileName, {"group":"magic-box"})
        self.sendMessage(payload)



if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    
    #factory = WebSocketClientFactory("ws://127.0.0.1:9001", debug=False)
    factory = WebSocketClientFactory("ws://141.19.142.171:9001", debug=False)
    factory.protocol = SendenClientProtocol

    reactor.connectTCP("141.19.142.171", 9001, factory)
    reactor.run()
