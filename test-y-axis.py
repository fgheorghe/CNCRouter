from CNCRouter import CNCRouter

CNCRouter().spin(0b00001100, 1500, 0b00001000);
CNCRouter().spin(0b00000100, 1500, 0b00000000);

print "done"

