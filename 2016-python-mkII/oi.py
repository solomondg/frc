import wpilib
from wpilib.joystick import Joystick
from wpilib import buttons
from math import fabs as abs

class IOStuff:
    """how we do the joystickz"""
    def __init__(self, robot):
        self.robot = robot
        self.gamepad1 = Joystick(0)
        self.deadzoneThreshold = 0.35

    def deadzone(self, value):
        if (abs(value) < self.deadzoneThreshold):
            return 0
        return value


    def getForward(self):
        return self.deadzone(self.gamepad1.getAxis(1))


    def getTurn(self):
        return self.deadzone(self.gamepad1.getAxis(3))
