import time
import json
import threading
import RPi.GPIO as GPIO
from subprocess import Popen

class ButtonListenerSenderThread(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self._stop = threading.Event()

    def showIcons (self, icon):

        print icon

        # XD LED an
        if icon == '"grinsSmilie"':
            GPIO.output(18, GPIO.HIGH)
        # Herz LED an
        if icon == '"herz"':
            GPIO.output(19, GPIO.HIGH)
        # Stern LED an
        if icon == '"stern"':
            GPIO.output(21, GPIO.HIGH)
        # Tele LED an
        if icon == '"tele"':
            GPIO.output(22, GPIO.HIGH)
        # :) LED an
        if icon == '"Smilie"':
            GPIO.output(23, GPIO.HIGH)


    def run(self):
        # RPi.GPIO Layout verwenden (wie Pin-Nummern)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) 

        # Pin auf Input setzen
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Pins auf Output setzen
        GPIO.setup(16, GPIO.OUT)  # Beleuchtung Foto
        
        GPIO.setup(18, GPIO.OUT)  # icon
        GPIO.setup(19, GPIO.OUT)  # icon herz
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)

        imageName = "image.jpg"
        prev_input = 0

        # Dauersschleife
        while not self.stopped():

            input = GPIO.input(11)
            data = False

            # bedingung Foto (button 11 gedrueckt)
            if ((not prev_input) and input):

                # Beleuchtung anschalten
                GPIO.output(16, GPIO.HIGH)
                # Bild machen
                Popen(["fswebcam", "--save", imageName])
                time.sleep(0.5)
                # Bild senden
                self.client.sendImage(imageName)

                GPIO.output(18, GPIO.LOW)
                GPIO.output(19, GPIO.LOW)
                GPIO.output(21, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)

            prev_input = input
            time.sleep(0.1)

            # beleuchtung aus schalten
            GPIO.output(16, GPIO.LOW)

    # stop the thread
    def stop(self):
        self._stop.set()

    # is the thread stopped?
    def stopped(self):
        return self._stop.is_set()


class ButtonListenerReceiverThread(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self._stop = threading.Event()

    def showLight(self):
        # signalleuchte an
        GPIO.output(11, GPIO.HIGH) 

    def run(self):

        # RPi.GPIO Layout verwenden (wie Pin-Nummern)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        # Pins auf Output setzen
        GPIO.setup(11, GPIO.OUT)
        # signalleuchte an
        GPIO.output(11, GPIO.LOW) 


        # Pins auf Input setzen
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Variaben
        prev_input_18 = 0
        prev_input_19 = 0
        prev_input_21 = 0
        prev_input_22 = 0
        prev_input_23 = 0

        # endlos schleife
        while not self.stopped():

            input_18 = GPIO.input(18)
            input_19 = GPIO.input(19)
            input_21 = GPIO.input(21)
            input_22 = GPIO.input(22)
            input_23 = GPIO.input(23)


            if ((not prev_input_18) and input_18):
                # info senden
                self.client.sendIcon("grinsSmilie")
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_19) and input_19):
                # info senden
                self.client.sendIcon("herz")
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_21) and input_21):
                # info senden
                self.client.sendIcon("stern")
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_22) and input_22):
                # info senden
                self.client.sendIcon("tele")
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_23) and input_23):
                # info senden
                self.client.sendIcon("Smilie")
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            prev_input_18 = input_18
            prev_input_19 = input_19
            prev_input_21 = input_21
            prev_input_22 = input_22
            prev_input_23 = input_23
            time.sleep(0.05)

        # stop the thread
    def stop(self):
        self._stop.set()

    # is the thread stopped?
    def stopped(self):
        return self._stop.is_set()
