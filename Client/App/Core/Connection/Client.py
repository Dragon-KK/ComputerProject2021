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
            Console.info("Connected to server succesfully")
            onConnection()

        except Exception as e:
            print(e)
            self.Disconnect()
            onError()

    def Connect(self, serverAddr, onError = lambda:0, onConnection = lambda:0):
        '''Connects to the server (asynchronously)'''
        threading.Thread(target=self._Connect, args = (serverAddr,onError,onConnection),daemon=True).start()

    def Disconnect(self):
        Console.info("Disconnecting")
        if self.TalkerIsConnected:
            self.TalkerIsConnected = False
            try:self.TalkerSock.shutdown(socket.SHUT_WR)
            except:pass
        if self.ListenerIsConnected:
            self.ListenerIsConnected = False
            try:self.ListenerSock.shutdown(socket.SHUT_WR)
            except:pass

    def Close(self):
        Console.info("Closing Client")
        try:
            Worker.SendMessage(self.TalkerSock,{'command':Commands.DISCONNECT})
        except:
            pass
        finally:
            self.Disconnect()

    def _Listen(self, callback):
        Console.info("Listening to server")
        while 1:
            msg = Worker.GetMessage(self.ListenerSock,cancel = lambda:not self.TalkerIsConnected)
            if msg == '!Error':break
            if callback(msg):break

        Console.info("Stopping listening")

    def Listen(self,callback):
        threading.Thread(target = self._Listen, args = (callback,),daemon = True).start()

    def RequestGameList(self):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.GetGames
        })

    def AcceptGame(self, game, addr):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.AcceptGame,
            'addr' : addr,
            'game' : game
        })

    def CancelGame(self, game):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.CancelGame,
            'game' : game
        })

    def CreateGame(self, game):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.CreateGame,
            'game' : game
        })
