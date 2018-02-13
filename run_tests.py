#!/usr/bin/env python3

import random
import gym
import numpy as np
from gym_minigrid.register import envSet
from gym_minigrid.minigrid import Grid

# Test specifically importing a specific environment
from gym_minigrid.envs import DoorKeyEnv

# Test importing wrappers
from gym_minigrid.wrappers import *

##############################################################################

print('%d environments registered' % len(envSet))

for envName in sorted(envSet):
    print('testing "%s"' % envName)

    # Load the gym environment
    env = gym.make(envName)
    env.reset()
    env.render('rgb_array')

    # Verify that the same seed always produces the same environment
    for i in range(0, 5):
        seed = 1337 + i
        env.seed(seed)
        grid1 = env.grid.encode()
        env.seed(seed)
        grid2 = env.grid.encode()
        assert np.array_equal(grid2, grid1)

    env.reset()

    # Run for a few episodes
    for i in range(5 * env.maxSteps):
        # Pick a random action
        action = random.randint(0, env.action_space.n - 1)

        obs, reward, done, info = env.step(action)

        # Test observation encode/decode roundtrip
        img = obs if type(obs) is np.ndarray else obs['image']
        grid = Grid.decode(img)
        img2 = grid.encode()
        assert np.array_equal(img2, img)

        # Check that the reward is within the specified range
        assert reward >= env.reward_range[0], reward
        assert reward <= env.reward_range[1], reward

        if done:
            env.reset()

            # Check that the agent doesn't overlap with an object
            assert env.grid.get(*env.agentPos) is None

        env.render('rgb_array')

    env.close()

##############################################################################

# Test the env.agentSees() function
env = gym.make('MiniGrid-Empty-6x6-v0')
goalPos = (env.grid.width - 2, env.grid.height - 2)

def goalInObs(obs):
    grid = Grid.decode(obs)
    for j in range(0, grid.height):
        for i in range(0, grid.width):
            cell = grid.get(i, j)
            if cell and cell.color == 'green':
                return True
    return False

env.reset()
for i in range(0, 200):
    action = random.randint(0, env.action_space.n - 1)
    obs, reward, done, info = env.step(action)
    assert env.agentSees(*goalPos) == goalInObs(obs)
    if done:
        env.reset()
