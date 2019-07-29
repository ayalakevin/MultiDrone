import airsim
import cv2
import numpy as np
import os
import pprint
import setup_path 
import tempfile
import time
import math

# Use below in settings.json with Blocks environment
"""
{
	"SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
	"SettingsVersion": 1.2,
	"SimMode": "Multirotor",
	"ClockSpeed": 1,
	
	"Vehicles": {
                "PX4": {
                  "VehicleType": "PX4Multirotor",
                  "X": -2, "Y": 0, "Z": -1,
                  "LogViewerHostIp": "127.0.0.1",
                  "LogViewerPort": 14388,
                  "OffboardCompID": 1,
                  "OffboardSysID": 134,
                  "QgcHostIp": "127.0.0.1",
                  "QgcPort": 14550,
                  "SerialBaudRate": 115200,
                  "SerialPort": "*",
                  "SimCompID": 42,
                  "SimSysID": 142,
                  "SitlIp": "127.0.0.1",
                  "SitlPort": 14556,
                  "UdpIp": "127.0.0.1",
                  "UdpPort": 14560,
                  "UseSerial": true,
                  "VehicleCompID": 1,
                  "VehicleSysID": 135,
                  "Model": "Generic",
                  "LocalHostIp": "127.0.0.1"
                },
		"Drone1": {
		  "VehicleType": "SimpleFlight",
		  "X": 0, "Y": 0, "Z": -1
		},
		"Drone2": {
		  "VehicleType": "SimpleFlight",
		  "X": 12, "Y": 1, "Z": -1
		},
		"Drone3": {
		  "VehicleType": "SimpleFlight",
		  "X": 25, "Y": 1, "Z": -1
		}
	}
}
"""


# connect to the AirSim simulator

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True, "Drone1")
client.enableApiControl(True, "Drone2")
client.enableApiControl(True, "Drone3")
client.armDisarm(True, "Drone1")
client.armDisarm(True, "Drone2")
client.armDisarm(True, "Drone3")
airsim.DrivetrainType.ForwardOnly


#                                                           T A K E O F F
airsim.wait_key('Taking Off')
f1 = client.takeoffAsync(vehicle_name="Drone1")
f2 = client.takeoffAsync(vehicle_name="Drone2")
f3 = client.takeoffAsync(vehicle_name="Drone3")
f1.join()
f2.join()
f3.join()

#                                                           S T A T U S - U P D A T E
'''
state1 = client.getMultirotorState(vehicle_name="Drone1")
state2 = client.getMultirotorState(vehicle_name="Drone2")
s1 = pprint.pformat(state1)
s2 = pprint.pformat(state2)
print("state: %s" % s1)
print("state: %s" % s2)
'''
time.sleep(3)

#                                                       D R O N E S - M O V I N G

airsim.wait_key('Moving To Position')
move1 = (40,0,-2,1)
f1 = client.moveToPositionAsync(move1[0], move1[1], move1[2], move1[3], vehicle_name="Drone1")

for i in range(500):
    
    pos1 = (client.getMultirotorState("Drone1").kinematics_estimated.position.x_val,
          client.getMultirotorState("Drone1").kinematics_estimated.position.y_val,
          client.getMultirotorState("Drone1").kinematics_estimated.position.z_val)

    pos2 = (client.getMultirotorState("Drone2").kinematics_estimated.position.x_val+12,
          client.getMultirotorState("Drone2").kinematics_estimated.position.y_val+1,
          client.getMultirotorState("Drone2").kinematics_estimated.position.z_val)

    pos3 = (client.getMultirotorState("Drone3").kinematics_estimated.position.x_val+18,
          client.getMultirotorState("Drone3").kinematics_estimated.position.y_val+1,
          client.getMultirotorState("Drone3").kinematics_estimated.position.z_val)

    distance12 = math.sqrt( ((pos2[0]-pos1[0])**2)+((pos2[1]-pos1[1])**2)+((pos2[2]-pos1[2])**2) )
    distance13 = math.sqrt( ((pos3[0]-pos1[0])**2)+((pos3[1]-pos1[1])**2)+((pos3[2]-pos1[2])**2) )
    print('This is the DISTANCE of 1&2~~~~~~~~~~~~~~~~~~',distance12)
    print('This is the DISTANCE of 1&3~~~~~~~~~~~~~~~~~~',distance13)

    if (distance12 > 3 and distance12 <=6) or (distance13 > 3 and distance13 <=6):
        print('Entering Danger Bubble')
    elif distance12 <= 2:
        client.landAsync(vehicle_name="Drone2")
        print('Landing Drone 2')
    elif distance13 <=2:
        client.landAsync(vehicle_name="Drone3")
        print('Landing Drone 3')
    else:
        print('...')

