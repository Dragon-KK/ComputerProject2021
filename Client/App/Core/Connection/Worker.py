from .Helper import Helper
from .Protocol import Protocol
import threading
class Worker:
    @staticmethod
    def SendMessageAndGetRespose(conn,msg):
        Worker.SendMessage(conn, msg)
        return Worker.GetMessage(conn)
    @staticmethod
    def AsyncSendMessageAndGetResponse(conn,msg,callback):
        threading.Thread(target = Worker._AsyncSendMessageAndGetResponse, args = (conn,msg,calback), daemon = True).start()
    @staticmethod
    def _AsyncSendMessageAndGetResponse(conn,msg,callback):
        callback(Worker.SendMessageAndGetRespose(conn, msg))

    @staticmethod
    def GetMessage(conn,cancel = lambda:0):
        msg = "!Error"
        while 1:
            try:
                if cancel():break
                msgLen_unparsed = conn.recv(Protocol.HEADER_LENGTH) # A header message is always sent first followed by the actual message
                msgLen = Helper.ParseHeader(msgLen_unparsed) 

                if not msgLen:break # Sometimes an empty message is empty, if so just ignore it

                msg_unparsed = conn.recv(int(msgLen))
                msg = Helper.ParseMessage(msg_unparsed)
                break
            except WindowsError as e:
                print("Windows error", e)
                break
            except Exception as e:
                print("Get error",e)
                break
        return msg

    def AsyncGetMessage(conn, callback, cancel = lambda:0):
        threading.Thread(target = Worker._AsyncGetMessage,args = (conn,callback,cancel),daemon = True).start()

    def _AsyncGetMessage(conn, callback, cancel):
        callback(Worker.GetMessage(conn, cancel=cancel))

    def SendMessage(conn, msg):
        '''Sends a jsonifiable object given a connection'''
        encodedMsg = Helper.EncodeMessage(msg) # Encode the message
        header = Helper.GetHeader(encodedMsg) # Get the header
        conn.send(header) # Send the header
        conn.send(encodedMsg) # Send the message