# lets make the client code
import socket, cv2, pickle, struct

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '139.177.198.251'  # paste your server ip address here
#host_ip = '192.168.56.1'
port = 8089
client_socket.connect((host_ip, port))  # a tuple

data = b''
payload_size = struct.calcsize("L")

while True:
    # Retrieve message size
    while len(data) < payload_size:
        data += client_socket.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += client_socket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    print(data)

    # Extract frame
    frame = pickle.loads(frame_data)

    # Display
    cv2.imshow('normal_client', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()