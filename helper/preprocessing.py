#!/usr/bin/python3
import numpy as np

class preProcess():
    '''
        preprocesses data obtained from observation 
        of the environment and creates a feature vector
    '''
    def __init__(self):
        self.observation = {}
        self.maxRpm=10000
        self.maxSpeed=200

    def getVector(self, observation, vision_on):
        self.featureVect = []
        if vision_on is False:
            focus, speedX, speedY, speedZ, opponents, rpm,\
                track, wheelSpinVel, angle = observation
            # input_vector=[focus,speedX,speedY,speedZ,opponents,rpm,track,wheelSpinVel]
        else:
            focus, speedX, speedY, speedZ, opponents, rpm, \
                track, wheelSpinVel, angle ,vision = observation
        #     observation['vision']=vision    

        # observation['focus']=focus
        # observation['speedX']=speedX
        # observation['speedY']=speedY
        # observation['speedZ']=speedZ
        # observation['opponents']=opponents
        # observation['rpm']=rpm
        # observation['track']=track
        # observation['wheelSpinVel']=wheelSpinVel
        # observation['angle']=angle

        '''
        convert everything from -1 to 1
        '''
        # angle -pi<a<pi
        self.featureVect.append(angle/np.pi)
        # self.featureVect.append(rpm/self.maxRpm)
        # self.featureVect.append(speedX/self.maxSpeed)

        self.featureVect = np.array(self.featureVect)
        vect_dim = np.shape(self.featureVect)

        return self.featureVect,vect_dim



    def __str__(self):
        helpStr = '''
        '''
        return helpStr