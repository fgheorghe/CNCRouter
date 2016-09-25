from CNCRouter import CNCRouter

CNCRouter().spin(0b00000001, 10000, 0b00000000);
CNCRouter().spin(0b00000011, 10000, 0b00000010);

print "done"
