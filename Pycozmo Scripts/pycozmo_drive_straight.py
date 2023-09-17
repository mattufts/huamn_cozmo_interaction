# from threading import Event

# import pycozmo

# SPEED_MMPS = 100.0
# ACCEL_MMPS2 = 20.0
# DECEL_MMPS2 = 20.0

# e = Event()

# #on_path_following_event is for the robot to stop after it has completed the path
# def on_path_following_event(cli, pkt: pycozmo.protocol_encoder.PathFollowingEvent):
#     print(pkt.event_type)
#     # if the packet is not a path started event, set the event
#     if pkt.event_type != pycozmo.protocol_encoder.PathEventType.PATH_STARTED:
#         #set the event
#         e.set()

# def on_robot_pathing_change(cli, state: bool):
#     if state:
#         print("Started pathing.")
#     else:
#         print("Stopped pathing.")


# #connect to the robot
# with pycozmo.connect() as cli:
#     #add the event handlers
#     cli.add_handler(pycozmo.protocol_encoder.PathFollowingEvent, on_path_following_event)
#     #add the event handler to the robot pathing change event
#     cli.add_handler(pycozmo.event.EvtRobotPathingChange, on_robot_pathing_change)

#     #pkt is for the robot to drive straight
#     pkt = pycozmo.protocol_encoder.AppendPathSegLine(
#         #from_x and from_y are the starting coordinates
#         from_x=0.0, from_y=0.0,
#         #to_x and to_y are the ending coordinates
#         to_x=150.0, to_y=0.0,
#         #speed_mmps is the speed of the robot in millimeters per second
#         speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
#     #send the packet
#     cli.conn.send(pkt)
#     #pkt is for the robot to execute the path
#     pkt = pycozmo.protocol_encoder.ExecutePath(event_id=1)
#     cli.conn.send(pkt)

#     e.wait(timeout=30.0)


#simplified drive forward script
import pycozmo
cli = pycozmo.Client()
cli.start()
cli.connect()
cli.wait_for_robot()

#Set the animations to False for turning off the background animations
#doing this will turn the animations off as the robot moves
cli.anim_controller.enable_animations(False)


cli.anim_controller.enable_animations()
# pycozmo.anim_controller.stop()
cli.drive_wheels(lwheel_speed=50.0, rwheel_speed=50.0, duration=6.0)
cli.disconnect()
cli.stop()
