import numpy as np
import matplotlib.pyplot as plt
# import keras
import time
from helper.preprocessing import preProcess

class Agent(object):

    def __init__(self, dim_action, verbose=False):
        self.dim_action = dim_action
        self.verbose = verbose
        self.preProcess = preProcess()

    def debugger(self, *args, **kwargs):
        # for arg in args:
        if self.verbose is True:
            print(args)

    def act(self, ob, reward, done, vision_on):
        # print("ACT!")

        # Get an Observation from the environment.
        # Each observation vectors are numpy array.
        # focus, opponents, track sensors are scaled into [0, 1]. When the agent
        # is out of the road, sensor variables return -1/200.
        # rpm, wheelSpinVel are raw values and then needed to be preprocessed.
        # vision is given as a tensor with size of (64*64, 3) = (4096, 3) <-- rgb
        # and values are in [0, 255]
        if vision_on is False:
            focus, speedX, speedY, speedZ, opponents, rpm,\
                track, wheelSpinVel, angle = ob
            # input_vector=[focus,speedX,speedY,speedZ,opponents,rpm,track,wheelSpinVel]
        else:
            focus, speedX, speedY, speedZ, opponents, rpm, \
                track, wheelSpinVel, vision = ob

            """ The code below is for checking the vision input. 
                This is very heavy for real-time Control
                So you may need to remove.
            """
            print(vision.shape)

        print ("speedX",speedX)
        print ("speedY",speedY)
        print ("speedZ",speedZ)
        # print ("opponents",opponents)
        print ("focus",focus) # 5 range finder sensors
        print ("track",track) # 19 range finder sensors

        print ("angle",angle)
        print ("rpm",rpm)
        print ("wheelSpinVel",wheelSpinVel)

        # self.debugger("speedX", speedX)
        # self.debugger("speedY", speedY)
        # self.debugger("speedZ", speedZ)
        # self.debugger("opponents",opponents)
        # self.debugger("focus", focus)  # 5 range finder sensors
        # self.debugger("track", track)  # 19 range finder sensors

        # self.debugger("angle", angle)
        # self.debugger("rpm", rpm)
        # self.debugger("wheelSpinVel", wheelSpinVel)


        # steerAngle = angle/3.14
        featureVect,vect_dim = self.preProcess.getVector(ob,vision_on)
        
        self.debugger('featureVect',featureVect,'vect_dim',vect_dim)


        steerAngle = np.tanh(10*angle/3.14)
        # time.sleep(0.1)
        # steerAngle = np.tanh(np.random.randn(self.dim_action))
        print("steerAngle:", steerAngle/3.14,'\n')
        # steerout = np.tanh(np.random.randn(self.dim_action)) # random action
        # print("steerout",type(steerout),steerout)
        # return steerout

        steerAngle = np.array([steerAngle])
        print('steerAngle',type(steerAngle),steerAngle)
        return steerAngle  # random action
