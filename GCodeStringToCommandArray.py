import pprint

class GCodeStringToCommandArray:
    # Converts a string of GCode instructions to an array.
    def convert(self, string):
        commandArray = []
        lines = string.split("\n")
        for line in lines:
            parts = line.split(" ")
            if parts[0][0:2] == "G1":
                commandArray.append({ 'command': parts[0][0:2], 'parameters': self.parseG1(parts)})
        #pprint.pprint(commandArray)
        return commandArray

    # Parses a G1 command.
    def parseG1(self, parts):
        result = {
            'X': None, #Xnnn The position to move to on the X axis
            'Y': None, #Ynnn The position to move to on the Y axis
            'Z': None, #Znnn The position to move to on the Z axis
            'E': None, #Ennn The amount to extrude between the starting point and ending point
            'F': None, #Fnnn The feedrate per minute of the move between the starting point and ending point (if supplied)
            'S': None #Snnn Flag to check if an endstop was hit (S1 to check, S0 to ignore, S2 see note, default is S0)1
        }

        for part in parts:
            if part[0] == "X":
                result['X'] = float(part[1:len(part)])
            elif part[0] == "Y":
                result['Y'] = float(part[1:len(part)])
            elif part[0] == "Z":
                result['Z'] = float(part[1:len(part)])
            elif part[0] == "E":
                result['E'] = float(part[1:len(part)])
            elif part[0] == "F":
                result['F'] = float(part[1:len(part)])
            elif part[0] == "S":
                result['S'] = float(part[1:len(part)])

        #pprint.pprint(result)

        return result