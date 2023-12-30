from time import sleep
import keyboard

from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics

from calculations import rotation_speed_angle, drift_angle
from systems import direction_stabilization, drift_aspiration

# Instantiate BeamNGpy instance running the simulator from the given path,
# communicating over localhost:64256
bng = BeamNGpy('localhost', 64256, home='F:\Steam\steamapps\common\BeamNG.drive',
               user='C:/Users/angry/AppData/Local/BeamNG.drive/0.31')
# Launch BeamNG.tech
bng.open()
# Create a scenario in west_coast_usa called 'example'
scenario = Scenario('smallgrid', 'camera_control_test')
config = 'vehicles/coupe/drift.pc'
vehicle = Vehicle('vehicle', model='coupe', part_config=config)
electrics = Electrics()
vehicle.sensors.attach('electrics', electrics)
# Add it to our scenario at this position and rotation
scenario.add_vehicle(vehicle, pos=(0, 0, 0))
# Place files defining our scenario for the simulator to read
scenario.make(bng)

# Load and start our scenario
bng.scenario.load(scenario)
bng.scenario.start()

vehicle.control(throttle=1)
sleep(10)
vehicle.control(steering=1)
sleep(0.5)
vehicle.control(steering=-1)
vehicle.control(parkingbrake=1)
vehicle.control(clutch=1)
vehicle.control(gear=3)
sleep(0.9)
vehicle.control(clutch=0)
vehicle.control(parkingbrake=0)
steering = 0
vehicle.control(steering=steering)
target_drift_angle = -30

while True:
    vehicle.sensors.poll()
    event = keyboard.read_event()

    if vehicle.sensors['electrics']['airspeed'] < 1 or event.event_type == keyboard.KEY_DOWN:
        continue

    vel_x = round(vehicle.sensors['state']['vel'][0], 3)
    vel_y = round(vehicle.sensors['state']['vel'][1], 3)
    dir_x = round(vehicle.sensors['state']['dir'][0], 3)
    dir_y = round(vehicle.sensors['state']['dir'][1], 3)
    rotation_1 = vehicle.sensors['state']['rotation'][2]

    vehicle.sensors.poll()

    rotation_2 = vehicle.sensors['state']['rotation'][2]

    rotation_speed_angle_ = rotation_speed_angle.calculate(rotation_1, rotation_2)
    steering = direction_stabilization.calculate(rotation_speed_angle_)
    drift_angle_ = drift_angle.calculate(vel_x, vel_y, dir_x, dir_y)
    steering = drift_aspiration.calculate(drift_angle_, rotation_speed_angle_, target_drift_angle, steering)

    vehicle.control(steering=steering)
    # bng.set_relative_camera(vehicle.sensors['state']['pos'], vehicle.sensors['state']['dir'])

    print('rotation_speed_angle: ' + str(rotation_speed_angle_),
          'drift_angle: ' + str(drift_angle_),
          'steering: ' + str(steering),
          'airspeed: ' + str(vehicle.sensors['electrics']['airspeed']))

    sleep(0.001)
