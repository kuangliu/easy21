import random
import numpy as np

from plot import Plotter
from env import State, Env, Action


class MCAgent:
    '''Monte-Carlo control agent.'''

    def __init__(self):
        self.Q = np.zeros((11, 22, 2))  # dealer_first_card, player_sum, action
        self.N = np.zeros((11, 22, 2))  # N(s,a)
        self.history = []

    def policy(self, state):
        '''Epsilon greedy policy.'''
        i, j = state.dealer_first_card, state.player_sum
        Ns = self.N.sum(2)      # N(s)
        eps = 100 / (100 + Ns[i, j])  # eps = N0 / (N0 + N(s)) where N0 = 100
        if random.random() < eps:
            action = random.choice([Action.HIT, Action.STICK])
        else:
            Q = self.Q[i, j]
            action = Action.HIT if Q[0] >= Q[1] else Action.STICK
        k = [Action.HIT, Action.STICK].index(action)
        self.N[i, j, k] += 1
        self.history.append([state, action])
        return action

    def update(self, reward):
        for state, action in self.history:
            i, j = state.dealer_first_card, state.player_sum
            k = [Action.HIT, Action.STICK].index(action)
            alpha = 1. / self.N[i, j, k]
            self.Q[i, j, k] += alpha * (reward - self.Q[i, j, k])

    def print_history(self):
        for state, action in self.history:
            print(state.dealer_first_card, state.player_sum, action)

    def reset(self):
        self.history = []


def play_once(agent):
    print('========= Game Start =========')
    env = Env()
    dealer_first_card_value = random.randint(1, 10)
    player_first_card_value = random.randint(1, 10)
    state = State(dealer_first_card_value, player_first_card_value)
    print('Dealer first card: %d, player first card: %d' %
          (dealer_first_card_value, player_first_card_value))
    while True:
        action = agent.policy(state)
        state, reward = env.step(state, action)
        if reward != 0:
            break
    if reward == 1:
        agent.update(1)
    elif reward == -1:
        agent.update(0)
    agent.reset()
    return reward


if __name__ == '__main__':
    agent = MCAgent()
    player_win = player_lose = player_tie = 0
    plotter = Plotter()
    for i in range(100000):
        print(i)
        ret = play_once(agent)
        if ret == 1:
            player_win += 1
        elif ret == -1:
            player_lose += 1
        else:
            player_tie += 1
    print(player_win, player_lose, player_tie)
    plotter.plot(agent.Q)
    plotter.show()
