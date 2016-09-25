# Load libraries.
import pprint
import sys
#import RPi.GPIO as GPIO
#from Nema17 import Nema17
from GCodeStringToCommandArray import GCodeStringToCommandArray
from CNCRouter import CNCRouter

# Check command line parameters.
if len(sys.argv) != 2:
    print "Usage: python cli.py filename.gcode"
    sys.exit(-1)

# Read gcode file.
with open(str(sys.argv[1]), 'r') as GCodeFile:
    GCode = GCodeFile.read()

# Parse GCode instructions.
GCodeCommandsArray = GCodeStringToCommandArray().convert(GCode);

# Execute G Code Instructions
CNCRouter().execGCode(GCodeCommandsArray)
