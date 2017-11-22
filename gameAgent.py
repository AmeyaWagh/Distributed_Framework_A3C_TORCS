import numpy as np
import matplotlib.pyplot as plt
# import keras
import time
from helper.preprocessing import preProcess
from networks.models import ActorModel, CriticModel
import random
from keras.models import model_from_json
from keras.optimizers import RMSprop, SGD
import os
from torcs_central.torcsWebClient import torcsWebClient
from keras.utils import plot_model
import json

class Agent(object):

    def __init__(self, dim_action, verbose=False,gamma=0.975,maxBuffLen=100,batchSize=50):
        self.dim_action = dim_action
        self.verbose = verbose
        self.preProcess = preProcess()
        self.ReplayBuffActor = list()
        self.ReplayBuffCritic = list()
        self.maxBuffLen = maxBuffLen
        self.modelPath = './models'
        self.plotterPath = './plots'
        self.OBSERVATION_SPACE = 1
        self.ACTION_SPACE = 1
        self.loadModel()  
        # self.actor = ActorModel(3,1).actor
        # self.critic = CriticModel(3).critic
        self.gamma = gamma
        self.batchSize = batchSize
        self.config = json.load(open('./torcs_central/config.json'))
        self.t_client = torcsWebClient(configPath="./torcs_central/config.json")
        # if self.t_client.pingServer():
        #     print("pulling weights")
        #     self.weights = self.t_client.pullData()
        # else:
        #     print("Error communicating with server")
        #     raise AttributeError("Could not able to connect to Server")

    def pushToServer(self,metaData):
        # payload = {
        #             "actor":[0,1,2,3,4],
        #             "critic":[0,1,2,3,4]
        #             }
        if self.t_client.pingServer(): 
            print("pushing metaData to server")           
            self.t_client.pushData(metaData)
        else:
            print("Error communicating with server")
            raise AttributeError("Could not able to connect to Server")

    def pullFromServer(self):
        if self.t_client.pingServer(): 
            print("pulling weights from server")           
            self.weights = self.t_client.pullData()
            print(self.weights)
        else:
            print("Error communicating with server")
            raise AttributeError("Could not able to connect to Server")
            
        if os.path.isdir(self.config['pulledModels']):
            self.actor.load_weights(os.path.join(self.config['pulledModels'], "actor.h5"))
            a_optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
            self.actor.compile(loss='mse',
                                 optimizer=a_optimizer,
                                 metrics=['accuracy'])
            self.critic.load_weights(os.path.join(self.config['pulledModels'], "critic.h5"))
            a_optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
            self.critic.compile(loss='mse',
                                 optimizer=a_optimizer,
                                 metrics=['accuracy'])


    def loadModel(self):
        '''
            load trained model from model.json and weights from model.h5
        '''
        self.actor=None
        self.critic=None

        if os.path.isdir(self.modelPath):
            if os.path.exists(os.path.join(self.modelPath,'actor.json')) and os.path.exists(os.path.join(self.modelPath,'actor.h5')):
                with open(
                        os.path.join(self.modelPath, 'actor.json'), 'r') as json_file:
                    loaded_model_json = json_file.read()

                loaded_model = model_from_json(loaded_model_json)

                # load weights into new model
                loaded_model.load_weights(os.path.join(self.modelPath, "actor.h5"))
                a_optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
                loaded_model.compile(loss='mse',
                                     optimizer=a_optimizer,
                                     metrics=['accuracy'])
                print("Loaded actor from disk")
                self.actor=loaded_model
            
            else:
                self.actor = ActorModel(self.OBSERVATION_SPACE,1).actor
                print("New Actor Created")
                    

            if os.path.exists(os.path.join(self.modelPath,'critic.json')) and os.path.exists(os.path.join(self.modelPath,'critic.h5')):
                with open(
                        os.path.join(self.modelPath, 'critic.json'), 'r') as json_file:
                    loaded_model_json = json_file.read()

                loaded_model = model_from_json(loaded_model_json)

                # load weights into new model
                loaded_model.load_weights(os.path.join(self.modelPath, "actor.h5"))
                c_optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
                loaded_model.compile(loss='mse',
                                     optimizer=c_optimizer,
                                     metrics=['accuracy'])
                print("Loaded critic from disk")
                self.critic=loaded_model
            else:
                self.critic = CriticModel(self.ACTION_SPACE).critic
                print("New Critic Created")

        else:
            if self.actor is None:
                self.actor = ActorModel(self.OBSERVATION_SPACE,1).actor
                print("New Actor Created")
            
            if self.critic is None:
                self.critic = CriticModel(self.ACTION_SPACE).critic
                print("New Critic Created")

            else:
                raise AttributeError("Something went wrong in loading models")    


    def dumpModels(self,metaData={}):
        if not os.path.isdir(self.modelPath):
            os.mkdir(self.modelPath)
            print("Directory created at ",self.modelPath)
        

        # Actor

        # serialize model to JSON
        model_json = self.actor.to_json()
        with open(os.path.join(self.modelPath,"actor.json"), "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.actor.save_weights(os.path.join(self.modelPath,"actor.h5"))
        print("Saved Actor to disk")

        # Critic
        # serialize model to JSON
        model_json = self.critic.to_json()
        with open(os.path.join(self.modelPath,"critic.json"), "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.critic.save_weights(os.path.join(self.modelPath,"critic.h5"))
        print("Saved Critic to disk")

        self.pushToServer(metaData)
        # print("weights:",self.actor.trainable_weights,type(self.actor.trainable_weights))
        # print("weights:",self.actor.trainable_weights,type(self.actor.trainable_weights))
        
        # if not os.path.isdir(self.plotterPath):
        #     os.mkdir(self.plotterPath)
        #     plot_model(self.actor, to_file=os.path.join(self.plotterPath,'actor.png'))
        #     plot_model(self.critic, to_file=os.path.join(self.plotterPath,'critic.png'))
    


    def debugger(self, *args, **kwargs):
        # for arg in args:
        if self.verbose is True:
            print(args)


    def act(self,env,ob,reward, done, vision_on):
        
        # os.system('clear')

        observation,vect_dim = self.preProcess.getVector(ob,vision_on)

        # [r,c] = vect_dim
        # self.debugger('observation',observation,'vect_dim',vect_dim)
        action = self.actor.predict(np.reshape(observation,(1,vect_dim[0]))) 
        # print("new_action",action)

        new_observation,new_reward,done,_ = env.step(np.array([action]))
        new_ob=new_observation
        new_observation,vect_dim = self.preProcess.getVector(new_observation,vision_on)
        # print('new_observation',new_observation,'new_reward',new_reward)    

        orig_val = self.critic.predict(np.reshape(observation,(1,vect_dim[0])))
        # print('orig_val',orig_val,'new_action',action)

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
        # print('shape of Actor replay',np.shape(self.ReplayBuffActor))
        # print('shape of Critic replay',np.shape(self.ReplayBuffCritic))

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
            # print('X_train shape',np.shape(X_train))
            print('train Critic')
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
            print('train Actor')
            self.actor.fit(X_train, y_train, batch_size=self.batchSize, epochs=1, verbose=1)


        # steerAngle = np.tanh(20*observation[0]) #observation[0] is angle
        steerAngle = 50*action[0][0]
        
        steerAngle = np.array([steerAngle])
        print('steerAngle',steerAngle)
        return steerAngle,new_ob  # random action
