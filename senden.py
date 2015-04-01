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
        payload = {"name": "senderBox", "group":"magic-box"}
        self.listener = ButtonListeners.ButtonListenerSenderThread(self)
        self.listener.daemon = True;
        self.listener.start()
        self.sendMessage(json.dumps(payload))

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print "recive Icons"
            payload = binaryhelper.json_to_file(payload)
            self.listener.showIcons(payload)


    def sendImage(self, fileName):
        print "Sending image", fileName
        payload = binaryhelper.file_to_json(fileName, {})
        self.sendMessage(payload, isBinary = False)

if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://109.239.57.147:9910", debug=False,debugCodePaths=False)
    factory.protocol = SendenClientProtocol
    factory.setProtocolOptions(allowHixie76=True)

    reactor.connectTCP("109.239.57.147", 9910, factory)
    reactor.run()