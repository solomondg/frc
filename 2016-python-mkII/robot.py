#!/usr/bin/python3

import os

import wpilib as wpi

from wpilib import IterativeRobot

from drive import DriveStuff
from oi import IOStuff
# from teleop import TeleopStuff


class nutshack(IterativeRobot):
    """ yaaooo extine here boyz """

    def robotInit(self):
        """this is where the memes happen"""
        self.oiInstance = IOStuff(self)
        self.driveInstance = DriveStuff(self)
        # self.teleopInstance = TeleopStuff(self)
        # self.teleopInstance.start()
        self.driveInstance.enable()

    def autonomousPeriod(self):
        pass

    def teleopPeriod(self):
        self.left = self.driveInstance.\
            getDriveLeft(joystick=self.oiInstance.gamepad1)
        self.right = self.driveInstance.\
            getDriveRight(joystick=self.oiInstance.gamepad1)
        self.driveInstance.move(self.left, self.right)

    def testPeriod(self):
        pass


if __name__ == "__main__":
    wpi.run(nutshack)
