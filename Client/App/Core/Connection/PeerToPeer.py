import socket
import threading
from .Worker import Worker
from ..Diagnostics.Debugging import Console
from .Commands import Commands
import time


class PeerToPeer:
    
    def __init__(self, listenerSock):
        self.TalkerAddr = (0,0)
        self.ListenerAddr = (0,0)
        self.TalkerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.ListenerSock = listenerSock
        self.ImageSenderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.TalkerIsConnected = True
        self.ListenerIsConnected = False
        self.__Connections = []
        Console.info("Initializing p2p connection")



    def _Connect(self, peerAddr, onError, onConnection,wait):
        time.sleep(wait)
        print(peerAddr)
        try:
            self.TalkerSock.connect(peerAddr)
            self.TalkerIsConnected = True
            self.TalkerAddr = self.TalkerSock.getsockname()

            self.ImageSenderSock.connect(peerAddr)
            Console.info("Connected to peer succesfully")
            onConnection()

        except Exception as e:
            print(e)
            Console.info("Could not connect to peer")
            self.Disconnect()
            onError()

    def __Listen(self,conn,callback):
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
        self.Disconnect()
        Console.info("Stopped Listening")
    def _Listen(self, listeningAddr,callback):
        Console.info("Setting up p2p listener")
        
        retryCount = 0
        while True:
            try:
                self.ListenerIsConnected = True
                self.ListenerSock.listen()
                Console.info("Waiting for peer")
                connT,addrT = self.ListenerSock.accept()                
                connI,addrI = self.ListenerSock.accept()                
                break
            except Exception as e:
                retryCount += 1
                Console.error(e)
                if retryCount > 20:
                    self.Disconnect()
                    return
                time.sleep(0.5)
        Console.info("Peer has connected")
        self.__Connections = [connI,connT]  
        threading.Thread(target = self.__Listen, args = (connT, callback),daemon = True).start()
        threading.Thread(target = self.__Listen, args = (connI, callback),daemon = True).start()

    def Listen(self,listeningAddr,callback):
        listeningAddr = tuple(listeningAddr)
        threading.Thread(target = self._Listen, args = (listeningAddr,callback),daemon = True).start()

    def Connect(self, peerAddr, onError = lambda:0, onConnection = lambda:0, wait = 0):
        '''Connects to the peer (asynchronously)'''
        peerAddr = tuple(peerAddr)
        
        threading.Thread(target=self._Connect, args = (peerAddr,onError,onConnection,wait),daemon=True).start()

    def Disconnect(self):
        Console.info("Disconnecting")
        for conn in self.__Connections:
            try:
                conn.shutdown(socket.SHUT_WR)
                conn.close()
            except:pass
        self.TalkerIsConnected = False
        self.ListenerIsConnected = False
        try:self.TalkerSock.shutdown(socket.SHUT_WR)
        except:pass
        
        try:self.ListenSock.shutdown(socket.SHUT_RDWR) # Close the socket
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

    def RaiseInconsistency(self):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.RaiseInconsistency
        })

    def StartRound(self):
        Worker.SendMessage(self.TalkerSock, {
            'command' : Commands.StartRound
        })

    def _SendImages(self, cancel, data, delay):
        Console.info("Sending images")
        try:
            while 1:
                time.sleep(delay)
                if cancel() or (not self.TalkerIsConnected):return
                Worker.SendMessage(self.ImageSenderSock, {
                    'command' : Commands.UpdateImage,
                    'data' : data()
                })
        except ConnectionResetError:
            Console.info("Connection has been resetted 124rqwe")            
        except Exception as e:
            Console.error(errorDesc = e)

        Console.info("Stopped sending images")


    def SendImages(self, cancel = lambda:False,data = lambda:{}, delay = 0):
        threading.Thread(target=self._SendImages, args = (cancel, data, delay), daemon = True).start()
