import time
import cups
import socket
import binaryhelper
import RPi.GPIO as GPIO
from subprocess import Popen

# Internet verbindung
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('141.19.142.171', 10000)
sock.bind(server_address)
sock.listen(1)


# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pins auf Output setzen
GPIO.setup(11, GPIO.OUT)

# Pins auf Input setzen
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variaben 
prev_input_18 = 0
prev_input_19 = 0
prev_input_21 = 0
prev_input_22 = 0

imageName = "image.jpg"

# endlos schleife
while True:
  
  input_18 = GPIO.input(18)
  input_19 = GPIO.input(19)
  input_21 = GPIO.input(21)
  input_22 = GPIO.input(22)

#verbindung
  connection, client_address = sock.accept()
  data = connection.recv(16)

  if data:
    # json zu bild
    json_to_file(data, imageName)
    # Bild drucken
    Popen(["lp",imageName])
    
    time.sleep(0.1)
    GPIO.output(11, GPIO.HIGH) #signalleuchte an    


  if ((not prev_input_18) and input_18):
    #info senden
    time.sleep(0.05)
    GPIO.output(11, GPIO.LOW) #signalleuchte aus
    
  if ((not prev_input_19) and input_19):
    #info senden
    time.sleep(0.05)
    GPIO.output(11, GPIO.LOW) #signalleuchte aus
   
  if ((not prev_input_21) and input_21):
    #info senden
    time.sleep(0.05)
    GPIO.output(11, GPIO.LOW) #signalleuchte aus
   
  if ((not prev_input_22) and input_22):
    #info senden
    time.sleep(0.05)
    GPIO.output(11, GPIO.LOW) #signalleuchte aus

     

  prev_input_18 = input_18
  prev_input_19 = input_19
  prev_input_21 = input_21
  prev_input_22 = input_22
  time.sleep(0.05)