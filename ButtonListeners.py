import time
import json
import binaryhelper
# import RPi.GPIO as GPIO
from subprocess import Popen
import threading
import cups

class ButtonListenerSenderThread(threading.Thread):
    # RPi.GPIO Layout verwenden (wie Pin-Nummern)

    def run():
        GPIO.setmode(GPIO.BOARD)

        # Pin 18 (GPIO 24) auf Input setzen
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Pins auf Output setzen
        GPIO.setup(23, GPIO.OUT)  # Beleuchtung Foto
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
                Popen(["fswebcam", "--save", imageName])
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

            # beleuchtung aus schalten
            GPIO.output(23, GPIO.LOW)


class ButtonListenerReceiverThread(threading.Thread):

    def run():
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

        # verbindung
            connection, client_address = sock.accept()
            data = connection.recv(16)

            if data:
                # json zu bild
                json_to_file(data, imageName)
                # Bild drucken
                Popen(["lp", imageName])

                time.sleep(0.1)
                GPIO.output(11, GPIO.HIGH)  # signalleuchte an

            if ((not prev_input_18) and input_18):
                # info senden
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_19) and input_19):
                # info senden
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_21) and input_21):
                # info senden
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            if ((not prev_input_22) and input_22):
                # info senden
                time.sleep(0.05)
                GPIO.output(11, GPIO.LOW)  # signalleuchte aus

            prev_input_18 = input_18
            prev_input_19 = input_19
            prev_input_21 = input_21
            prev_input_22 = input_22
            time.sleep(0.05)
