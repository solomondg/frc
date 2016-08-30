# import wpilib
from wpilib.command import Subsystem
from wpilib import CANTalon, robotdrive


class DriveStuff(Subsystem):

    def __init__(self, robot, name=None):
        super().__init__(name=name)
        self.robot = robot
        self.l1 = CANTalon(1)
        self.l2 = CANTalon(2)
        self.r1 = CANTalon(3)
        self.r2 = CANTalon(4)
        self.robotDrive = robotdrive.RobotDrive(
            self.l1, self.l2, self.r1, self.r2
        )
        self.enabled = False
        self.speed = [0.0, 0.0]

    def move(self, throttle, turn):
        if (not self.enabled):
            return
        self.speed[0] = throttle
        self.speed[1] = turn
        self.robotDrive.tankDrive(self.speed[0], self.speed[1])

    def getEncoderValues(self):
        result = [
            self.l1.getEncPosition(), self.l2.getEncPosition,
            self.r1.getEncPosition(), self.r2.getEncPosition
        ]
        return result

    def resetEncoders(self):
        self.l1.setEncPosition(0)
        self.r1.setEncPosition(0)

    def setBrake(self):
        self.l1.enableBrakeMode(True)
        self.l2.enableBrakeMode(True)
        self.r1.enableBrakeMode(True)
        self.r2.enableBrakeMode(True)

    def setCoast(self):
        self.l1.enableBrakeMode(False)
        self.l2.enableBrakeMode(False)
        self.r1.enableBrakeMode(False)
        self.r2.enableBrakeMode(False)

    def stop(self):
        self.robotDrive.stopMotor()
        self.speed[0] = 0.0
        self.speed[1] = 0.0

    def enable(self):
        self.enable = True

    def disable(self):
        self.enabled = False
        self.stop()
        self.resetEncoders

    def initDefaultCommand(self):
        pass

    def setDefault(self):
        pass

    def resetDefault(self):
        self.setDefaultCommand(None)

    @classmethod
    def _getBaseDrive(cls, joystick):
        """
        Calculates base drive speed, regardless of side.
        """

        yAxis = joystick.getRawAxis(1)
        return -yAxis / cls.DRIVE_SPD_DIVISOR

    @classmethod
    def getDriveLeft(cls, joystick):
        print ("kek")
        """
        Calculates and returns the speed of the left drive motors, relative
        to input.
        """

        xAxis = joystick.getRawAxis(3)
        fwd = cls._getBaseDrive(joystick)
        turbo = cls.TURBO_FACTOR if cls.ALLOW_TURBO and joystick.getRawButton(
            5) else 1

        if abs(fwd) <= cls.DRIVE_DEADBAND < abs(xAxis):  # Stationary pivot
            return xAxis / cls.TURN_SPD_DIVISOR * turbo
        elif abs(fwd) > cls.DRIVE_DEADBAND:  # Turn whilst driving
            turn = abs(xAxis * cls.TURN_SPD_DIVISOR) + 1
            fwd *= turbo
            return (fwd * turn) if xAxis > cls.DRIVE_DEADBAND else (fwd / turn)
        return 0.0

    @classmethod
    def getDriveRight(cls, joystick):
        """
        Calculates and returns the speed of the right drive motors, relative
        to input.
        """

        xAxis = joystick.getRawAxis(3)
        fwd = -cls._getBaseDrive(joystick)
        turbo = cls.TURBO_FACTOR if cls.ALLOW_TURBO and joystick.getRawButton(
            5) else 1

        if abs(fwd) <= cls.DRIVE_DEADBAND < abs(xAxis):
            return xAxis / cls.TURN_SPD_DIVISOR * turbo
        elif abs(fwd) > cls.DRIVE_DEADBAND:
            turn = abs(xAxis) + 1
            fwd *= turbo
            return (fwd / turn) if xAxis > cls.DRIVE_DEADBAND else (fwd * turn)
        return 0.0
