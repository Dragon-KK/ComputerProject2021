from ..Diagnostics.Debugging import Console
from .Protocol import Protocol
from .Helper import Helper
import threading
import socket

class Server:
    def __init__(self):
        self.PORT = 8008 # The port the socket will be running on
        self.ADDR = socket.gethostbyname(socket.gethostname()) # The address

        self.OnlineMultiplayerGameRequestees = { } # {(conn,addr) : [gamerequests]}

        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
        # AF_INET basically tells that we will be dealing with IP v4 addresses
        # SOCK_STREAM means data will be streamed from both sides and the order will be maintained

        self.Sock.bind((self.ADDR, self.PORT)) # Bind our socket to our address

        Console.serverLog("Initializing Server")

    def SendMessage(self,conn, msg):
        '''Sends a jsonifiable object given a connection'''
        encodedMsg = Helper.EncodeMessage(msg) # Encode the message
        header = Helper.GetHeader(encodedMsg) # Get the header
        conn.send(header) # Send the header
        conn.send(encodedMsg) # Send the message

    def Run(self):
        Console.serverLog(f"Listening on {self.ADDR}:{self.PORT}")

        self.Sock.listen()
        while 1: # Our socket runs forever (until we close it)

            conn, addr = self.Sock.accept() # Accept connections and keep the connection object and the adress

            threading.Thread(
                target=self.HandleClient, # The target of our thread
                daemon=True,  # This basically makes it so that if the main program ends before this thread, the thread will be destroyed along with the main program
                args = (conn, addr)).start()
            
            self.OnlineMultiplayerGameRequestees[(conn,addr)] = []
            Console.info(f"Total active connections : {len(self.OnlineMultiplayerGameRequestees.keys())}")

    def BroadcastGameRequestDeletion(self, conn, addr, gamerequests):
        for (c, a) in self.OnlineMultiplayerGameRequestees:
            if (c,a) != (conn, addr): # We dont want to send gamerequest deletion back to the sender
                self.SendMessage(c, {
                    "type" : "NewGameRequest",
                    "data" : gamerequests,
                    "source" : addr
                })
    
    def BroadcastGameRequestCreation(self, conn,addr, request):
        for (c, a) in self.OnlineMultiplayerGameRequestees:
            if (c,a) != (conn, addr): # We dont want to send gamerequest creation back to the sender
                self.SendMessage(c, {
                    "type" : "CancelGameRequests",
                    "data" : request,
                    "source" : addr
                })
        
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

            if msg['type'] == "RequestCreation":
                self.BroadcastGameRequestCreation(conn, addr, msg['data'])
            elif msg['type'] == 'RequestDeletion':
                self.BroadcastGameRequestDeletion(conn, addr, [msg['data']])

        self.BroadcastGameRequestDeletion(conn, addr, self.OnlineMultiplayerGameRequestees[(conn,addr)]) # Remove the game requests made by the disconnecting client
        del self.OnlineMultiplayerGameRequestees[(conn,addr)] # Delete the dictionary item of this client
        Console.clientLog(addr, "Disconnecting")
        Console.info(f"Total active connections : {len(self.OnlineMultiplayerGameRequestees.keys())}")
        conn.close() # Close the connection

        


