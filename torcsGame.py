#!/usr/bin/python3
from gym_torcs.gym_torcs import TorcsEnv
from gameAgent import Agent
import numpy as np
import os
import time
import random
import json
config=json.load(open("./torcs_central/config.json"))

vision = False
episode_count = config['maxEpisodes']
max_steps = config['maxSteps']
reward = 0
done = False
step = 0

# Generate a Torcs environment
env = TorcsEnv(vision=vision, 
    throttle=False ,
    default_speed=config['default_speed'] ,
    textMode=True,xmlPath='./gym_torcs/practice.xml')

agent = Agent(1,verbose=True)  # steering only

epsilon=config['exploration']

print("TORCS Experiment Start.")
for i in range(episode_count):
    try:
        print("Episode : " + str(i))

        agent.pullFromServer()
        time.sleep(1)
        if np.mod(i, 3) == 0:
            # Sometimes you need to relaunch TORCS because of the memory leak error
            ob = env.reset(relaunch=True)
            
        else:
            ob = env.reset()

        total_reward = 0.
        
        action=np.array([np.random.normal(0,1)])

        for j in range(max_steps):
            ob, reward, done, _ = env.step(action)

            action = agent.act(env, ob, reward, done, vision)[0]  

            total_reward += reward
            print ("reward",reward)
            step += 1
            if done:
                print('-'*80,'\nDone\n','-'*80)
                # agent.pushToServer()
                agent.dumpModels(metaData={'total_reward':total_reward,
                                            'steps_taken':step,
                                            'episode_done':i
                                            })
                time.sleep(1)
                break

        print("TOTAL REWARD @ " + str(i) +" -th Episode  :  " + str(total_reward))
        print("Total Step: " + str(step))
        print("")
        time.sleep(0.5)
    except KeyboardInterrupt:
        print ("process killed by user")
        os.system('pkill torcs')
        agent.dumpModels(metaData={'total_reward':total_reward,
                                            'steps_taken':step,
                                            'episode_done':i
                                            })
        quit()

    # finally:
    #     print ("process killed by system")
    #     os.system('pkill torcs')
    #     agent.dumpModels(metaData={'total_reward':total_reward,
    #                                         'steps_taken':step,
    #                                         'episode_done':i
    #                                         })
    #     quit()

env.end()  # This is for shutting down TORCS
print("Finish.")
