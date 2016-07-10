import RPi.GPIO as GPIO
from Nema17 import Nema17

GPIO.setmode(GPIO.BCM)

OZ = Nema17(GPIO, 12, 27)

OZ.spin(100, OZ.ANTICLOCKWISE)
OZ.spin(100, OZ.CLOCKWISE)

GPIO.cleanup()