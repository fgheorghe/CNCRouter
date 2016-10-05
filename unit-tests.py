import unittest
from Nema17 import Nema17
import mock
from mock import call
from CNCRouter import CNCRouter

class TestStringMethods(unittest.TestCase):

    def test_motor_constructor(self):
        # Create a fake object, used for emulating the RPI library.
        RPILibraryMock = mock.Mock()

        # A fake 'constant' for setting pin status to out.
        RPILibraryMock.OUT = "out"

        # Create the test subject, and inject the mock library.
        motor = Nema17(RPILibraryMock, 0, 1)

        # Verify it set-up the pins for output mode.
        RPILibraryMock.setup.assert_has_calls([
            call(0, RPILibraryMock.OUT),
            call(1, RPILibraryMock.OUT)
        ])

    def test_motor_spin(self):
    	# Same as above.
        RPILibraryMock = mock.Mock()
        RPILibraryMock.OUT = "out" 
        motor = Nema17(RPILibraryMock, 0, 1)

        # Spin 10 times in direction.
        motor.spin(10, False)

        # Spin 10 times the opposite direction.
        motor.spin(10, True)

        # Verify signals have been sent.
        RPILibraryMock.output.assert_has_calls(
            [
                # Ensure the direction is set.
                call(1, True),
                # Ensure motor signal is sent to spin, then pulse is stopped.
                call(0, True),
                call(0, False),
            ]
        )

    def test_gcode_execution(self):
        # Create fake motors.
        OXMock = mock.Mock()
        OYMock = mock.Mock()
        OZMock = mock.Mock()

        # Define fake direction "constants"
        OXMock.CLOCKWISE = 99
        OXMock.ANTICLOCKWISE = 100
        OYMock.CLOCKWISE = 99
        OYMock.ANTICLOCKWISE = 100
        OZMock.CLOCKWISE = 99
        OZMock.ANTICLOCKWISE = 100

        # Create CNC Router test subject.
        router = CNCRouter(OXMock, OYMock, OZMock)
        router.execGCode([
            {
                'command': "G1",
                'parameters': {
                    'X': 10,
                    'Y': 1,
                    'Z': 3
                }
            }
        ])

        # Ensure the OX motor is spun 10 times on direction, then back.
        OXMock.spin.assert_has_calls(
            [
                call(10, OXMock.CLOCKWISE),
                call(10, OXMock.ANTICLOCKWISE)
            ]
        )

        # Same for all other motors.
        OYMock.spin.assert_has_calls(
            [
                call(1, OYMock.CLOCKWISE),
                call(1, OYMock.ANTICLOCKWISE)
            ]
        )

        OZMock.spin.assert_has_calls(
            [
                # Z Axis moves in a different order.
                call(3, OZMock.ANTICLOCKWISE),
                call(3, OZMock.CLOCKWISE)
            ]
        )

if __name__ == '__main__':
    unittest.main()
