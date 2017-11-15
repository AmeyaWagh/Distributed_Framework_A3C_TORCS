import numpy as np
import matplotlib.pyplot as plt
# import keras
import time
from helper.preprocessing import preProcess
from networks.models import ActorModel, CriticModel
import random

class Agent(object):

    def __init__(self, dim_action, verbose=False,gamma=0.975,batchSize=10):
        self.dim_action = dim_action
        self.verbose = verbose
        self.preProcess = preProcess()
        self.ReplayBuffActor = list()
        self.ReplayBuffCritic = list()
        self.maxBuffLen = 20
        self.actor = ActorModel(3,1).actor
        self.critic = CriticModel(3).critic
        self.gamma = gamma
        self.batchSize = batchSize

    def debugger(self, *args, **kwargs):
        # for arg in args:
        if self.verbose is True:
            print(args)

    def act(self,env,ob,reward, done, vision_on):
        
        observation,vect_dim = self.preProcess.getVector(ob,vision_on)

        # [r,c] = vect_dim
        self.debugger('observation',observation,'vect_dim',vect_dim)
        action = self.actor.predict(np.reshape(observation,(1,vect_dim[0]))) 
        print("new_action",action)

        new_observation,new_reward,done,_ = env.step(np.array([action]))
        new_ob=new_observation
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
        print('shape of Actor replay',np.shape(self.ReplayBuffActor))
        print('shape of Critic replay',np.shape(self.ReplayBuffCritic))

        # Critic Replay training
        if len(self.ReplayBuffCritic) > self.maxBuffLen:
            self.ReplayBuffCritic.pop(0)
            print('-')
            minibatch = random.sample(self.ReplayBuffCritic,self.batchSize)
            X_train=[]
            y_train=[]
            for memory in minibatch:
                _state,_val=memory
                _val=np.array([_val])
                X_train.append(np.reshape(_state,(vect_dim[0],)))
                y_train.append(np.reshape(_val,(1,)))
            X_train=np.array(X_train)
            y_train=np.array(y_train)
            print('X_train shape',np.shape(X_train))
            self.critic.fit(X_train,y_train,batch_size=self.batchSize,epochs=1,verbose=1)

        if len(self.ReplayBuffActor) > self.maxBuffLen:
            self.ReplayBuffActor.pop(0)
            print('-')
            X_train = []
            y_train = []
            minibatch = random.sample(self.ReplayBuffActor, self.batchSize)
            for memory in minibatch:
                m_orig_state, m_action, m_value = memory
                old_qval = self.actor.predict( m_orig_state.reshape(1,vect_dim[0],) )
                y=np.array([old_qval])
                X_train.append(m_orig_state.reshape((vect_dim[0],)))
                y_train.append(y.reshape((1,)))
            X_train = np.array(X_train)
            y_train = np.array(y_train)
            self.actor.fit(X_train, y_train, batch_size=self.batchSize, epochs=1, verbose=1)


        # steerAngle = np.tanh(20*observation[0]/3.14) #observation[0] is angle
        steerAngle = action
        
        steerAngle = np.array([steerAngle])
        print('steerAngle',type(steerAngle),steerAngle)
        return steerAngle,new_ob  # random action
