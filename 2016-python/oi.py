import wpilib
from wpilib.joystick import Joystick
from wpilib import buttons
from math import fabs as abs


class OI:

    def __init__(self, robot):
        self.robot = robot

        self.gamepad1 = Joystick(0)

        self.deadzoneThreshold = 0.35

    def deadzone(self, value):
        if (abs(value) < self.deadzoneThreshold):
            return 0
        return value
