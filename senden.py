import time
import json
import binaryhelper
# import RPi.GPIO as GPIO
from subprocess import Popen
from autobahn.twisted.websocket import WebSocketClientProtocol
import threading
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class SendenClientProtocol(WebSocketClientProtocol):

    def onOpen(self):
        payload = {"name": "sendenBox", "group": "magic-box"}
        self.sendMessage(json.dumps(payload).encode("utf8"))
        self.sendImage("image.jpg")

    def onMessage(self, payload, isBinary):
        # here be dragons
        pass

    def sendImage(self, fileName):
        payload = binaryhelper.file_to_json(fileName, {"group":"magic-box"})
        self.sendMessage(payload)
        self.sendClose()



if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(
        "ws://127.0.0.1:9001", debug=False)
    factory.protocol = SendenClientProtocol

    reactor.connectTCP("127.0.0.1", 9001, factory)
    reactor.run()
