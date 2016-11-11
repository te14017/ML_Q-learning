# copyright Team Terminator
from robot import Robot
from environment import Environment
from helpers import *


def main():
    environment = Environment()
    robot = Robot()
    i = 1
    n = 10
    while i <= n:
        objective_found = False
        while not objective_found:
            action = robot.doAction()
            new_position, action, profit_change, objective_found = environment.performRobotAction(action=action)
            robot.update(next_position=new_position, action=action, profit_change=profit_change)
        print robot
        robot.reset()
        i += 1


if __name__ == '__main__':
    main()
