#cozmo robot calibration
#This script will run in the background of cozmo is used to test out cozmo's
#wheel odometry.

#!/usr/bin/env python
#example of threading different movements with cozmo 

from threading import Event

import pycozmo


SPEED_MMPS = 100.0
ACCEL_MMPS2 = 20.0
DECEL_MMPS2 = 20.0

e = Event()


def on_path_following_event(cli, pkt: pycozmo.protocol_encoder.PathFollowingEvent):
    print(pkt.event_type) #update the pathing change with the threading object "Event"
    if pkt.event_type != pycozmo.protocol_encoder.PathEventType.PATH_STARTED: 
        #if the event type does not match the current path type
        e.set() #set the current event type
        # Accumulate distances
        total_distance_x += pkt.delta_x_mm
        total_distance_y += pkt.delta_y_mm

        print(f"Total Distance (x, y): ({total_distance_x} mm, {total_distance_y} mm)")


def on_robot_pathing_change(cli, state: bool):
    if state:
        print("Started pathing.")
    else:
        print("Stopped pathing.")


with pycozmo.connect() as cli:
    cli.add_handler(pycozmo.protocol_encoder.PathFollowingEvent, on_path_following_event)
    cli.add_handler(pycozmo.event.EvtRobotPathingChange, on_robot_pathing_change)

    while True:
        pkt = pycozmo.protocol_encoder.AppendPathSegLine(
            from_x=0.0, from_y=0.0,
            to_x=150.0, to_y=0.0,
            speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
        cli.conn.send(pkt)
        pkt = pycozmo.protocol_encoder.AppendPathSegLine(
            from_x=254.0, from_y=0.0,
            to_x=254.0, to_y=254.0,
            speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
        cli.conn.send(pkt)
        pkt = pycozmo.protocol_encoder.AppendPathSegLine(
            from_x=254.0, from_y=254.0,
            to_x=0.0, to_y=254.0,
            speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
        cli.conn.send(pkt)
        pkt = pycozmo.protocol_encoder.AppendPathSegLine(
            from_x=0.0, from_y=254.0,
            to_x=0.0, to_y=0.0,
            speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
        cli.conn.send(pkt)
        pkt = pycozmo.protocol_encoder.AppendPathSegPointTurn(
            x=0.0, y=0.0,
            angle_rad=pycozmo.util.Angle(degrees=0.0).radians,
            angle_tolerance_rad=0.01,
            speed_mmps=SPEED_MMPS, accel_mmps2=ACCEL_MMPS2, decel_mmps2=DECEL_MMPS2)
        cli.conn.send(pkt)

        pkt = pycozmo.protocol_encoder.ExecutePath(event_id=1)
        cli.conn.send(pkt)

        e.wait(timeout=30.0)
