import socket
from .Helper import Helper
from .Protocol import Protocol
from threading import Thread
from ..Diagnostics.Debugging import Console
# We should get the source port (client listening port) and the listening port (Same as what was used to connect to the server)
class PeerToPeer:
    def __init__(self):
        self.OutSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.ListenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        self.IsConnected = False
        self.Disconnect = False
        
        
    def ConnectToPeer(self, peerAddr):
        '''Connects to the server'''
        peerAddr = tuple(peerAddr)
        self.PeerAddress = peerAddr
        try:
            self.OutSock.connect(peerAddr) # Connect to the server address
            self.IsConnected = True # Set my connection status
            self.Address = self.OutSock.getsockname()
            Console.clientLog(peerAddr,"Connection Accepted")
            return True
        except WindowsError as e: # The error called when the connection cannot be made
            self.Address = ('0.0.0.0',0000)
            print(e)
            Console.clientLog(peerAddr,"Connection Declined")
            return False

    def _Listen(self, listeningAddr,callback,delay, OnConnectionReset = lambda:0):
        from time import sleep
        retryCount = 0
        while True:
            try:
                self.ListeningAddress = listeningAddr
                self.ListenSock.bind(listeningAddr)
                self.ListenSock.listen()
                Console.info("Listening to peer")
                conn,addr = self.ListenSock.accept()
                break
            except:
                retryCount += 1
                Console.error("Listening socket is being used")
                if retryCount > 10:
                    return
                sleep(1)

        
        while True:           
            try:
                # region Get Message
                sleep(delay)
                if self.Disconnect:break
                msgLen_unparsed = conn.recv(Protocol.HEADER_LENGTH) # A header message is always sent first followed by the actual message
                msgLen = Helper.ParseHeader(msgLen_unparsed)
                if not msgLen:continue

                msg_unparsed = conn.recv(int(msgLen))
                msg = Helper.ParseMessage(msg_unparsed)

                # endregion

                if callback(msg):break
            except ConnectionResetError:
                Console.info("Connection has been resetted")
                OnConnectionReset()
                break
            except Exception as e:
                print("aglio ugllio",e)
                break
        Console.info("Stopped Listening")

    def Listen(self, listeningAddr,callback, delay = 0):
        '''Listens for messages from the server and gives it to the callback function'''
        listeningAddr = tuple(listeningAddr)
        self.myThread = Thread(target=self._Listen,args=(listeningAddr,callback,delay),daemon=True).start()
    def SendMessage(self, msg):
        '''Sends a jsonifiable object to the server'''
        if not self.IsConnected:
            Console.error(errorType="Connection Error", errorLevel = 1,errorDesc=f"Tried to send {msg} when not connected")
            return
        encodedMsg = Helper.EncodeMessage(msg) # Encode the message
        header = Helper.GetHeader(encodedMsg) # Get the header
        self.OutSock.send(header) # Send the header
        self.OutSock.send(encodedMsg) # Send the message

    def Close(self):
        '''Safely closes the connection'''
        self.Disconnect = True
        if self.IsConnected:
            try:
                self.SendMessage(Protocol.Commands.DISCONNECT) # Send the disconnect message
                self.IsConnected = False
                self.OutSock.shutdown(socket.SHUT_WR) # Close the socket
                self.ListenSock.close() # Close the socket
                Console.serverLog("Disconnecting")
            except socket.error:
                self.IsConnected = False
                self.OutSock.shutdown(socket.SHUT_WR) # Close the socket
                self.ListenSock.close() # Close the socket
                Console.serverLog("Disconnecting")

    def WordlessClose(self):
        self.Disconnect = True
        self.IsConnected = False
        self.OutSock.shutdown(socket.SHUT_WR) # Close the socket
        self.ListenSock.close() # Close the socket
        Console.serverLog("Disconnecting")