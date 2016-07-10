import RPi.GPIO as GPIO
from Nema17 import Nema17

GPIO.setmode(GPIO.BCM)

OX = Nema17(GPIO, 6, 18)

OX.spin(200, OX.CLOCKWISE)
OX.spin(200, OX.ANTICLOCKWISE)

GPIO.cleanup()