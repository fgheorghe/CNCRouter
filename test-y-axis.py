import RPi.GPIO as GPIO
from Nema17 import Nema17

GPIO.setmode(GPIO.BCM)

OY = Nema17(GPIO, 13, 17)

OY.spin(200, OY.CLOCKWISE)
OY.spin(200, OY.ANTICLOCKWISE)

GPIO.cleanup()