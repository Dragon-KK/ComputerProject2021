import socket

PORT = 5001
HEADER = 32
DISCONNECT_MESSAGE = "$$Disconnect$$"
SERVER = "10.0.0.123"
ADDR = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    m = msg.encode('utf-8')
    l = len(m)
    sendLength = str(l).encode('utf-8')
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(m)
send("Hello WOrld")
input("End Connection")
send(DISCONNECT_MESSAGE)
