from ..DataTypes.UI import Resource
from ..DataManagers import FileManager
import socket

class Networking(Resource):
    def __init__(self):
        super().__init__("Networking")
        self.__Connections = {}

    def __getattr__(self, name):
        return self.__Connections.get(name, {})

    def HoldResource(self, name, resource):
        self.__Connections[name] = resource
    
    def ReleaseResource(self, name):
        if self.__Connections.get(name):del self.__Connections[name]

    def Unload(self):
        for value in self.__Connections.keys():
            try:
                value.close()
                value.shutdown(socket.SHUT_WR)
            except:pass
    def Load(self):
        pass