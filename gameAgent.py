import numpy as np
import matplotlib.pyplot as plt
# import keras
import time
from helper.preprocessing import preProcess
from networks.models import ActorModel, CriticModel

class Agent(object):

    def __init__(self, dim_action, verbose=False,gamma=0.975):
        self.dim_action = dim_action
        self.verbose = verbose
        self.preProcess = preProcess()
        self.ReplayBuffActor = list()
        self.ReplayBuffCritic = list()
        self.maxBuffLen = 80
        self.actor = ActorModel(3,1).actor
        self.critic = CriticModel(3).critic
        self.gamma = gamma

    def debugger(self, *args, **kwargs):
        # for arg in args:
        if self.verbose is True:
            print(args)

    def act(self,env,ob, prev_ob,reward, done, vision_on):
        
        observation,vect_dim = self.preProcess.getVector(ob,vision_on)

        # [r,c] = vect_dim
        self.debugger('observation',observation,'vect_dim',vect_dim)
        action = self.actor.predict(np.reshape(observation,(1,vect_dim[0]))) 
        print("new_action",action)

        new_observation,new_reward,done,_ = env.step(np.array([action]))
        new_observation,vect_dim = self.preProcess.getVector(new_observation,vision_on)
        print('new_observation',new_observation,'new_reward',new_reward)    

        orig_val = self.critic.predict(np.reshape(observation,(1,vect_dim[0])))
        print('orig_val',orig_val,'new_action',action)

        new_val = self.critic.predict(np.reshape(new_observation,(1,vect_dim[0])))

        if not done:
            target = reward + self.gamma*new_val
        else:
            target = reward + self.gamma*new_reward

        best_val = max((orig_val*self.gamma),target)


        self.ReplayBuffCritic.append([observation,best_val])
        if done is True:
            self.ReplayBuffCritic.append([new_observation,float(new_reward)])


        actor_delta = new_val - orig_val


        self.ReplayBuffActor.append([observation,action,actor_delta])
        
        #--------------------------------------------------------------------------------#
        print('shape of replay',np.shape(self.ReplayBuffActor))

        if len(self.ReplayBuffActor) > 80:
            self.ReplayBuffActor.pop(0)
            print('-')

        steerAngle = np.tanh(20*observation[0]/3.14) #observation[0] is angle
        
        steerAngle = np.array([steerAngle])
        print('steerAngle',type(steerAngle),steerAngle)
        return steerAngle  # random action
