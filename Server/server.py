from Core import Commands,Worker
from Diagnostics.Debugging import Console
import socket
import threading
class Server:
    def __init__(self, port):
        self.PORT = port # The port the socket will be running on
        self.ADDR = socket.gethostbyname(socket.gethostname()) # The address

        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
        # AF_INET basically tells that we will be dealing with IP v4 addresses
        # SOCK_STREAM means data will be streamed from both sides and the order will be maintained

        self.Sock.bind((self.ADDR, self.PORT)) # Bind our socket to our address

        self.Clients = {} # {addr : {'talker':conn,'listener':conn,'gamerequests':[]}}

        Console.serverLog("Initialized")

    def AcceptConnections(self):
        Console.serverLog(f"Listening on {self.ADDR}:{self.PORT}")
        self.Sock.listen()
        while 1: # Our socket runs forever (until we close it)
            
            conn, addr = self.Sock.accept() # Accept connections and keep the connection object and the adress
            threading.Thread(
                target=self.HandleClient, # The target of our thread
                daemon=True,  # This basically makes it so that if the main program ends before this thread, the thread will be destroyed along with the main program
                args = (conn, addr)
            ).start()

            Console.info(f"Total active threads : {threading.active_count()}")

    def HandleClient(self, conn, addr):
        '''Called initially when the connection is made to initialize the connection'''
        Console.clientLog(addr, "Connected to server")
        try:
            initmsg = Worker.GetMessage(conn)
            if initmsg == "!Error":
                raise Exception("Initial message was a dud")
            elif initmsg['command'] == Commands.CONNECT_MAIN:
                a = tuple(initmsg['addr'])
                self.Clients[a] = {'talker':conn,'listener':None,'games':[]}
                Worker.SendMessage(conn, {'command':Commands.VALIDATE_LISTENER})
                readymsg = Worker.GetMessage(conn)
                if readymsg['command'] == Commands.VALIDATE_LISTENER:
                    if self.Clients[a]['listener']:
                        self.ServeClient(a)
                    else:
                        raise Exception("Y u lie, listener didnt connect")
            elif initmsg['command'] == Commands.CONNECT_LISTENER:
                self.Clients[tuple(initmsg['talkerAddr'])]['listener'] = conn
                Worker.SendMessage(conn, {'command':Commands.LISTENER_REGISTERED})
            else:
                raise Exception("Initial message must be a connection management message")
        except Exception as e:
            print(e)
            Console.clientLog(addr, "Disconnecting")
            
            if self.Clients.get(addr):del self.Clients[addr]
            Console.info(f"Total active threads : {threading.active_count() - 1}")
            conn.close() # Close the connection

    def Broadcast(self, msg, src = None):
        for i in self.Clients:
            if i == src or self.Clients[i]['listener'] is None:continue
            try:Worker.SendMessage(self.Clients[i]['listener'], msg)
            except:pass
            
            
    def ServeClient(self, addr):
        '''Serves a client that has been initialized'''
        try:            
            while 1:
                msg = Worker.GetMessage(self.Clients[addr]['talker'], cancel = lambda:not (addr in self.Clients))
                if msg == "!Error":
                    break
                elif msg['command'] == Commands.DISCONNECT:
                    break
                elif msg['command'] == Commands.CreateGame:
                    self.Clients[addr]['games'].append(msg['game'])
                    self.Broadcast({
                        'command' : Commands.ShowGames,
                        'games' : [msg['game']]
                    }, src = addr)
                elif msg['command'] == Commands.CancelGame:
                    self.Broadcast({
                        'command' : Commands.HideGames,
                        'games' : [msg['game']]
                    }, src = addr)
                elif msg['command'] == Commands.AcceptGame:
                    otherAddr = tuple(msg['addr'])
                    gamesToDelete = self.Clients[addr]['games'] + self.Clients.get(otherAddr, {'games':[]})['games']
                    try:
                        Worker.SendMessage(self.Clients[otherAddr]['listener'], {
                            'command':Commands.BeginGame,
                            'game' : msg['game'],
                            'addr' : addr
                        })                    
                        Worker.SendMessage(self.Clients[addr]['listener'],{
                            'command':Commands.BeginGame,
                            'game' : msg['game'],
                            'addr' : otherAddr
                        })
                        del self.Clients[addr]
                        del self.Clients[otherAddr]
                    except:
                        pass
                    finally:
                        self.Broadcast({
                            'command' : Commands.HideGames,
                            'games' : gamesToDelete
                        })
                    
                elif msg['command'] == Commands.GetGames:
                    allGames = []
                    for i in self.Clients:allGames.extend(self.Clients[i]['games'])
                    Worker.SendMessage(self.Clients[addr]['listener'], {
                        'command' : Commands.ShowGames,
                        'games' : allGames
                    })
                    allGames.clear()
        except Exception as e:
            print(e)
        finally:
            Console.clientLog(addr, "Disconnecting")
            Console.info(f"Total active threads : {threading.active_count() - 1}")
            if not self.Clients.get(addr):return
            self.Broadcast({
                'command' : Commands.HideGames,
                'games' : self.Clients[addr]['games']
            }, src=addr)
            try:self.Clients[addr]['talker'].close()
            except:pass
            try:self.Clients[addr]['listener'].close()
            except:pass
            del self.Clients[addr]

MyServer = Server(8008) # Create my server
MyServer.AcceptConnections() # Accept connections from outside