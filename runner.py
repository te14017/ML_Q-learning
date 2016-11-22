# Copyright Team Terminator
from robot import Robot
from environment import Environment
from helpers import *


def main(simulation=False):
    environment = Environment()
    robot = Robot()
    i = 1
    n = 100
    while i <= n:
        objective_found = False
        steps = 0
        while not objective_found:
            action = robot.doAction()
            new_position, action, profit_change, objective_found = environment.performRobotAction(action=action)
            robot.update(next_position=new_position, action=action, profit_change=profit_change)
            steps += 1
        if not simulation:
            print "Trial %s: # steps: %d - %s. Objective is: %d" % (i, steps, robot, profit_change)
        if i == 100 and simulation:
            print robot
        robot.reset()
        i += 1
    # check the Q value learnt by robot
    #for qValue in sorted(robot.q.keys()):
     #   print str(qValue) + ": " + str(robot.q[qValue])


if __name__ == '__main__':
    main()
