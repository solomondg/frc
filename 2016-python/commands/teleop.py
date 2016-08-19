import wpilib
from wpilib.command import Command

from subsystems.drive import Drive
from commands.teleopdrive import TeleOpDrive

class TeleOp(Command):

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)

        self.requires(robot.drive)
#         self.robot = robot(self)

        self.drive = Drive(self)

        self.speed = 0.95
        self.tOp = TeleOpDrive(self)

    def initialize(self):
        self.drive.setDefault()
        self.tOp.start()
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False

    def end(self):
        self.drive.resetDefault()

    def interrupted(self):
        self.end()
