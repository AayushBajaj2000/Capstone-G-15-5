import cv2
import socket
import pickle
import struct

cap = cv2.VideoCapture(0)

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '139.177.198.251'  # paste your server ip address here
# host_ip = '192.168.56.1'

port = 12345
client_socket.connect((host_ip, port))  # a tuple

while True:
    ret, frame = cap.read()

    # Serialize frame
    data = pickle.dumps(frame)
    # Send message length first
    message_size = struct.pack("L", len(data))

    # Then data
    client_socket.sendall(message_size + data)