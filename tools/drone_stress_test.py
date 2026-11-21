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

client.enableApiControl(True, "Drone0")
client.armDisarm(True, "Drone0")
client.takeoffAsync(vehicle_name="Drone0").join()

for i in range(1, 101):
    name=f"Drone{i}"
    x=(i//10)
    y=1+2*(i%10)
    z=0

    client.simAddVehicle(name, "SimpleFlight", airsim.Pose(airsim.Vector3r(x,y,z), airsim.Quaternionr(0,0,0)))
    client.enableApiControl(True, name)
    client.armDisarm(True, name)
    client.takeoffAsync(vehicle_name=name).join()
    print("Drones up:", i+1)
    time.sleep(1.0)

print("client.listVehicles(): ", client.listVehicles())

