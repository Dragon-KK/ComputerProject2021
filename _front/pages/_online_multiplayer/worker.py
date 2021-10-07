import socket
from . import constants
from . import protocols
import json
from .logger import console

def getMessage(conn : socket.socket):
    '''
    Gets a message from the other side of the connection\n
    Params -\n
    conn (socket.socket) : The socket
    ''' 
    # First recieve a header which basically tells the length of the message
    # Then recieve a message of length l (given by header)
    try:
        size = conn.recv(constants.HEADER_LENGTH).decode('utf-8').strip() # Get the msg size
        while len(size) == 0: # Sometimes it gets "" messages god knows why
            # this works for now
            size = conn.recv(constants.HEADER_LENGTH).decode('utf-8').strip()
        if not size.isnumeric(): # I need it to be a number if its not numeric then that means something went wrong
            console.error(errorType="Protocol Error", errorLevel="Fatal", errorDesc=f"Recieved header is not a number, it is = {size}") # Show an error message
            return protocols.FAIL,{'type' : "Protocol Error", 'level' : "Fatal", 'desc' : f"Recieved header is not a number, it is = {size}"} # Return Failure

        return protocols.SUCCESS,json.loads(conn.recv(int(size)).decode('utf-8')) # Return Succes
    except Exception as e: # If some other error (like some error when un-json-ifying the msg ...etc)
        console.error(errorType=type(e).__name__, errorLevel="Fatal", errorDesc=repr(e)) # Show an error message
        return protocols.FAIL,{'type' : type(e).__name__, 'level' : "Fatal", 'desc' : repr(e)} # Return Failure

def sendMessage(msg, conn : socket.socket):
    '''
    Sends a message to the other side of the connection\n
    Params -\n
    msg (any) : Any jsonify-able object\n
    conn (socket.socket) : The socket
    ''' 
    # First send a header which basically tells the length of the message
    # Then send a message of length l (given by header)
    try:
        encodedMessage = json.dumps(msg).encode('utf-8') # Encode the message
        size = str(len(encodedMessage)).encode('utf-8') # Get size of encoded message
        size += b' ' * (constants.HEADER_LENGTH - len(size)) # Pad our size (since first message HAS to be HEADER_LENGTH long)
        conn.send(size) # Send the size
        conn.send(encodedMessage) # Send the message
        return protocols.SUCCESS,True # Return Succes
    except Exception as e: # If some error (like some error when jsonifying the msg ...etc)
        console.error(errorType=type(e).__name__, errorLevel="Fatal", errorDesc=repr(e)) # Show an error message
        return protocols.FAIL,{'type' : type(e).__name__, 'level' : "Fatal", 'desc' : repr(e)} # Return Failure

def message(msg, conn):
    '''
    Sends a message to the other side of the connection and waits for a reply
    '''

    state,resp = sendMessage(msg, conn)
    if state == protocols.FAIL:
        return state,resp
    return getMessage(conn)
