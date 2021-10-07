import socket
import json
PORT = 5001
HEADER = 32
DISCONNECT_MESSAGE = "$$Disconnect$$"
SERVER = "10.0.0.123"
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)

from worker import message,sendMessage
print(message({1:2},client))
sendMessage(DISCONNECT_MESSAGE,client)
