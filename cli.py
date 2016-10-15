# Load libraries.
import pprint
import sys
import time
import RPi.GPIO as GPIO
from Nema17 import Nema17
from GCodeStringToCommandArray import GCodeStringToCommandArray
from CNCRouter import CNCRouter

# Check command line parameters.
if len(sys.argv) != 2:
    print "Usage: python cli.py filename.gcode"
    sys.exit(-1)

# Read gcode file.
with open(str(sys.argv[1]), 'r') as GCodeFile:
    GCode = GCodeFile.read()

# Set PIN mapping to BCM: https://cdn.shopify.com/s/files/1/0176/3274/files/Pins_Only_grande.png?2408547127755526599
GPIO.setmode(GPIO.BCM)

# Create OX and OY axis motor controllers.
OX = Nema17(GPIO, 6, 18, time)
OY = Nema17(GPIO, 13, 17, time)
OZ = Nema17(GPIO, 12, 27, time)

# Parse GCode instructions.
GCodeCommandsArray = GCodeStringToCommandArray().convert(GCode);

# Execute G Code Instructions
CNCRouter(OX, OY, OZ).execGCode(GCodeCommandsArray)

# Free GPIO Pins.
GPIO.cleanup()
