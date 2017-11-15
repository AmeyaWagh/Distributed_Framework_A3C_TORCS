#!/usr/bin/python3
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop, SGD


HIDDEN_LAYER1=300
HIDDEN_LAYER2=600

class ActorModel():
    def __init__(self,OBSERVATION_SPACE,ACTION_SPACE):
        self.OBSERVATION_SPACE = OBSERVATION_SPACE
        self.ACTION_SPACE = ACTION_SPACE
        self.actor = self.actorModel()

    def actorModel(self):
        actor_model = Sequential()
        actor_model.add(Dense(HIDDEN_LAYER1, kernel_initializer='lecun_uniform', input_shape=(self.OBSERVATION_SPACE,)))
        actor_model.add(Activation('relu'))

        actor_model.add(Dense(HIDDEN_LAYER2, kernel_initializer='lecun_uniform'))
        actor_model.add(Activation('relu'))

        actor_model.add(Dense(self.ACTION_SPACE, kernel_initializer='lecun_uniform'))
        actor_model.add(Activation('tanh'))

        a_optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        actor_model.compile(loss='mse', optimizer=a_optimizer)
        return actor_model

class CriticModel():
    def __init__(self,OBSERVATION_SPACE):
        self.OBSERVATION_SPACE = OBSERVATION_SPACE
        self.critic = self.criticModel()

    def criticModel(self):
        critic_model = Sequential()
        critic_model.add(Dense(HIDDEN_LAYER1, kernel_initializer='lecun_uniform', input_shape=(self.OBSERVATION_SPACE,)))
        critic_model.add(Activation('relu'))
        critic_model.add(Dense(HIDDEN_LAYER2, kernel_initializer='lecun_uniform'))
        critic_model.add(Activation('relu'))
        critic_model.add(Dense(1, kernel_initializer='lecun_uniform'))
        critic_model.add(Activation('linear'))

        c_optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
        critic_model.compile(loss='mse', optimizer=c_optimizer)
        
        return critic_model

class A3C():
    def __init__(self):
        pass