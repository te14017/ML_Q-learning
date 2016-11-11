import random

from helpers import *
import operator


class Robot(object):
    """Robot Class"""

    def __init__(self):
        self.state = Position(1, 1)
        self.profit = 0
        self.q = {}
        self.alpha = 0.9
        self.gamma = 0.9

    def __repr__(self):
        return "%s is @ %s. Profit is: %d" % (self.__class__.__name__, self.state, self.profit)

    def doAction(self):
        """ Lets the robot perform his movement
        :return Movement
        """
        available_qs = {
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveDown())): 0,
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveUp())): 0,
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveLeft())): 0,
            (self.state, Movement(current_position=self.state, desired_position=self.state.moveRight())): 0,
        }
        for state_action_pair in self.q:
            if self.state == state_action_pair[0]:
                available_qs[state_action_pair[1]] = self.q[state_action_pair]

        biggest_reward = 0
        for idx, reward in enumerate(available_qs.values()):
            if idx == 0:
                biggest_reward = reward
            if reward > biggest_reward:
                biggest_reward = reward

        feasible_actions = []
        for state_action_pair, reward in available_qs.iteritems():
            if reward == biggest_reward:
                feasible_actions.append(state_action_pair)
        if len(feasible_actions) == 1:
            return feasible_actions[0]
        else:
            random.seed(2016)
            if len(feasible_actions) <= 0:
                a = 1
            choice = random.randint(0, len(feasible_actions)-1)
            return feasible_actions[choice]

    def update(self, next_position, action, profit_change):
        self._updateQ(next_position=next_position, action=action, profit_change=profit_change)
        self.state = next_position
        self.profit += profit_change

    def _updateQ(self, next_position, action, profit_change):
        q_state_action = self.q.get((self.state, action), 0)
        value_list = []
        for state_action_pair, value in self.q.iteritems():
            if next_position == state_action_pair[0]:
                value_list.append(value)
        next_q = max(value_list) if value_list else profit_change

        new_q = q_state_action + self.alpha * (profit_change + self.gamma * next_q - q_state_action)

        self.q[(self.state, action)] = new_q

    def reset(self):
        self.state = Position(1, 1)
        self.profit = 0
