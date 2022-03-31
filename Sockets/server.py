import socket
import threading
import time

HEADER = 64
HEADERSIZE = 10
SERVER = ''
PORT = 5050
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = set()
count = 0

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        full_msg = ''
        new_msg = True
        while True:
            msg = conn.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            full_msg += msg.decode('utf-8')

            if len(full_msg) - HEADERSIZE == msglen:
                data = full_msg[HEADERSIZE:]
                # print(data)
                for client in clients:
                    if client != conn:
                        data = f'{len(data):<{HEADERSIZE}}' + data
                        while len(data) != 100:
                            data += ' '
                        client.send(bytes(data, 'utf-8'))
                new_msg = True
                full_msg = ''

        conn.close()


def start():
    global count
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        count += 1
        clients.add(conn)
        print(count)
        if count == 1:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        print(clients)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()