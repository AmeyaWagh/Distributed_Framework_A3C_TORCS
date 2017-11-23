import sys
import os
from inspect import getsourcefile
import json
import numpy as np
import traceback

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0,parent_dir)

from networks.models import ActorModel, CriticModel
from keras.optimizers import RMSprop, SGD

config=json.load(open("./torcs_central/config.json"))
resourcePath=config['resourcePath']
tempPath=config['tempPath']

class CentralModel():
    def __init__(self):
        self.OBSERVATION_SPACE = 1
        self.ACTION_SPACE = 1
        self.learningRate = config['learningRate']
        self.tau=config['tau']
        self.target_actor = ActorModel(self.OBSERVATION_SPACE,1).actor
        self.target_critic = CriticModel(self.ACTION_SPACE).critic
        self.worker_actor = ActorModel(self.OBSERVATION_SPACE,1).actor
        self.worker_critic = CriticModel(self.ACTION_SPACE).critic
        
        try:
            self.target_actor.load_weights(os.path.join(resourcePath, "actor.h5"))
            self.target_critic.load_weights(os.path.join(resourcePath, "critic.h5"))
        except Exception as e:
            print("could not load weights from resourcePath")

        self.c_optimizer = SGD(lr=self.learningRate, decay=1e-6, momentum=0.9, nesterov=True)
       
        self.target_actor.compile(loss='mse',
                             optimizer=self.c_optimizer,
                             metrics=['accuracy'])
        self.target_critic.compile(loss='mse',
                             optimizer=self.c_optimizer,
                             metrics=['accuracy'])

    def updateWeights(self):
        try:
            self.target_actor.load_weights(os.path.join(tempPath, "actor.h5"))
            self.target_critic.load_weights(os.path.join(tempPath, "critic.h5"))
            self.worker_actor.compile(loss='mse',
                             optimizer=self.c_optimizer,
                             metrics=['accuracy'])
            self.worker_critic.compile(loss='mse',
                             optimizer=self.c_optimizer,
                             metrics=['accuracy'])
            
            self.target_actor_weights = self.target_actor.get_weights()
            self.target_critic_weighs = self.target_critic.get_weights()

            self.worker_actor_weights = self.worker_actor.get_weights()
            self.worker_critic_weights = self.worker_critic.get_weights()

            for i in range(len(self.target_actor_weights)):
                self.target_actor_weights[i] = self.tau * self.worker_actor_weights[i] + (1 - self.tau)* self.target_actor_weights[i]
            self.target_actor.set_weights(self.target_actor_weights)

            for i in range(len(self.target_critic_weighs)):
                self.target_critic_weighs[i] = self.tau * self.worker_critic_weights[i] + (1 - self.tau)* self.target_critic_weighs[i]
            self.target_critic.set_weights(self.target_critic_weighs)

            self.target_actor.save_weights(os.path.join(resourcePath, "actor.h5"))
            self.target_critic.save_weights(os.path.join(resourcePath, "critic.h5"))
            print("model weighs updated")

        except Exception as e:
            traceback.print_exc()
            print("could not load weights from tempPath")