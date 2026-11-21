import airsim
import time

client=airsim.MultirotorClient()
client.confirmConnection()
print("Connected to AirSim")

# names=client.simListSceneObjects() #gets a list of all objects in the airsim envioronment.
# for name in names:      #print the names of the list of objects to the console.
#     print(name)

cube_pose = client.simGetObjectPose("TemplateCube_Rounded_4") #gets the position of the object named "TemplateCube_Rounded_4" in the AirSim environment.
cube_pos = cube_pose.position #gets the position of the object from the pose object. this can also contain orientation.
# print(f"TemplateCube_Rounded_4 position: x={cube_pos.x_val:.10f} y={cube_pos.y_val:.10f} z={cube_pos.z_val:.10f}") #prints the position of the object to the console in a formatted string. The .1f format specifier indicates that the values should be printed with one decimal place.


client.reset() #resets the AirSim environment to its initial state. This is useful if you want to start a new flight or if you want to reset the environment after a crash.
client.enableApiControl(True, "Drone0")
client.armDisarm(True, "Drone0")

# Reads colision information for the drone before it takes off.
# This is useful for testing if the drone has collided with any objects during flight.
# The collision info includes whether the drone has collided, the name of the object it collided with, and the time of the collision.
#______________________________________________________________________________________________________________________________________

# Uncomment the following lines to reset drone collision info before take off.
# before=client.simGetCollisionInfo(vehicle_name="Drone0") #gets the collision info for the drone named "Drone0". This includes information about whether the drone has collided with any objects, the position of the collision, and the normal of the surface that was collided with.
# print(f"Before flight: Collided: {before.has_collided}, object: {before.object_name}, time:{before.time_stamp}")
#_______________________________________________________________________________________________________________________________________

client.takeoffAsync(vehicle_name="Drone0").join()

# Uncomment the following lines to read collision info after take off.
before=client.simGetCollisionInfo(vehicle_name="Drone0") #gets the collision info for the drone named "Drone0". This includes information about whether the drone has collided with any objects, the position of the collision, and the normal of the surface that was collided with.
print(f"Before flight: Collided: {before.has_collided}, object: {before.object_name}, time:{before.time_stamp}")
#_______________________________________________________________________________________________________________________________________

face_forward = airsim.YawMode(False, 0)
client.moveToPositionAsync(cube_pos.x_val, cube_pos.y_val, cube_pos.z_val, 10,
                           timeout_sec=10,
                           drivetrain=airsim.DrivetrainType.ForwardOnly,
                           yaw_mode=face_forward,
                           vehicle_name="Drone0").join()
print("Drone0 has reached the position of TemplateCube_Rounded_4 or timed out after 10 seconds.")

collision=client.simGetCollisionInfo(vehicle_name="Drone0") #gets the collision info for the drone named "Drone0". This includes information about whether the drone has collided with any objects, the position of the collision, and the normal of the surface that was collided with.
print(f"Collided: {collision.has_collided}")
print(f"Hit object name: {collision.object_name}")
hit=collision.impact_point
print(f"Impact point: x={hit.x_val:.10f} y={hit.y_val:.10f} z={hit.z_val:.10f}")

client.moveToPositionAsync(0,0,-3,3, timeout_sec=10, vehicle_name="Drone0").join()
time.sleep(3)
later=client.simGetCollisionInfo(vehicle_name="Drone0")
print(f"after backing away: Collided: {later.has_collided}, object: {later.object_name}, time: {later.time_stamp}")
print(f"Crash time: {collision.time_stamp}")
print(f"Later time: {later.time_stamp}")
