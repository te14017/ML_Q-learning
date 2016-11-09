import random

from helpers import *


class Robot(object):
    """Robot Class"""

    def __init__(self):
        self.state = {'position': Position(1, 1)}
        self.profit = 0

    def __repr__(self):
        return "%s is @ %s. Profit is: %d" % (self.__class__.__name__, self.state['position'], self.profit)

    def doAction(self):
        """ Lets the robot perform his movement
        :return Movement
        """
        if self._qAvailable():
            # we have a good movement already learnt
            pass
        else:
            # dont know yet what is good to do
            random.seed(2016)
            choice = random.randint(1, 4)
            if choice == 1:
                # try to move up
                return Movement(
                    current_position=self.state['position'],
                    desired_position=self.state['position'].moveUp()
                )
            if choice == 2:
                return Movement(
                    # try to move down
                    current_position=self.state['position'],
                    desired_position=self.state['position'].moveDown()
                )
            if choice == 3:
                # try to move left
                return Movement(
                    current_position=self.state['position'],
                    desired_position=self.state['position'].moveLeft()
                )
            # else
            # try to move right
            return Movement(
                    current_position=self.state['position'],
                    desired_position=self.state['position'].moveRight()
                )



    def _qAvailable(self):
        return False
