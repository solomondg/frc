import wpilib
from wpilib.command import Command

from oi import OI
from subsystems.drive import Drive

class TeleOp(Command):

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)

        self.requires(robot.drive)
        self.robot = robot(self)

        self.drive = Drive(self)

        self.oi = OI(self)

        self.speed = 0.95

    def initialize(self):
        self.drive.setDefault()
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False

    def end(self):
        pass

    def interrupted(self):
        pass

