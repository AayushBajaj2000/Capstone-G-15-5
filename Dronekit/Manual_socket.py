import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import pygame
from pygame.locals import *
import time
import sys
import socket
import pickle

HEADER = 64
HEADERSIZE = 10
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = '192.168.56.1'
SERVER = "139.177.198.251"
ADDR = (SERVER, PORT)

# -- Connect to the vehicle
print('Connecting...')
# Create the connection
master = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
#master = mavutil.mavlink_connection("/dev/ttyTHS1", baud=57600)

# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Pygame Settings
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

# Output array
output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def modeChange(mode):
    # Check if mode is available
    if mode not in master.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(master.mode_mapping().keys()))
        sys.exit(1)

    # Get mode ID
    mode_id = master.mode_mapping()[mode]
    # Set new mode
    # master.mav.command_long_send(
    #    master.target_system, master.target_component,
    #    mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
    #    0, mode_id, 0, 0, 0, 0, 0) or:
    # master.set_mode(mode_id) or:
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)


def mapValue(value, leftMin, leftMax, rightMin, rightMax):

    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def arm():
    # Arm
    # master.arducopter_arm() or:
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0)

    # wait until arming confirmed (can manually check with master.motors_armed())
    print("Waiting for the vehicle to arm")
    master.motors_armed_wait()
    print('Armed!')

def set_rc_channel_pwm(channel_id, pwm=1500):
    """ Set RC channel pwm value
    Args:
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(8)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)                  # RC channel list, in microseconds.

def set_channel(roll,pitch,throttle,yaw):
    set_rc_channel_pwm(1, int(roll))
    set_rc_channel_pwm(2, int(pitch))
    set_rc_channel_pwm(3, int(throttle))
    set_rc_channel_pwm(4, int(yaw))


# -- Setup the commanded flying speed
max_speed = [0.1, 0.25]  # [m/s]
speed_limit = 0

modeChange('STABILIZE')
arm()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

while True:
    data = client.recv(100).decode(FORMAT)
    print(data)
    output = data.split(",")

    land = float(output[4][2:])

    if land:
        modeChange('LAND')

    roll = float(output[0][2:])
    pitch = float(output[1][2:])
    throttle = float(output[2][2:])
    yaw = float(output[3][2:])

    set_channel(roll, pitch, throttle, yaw)


