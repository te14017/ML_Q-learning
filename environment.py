from helpers import *


class Environment(object):
    """Environment"""

    def __init__(self):
        self.rewards = [
            Reward(value=100, row=2, column=4, name='+100'),
            Reward(value=50, row=2, column=3, name='+50'),
            Reward(value=-100, row=2, column=2, name='-100')
        ]
        self.square_size = 5
        self.penalty = -2
        self.movement_cost = -1
        self.forbidden_movements = [
            # forbidden movements need only to be declared once because the reverse movement will be checked
            # boundaries first row from left to right
            Movement(current_position=Position(1, 2), desired_position=Position(2, 2)),
            Movement(current_position=Position(1, 4), desired_position=Position(2, 4)),
            # boundaries second row from left to right
            Movement(current_position=Position(2, 1), desired_position=Position(2, 2)),
            Movement(current_position=Position(2, 2), desired_position=Position(2, 3)),
            Movement(current_position=Position(2, 3), desired_position=Position(3, 3)),
            Movement(current_position=Position(2, 3), desired_position=Position(2, 4)),
            Movement(current_position=Position(2, 4), desired_position=Position(3, 5)),
            # boundaries third row from left to right
            Movement(current_position=Position(3, 1), desired_position=Position(3, 2)),
            Movement(current_position=Position(3, 2), desired_position=Position(3, 3)),
            Movement(current_position=Position(3, 3), desired_position=Position(3, 4)),
            Movement(current_position=Position(3, 4), desired_position=Position(3, 5)),
            # boundaries fourth row from left to right
            Movement(current_position=Position(4, 1), desired_position=Position(3, 2)),
            Movement(current_position=Position(4, 2), desired_position=Position(3, 3)),
            Movement(current_position=Position(4, 3), desired_position=Position(3, 4)),
            Movement(current_position=Position(4, 4), desired_position=Position(3, 5)),
        ]

    def _isLegalMovement(self, movement):
        movement_legal = True
        if self._isForbiddenMovement(movement):
            movement_legal = False
        if self._isMovementOutOfBounds(movement):
            movement_legal = False
        return movement_legal

    def _isForbiddenMovement(self, movement):
        return movement in self.forbidden_movements or movement.reverse() in self.forbidden_movements

    def _isMovementOutOfBounds(self, movement):
        return movement.desired_position.row <= 0 or movement.desired_position.row > self.square_size or \
                        movement.desired_position.column <= 0 or movement.desired_position.column > self.square_size

    def _foundObjective(self, position):
        rewards = self.rewards
        for reward in rewards:
            if position == reward.position:
                return True, reward.value
        else:
            return False, 0

    def performRobotAction(self, action):
        """
        :param action: Movement
        :return position: Position, profit_change: int
        """
        if not self._isLegalMovement(action):
            return action.current_position, self.penalty

        objective_found, objective_value = self._foundObjective(action.desired_position)
        if objective_found:
            return action.desired_position, objective_found

        return action.desired_position, self.movement_cost
