import random
import numpy as np
from enum import Enum


class Action(Enum):
    HIT = 1
    STICK = 2


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return '%s %d' % (self.color, self.value)


class State:
    def __init__(self, dealer_first_card, player_sum):
        self.dealer_first_card = dealer_first_card
        self.player_sum = player_sum


class Env:
    def __init__(self):
        self.dealer_sum = 0

    def step(self, state, action):
        if self.dealer_sum == 0:
            self.dealer_sum += state.dealer_first_card

        reward = 0
        player_sum = state.player_sum
        if action == Action.HIT:
            player_card = self.draw_one_card()
            player_sum += player_card.value
            print('Player HIT, draw %s, sum %d' % (player_card, player_sum))
            if player_sum > 21 or player_sum < 1:  # busted
                print('Player busted, player lose')
                reward = -1
        else:
            print('Play STICK Dealer turn:')
            while self.dealer_sum < 17:  # dealer always stick on sum of 17 or greater
                dealer_card = self.draw_one_card()
                self.dealer_sum += dealer_card.value
                print('Dealer draw %s, sum: %d' %
                      (dealer_card, self.dealer_sum))
            if self.dealer_sum > 21 or self.dealer_sum < 1 or state.player_sum > self.dealer_sum:
                print('Player win!!!')
                reward = 1
            elif player_sum < self.dealer_sum:
                print('Player lose!!!')
                reward = -1
        next_state = State(state.dealer_first_card, player_sum)
        return next_state, reward

    def draw_one_card(self):
        color = random.choice(['red', 'black', 'black'])  # 1/3 red, 2/3 black
        value = random.randint(1, 10)
        if color == 'red':
            value = -value
        return Card(color, value)


def simple_policy(state):
    if state.player_sum > 10:
        return Action.STICK
    else:
        return Action.HIT
