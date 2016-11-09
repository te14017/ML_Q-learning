from robot import Robot
from environment import Environment
from helpers import *


def main():
    environment = Environment()
    robot = Robot()

    action = robot.doAction()

    new_position, profit_change = environment.performRobotAction(action=action)
    robot.state['position'] = new_position
    robot.profit += profit_change
    print action
    print new_position
    print profit_change
    print robot

if __name__ == '__main__':
    main()
