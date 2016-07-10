import time

class Nema17:
    # Pins for steps and direction.
    pin_clk = 0
    pin_cw = 0

    # GPIO library.
    GPIO = None

    # Directions to spin.
    CLOCKWISE = True
    ANTICLOCKWISE = False

    # Gap in seconds between each step.
    interval = 0.001

    # Sets pins for rotation and direction.
    def __init__(self, GPIO, pin_clk, pin_cw):
        self.pin_clk = pin_clk
        self.pin_cw = pin_cw
        self.GPIO = GPIO
        GPIO.setup(pin_clk, GPIO.OUT)
        GPIO.setup(pin_cw, GPIO.OUT)

    # Spins a number of steps in a given direction.
    def spin(self, steps, direction):
        self.GPIO.output(self.pin_cw, not direction)
        for i in range(0, steps):
            self.GPIO.output(self.pin_clk, True)
            time.sleep(self.interval)
            self.GPIO.output(self.pin_clk, False)

        self.GPIO.output(self.pin_clk, False)
        self.GPIO.output(self.pin_cw, False)