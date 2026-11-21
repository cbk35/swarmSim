import airsim
import time
import csv

client = airsim.MultirotorClient()
client.confirmConnection()

print("Connected to AirSim")
hold_north=airsim.YawMode(False, 0)

all_drones=client.listVehicles()

with open("results/collision_report.csv", "w", newline='') as f:
    writer=csv.writer(f)
    writer.writerow(["phase", "drone", "altitude_m", "has_collided", "object_name"])  # header: added "phase"

    for name in all_drones:
          info=client.simGetCollisionInfo(vehicle_name=name)
          z=client.getMultirotorState(vehicle_name=name).kinematics_estimated.position.z_val
          writer.writerow(["before", name, -z, info.has_collided, info.object_name])  # row: added "before", -

for name in all_drones:
    client.enableApiControl(True, name)
    client.armDisarm(True, name)

tasks=[]
for name in all_drones:
    tasks.append(client.moveToZAsync(-10, 10, timeout_sec=15, vehicle_name=name))


for t in tasks:
    t.join()

with open("results/collision_report.csv", "a", newline='') as f:
    writer=csv.writer(f)
        

    for name in all_drones:
          info=client.simGetCollisionInfo(vehicle_name=name)
          z=client.getMultirotorState(vehicle_name=name).kinematics_estimated.position.z_val
          writer.writerow(["after", name, -z, info.has_collided, info.object_name])
    

print("All", len(all_drones), "up")

