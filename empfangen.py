import time
import json
import binaryhelper
import ButtonListeners
import sys
from subprocess import Popen
from twisted.python import log
from twisted.internet import reactor
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
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print "recive Image"
            binaryhelper.json_to_file(payload)
            print "Print image"
            Popen(["lp", "image.jpg"])
            self.listener.showLight()

    def sendIcon(self, icon):
        print "send icon: ", icon
        payload = {"icons": icon}
        self.sendMessage(json.dumps(payload))


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://109.239.57.147:9910", debug=False,debugCodePaths=False)
    factory.protocol = ReceiverClientProtocol 
    factory.setProtocolOptions(allowHixie76=True)

    reactor.connectTCP("109.239.57.147", 9910, factory)
    reactor.run()