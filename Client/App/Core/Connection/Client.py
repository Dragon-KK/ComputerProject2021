import socket
import threading
from .Worker import Worker
from ..Diagnostics.Debugging import Console
from .Commands import Commands


class Client:

    def __init__(self):
        self.TalkerAddr = (0,0)
        self.TalkerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.ListenerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.TalkerIsConnected = False
        self.ListenerIsConnected = False
        Console.info("Initializing client connection")

    def _Connect(self, serverAddr, onError, onConnection):
        try:
            self.TalkerSock.connect(serverAddr)
            self.TalkerIsConnected = True
            self.TalkerAddr = self.TalkerSock.getsockname()

            self.ListenerSock.connect(serverAddr)
            self.ListenerIsConnected = True
            Worker.SendMessage(self.TalkerSock, {'command' : Commands.CONNECT_MAIN})
            res = Worker.SendMessageAndGetRespose(self.ListenerSock, {
                'command' : Commands.CONNECT_LISTENER,
                'talkerAddr' : self.TalkerAddr
            })
            if res['command'] != Commands.LISTENER_REGISTERED:raise Exception("Server gave invalid response")

            Worker.SendMessage(self.TalkerSock, {'command' : Commands.VALIDATE_LISTENER})

            onConnection()

        except Exception as e:
            print(e)
            self.Disconnect()
            onError()

    def Connect(self, serverAddr, onError = lambda:0, onConnection = lambda:0):
        '''Connects to the server (asynchronously)'''
        threading.Thread(target=self._Connect, args = (serverAddr,onError,onConnection),daemon=True).start()

    def Disconnect(self):
        if self.TalkerIsConnected:
            try:self.TalkerSock.shutdown(socket.SHUT_WR)
            except:pass
        if self.ListenerIsConnected:
            try:self.ListenerSock.shutdown(socket.SHUT_WR)
            except:pass

    def Close(self):
        try:
            Worker.SendMessage(self.TalkerSock,{'command':Commands.DISCONNECT})
        except:
            pass
        finally:
            self.Disconnect()

    def _Listen(self, callback):
        while 1:
            if not self.TalkerIsConnected:break

            msg = Worker.GetMessage(self.ListenerSock)
            if callback(msg):break

    def Listen(self,callback):
        threading.Thread(target = self._Listen, args = (callback,),daemon = True).start()

    def RequestGameList(self):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.GetGames
        })
