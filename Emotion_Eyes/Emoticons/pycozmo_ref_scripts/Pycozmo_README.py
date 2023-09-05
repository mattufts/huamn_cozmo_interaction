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
head_angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
cli.set_head_angle(head_angle) 
time.sleep(1) #may be optional


#how to make cozmo go to a specific pose
#this is used in go_to_pose.py script
#it utilizes the pycozmo.util object
with pycozmo.connect() as cli:
	target = pycozmo.util.Pose(200, 100.0, 0.0, angle_z =pycozmo.util.Angle(degrees=0.0))
	cli.go_to_pose(target, relative_to_robot=True)


#how to define paramters for angle, distance, speed, expression, and duration
#this is made use of int the path.py script
SPEED_MMPS = 100.0 
ACCEL_MMPS2 = 20.0
DECEL_MMPS2 = 20.0 #keep these as global variables

e = Event()  #this is part of the threading function 

def on_path_following(......)
	#this is for event handling using the 'threading' library

with pycozmo.connect() as cli:
		cli.add_handler(pycozmo.protocol_encoder.PathFollowingEvent, on_path_following)  #event handling for following events
		cli.add_handler(pycozmo.EvtRobotPathingChang, on_robot_pathing_change) #event handling print statements
		
		#use the pycozmo object protocol_encoder and AppendPathSegLine to 
		#obtain the values for from_x, from_y and to_x and to_y for where the 
		#robot will be travelling
		pkt = pycozmo.protocol_encoder.AppendPathSegLine(
			from_x = 0.0, from_y = 0.0
			to_x = 150.0, to_y = 0.0 
			speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2 = DECEL_MMPS2)
		cli.conn.send(pkt) #send and update the variables using the protocol_encoder and pkt object




