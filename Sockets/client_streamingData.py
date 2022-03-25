# Importing the relevant libraries
import pygame
from pygame.locals import *
import socket

# Socket IO Settings
HEADER = 64
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
output=[0.0, 0.0, 0.0]

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

while True:
    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            # Left -> -ve and Right -> +ve
            output[0] = joysticks[0].get_axis(0)
            # Forward -> -ve and Back -> +ve
            output[1] = joysticks[0].get_axis(1)
            # Yaw
            output[2] = joysticks[0].get_axis(2)
    # 1 -> Right, 2-> Back , 3-> Turn Right
    send(f"R:{output[0]},B:{output[1]},TR:{output[2]}")

