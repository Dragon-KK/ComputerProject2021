import socket
import json
import protocols
from logger import console

class constants:
    PORT = 5001 # The port on which we are listening on
    HEADER_LENGTH = 32 # The length of our initial message (refer ot protocol)

"""
the only method to message will be to send and recieve

sender gives prevMessageID + 1s
reciever sends back response with said messageID

no one sided messages allowed
"""

class worker:
    def __init__(self, connection : socket.socket):
        self.connection = connection
        self.sentStack = {} # { id : callBack }

    def getMessage(self):
        '''
        wait and get a message from the other side of the connection\n
        ''' 
        # First recieve a header which basically tells the length of the message
        # Then recieve a message of length l (given by header)
        try:
            size = self.connection.recv(constants.HEADER_LENGTH).decode('utf-8').strip() # Get the msg size
            while len(size) == 0: # Sometimes it gets "" messages god knows why
                # this works for now
                size = self.connection.recv(constants.HEADER_LENGTH).decode('utf-8').strip()
            if not size.isnumeric(): # I need it to be a number if its not numeric then that means something went wrong
                console.error(errorType="Protocol Error", errorLevel="Fatal", errorDesc=f"Recieved header is not a number, it is = {size}") # Show an error message
                return protocols.FAIL,{'type' : "Protocol Error", 'level' : "Fatal", 'desc' : f"Recieved header is not a number, it is = {size}"} # Return Failure

            return protocols.SUCCESS,json.loads(self.connection.recv(int(size)).decode('utf-8')) # Return Succes
        except Exception as e: # If some other error (like some error when un-json-ifying the msg ...etc)
            console.error(errorType=type(e).__name__, errorLevel="Fatal", errorDesc=repr(e)) # Show an error message
            return protocols.FAIL,{'type' : type(e).__name__, 'level' : "Fatal", 'desc' : repr(e)} # Return Failure

    def sendMessage(self,msg):
        '''
        Sends a message to the other side of the connection\n
        Params -\n
        msg (any) : Any jsonify-able object\n
        ''' 
        # First send a header which basically tells the length of the message
        # Then send a message of length l (given by header)
        try:
            encodedMessage = json.dumps(msg).encode('utf-8') # Encode the message
            size = str(len(encodedMessage)).encode('utf-8') # Get size of encoded message
            size += b' ' * (constants.HEADER_LENGTH - len(size)) # Pad our size (since first message HAS to be HEADER_LENGTH long)
            self.connection.send(size) # Send the size
            self.connection.send(encodedMessage) # Send the message
            return protocols.SUCCESS,True # Return Succes
        except Exception as e: # If some error (like some error when jsonifying the msg ...etc)
            console.error(errorType=type(e).__name__, errorLevel="Fatal", errorDesc=repr(e)) # Show an error message
            return protocols.FAIL,{'type' : type(e).__name__, 'level' : "Fatal", 'desc' : repr(e)} # Return Failure

    def message(self,msg):
        '''
        Sends a message to the other side of the connection and waits for a reply
        '''

        state,resp = self.sendMessage(msg)
        if state == protocols.FAIL:
            return state,resp
        return self.getMessage()