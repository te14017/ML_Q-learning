# copyright (C) Team Terminator
# Authors: V. Barth, A. Eiselmayer, J. Luo, F. Panakkal, T. Tan

from robot import *
from environment import Environment
import random


def _trial(robot):
    environment = Environment()
    robot = robot
    i = 1
    n = 100
    random.seed(2016)
    while i <= n:
        objective_found = False
        steps = 0
        while not objective_found:
            action = robot.doAction()
            new_position, action, profit_change, objective_found = environment.performRobotAction(action=action)
            robot.update(next_position=new_position, action=action, profit_change=profit_change)
            steps += 1
        print "Trial %s: # steps: %d - %s. Objective is: %d" % (i, steps, robot, profit_change)
        robot.reset()
        i += 1


def main():
    _trial(Robot())
    _trial(RandomRobot())


if __name__ == '__main__':
    main()
