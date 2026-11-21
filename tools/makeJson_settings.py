import json
import os
import shutil

num_drones = 60

#where airsim settings.json is located
settings_path=os.path.expanduser("~/Documents/AirSim/settings.json")

#backup the current json file
shutil.copy(settings_path, settings_path+".bak")

vehicles={}
for i in range(num_drones):
    name=f"Drone{i}"
    vehicles[name]={
        "VehicleType": "SimpleFlight",
        "X":2*(i//10),"Y":1+2*(i%10),"Z":0
    }

setting={
    "SettingsVersion": 1.2,
    "SimMode": "Multirotor",
    "ClockSpeed": 1.0,
    "Vehicles": vehicles
}

with open(settings_path, "w") as f:
    json.dump(setting,f,indent=2)

print("Wrote", num_drones, "drones to", settings_path)

