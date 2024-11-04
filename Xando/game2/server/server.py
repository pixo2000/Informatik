import socket
from _thread import *
import sys
# error can be fixed: the client packet should start with [Ping] or [Join] and the server needs to detect that and if its just ping dont expect anything


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 52983

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]

def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                packet_type, content = data.split(":", 1)
                if packet_type == "ping":
                    conn.sendall(str.encode("pong"))
                elif packet_type == "start_game":
                    arr = content.split(":")
                    id = int(arr[0])
                    pos[id] = content

                    if id == 0: nid = 1
                    if id == 1: nid = 0

                    reply = pos[nid][:]
                    conn.sendall(str.encode(reply))
                print(f"Received {packet_type} packet: {content}")
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))