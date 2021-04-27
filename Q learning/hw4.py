import random
import time

import gym
import numpy as np

random.seed(0)


class MountainCarQLearningAgent:
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.gamma (discount rate)

      Functions you should use
        - self.get_legal_actions(state)
          which returns legal actions for a state
        - self.observation_to_state(state)
          which transfer an observation to discrete state
        - self.decay_epsilon()
          which should be called after each train episode to
          decay the exploration ratio. The epsilon will be
          reduced to 0 after the half of episode
        - self.test()
          which show your learning result by a rendered animation.
    """

    def __init__(self, alpha=0.5, epsilon=1, gamma=0.95, max_steps_per_episode=1000,
                 num_episode=1000):
        """
        alpha    - learning rate
        epsilon  - exploration rate (initial value)
        gamma    - discount factor
        max_steps_per_episode - number of maximize steps in each episode
        num_episode - number of training episodes, i.e. no learning after these many episodes
        """
        self.env = gym.make('MountainCar-v0')
        self.env.seed(0)

        self.alpha = alpha
        self.epsilon = epsilon
        self.epsilon_decay = self.epsilon / (num_episode // 2)
        self.gamma = gamma
        self.max_steps_per_episode = max_steps_per_episode
        self.num_episode = num_episode
        self.env._max_episode_steps = max_steps_per_episode
        self.state_number = 20
        self.action_number = 3

        "You can initialize Q-values here..."
        "The size of the table should be (self.state_number*2, self.action_number)"
        "*** YOUR CODE HERE ***"
        self.qtable = np.zeros([self.state_number * 2, self.action_number])
        "*** END YOUR CODE ***"

    def observation_to_state(self, ob):
        e = self.env.env
        position = ob[0]
        velocity = ob[1]
        if velocity >= 0:
            v = 1
        else:
            v = 0
        section = (e.max_position - e.min_position) / self.state_number
        p = position - e.min_position
        p = int(p / section)
        s = p + v * self.state_number
        return s

    def get_legal_actions(self, state):
        return [0, 1, 2]

    def get_policy_action(self, state):
        "Choose an action according to the policy"
        "*** YOUR CODE HERE ***"
        action = None
        # 从Q表中选择最大值对应的action
        action = int(np.argmax(self.qtable[state]))
        "*** END YOUR CODE ***"
        return action

    def get_action(self, state):
        "Choose an action according to the policy with random exploration."
        "You could use self.epsilon as prop for exloration"
        "*** YOUR CODE HERE ***"
        action = None
        if np.random.rand() < self.epsilon:
            # 随机explore
            action = np.random.choice(self.get_legal_actions(state))
        else:
            # 从Q表中选择最大值对应的action
            action = int(np.argmax(self.qtable[state]))
        "*** END YOUR CODE ***"
        return action

    def update(self, state, action, next_state, reward):
        "Update your qvalues"
        "*** YOUR CODE HERE ***"
        old_value = self.qtable[state, action]
        next_max = np.max(self.qtable[next_state])
        self.qtable[state, action] = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        "*** END YOUR CODE ***"

    def decay_epsilon(self):
        if self.epsilon > 0:
            self.epsilon -= self.epsilon_decay
        else:
            self.epsilon = 0

    def train_one_episode(self):
        ob = self.env.reset()
        steps = 0
        for _ in range(self.max_steps_per_episode):
            "Traing your agent for one episode. Please check the gym_example"
            "*** YOUR CODE HERE ***"
            state = self.observation_to_state(ob)
            action = self.get_action(state)
            ob, reward, done, info = self.env.step(action)
            next_state = self.observation_to_state(ob)
            # update
            self.update(state, action, next_state, reward)
            if done:
                break
            "*** END YOUR CODE ***"
            steps += 1
        return steps

    def train(self):
        "Traing your agent for mutliple episode. Please call train_one_episode"
        "*** YOUR CODE HERE ***"
        steps_list = []
        for i in range(self.num_episode):
            steps_list.append(self.train_one_episode())
            # decay_epsilon
            self.decay_epsilon()
            print('第' + str(i + 1) + '次')
            print('epsilon = ' + str(self.epsilon))
            print('steps = ' + str(steps_list[-1] + 1))
            print('----------------------')
        return steps_list
        "*** END YOUR CODE ***"

    def test(self):
        ob = self.env.reset()
        self.env.render()
        for _ in range(self.max_steps_per_episode):
            self.env.render()
            state = self.observation_to_state(ob)
            action = self.get_policy_action(state)
            ob, reword, done, info = self.env.step(action)
            if done:
                time.sleep(30)
                break

    def stop(self):
        self.env.close()


if __name__ == "__main__":
    rl_agent = MountainCarQLearningAgent()
    rl_agent.train()
    rl_agent.test()
    rl_agent.stop()
