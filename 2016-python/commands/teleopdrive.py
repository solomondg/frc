# import wpilib
from wpilib import smartdashboard
from wpilib.command import Command

from oi import OI
from subsystems.drive import Drive


class TeleOpDrive(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self.requires(robot.drive)
        self.robot = robot(self)
        self.drive = Drive(self)
        self.oi = OI(self)

        self.multiplier = 0.9
        self.multiplierTurn = 1
        self.isCoast = True
        self.isBrake = False

    def TeleopDrive(self):
        self.requires(self.robot.drive)

    def initialize(self):
        self.drive.enable()
        self.drive.setCoast()

    def execute(self):
        if self.isBrake:
            smartdashboard.putString("Drive Mode", "Brake")
        if self.isCoast:
            smartdashboard.putString("Drive Mode", "Coast")
        self.drive.move(self.OI.deadzone(self.robot.oi.gamepad1.getY()) *
                        self.multiplier,
                        self.OI.deadzone(self.robot.oi.gamepad1.getRawAxis(4)) *
                        self.multiplierTurn)
        encoderValues = self.drive.getEncoderValues()
        smartdashboard.putNumber("Left Encoder", encoderValues[0])
        smartdashboard.putNumber("Right Encoder", encoderValues[1])

    def isFinished(self):
        return False

    def end(self):
        self.drive.disable()

    def interrupted(self):
        self.end()
