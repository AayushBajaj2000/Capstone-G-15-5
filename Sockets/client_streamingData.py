# Importing the relevant libraries
import pygame
from pygame.locals import *
import socket
import time

# Socket IO Settings
HEADERSIZE = 10
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '139.177.198.251'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Pygame Settings
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

# Output array
output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def mapValue(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

land = 0
while True:
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            # Left -> -ve and Right -> +ve
            output[0] = joysticks[0].get_axis(0)
            # Forward -> -ve and Back -> +ve
            output[1] = joysticks[0].get_axis(1)
            # Yaw
            output[2] = joysticks[0].get_axis(2)
            # Throttle
            output[3] = joysticks[0].get_axis(3)

        if event.type == JOYBUTTONDOWN:
            if joysticks[0].get_button(0):
                land = 1

    roll = mapValue(output[0], -1, 1, 1100, 1900)
    pitch = mapValue(output[1], -1, 1, 1100, 1900)
    throttle = mapValue(output[3], 1, -1, 1100, 1900)
    yaw = mapValue(output[2], -1, 1, 1100, 1900)
    message = f"R:{roll},P:{pitch},T:{throttle},Y:{yaw},L:{land}"

    while len(message) != 100:
        message += " "

    client.send(bytes(message, 'utf-8'))
    time.sleep(0.01)
