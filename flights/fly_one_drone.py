import airsim #loads the airsim library, which is a Python client for the AirSim simulator. think C++ #include
import time #loads the time library, which is a standard Python library for waiting/sleeping.


client = airsim.MultirotorClient() #creates a client object that allows you to communicate with the AirSim simulator. think of it as a remote control for the drone
client.confirmConnection() #checks if the connection to the AirSim simulator is successful. If not, it will raise an error and stop the program. think of it as a handshake between your code and the simulator
print("Connected to AirSim") #prints a message to the console indicating that the connection to the AirSim simulator was successful

client.enableApiControl(True, "Drone0") #enables API control for the drone named "Drone0". This allows your code to send commands to the drone instead of controlling it manually. think of it as giving your code the ability to fly the drone
#client.enableApiControl(False, "Drone0") # False would disable the API control and give control back to the user. Like turning autopilot off and letting the pilot take over. This is useful if you want to switch between manual and automated control of the drone.

#client.armDisarm(Flase, "Drone0, Drone1, Drone2, Drone3, Drone4, Drone5") #disables the motors for all drones in preparation for flight. A "True" would arm the drones and turn on the motors. This is useful if you want to reset the drones before starting a new flight.
client.armDisarm(True, "Drone0") #arms the drone named "Drone0". This turns on the motors for the drone in preparation for flight. A "False" would disarm the drone.
hold_north = airsim.YawMode(False, 0) #creates a yaw mode object that tells the drone to hold 0 degress north and not rotate. The first argument is a boolean that indicates whether to use the yaw mode or not. The second argument is the desired yaw angle in degrees. In this case, we are not using the yaw mode and the desired yaw angle is 0 degrees.

state = client.getMultirotorState(vehicle_name="Drone0") #gets the current state of the drone named "Drone0". This includes information about the drone's position, orientation, velocity, and other parameters.
start_pos = state.kinematics_estimated.position #gets the estimated position of the drone from the state object. This is a 3D vector that represents the drone's position in the AirSim world.

print(f"Drone0 position at take off: x={start_pos.x_val:.10f} y={start_pos.y_val:.10f} z={start_pos.z_val:.10f}") #prints the estimated position of the drone to the console in a formatted string. The .1f format specifier indicates that the values should be printed with one decimal place.

client.takeoffAsync(vehicle_name="Drone0").join() #sends command to drone to lift off and wait for it to finish before moving on. The .join() method waits for the command to finish before moving on to the next line of code. If you don't call join(), the next line of code will run immediately, which may not be what you want.
client.moveToZAsync(-10, 2, vehicle_name="Drone0").join() #sends command to drone to move to Z = -10 at 2 m/s. Z is NEGATIVE for up in AirSim (flipped axis). The .join() method waits for the command to finish before moving on to the next line of code. If you don't call join(), the next line of code will run immediately, which may not be what you want.
client.moveToPositionAsync(10, 0, -10, 10, yaw_mode=hold_north, vehicle_name="Drone0").join() #sends command to drone to move to position (10, 0, -10) at 5 m/s.
#time.sleep(3) #pauses the script for 3 seconds while the drone hovers in place. This is useful if you want to give the drone time to stabilize or if you want to wait for a specific event to occur before moving on.
client.moveToPositionAsync(10, 10,-10, 10, yaw_mode=hold_north, vehicle_name="Drone0").join() #sends command to drone to move to position (10, 10, -10) at 3 m/s.
client.moveToPositionAsync(0, 10, -10, 10, yaw_mode=hold_north, vehicle_name="Drone0").join() #sends command to drone to move to position (0, 10, -10) at 5 m/s.
client.moveToPositionAsync(0, 0, -10, 10, yaw_mode=hold_north, vehicle_name="Drone0").join() #sends command to drone to move to position (0, 0, -10) at 5 m/s. 
client.hoverAsync(vehicle_name="Drone0").join() #sends command to drone to hover in place and wait for it to finish before moving on.
time.sleep(5)

print("beginning landing sequence...")
client.moveToPositionAsync(0, 0, -2, 5, yaw_mode=hold_north, vehicle_name="Drone0").join() #sends command to drone to move to position (0, 0, 0) at 2 m/s. This is the landing position.
client.moveByVelocityAsync(0, 0, 0.2, 3, yaw_mode=hold_north, vehicle_name="Drone0").join() #sends command to drone to move down at 1 m/s for 2 seconds. This is the final descent before landing.
client.landAsync(vehicle_name="Drone0").join() #sends command to drone to land and wait for it to finish before moving on.
print("drone has landed successfully!") #prints a message to the console indicating that the drone has landed successfully.
client.armDisarm(False, "Drone0")

state = client.getMultirotorState(vehicle_name="Drone0")
end_pos = state.kinematics_estimated.position
print(f"Drone0 position after landing: x={end_pos.x_val:.10f} y={end_pos.y_val:.10f} z={end_pos.z_val:.10f}")
dx = end_pos.x_val - start_pos.x_val    #how far the drone moved in the x direction from takeoff to landing
dy = end_pos.y_val - start_pos.y_val    #how far the drone moved in the y direction from takeoff to landing
error = (dx**2 + dy**2)**0.5            #straight line distance on the ground
print(f"Drone0 error after landing: {error:.10f} meters")