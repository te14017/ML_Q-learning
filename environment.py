# copyright (C) Team Terminator
# Authors: V. Barth, A. Eiselmayer, J. Luo, F. Panakkal, T. Tan

from helpers import *
import random


class Environment(object):
    """Environment"""

    def __init__(self):
        self.rewards = [
            Reward(value=100, position=Position(2, 4), name='+100'),
            Reward(value=50, position=Position(2, 3), name='+50'),
            Reward(value=-100, position=Position(2, 2), name='-100')
        ]
        self.square_size = 5  # Size of our maze
        self.penalty = -10  # penalty for hitting a wall or trying to leave the maze
        self.movement_cost = -1
        # forbidden movements need only to be declared once because the reverse movement will be checked
        # boundaries first row from left to right
        self.forbidden_movements = [
            Movement(current_position=Position(1, 2), desired_position=Position(2, 2)),
            Movement(current_position=Position(1, 4), desired_position=Position(2, 4)),
            # boundaries second row from left to right
            Movement(current_position=Position(2, 1), desired_position=Position(2, 2)),
            Movement(current_position=Position(2, 2), desired_position=Position(2, 3)),
            Movement(current_position=Position(2, 3), desired_position=Position(3, 3)),
            Movement(current_position=Position(2, 3), desired_position=Position(2, 4)),
            Movement(current_position=Position(2, 4), desired_position=Position(2, 5)),
            # boundaries third row from left to right
            Movement(current_position=Position(3, 1), desired_position=Position(3, 2)),
            Movement(current_position=Position(3, 2), desired_position=Position(3, 3)),
            Movement(current_position=Position(3, 3), desired_position=Position(3, 4)),
            Movement(current_position=Position(3, 4), desired_position=Position(3, 5)),
            # boundaries fourth row from left to right
            Movement(current_position=Position(4, 1), desired_position=Position(4, 2)),
            Movement(current_position=Position(4, 2), desired_position=Position(4, 3)),
            Movement(current_position=Position(4, 3), desired_position=Position(4, 4)),
            Movement(current_position=Position(4, 4), desired_position=Position(4, 5)),
        ]

    def _isLegalMovement(self, movement):
        """
        Checks if movement is leaving the maze or hitting a wall
        :param movement: Movement which the robot would like to perform
        :return: True if the movement is ok otherwise returns False
        """
        movement_legal = True
        if self._isForbiddenMovement(movement):
            movement_legal = False
        if self._isMovementOutOfBounds(movement):
            movement_legal = False
        return movement_legal

    def _isForbiddenMovement(self, movement):
        """
        Checks movement hits a wall
        :param movement: Movement which the robot would like to perform
        :return: True if it hits a wall False otherwise
        """
        return movement in self.forbidden_movements or movement.reverse() in self.forbidden_movements

    def _isMovementOutOfBounds(self, movement):
        """
        Check if movement would leave the maze
        :param movement: Movement which the robot would like to perform
        :return: True if robot would leave the maze, False otherwise
        """
        return movement.desired_position.row <= 0 or movement.desired_position.row > self.square_size or \
               movement.desired_position.column <= 0 or movement.desired_position.column > self.square_size

    def _foundObjective(self, movement):
        """
        Checks whether on the next position of the robot is a reward or not
        :param movement: Movement which the robot would like to perform
        :return: True and reward value if there is a reward, False and 0 otherwise
        """
        rewards = self.rewards
        for reward in rewards:
            if movement.desired_position == reward.position:
                return True, reward.value
        else:
            return False, 0

    def performRobotAction(self, action):
        """
        Performs the action of the robot in the environment if possible
        :param action: (Position, Movement) the robot wants to do
        :return: position: Position, action: Action, profit_change: int, objective_found: boolean
        """
        # environments chooses if the robot will go to its desired position or change to left or right
        action_indicator = random.uniform(0, 1)  # random number 0 <= x <= 1
        if action_indicator <= 0.8:
            # do nothing
            pass
        elif action_indicator <= 0.9:
            # change action to 90 left
            movement = action[1]
            action = (action[0], movement.turnLeft())
        else:
            # change action to 90 right
            movement = action[1]
            action = (action[0], movement.turnRight())
        objective_found = False
        if not self._isLegalMovement(action[1]):
            return action[0], action, self.penalty + self.movement_cost, objective_found

        objective_found, objective_value = self._foundObjective(action[1])
        if objective_found:
            return action[1].desired_position, action, objective_value + self.movement_cost, objective_found
        return action[1].desired_position, action, self.movement_cost, objective_found
