import unittest
from Nema17 import Nema17
import mock
from mock import call

class TestStringMethods(unittest.TestCase):

    def test_constructor(self):
        # Create a fake object, used for emulating the RPI library.
        RPILibraryMock = mock.Mock()

        # A fake 'constant' for setting pin status to out.
        RPILibraryMock.OUT = "out"

        # Create the test subject, and inject the mock library.
        motor = Nema17(RPILibraryMock, 0, 1)

        # Verify it set-up the pins for output mode.
        RPILibraryMock.setup.assert_has_calls([call(0, 'out'), call(1, 'out')])

    def test_spin(self):
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

if __name__ == '__main__':
    unittest.main()
