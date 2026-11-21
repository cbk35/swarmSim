"""
Quick sanity check: arm, takeoff, hover, land a single drone.
Run this AFTER AirSim Blocks is open and loaded.
"""

import airsim  # the AirSim Python library we installed
import time    # standard Python library for waiting/sleeping

# Connect to the AirSim sim running on this computer
client = airsim.MultirotorClient()
client.confirmConnection()  # throws an error if AirSim isn't running
print("Connected to AirSim")

# Tell AirSim we want to control Drone0 via Python (not manually)
client.enableApiControl(True, "Drone0")
# Arm the drone — like flipping the power switch before flight
client.armDisarm(True, "Drone0")

client.enableApiControl(True, "Drone1")
client.armDisarm(True, "Drone1")
client.enableApiControl(True, "Drone2")
client.armDisarm(True, "Drone2")
client.enableApiControl(True, "Drone3")
client.armDisarm(True, "Drone3")
client.enableApiControl(True, "Drone4")
client.armDisarm(True, "Drone4")
client.enableApiControl(True, "Drone5")
client.armDisarm(True, "Drone5")

print("Taking off...")
# Send the takeoff command and WAIT for it to finish before moving on
# client.takeoffAsync(vehicle_name="Drone0").join() the .join() method waits for the command to finish before moving on to the next line of code. If you don't call join(), the next line of code will run immediately, which may not be what you want.
t0 = client.takeoffAsync(vehicle_name="Drone0")
t1 = client.takeoffAsync(vehicle_name="Drone1")
t2 = client.takeoffAsync(vehicle_name="Drone2")
t3 = client.takeoffAsync(vehicle_name="Drone3")
t4 = client.takeoffAsync(vehicle_name="Drone4")
t5 = client.takeoffAsync(vehicle_name="Drone5")
# Wait for ALL drones to finish taking off before moving on
t0.join(); t1.join(); t2.join(); t3.join(); t4.join(); t5.join()

print("Flying up to 10m...")
# Move to Z = -10 at 2 m/s. Z is NEGATIVE for up in AirSim (flipped axis)
m0 = client.moveToZAsync(-10, 2, vehicle_name="Drone0")
m1 = client.moveToZAsync(-10, 2, vehicle_name="Drone1")
m2 = client.moveToZAsync(-10, 2, vehicle_name="Drone2")
m3 = client.moveToZAsync(-10, 2, vehicle_name="Drone3")
m4 = client.moveToZAsync(-10, 2, vehicle_name="Drone4")
m5 = client.moveToZAsync(-10, 2, vehicle_name="Drone5")
# Wait for ALL drones to reach altitude before moving on
m0.join(); m1.join(); m2.join(); m3.join(); m4.join(); m5.join()

print("Hovering 3 seconds...")
# Pause the script for 3 seconds while the drone hovers in place
time.sleep(3)

# Print each drone's position separately — fixes the overwrite bug
for name in ["Drone0", "Drone1", "Drone2", "Drone3", "Drone4", "Drone5"]:
    state = client.getMultirotorState(vehicle_name=name)
    pos = state.kinematics_estimated.position
    print(f"{name} position: x={pos.x_val:.1f} y={pos.y_val:.1f} z={pos.z_val:.1f}")

print("Landing...")
# Send the land command and wait for all to finish
l0 = client.landAsync(vehicle_name="Drone0")
l1 = client.landAsync(vehicle_name="Drone1")
l2 = client.landAsync(vehicle_name="Drone2")
l3 = client.landAsync(vehicle_name="Drone3")
l4 = client.landAsync(vehicle_name="Drone4")
l5 = client.landAsync(vehicle_name="Drone5")
# Wait for ALL drones to land before moving on
l0.join(); l1.join(); l2.join(); l3.join(); l4.join(); l5.join()

# Disarm and release API control — good practice to clean up
client.armDisarm(False, "Drone0")
client.armDisarm(False, "Drone1")
client.armDisarm(False, "Drone2")
client.armDisarm(False, "Drone3")
client.armDisarm(False, "Drone4")
client.armDisarm(False, "Drone5")
client.enableApiControl(False, "Drone0")
client.enableApiControl(False, "Drone1")
client.enableApiControl(False, "Drone2")
client.enableApiControl(False, "Drone3")
client.enableApiControl(False, "Drone4")
client.enableApiControl(False, "Drone5")
print("Done.")