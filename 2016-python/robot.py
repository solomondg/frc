#!/usr/bin/env python3

import wpilib
from wpilib import IterativeRobot, CANTalon, command
from subsystems.drive import Drive
from commands.teleop import TeleOp
import oi


class MyRobot(IterativeRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        pass

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        pass

    def testPeriodic(self):
        """This function is called periodically during test mode."""

if __name__ == "__main__":
    wpilib.run(MyRobot)
