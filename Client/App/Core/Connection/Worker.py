import socket
from .Helper import Helper
from .Protocol import Protocol
from threading import Thread
from ..Diagnostics.Debugging import Console

class Worker:
    def __init__(self):
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # The socket
        self.IsConnected = False
        
    def ConnectToServer(self):
        '''Connects to the server'''
        try:
            self.Sock.connect(Helper.GetServerAddress()) # Connect to the server address
            self.IsConnected = True # Set my connection status
            Console.serverLog("Connection Accepted")
            return True
        except WindowsError: # The error called when the connection cannot be made
            Console.serverLog("Connection Declined")
            return False

    def _Listen(self, callback,delay, OnConnectionReset = lambda:0):
        from time import sleep
        Console.info("Listening to server")
        while True:           
            try:
                # region Get Message
                sleep(delay)
                msgLen_unparsed = self.Sock.recv(Protocol.HEADER_LENGTH) # A header message is always sent first followed by the actual message
                msgLen = Helper.ParseHeader(msgLen_unparsed)
                if not msgLen:continue

                msg_unparsed = self.Sock.recv(int(msgLen))
                msg = Helper.ParseMessage(msg_unparsed)

                # endregion

                callback(msg)
            except ConnectionResetError:
                Console.info("Connection has been resetted")
                self.IsConnected = False
                OnConnectionReset()
                break

    def Listen(self, callback, delay = 0):
        '''Listens for messages from the server and gives it to the callback function'''
        self.myThread = Thread(target=self._Listen,args=(callback,delay),daemon=True).start()

    def SendMessage(self, msg):
        '''Sends a jsonifiable object to the server'''
        if not self.IsConnected:
            Console.error(errorType="Connection Error", errorLevel = 1,errorDesc=f"Tried to send {msg} when not connected")
            return
        encodedMsg = Helper.EncodeMessage(msg) # Encode the message
        header = Helper.GetHeader(encodedMsg) # Get the header
        self.Sock.send(header) # Send the header
        self.Sock.send(encodedMsg) # Send the message

    def Close(self):
        '''Safely closes the connection'''
        if self.IsConnected:
            try:
                self.SendMessage(Protocol.Commands.DISCONNECT) # Send the disconnect message
                self.Sock.shutdown(socket.SHUT_WR) # Close the socket
                Console.serverLog("Disconnecting")
            except socket.error:
                self.Sock.shutdown(socket.SHUT_WR) # Close the socket
                Console.serverLog("Disconnecting")