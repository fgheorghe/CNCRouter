from CNCRouter import CNCRouter

CNCRouter().spin(0b00000011, 7500, 0b00000010);
CNCRouter().spin(0b00000001, 7500, 0b00000000);

print "done"
