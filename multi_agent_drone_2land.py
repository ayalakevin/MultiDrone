import airsim
import cv2
import numpy as np
import os
import pprint
import setup_path 
import tempfile
import time
import math

#kevin ayala path
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
                  "X": 0, "Y": 0, "Z": -2,
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
                }
		"Drone1": {
		  "VehicleType": "SimpleFlight",
		  "X": 4, "Y": 0, "Z": -2
		},
		"Drone2": {
		  "VehicleType": "SimpleFlight",
		  "X": 8, "Y": 0, "Z": -2
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
#print("taking off")
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
'''
move2 = (-12, 0,-2,1)
f2 = client.moveToPositionAsync(move2[0], move2[1], move2[2], move2[3], vehicle_name="Drone2")

iterations = 0
'''
for i in range(500):
    #pos = client.getMultirotorState("Drone1")
    #print(pos)
    pos1 = (client.getMultirotorState("Drone1").kinematics_estimated.position.x_val,
          client.getMultirotorState("Drone1").kinematics_estimated.position.y_val,
          client.getMultirotorState("Drone1").kinematics_estimated.position.z_val)
    #print(pos1[0],pos1[1],pos1[2])

    pos2 = (client.getMultirotorState("Drone2").kinematics_estimated.position.x_val+12,
          client.getMultirotorState("Drone2").kinematics_estimated.position.y_val+1,
          client.getMultirotorState("Drone2").kinematics_estimated.position.z_val)

    pos3 = (client.getMultirotorState("Drone3").kinematics_estimated.position.x_val+18,
          client.getMultirotorState("Drone3").kinematics_estimated.position.y_val+1,
          client.getMultirotorState("Drone3").kinematics_estimated.position.z_val)

    #print(pos2[0],pos2[1],pos2[2])

    distance12 = math.sqrt( ((pos2[0]-pos1[0])**2)+((pos2[1]-pos1[1])**2)+((pos2[2]-pos1[2])**2) )
    distance13 = math.sqrt( ((pos3[0]-pos1[0])**2)+((pos3[1]-pos1[1])**2)+((pos3[2]-pos1[2])**2) )
    print('This is the DISTANCE of 1&2~~~~~~~~~~~~~~~~~~',distance12)
    print('This is the DISTANCE of 1&3~~~~~~~~~~~~~~~~~~',distance13)

    
    #print(pos1[0],pos1[1],pos1[2])
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

    '''    
    if distance12 <= 2:
        client.landAsync(vehicle_name="Drone2")
        print('Landing Drone 2')
    elif distance13 <=2:
        client.landAsync(vehicle_name="Drone3")
        print('Landing Drone 3')
    elif distance12 > 2 and distance12 <=6:
        print('Getting Close 12')
    elif distance13 > 2 and distance13 <=6:
        print('Getting Close 13~~~~~~')
    else:
        print('...')
      '''  
        
    



#time.sleep(seconds)
#time.sleep(3)
'''
airsim.wait_key('Moving To NEW Position')
f1 = client.moveToPositionAsync(10, 0, -4, 5, vehicle_name="Drone1")
f2 = client.moveToPositionAsync(9, 0, -5, 5, vehicle_name="Drone2")
f1.join()
f2.join()
time.sleep(1)
'''
#                                                               L A N D I N G
'''
global land
airsim.wait_key('Attempting To Land')
landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("landing...")
    f3 = client.landAsync(vehicle_name="Drone1")
    f4 = client.landAsync(vehicle_name="Drone2")
    f3.join()
    f4.join()
else:
    print("already landed...")
    '''

'''
airsim.wait_key('Attempting To Land')
landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("landing...")
    f3 = client.landAsync(vehicle_name="Drone1")
    f3.join()
else:
    print("already landed...")
    
landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("already landed...") 
else:
    print("landing...")
    f4 = client.landAsync(vehicle_name="Drone2")
    f4.join()

'''
'''
airsim.wait_key('Press any key to take images')
# get camera images from the car
responses1 = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
    airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)], vehicle_name="Drone1")  #scene vision image in uncompressed RGB array
print('Drone1: Retrieved images: %d' % len(responses1))
responses2 = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
    airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)], vehicle_name="Drone2")  #scene vision image in uncompressed RGB array
print('Drone2: Retrieved images: %d' % len(responses2))

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
print ("Saving images to %s" % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

for idx, response in enumerate(responses1 + responses2):

    filename = os.path.join(tmp_dir, str(idx))

    if response.pixels_as_float:
        print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
        airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
    elif response.compress: #png format
        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
    else: #uncompressed array
        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) #get numpy array
        img_rgb = img1d.reshape(response.height, response.width, 3) #reshape array to 3 channel image array H X W X 3
        cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png

airsim.wait_key('Press any key to reset to original state')

client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")
client.reset()

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False, "Drone1")
client.enableApiControl(False, "Drone2")
'''










#JUST PX4
'''
{
	"SeeDocsAt": "https://github.com/Microsoft/AirSim/blob/master/docs/settings.md",
	"SettingsVersion": 1.2,
	"SimMode": "Multirotor",
	"ClockSpeed": 1,
	
	"Vehicles": {
                "PX4": {
                  "VehicleType": "PX4Multirotor",
                  "X": 0, "Y": 0, "Z": -5,
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
                }
	}
}
'''
