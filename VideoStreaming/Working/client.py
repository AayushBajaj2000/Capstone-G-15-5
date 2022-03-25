import cv2
import numpy as np
import socket
import sys
import pickle
import struct

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.56.1' # YOUR IP ADDRESS

clientsocket.connect((host_ip, 12345))

while True:
    ret,frame=cap.read()
    # Serialize frame
    data = pickle.dumps(frame)

    # Send message length first
    print(len(data))
    message_size = struct.pack("L", len(data))

    # Then data
    clientsocket.sendall(message_size + data)