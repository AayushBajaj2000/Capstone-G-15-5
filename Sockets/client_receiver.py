import socket

HEADER = 64
HEADERSIZE = 10
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.56.1'
# SERVER = "139.177.198.251"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    full_msg = ''
    new_msg = True
    while True:
        msg = client.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode('utf-8')

        if len(full_msg) - HEADERSIZE == msglen:
            data = full_msg[HEADERSIZE:]
            print(data)
            new_msg = True
            full_msg = ''

while True:
    receive()
