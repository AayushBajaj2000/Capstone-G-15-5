# Importing the relevant libraries
import pygame
from pygame.locals import *
import socket
import pickle

# Socket IO Settings
HEADER = 10
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = '139.177.198.251'
SERVER = ''

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
output=[0.0, 0.0, 0.0, 0, 0, 0.0]
out = {"R": 0, "B": 0, "Y": 0, "A": 0, "M": 0, "L": 0}

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def sendDict(conn, dic):
    msg = pickle.dumps(dic)
    msg = bytes(f"{len(msg):<{HEADER}}", 'utf-8') + msg
    conn.send(msg)

clients = set()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")

            for client in clients:
                client.send(f"{msg}".encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(clients)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()

