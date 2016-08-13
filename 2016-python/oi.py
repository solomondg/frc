import wpilib
from wpilib import buttons
from wpilib import joystick
from commands.teleop import TeleOp
from Math import abs


class OI:

    def __init__(self, robot):
        self.robot = robot

        self.gamepad1 = joystick(0)
        self.gamepad2 = joystick(1)

        self.deadzoneThreshold = 0.35

    def deadzone(self, value):
        if (abs(value) < self.deadzoneThreshold):
            return 0
        return value
