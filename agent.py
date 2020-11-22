import random
import numpy as np

from plot import Plotter
from env import State, Env, Action


class MCAgent:
    '''Monte-Carlo Control agent.'''

    def __init__(self):
        self.Q = np.zeros((11, 22, 2))  # dealer_first_card, player_sum, action
        self.N = np.zeros((11, 22, 2))  # N(s,a)
        self.history = []

    def policy(self, state, greedy=False):
        '''Epsilon greedy policy.'''
        i, j = state.dealer_first_card, state.player_sum
        if greedy:
            Q = self.Q[i, j]
            action = Action.HIT if Q[0] >= Q[1] else Action.STICK
            return action

        Ns = self.N.sum(2)  # N(s)
        eps = 100 / (100 + Ns[i, j])
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


def play_once(agent, greedy=False):
    print('========= Game Start =========')
    env = Env()
    dealer_first_card_value = random.randint(1, 10)
    player_first_card_value = random.randint(1, 10)
    state = State(dealer_first_card_value, player_first_card_value)
    print('Dealer first card: %d, player first card: %d' %
          (dealer_first_card_value, player_first_card_value))
    while True:
        action = agent.policy(state, greedy)
        state, reward, terminate = env.step(state, action)
        if terminate:
            break

    if not greedy:  # update only in non-greedy mode
        if reward == 1:
            agent.update(1)
        elif reward == -1:
            agent.update(0)
    agent.reset()
    return reward


if __name__ == '__main__':
    agent = MCAgent()
    plotter = Plotter()
    # Train
    for i in range(100000):
        print(i)
        ret = play_once(agent)
    plotter.plot(agent.Q)
    plotter.show()

    # Test
    #  player_win = player_lose = player_tie = 0
    #  for i in range(100000):
    #     print(i)
    #     ret = play_once(agent, greedy=True)
    #     if ret == 1:
    #         player_win += 1
    #     elif ret == -1:
    #         player_lose += 1
    #     else:
    #         player_tie += 1
    #  print(player_win, player_lose, player_tie)
