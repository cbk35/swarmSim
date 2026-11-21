import airsim
import time

client = airsim.MultirotorClient()
client.confirmConnection()

print("Connected to AirSim")
hold_north=airsim.YawMode(False, 0)

vehicles=client.listVehicles()
if len(vehicles) > 1:
    print("Leftover vehicles from previous run", vehicles, "-stop and restart play to run again")
    exit()

x=0
y=1
z=0

client.enableApiControl(True, "Drone0")
client.armDisarm(True, "Drone0")

client.simAddVehicle("Drone1", "SimpleFlight", airsim.Pose(airsim.Vector3r(x,y,z), airsim.Quaternionr(0,0,0)))
client.enableApiControl(True, "Drone1")
client.armDisarm(True, "Drone1")

print("client.listVehicles(): ", client.listVehicles())

