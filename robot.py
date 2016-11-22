# copyright (C) Team Terminator
# Authors: V. Barth, A. Eiselmayer, J. Luo, F. Panakkal, T. Tan

import random
from helpers import *


class Robot(object):
    """Robot Class"""

    def __init__(self):
        self.state = Position(1, 1)
        self.profit = 0
        self.q = {}  # stores robots q values
        self.alpha = 0.99  # learning rate
        self.gamma = 0.95  # discount factor
        self.epsilon = 0.99  # exploration rate
        self.explorations = 0  # counts number of explorations

    def __repr__(self):
        return "%s is @ %s. Profit is: %d" % (self.__class__.__name__, self.state, self.profit)

    def doAction(self):
        """ Lets the robot perform his movement
        :return Movement
        """
        # initialize all possible movements with q value 0
        available_qs = {
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveDown())): 0,
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveUp())): 0,
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveLeft())): 0,
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveRight())): 0,
        }
        # search if there are q values for state action pair
        for state_action_pair in self.q:
            if self.state == state_action_pair[0]:
                available_qs[state_action_pair[1]] = self.q[state_action_pair]

        biggest_reward = 0  # value for best possible options
        smallest_reward = 0  # value for worst possible option
        for idx, reward in enumerate(available_qs.values()):
            if idx == 0:
                biggest_reward = reward
                smallest_reward = reward
            if reward > biggest_reward:
                biggest_reward = reward
            if reward < smallest_reward:
                smallest_reward = reward

        go_on_exploration = random.uniform(0, 1) < self.epsilon  # determines whether the robot should explore or not
        # the exploration rate will only be decrease when the robot was already exploring for some time
        if self.explorations > 1400:
            if self.epsilon > 0:
                self.epsilon -= 0.1

        feasible_actions = []  # holds actions which the robot can choose from
        if not go_on_exploration:
            # robot does not explore
            for state_action_pair, reward in available_qs.iteritems():
                if reward == biggest_reward:
                    # put only the action(s) with the biggest reward as a action to take
                    feasible_actions.append(state_action_pair)
        else:
            # robot is going on exploration
            self.explorations += 1
            for state_action_pair, reward in available_qs.iteritems():
                if smallest_reward == 0 or biggest_reward == 0:  # for the beginning, if there are no real values yet
                    if reward == 0:
                        feasible_actions.append(state_action_pair)
                else:
                    if smallest_reward == 0:  # for the beginning, if there are no real values for q yet
                        feasible_actions.append(state_action_pair)
                    elif reward > smallest_reward:
                        # this ensures that we never explore to the worst direction
                        # if the worst direction would be actually quite good, the robot will figure that out after a few interations
                        feasible_actions.append(state_action_pair)

        if len(feasible_actions) == 1:  # if the is only one good action to take, the robot takes that action
            return feasible_actions[0]
        else:  # if there are multiple good actions to take the robot chooses randomly which to take
            choice = random.randint(0, len(feasible_actions) - 1)
            return feasible_actions[choice]

    def update(self, next_position, action, profit_change):
        """
        Updates the robot after with the values from the environment
        :param next_position: Position where the robot will be next
        :param action: (Position, Movement) what the robot chose to do
        :param profit_change: number added to his current profit
        :return: nothing
        """
        self._updateQ(next_position=next_position, action=action, profit_change=profit_change)
        self.state = next_position
        self.profit += profit_change

    def _updateQ(self, next_position, action, profit_change):
        """
        Updates all q values
        :param next_position: Position where the robot will be next
        :param action: (Position, Movement) what the robot chose to do
        :param profit_change: number added to his current profit
        :return: nothing
        """
        current_q = self.q.get((self.state, action), 0)
        value_list = []
        for state_action_pair, value in self.q.iteritems():
            if next_position == state_action_pair[0]:
                value_list.append(value)
        next_q = max(value_list) if value_list else 0

        new_q = current_q + self.alpha * (profit_change + self.gamma * next_q - current_q)

        self.q[(self.state, action)] = new_q

    def reset(self):
        """Resets the robot to start without erasing the q values"""
        self.state = Position(1, 1)
        self.profit = 0


class RandomRobot(Robot):
    """
    Random Robot chooses actions randomly
    """

    def doAction(self):
        """ Lets the robot perform his movement
        :return Movement
        """
        # initialize all possible movements with q value 0
        available_qs = [
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveDown())),
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveUp())),
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveLeft())),
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveRight()))
        ]
        choice = random.randint(0, len(available_qs) - 1)
        return available_qs[choice]
