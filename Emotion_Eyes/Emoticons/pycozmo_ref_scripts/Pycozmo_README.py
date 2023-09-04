#Readme file to better help with documenting Pycozmo programs
#this is based off of the documentation and the examples found on the
#pycozmo script


#Format of every code goes as follows
import pycozmo

with pycozmo.connect() as cli: 
	cli.<something something something>
#first connect the robot to the computer
#use the client object to reference other objects


#minimal.py has a demonstration of the minimum code necessary to have a working
#pycozmo script

import time
import pycozmo
with pycozmo.connect() as cli:
    while True:
        time.sleep(0.1)


#how to get the head to tilt in a specific angle
angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
cli.set_head_angle(angle) 


#how to define paramters for angle, distance, speed, expression, and duration

