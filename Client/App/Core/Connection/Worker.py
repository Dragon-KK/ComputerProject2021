import socket
from .Helper import Helper

class Worker:
    def __init__(self):
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Sock.connect(Helper.GetAddress())

    def SendMessage(self, msg):
        encodedMsg = Helper.EncodeMessage(msg)
        header = Helper.GetHeader(encodedMsg)
        self.Sock.send(header)
        self.Sock.send(encodedMsg)