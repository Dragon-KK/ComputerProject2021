import socket
import threading
import json
import constants
import protocols
from logger import console
HOST = socket.gethostbyname(socket.gethostname()) # Get my ip addres
#HOST = "my ip address"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a new socket
server.bind((HOST, constants.PORT)) # Bind our socket to HOST ont the port : constant.PORT


def handleClient(c,a):
    console.clientLog(a, "Connection created")
    connected = True
    while connected:
        msg_len = c.recv(constants.HEADER_LENGTH).decode('utf-8')
        if not msg_len:continue
        l = int(msg_len)
        msg = c.recv(l).decode('utf-8')
        if msg == protocols.DISCONNECT:
            console.clientLog(a, "Disconnecting from server")
            break
            
        console.clientLog(a, msg)
    c.close()

def start():
    server.listen()
    console.serverLog(f"Listening on {HOST}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn,addr))
        thread.start()
        console.info(f"Currently active connections : {threading.activeCount() - 1}")

print("Starting server")
start()