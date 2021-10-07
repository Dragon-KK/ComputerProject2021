import socket
import threading
import json
import constants
import time
import protocols
from logger import console
import worker
HOST = socket.gethostbyname(socket.gethostname()) # Get my ip addres
#HOST = "my ip address"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a new socket
server.bind((HOST, constants.PORT)) # Bind our socket to HOST ont the port : constant.PORT

def handleRequest(state, message, addr):
    pass

def handleClient(conn,addr):
    
    console.clientLog(addr, "Connection created")
    connected = True
    handShakeMessage = worker.getMessage(conn)

    if handShakeMessage[0] == protocols.SUCCESS and handShakeMessage[1]['cmd'] == protocols.HANDSHAKE:
        worker.sendMessage((protocols.SUCCESS, {}), conn)
    else:
        console.clientLog(addr, "Error! handshake failed, closing connection")
        conn.close()
        return
    while connected:
        state,msg = worker.getMessage(conn)
        if state == protocols.SUCCESS:
            if msg == protocols.DISCONNECT:
                console.clientLog(addr, "Disconnecting from server")
                break
            else:
                #console.clientLog(addr, f"Recieved message : {msg}")
                worker.sendMessage(repr(time.time()), conn)
        else:
            console.clientLog(addr,"Fatal error has occured, closing connection")
            break
    conn.close()

def start():
    server.listen()
    console.serverLog(f"Listening on {HOST}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn,addr))
        thread.start()
        console.info(f"Currently active connections : {threading.activeCount() - 1}")

console.info("Starting Server")
start()