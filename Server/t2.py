import sys
import socket
from Core.Worker import Worker
addr = (sys.argv[1].split(":"))
addr[1] = int(addr[1])
addr = tuple(addr)
TalkerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
TalkerSock.connect(addr)
TalkerSock.send(b'hello')
TalkerSock.send(b'')
TalkerSock.close()