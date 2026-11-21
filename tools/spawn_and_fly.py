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


for i in range(1, 60): #
    name=f"Drone{i}"
    x=2*(i//10)
    y=2*(i%10)
    z=0

    client.simAddVehicle(name, "SimpleFlight", airsim.Pose(airsim.Vector3r(x,y,z), airsim.Quaternionr(0,0,0)))
    print("Drones up:", i+1)
    time.sleep(0.001)

print("client.listVehicles(): ", client.listVehicles())

all_drones=client.listVehicles()
for name in all_drones:
    client.enableApiControl(True, name)
    client.armDisarm(True, name)

tasks=[]
for name in all_drones:
    tasks.append(client.moveToZAsync(-10, 10, vehicle_name=name))

for t in tasks:
    t.join()

print("All", len(all_drones), "up")



