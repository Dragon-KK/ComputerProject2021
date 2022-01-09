from ..Diagnostics.Debugging import Console
from .Protocol import Protocol
from .Helper import Helper
import threading
import socket

class Server:
    def __init__(self):
        self.PORT = 8008 # The port the socket will be running on
        self.ADDR = socket.gethostbyname(socket.gethostname()) # The address

        self.ActiveConnections = 0

        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
        # AF_INET basically tells that we will be dealing with IP v4 addresses
        # SOCK_STREAM means data will be streamed from both sides and the order will be maintained

        self.Sock.bind((self.ADDR, self.PORT)) # Bind our socket to our address

        Console.serverLog("Initializing Server")

    def Run(self):
        Console.serverLog(f"Listening on {self.ADDR}:{self.PORT}")

        self.Sock.listen()
        while 1: # Our socket runs forever (until we close it)

            conn, addr = self.Sock.accept() # Accept connections and keep the connection object and the adress

            threading.Thread(target=self.HandleClient, args = (conn, addr)).start()
            self.ActiveConnections += 1
            Console.info(f"Total active connections : {self.ActiveConnections}")

    
        
    def HandleClient(self, conn : socket.socket, addr):
        Console.clientLog(addr, "Connected to server")
        while 1:

            # region Get Message
            msgLen_unparsed = conn.recv(Protocol.HEADER_LENGTH) # A header message is always sent first followed by the actual message
            msgLen = Helper.ParseHeader(msgLen_unparsed) 

            if not msgLen:continue # Sometimes an empty message is empty, if so just ignore it

            msg_unparsed = conn.recv(int(msgLen))
            msg = Helper.ParseMessage(msg_unparsed)
            # endregion

            # region Check For Special Commands
            if msg == Protocol.Commands.DISCONNECT: # If we have to disconnect
                break # Break out of this loop

            # endregion

            Console.clientLog(addr, msg)

        self.ActiveConnections -= 1 # Update the number of active connections
        Console.clientLog(addr, "Disconnecting")
        conn.close() # Close the connection

        


