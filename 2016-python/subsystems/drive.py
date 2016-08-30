import wpilib
from wpilib.command import Subsystem
from wpilib import cantalon, robotdrive
# from commands.teleopdrive import TeleOpDrive


class Drive2(Subsystem):

    def __init__(self, robot, name=None):
        super().__init__(name=name)
        self.robot = robot
        self.lmotors, self.rmotors = [], []


        self.lmotors.append(wpilib.CANTalon(1))
        self.lmotors.append(wpilib.CANTalon(2))
        self.rmotors.append(wpilib.CANTalon(3))
        self.rmotors.append(wpilib.CANTalon(4))

        self.drive = robotdrive.RobotDrive(
            self.lmotors[0], self.lmotors[1], self.rmotors[0], self.rmotors[1]
        )
        self.enabled = False
        self.currentSpeed = [0.0, 0.0]
        self.goalSpeed = [0.0, 0.0]

    def move(self, throttle, turn):
        if (not self.enabled):
            return
        self.goalSpeed[0] = throttle
        self.goalSpeed[1] = turn
        self.drive.arcadeDrive(self.goalSpeed[0], self.goalSpeed[1])

    def getEncoderValues(self):
        result = [
            self.lmotors[0].getEncPosition(), self.rmotors[0].getEncPosition()]
        return result

    def resetEncoders(self):
        self.lmotors[0].setEncPosition(0)
        self.rmotors[0].setEncPosition(0)

    def setBrake(self):
        self.lmotors[0].enableBrakeMode(True)
        self.lmotors[1].enableBrakeMode(True)
        self.rmotors[0].enableBrakeMode(True)
        self.rmotors[1].enableBrakeMode(True)
        return True

    def setCoast(self):
        self.lmotors[0].enableBrakeMode(False)
        self.lmotors[1].enableBrakeMode(False)
        self.rmotors[0].enableBrakeMode(False)
        self.rmotors[1].enableBrakeMode(False)
        return True

    def stop(self):
        self.drive.stopMotor()
        self.goalSpeed[0] = 0
        self.goalSpeed[1] = 0
        self.currentSpeed[0] = 0
        self.currentSpeed[1] = 0

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.stop()
        self.resetEncoders()

    def initDefaultCommand(self):
        pass

    def setDefault(self):
        # self.setDefaultCommand(TeleOpDrive())
        pass

    def resetDefault(self):
        self.setDefaultCommand(None)
