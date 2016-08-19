#!/usr/bin/env python3

import wpilib
from wpilib import IterativeRobot, CANTalon
from wpilib.command import Command
from subsystems.drive import Drive
from commands.teleop import TeleOp
from commands.teleopdrive import TeleOpDrive
from oi import OI


class MyRobot(IterativeRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drive = Drive(self)
        self.teleop = TeleOp(self)
        # self.teleop.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
