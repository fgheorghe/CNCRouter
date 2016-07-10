class CNCRouter:
    # Stores current positions for each axis.
    currentOXPosition = 0
    currentOYPosition = 0
    currentOZPosition = 0

    # Axis motors.
    OX = None
    OY = None
    OZ = None

    # Maximum number of rotations for each axis.
    OXMAX = 4600
    OYMAX = 4600
    OZMAX = 2500

    # Loads motors.
    def __init__(self, OX, OY, OZ):
        self.OX = OX
        self.OY = OY
        self.OZ = OZ

    # Executes array of GCode Commands as returned by GCodeStringToCommandArray.parseG.
    def execGCode(self, GCodeCommandsArray):
        for instruction in GCodeCommandsArray:
            if instruction['command'] == "G1":
                self.parseG1Command(instruction['parameters'])

        self.home()

    # Executes a G1 command.
    def parseG1Command(self, parameters):
        if parameters['X'] is not None:
            position = int(parameters['X'])
            self.moveXTo(position)
        if parameters['Y'] is not None:
            position = int(parameters['Y'])
            self.moveYTo(position)
        if parameters['Z'] is not None:
            position = int(parameters['Z'])
            self.moveZTo(position)

    # Moves axis to a given position.
    def moveXTo(self, position):
        if self.currentOXPosition <= position:
            rotations = position - self.currentOXPosition
            if position <= self.OXMAX:
                self.OX.spin(rotations, self.OX.CLOCKWISE)
                self.currentOXPosition = position
        elif self.currentOXPosition > position:
            rotations = self.currentOXPosition - position
            if position >= 0:
                self.OX.spin(rotations, self.OX.ANTICLOCKWISE)
                self.currentOXPosition = position

    # Moves Y axis to a given position.
    def moveYTo(self, position):
        if self.currentOYPosition <= position:
            rotations = position - self.currentOYPosition
            if position <= self.OYMAX:
                self.OY.spin(rotations, self.OY.CLOCKWISE)
                self.currentOYPosition = position
        elif self.currentOYPosition > position:
            rotations = self.currentOYPosition - position
            if position >= 0:
                self.OY.spin(rotations, self.OY.ANTICLOCKWISE)
                self.currentOYPosition = position

    # Moves Z axis to a given position. NOTE: Reverse orders, as this is a different controller.
    def moveZTo(self, position):
        if self.currentOZPosition <= position:
            rotations = position - self.currentOZPosition
            if position <= self.OZMAX:
                self.OZ.spin(rotations, self.OZ.ANTICLOCKWISE)
                self.currentOZPosition = position
        elif self.currentOZPosition > position:
            rotations = self.currentOZPosition - position
            if position >= 0:
                self.OZ.spin(rotations, self.OZ.CLOCKWISE)
                self.currentOZPosition = position

    # Homes all axis.
    def home(self):
        if self.currentOZPosition > 0:
            # Reverse order.
            self.OZ.spin(self.currentOZPosition, self.OZ.CLOCKWISE)
        if self.currentOXPosition > 0:
            self.OX.spin(self.currentOXPosition, self.OX.ANTICLOCKWISE)
        if self.currentOYPosition > 0:
            self.OY.spin(self.currentOYPosition, self.OY.ANTICLOCKWISE)