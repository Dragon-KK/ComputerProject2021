from ....Core.DataTypes.UI import Resource
from ....Core.Diagnostics.Debugging import Console



class ResourceManager:
    def __init__(self):
        self.__Resources = {}

    def __getattr__(self, name):
        return self.__Resources.get(name)

    def AddResource(self, resource):
        if resource.Name in self.__Resources.keys():
            Console.error("Tried to add a resource with same key")
            return
        self.__Resources[resource.Name] = resource
        resource.Load()

    def RemoveResource(self, resource):
        if type(resource) == str:
            self.__Resources[resource].Unload()
            del self.__Resources[resource]
        elif type(resource) == Resource:
            resource.Unload()
            del self.__Resources[resource.Name]
        else:
            pass

    def __add__(self, resource):
        self.AddResource(resource)
        return self

    def __sub__(self, resource):
        self.RemoveResource(resource)
        return self

    def RemoveAll(self):
        for resource in self.__Resources.values():
            resource.Unload()