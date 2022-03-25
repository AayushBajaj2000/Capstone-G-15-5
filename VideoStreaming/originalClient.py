# lets make the client code
import socket, cv2, pickle, struct, imutils

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.56.1'  # paste your server ip address here
port = 9999
client_socket.connect((host_ip, port))  # a tuple
data = b""
payload_size = struct.calcsize("Q")
vid = cv2.VideoCapture(0)

while True:
    img, frame = vid.read()
    if not img:
        break
    frame = imutils.resize(frame, width=320)
    a = pickle.dumps(frame)
    message = struct.pack("Q", len(a)) + a
    client_socket.sendall(message)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
