import numpy as np
import matplotlib.pyplot as plt
# import keras
import time

class Agent(object):
    def __init__(self, dim_action):
        self.dim_action = dim_action

    def act(self, ob, reward, done, vision_on):
        #print("ACT!")

        # Get an Observation from the environment.
        # Each observation vectors are numpy array.
        # focus, opponents, track sensors are scaled into [0, 1]. When the agent
        # is out of the road, sensor variables return -1/200.
        # rpm, wheelSpinVel are raw values and then needed to be preprocessed.
        # vision is given as a tensor with size of (64*64, 3) = (4096, 3) <-- rgb
        # and values are in [0, 255]
        if vision_on is False:
            focus, speedX, speedY, speedZ, opponents, rpm, track, wheelSpinVel,angle = ob
            # input_vector=[focus,speedX,speedY,speedZ,opponents,rpm,track,wheelSpinVel]
        else:
            focus, speedX, speedY, speedZ, opponents, rpm, track, wheelSpinVel, vision = ob

            """ The code below is for checking the vision input. This is very heavy for real-time Control
                So you may need to remove.
            """
            print(vision.shape)
            
            # img = np.ndarray((64,64,3))
            # for i in range(3):
            #     img[:, :, i] = 255 - vision[:, i].reshape((64, 64))

            # plt.imshow(img, origin='lower')
            # plt.draw()
            # plt.pause(0.001)

        print ("speedX",speedX)
        print ("speedY",speedY)
        print ("speedZ",speedZ)
        # print ("opponents",opponents)
        print ("focus",focus) # 5 range finder sensors
        print ("track",track) # 19 range finder sensors

        print ("angle",angle)
        print ("rpm",rpm)
        print ("wheelSpinVel",wheelSpinVel)
        # print(input_vector)

        # steerAngle = 0
        # if speedY<0:
        #     steerAngle = 0.99
        # elif speedY>0:
        #     steerAngle = -0.99
        # else:
        #     steerAngle = 0.00

        steerAngle = angle/3.14
        # time.sleep(0.1)
        # steerAngle = np.tanh(np.random.randn(self.dim_action))
        print("steerAngle:",steerAngle)
        # return np.tanh(np.random.randn(self.dim_action)) # random action
        return [steerAngle] # random action
