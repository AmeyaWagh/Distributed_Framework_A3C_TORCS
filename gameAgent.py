# from gym_torcs.gym_torcs import TorcsEnv
from gym_torcs.gym_torcs import *

#### Generate a Torcs environment
# enable vision input, the action is steering only (1 dim continuous action)
env = TorcsEnv(vision=True, throttle=False)

# without vision input, the action is steering and throttle (2 dim continuous action)
# env = TorcsEnv(vision=False, throttle=True)

ob = env.reset(relaunch=True)  # with torcs relaunch (avoid memory leak bug in torcs)
# ob = env.reset()  # without torcs relaunch

# Generate an agent
from sample_agent import Agent
agent = Agent(1)  # steering only
action = agent.act(ob, reward, done, vision=True)

# single step
ob, reward, done, _ = env.step(action)

# shut down torcs
env.end()