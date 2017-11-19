#!/usr/bin/python3
from gym_torcs.gym_torcs import TorcsEnv
from gameAgent import Agent
import numpy as np
import os
import time
import random

vision = False
episode_count = 100
max_steps = 5000
reward = 0
done = False
step = 0

# Generate a Torcs environment
env = TorcsEnv(vision=vision, throttle=False ,textMode=True,xmlPath='./gym_torcs/practice.xml')

agent = Agent(1,verbose=True)  # steering only

epsilon=0.001

print("TORCS Experiment Start.")
for i in range(episode_count):
    try:
        print("Episode : " + str(i))

        if np.mod(i, 3) == 0:
            # Sometimes you need to relaunch TORCS because of the memory leak error
            ob = env.reset(relaunch=True)
            # ob = env.reset(relaunch=False)
        else:
            ob = env.reset()

        total_reward = 0.
        # prev_ob = ob
        action=np.array([random.uniform(0,1)])
        agent.pullFromServer()
        for j in range(max_steps):
            # os.system('clear')
            ob, reward, done, _ = env.step(action)
            if (random.random()<epsilon):
                print('-'*40,"Random Exploration",'-'*40)
                # action=np.array([random.uniform(-1,1)])
                action=np.array([random.randint(-1,1)])
            else:
                op = agent.act(env, ob, reward, done, vision)
                action = op[0]
            # new_ob = op[1]
            #print(ob)
            total_reward += reward
            print ("reward",reward)
            # prev_ob = new_ob
            step += 1
            if done:
                print('-'*80,'\nDone\n','-'*80)
                agent.pushToServer()
                break

        print("TOTAL REWARD @ " + str(i) +" -th Episode  :  " + str(total_reward))
        print("Total Step: " + str(step))
        print("")
        time.sleep(0.5)
    except KeyboardInterrupt:
        print ("process killed by user")
        os.system('pkill torcs')
        agent.dumpModels()
        quit()

env.end()  # This is for shutting down TORCS
print("Finish.")
