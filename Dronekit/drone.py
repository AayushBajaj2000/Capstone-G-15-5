import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import socket
import pickle

HEADER = 64
HEADERSIZE = 10
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.56.1'
# SERVER = "139.177.198.251"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# -- Connect to the vehicle
print('Connecting...')
vehicle = connect('tcp:127.0.0.1:5762')

# -- Setup the commanded flying speed
max_speed = [0.1, 0.25]  # [m/s]
speed_limit = 0

# -- Define arm and takeoff
def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("waiting to be armable")
        time.sleep(1)

    print("Arming motors")

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed: time.sleep(1)

    print("Taking Off")
    vehicle.simple_takeoff(altitude)

    while True:
        v_alt = vehicle.location.global_relative_frame.alt
        print(">> Altitude = %.1f m" % v_alt)
        if v_alt >= altitude - 1.0:
            print("Target altitude reached")
            break
        time.sleep(1)


def land():
    vehicle.mode = VehicleMode("LAND")

    while vehicle.mode != 'LAND':
        time.sleep(1)
        print("Waiting for drone to land")
    print("Drone in land mode. Exiting script.")


# -- Define the function for sending mavlink velocity command in body frame
def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html

    Bitmask to indicate which dimensions should be ignored by the vehicle
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that
    none of the setpoint dimensions should be ignored). Mapping:
    bit 1: x,  bit 2: y,  bit 3: z,
    bit 4: vx, bit 5: vy, bit 6: vz,
    bit 7: ax, bit 8: ay, bit 9:
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0b0000111111000111,  # -- BITMASK -> Consider only the velocities
        0, 0, 0,  # -- POSITION
        vx, vy, vz,  # -- VELOCITY
        0, 0, 0,  # -- ACCELERATIONS
        0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()

arm_and_takeoff(10)
# flySquare()

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = client.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode('utf-8')
        #print(full_msg)

        if len(full_msg) - HEADERSIZE == msglen:
            data = full_msg[HEADERSIZE:]
            print(data)
            test = data.split(",")

            # First check if we want to land
            land_check = float(test[4][2:])

            if land_check == 1.0:
                land()
                break

            right = float(test[0][2:])
            back = float(test[1][2:])
            turnRight = float(test[2][2:])
            altitude = float(test[3][2:])
            mode = float(test[5][2:])

            if mode == 0:
                speed_limit = max_speed[0]
            elif mode == 1:
                speed_limit = max_speed[1]

            altitude_speed = abs(altitude - 1.0)
            vx = right * speed_limit
            vy = back * speed_limit
            vz = altitude_speed * speed_limit

            set_velocity_body(vehicle, vx, vy, vz)
            new_msg = True
            full_msg = ''