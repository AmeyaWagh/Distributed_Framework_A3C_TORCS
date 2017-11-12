#!/usr/bin/python3
from gym_torcs.gym_torcs import TorcsEnv
from gameAgent import Agent
import numpy as np
import os
import time

vision = False
episode_count = 10
max_steps = 5000
reward = 0
done = False
step = 0

# Generate a Torcs environment
env = TorcsEnv(vision=vision, throttle=False ,textMode=True,xmlPath='./gym_torcs/practice.xml')

agent = Agent(1,verbose=True)  # steering only


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
        for j in range(max_steps):
            action = agent.act(ob, reward, done, vision)

            ob, reward, done, _ = env.step(action)
            #print(ob)
            total_reward += reward
            print ("reward",reward)

            step += 1
            if done:
                print('-'*80,'\nDone\n','-'*80)
                break

        print("TOTAL REWARD @ " + str(i) +" -th Episode  :  " + str(total_reward))
        print("Total Step: " + str(step))
        print("")
        time.sleep(0.5)
    except KeyboardInterrupt:
        print ("process killed by user")
        os.system('pkill torcs')
        quit()

env.end()  # This is for shutting down TORCS
print("Finish.")
