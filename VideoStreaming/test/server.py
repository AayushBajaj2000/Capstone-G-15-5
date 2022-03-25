import pickle
import socket
import struct
import cv2
import threading

HOST = ''
PORT = 8089

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

server_socket.bind((HOST, PORT))
print('Socket bind complete')
server_socket.listen(10)
print('Socket now listening')

data = b''
payload_size = struct.calcsize("L")
conn, addr = server_socket.accept()

while True:
    if addr:
        # Retrieve message size
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)

        # Display
        cv2.imshow('normal_client', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
