# Welcome to PyShine
# lets make the client code
# In this code client is sending video to server
import socket,cv2, pickle,struct
import imutils # pip install imutils

camera = True

if camera == True:
	vid = cv2.VideoCapture(0)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.56.1' # Here according to your server ip write the address
port = 9999

client_socket.connect((host_ip,port))

if client_socket:
	while (vid.isOpened()):
		try:
			img, frame = vid.read()
			frame = imutils.resize(frame,width=380)
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			client_socket.send(message)
		except:
			print('VIDEO FINISHED!')
			break