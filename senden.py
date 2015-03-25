import time
import json
import binaryhelper
import threading
import RPi.GPIO as GPIO
from subprocess import Popen
from autobahn.twisted.websocket import WebSocketClientProtocol

class SendenClientProtocol(WebSocketClientProtocol):

  def onOpen(self):
    payload = { "name": "sendenBox", "group":"magic-box"}
    self.sendMessage(json.dumps(payload).encode("utf8"))
    
  def onMessage(self, payload, isBinary):
    # here be dragons
    pass

  def sendImage(fileName):
    payload = binaryhelper.file_to_json(fileName)
    self.sendMessage(payload)


class ButtonListenerThread(threading.Thread):
  # RPi.GPIO Layout verwenden (wie Pin-Nummern)
  
  def run():
    GPIO.setmode(GPIO.BOARD)

    # Pin 18 (GPIO 24) auf Input setzen
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Pins auf Output setzen
    GPIO.setup(23, GPIO.OUT) # Beleuchtung Foto
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    imageName = "imag.jpg"
    prev_input = 0

    # Dauersschleife
    while True:
      
      input = GPIO.input(11)
      data = False
      # bedinung fuer die LEDs
      if data:
        # Smilie LED an
        if data == 1:
          GPIO.output(18, GPIO.HIGH)
        # LED
        if data == 2:
          GPIO.output(19, GPIO.HIGH)
        # LED
        if data == 3:
          GPIO.output(21, GPIO.HIGH)
        # LED
        if data == 4:
          GPIO.output(22, GPIO.HIGH)
      
      
      # bedingung Foto (button 11)
      if ((not prev_input) and input):
        
        # Beleuchtung anschalten
        GPIO.output(23, GPIO.HIGH)
        # Bild machen
        Popen(["fswebcam","--save",imageName])
        # Bild zu json
        image = file_to_json(imageName, "utf-8")
        # Bild senden
        sock.sendall(image)
        
        GPIO.output(18, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
     
      prev_input = input
      time.sleep(0.05)
      
      #beleuchtung aus schalten
      GPIO.output(23, GPIO.LOW)

if __name__ == '__main__':
  import sys

  from twisted.python import log
  from twisted.internet import reactor
  
  log.startLogging(sys.stdout)

  from autobahn.twisted.websocket import WebSocketServerFactory, connectWS
  factory = WebSocketServerFactory("ws://109.239.57.147:9910", debug=False)
  factory.protocol = SendenClientProtocol
  connectWS(factory)
  reactor.run()