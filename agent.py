import random
import numpy as np
from env import State, Env, Action


class MCAgent:
    '''Monte-Carlo control agent.'''

    def __init__(self):
        self.alpha = 0.01
        self.Q = np.zeros((11, 22, 2))  # dealer_first_card, player_sum, action
        self.history = []

    def policy(self, state):
        '''Epsilon greedy policy.'''
        eps = 0.1
        if random.random() < eps:
            action = random.choice([Action.HIT, Action.STICK])
        else:
            Q = self.Q[state.dealer_first_card, state.player_sum]
            action = Action.HIT if Q[0] >= Q[1] else Action.STICK
        self.history.append([state, action])
        return action

    def update(self, reward):
        for state, action in self.history:
            i, j = state.dealer_first_card, state.player_sum
            k = [Action.HIT, Action.STICK].index(action)
            self.Q[i, j, k] += self.alpha * (reward - self.Q[i, j, k])


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
    return reward


if __name__ == '__main__':
    agent = MCAgent()
    player_win = player_lose = player_tie = 0
    for i in range(1000):
        ret = play_once(agent)
        if ret == 1:
            player_win += 1
        elif ret == -1:
            player_lose += 1
        else:
            player_tie += 1
    print(player_win, player_lose, player_tie)
