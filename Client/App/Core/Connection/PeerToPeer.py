import socket
import threading
from .Worker import Worker
from ..Diagnostics.Debugging import Console
from .Commands import Commands
import time


class PeerToPeer:
    
    def __init__(self):
        self.TalkerAddr = (0,0)
        self.ListenerAddr = (0,0)
        self.TalkerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.ListenerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.TalkerIsConnected = True
        self.ListenerIsConnected = False
        Console.info("Initializing p2p connection")



    def _Connect(self, peerAddr, onError, onConnection,wait):
        time.sleep(wait)
        try:
            self.TalkerSock.connect(peerAddr)
            self.TalkerIsConnected = True
            self.TalkerAddr = self.TalkerSock.getsockname()
            Console.info("Connected to peer succesfully")
            onConnection()

        except Exception as e:
            print(e)
            Console.info("Could not connect to peer")
            self.Disconnect()
            onError()

    def _Listen(self, listeningAddr,callback):
        Console.info("Setting up p2p listener")
        
        retryCount = 0
        conn = None
        while True:
            try:
                self.ListeningAddress = listeningAddr
                self.ListenerSock.bind(listeningAddr)
                self.ListenerIsConnected = True
                self.ListenerSock.listen()
                Console.info("Waiting for peer")
                conn,addr = self.ListenerSock.accept()                
                break
            except Exception as e:
                print(e)
                retryCount += 1
                Console.error("Listening socket is being used")
                if retryCount > 100:
                    self.Disconnect()
                    return
                time.sleep(1)
        Console.info("Peer has connected")     
        try:
            while 1:
                msg = Worker.GetMessage(conn,cancel = lambda:not self.TalkerIsConnected)
                if msg == '!Error':break
                if callback(msg):break
        except ConnectionResetError:
            Console.info("Connection has been resetted")            
        except Exception as e:
            Console.error(errorDesc = e)
        conn.close()   
        Console.info("Stopped Listening")

    def Listen(self,listeningAddr,callback):
        listeningAddr = tuple(listeningAddr)
        threading.Thread(target = self._Listen, args = (listeningAddr,callback),daemon = True).start()

    def Connect(self, peerAddr, onError = lambda:0, onConnection = lambda:0, wait = 0):
        '''Connects to the peer (asynchronously)'''
        peerAddr = tuple(peerAddr)
        threading.Thread(target=self._Connect, args = (peerAddr,onError,onConnection,wait),daemon=True).start()

    def Disconnect(self):
        Console.info("Disconnecting")
        self.TalkerIsConnected = False
        self.ListenerIsConnected = False
        try:self.TalkerSock.shutdown(socket.SHUT_WR)
        except:pass
        
        try:self.ListenSock.close() # Close the socket
        except:pass

    def Close(self):
        Console.info("Closing Client")
        try:
            Worker.SendMessage(self.TalkerSock,{'command':Commands.DISCONNECT})
        except:
            pass
        finally:
            self.Disconnect()

    def RequestRoundStart(self):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.RequestRoundStart
        })

    def UpdateImage(self, img):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.UpdateImage,
            'data' : img
        })

    def ValidateResult(self, res):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.UpdateScore,
            'data' : res
        })

    def RaiseInconsistency(self, res):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.RaiseInconsistency
        })

    def StartRound(self):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.StartRound
        })
