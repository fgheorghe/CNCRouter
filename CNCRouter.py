import parallel
import time

class CNCRouter:
    # Stores current positions for each axis.
    currentOXPosition = 0
    currentOYPosition = 0
    currentOZPosition = 0

    # Maximum number of rotations for each axis.
    OXMAX = 4600
    OYMAX = 4600
    OZMAX = 2500

    DELAY = 0.000005

    STEPXCLOCKWISE     = 0b00000001
    STEPXANTICLOCKWISE = 0b00000011
    STOPXCLOCKWISE     = 0b00000000
    STOPXANTICLOCKWISE = 0b00000010

    STEPYCLOCKWISE     = 0b00000100
    STEPYANTICLOCKWISE = 0b00001100
    STOPYCLOCKWISE     = 0b00000000
    STOPYANTICLOCKWISE = 0b00001000

    STEPZCLOCKWISE     = 0b00010000
    STEPZANTICLOCKWISE = 0b00110000
    STOPZCLOCKWISE     = 0b00000000
    STOPZANTICLOCKWISE = 0b00100000

    # Loads motors.
    def __init__(self):
	self.p = parallel.Parallel(0)  # open LPT1 or /dev/parport0
        self.p.setDataStrobe(0)

    def __del__(self):
        self.p.setDataStrobe(1)

    # Executes array of GCode Commands as returned by GCodeStringToCommandArray.parseG.
    def execGCode(self, GCodeCommandsArray):
        for instruction in GCodeCommandsArray:
            if instruction['command'] == "G1":
                self.parseG1Command(instruction['parameters'])

        self.home()

    # Executes a G1 command.
    def parseG1Command(self, parameters):
        if parameters['Z'] is not None:
            position = int(parameters['Z'])
            self.moveZTo(position)
        if parameters['X'] is not None:
            position = int(parameters['X'])
            self.moveXTo(position)
        if parameters['Y'] is not None:
            position = int(parameters['Y'])
            self.moveYTo(position)

    # Moves axis to a given position.
    def moveXTo(self, position):
        if self.currentOXPosition <= position:
            rotations = position - self.currentOXPosition
            if position <= self.OXMAX:
                self.spin(self.STEPXCLOCKWISE, rotations, self.STOPXCLOCKWISE)
                self.currentOXPosition = position
        elif self.currentOXPosition > position:
            rotations = self.currentOXPosition - position
            if position >= 0:
                self.spin(self.STEPXANTICLOCKWISE, rotations, self.STOPXANTICLOCKWISE)
                self.currentOXPosition = position

    # Moves Y axis to a given position.
    def moveYTo(self, position):
        if self.currentOYPosition <= position:
            rotations = position - self.currentOYPosition
            if position <= self.OYMAX:
                self.spin(self.STEPYCLOCKWISE, rotations, self.STOPYCLOCKWISE)
                self.currentOYPosition = position
        elif self.currentOYPosition > position:
            rotations = self.currentOYPosition - position
            if position >= 0:
                self.spin(self.STEPYANTICLOCKWISE, rotations, self.STOPYANTICLOCKWISE)
                self.currentOYPosition = position

    # Moves Z axis to a given position. NOTE: Reverse orders, as this is a different controller.
    def moveZTo(self, position):
        if self.currentOZPosition <= position:
            rotations = position - self.currentOZPosition
            if position <= self.OZMAX:
                self.spin(self.STEPZANTICLOCKWISE, rotations, self.STOPZANTICLOCKWISE)
                self.currentOZPosition = position
        elif self.currentOZPosition > position:
            rotations = self.currentOZPosition - position
            if position >= 0:
                self.spin(self.STEPZCLOCKWISE, rotations, self.STOPZCLOCKWISE)
                self.currentOZPosition = position

    # Homes all axis.
    def home(self):
        if self.currentOZPosition > 0:
            # Reverse order.
            self.spin(self.STEPZCLOCKWISE, self.currentOZPosition, self.STOPZCLOCKWISE)
        if self.currentOXPosition > 0:
            self.spin(self.STEPXANTICLOCKWISE, self.currentOXPosition, self.STOPXANTICLOCKWISE)
        if self.currentOYPosition > 0:
            self.spin(self.STEPYANTICLOCKWISE, self.currentOYPosition, self.STOPYANTICLOCKWISE)

    def spin(self, axis, rotations, stop):
	for x in range(0, rotations):
	        self.p.setData(axis)
	        time.sleep(self.DELAY)
	        self.p.setData(stop)
	        time.sleep(self.DELAY)
