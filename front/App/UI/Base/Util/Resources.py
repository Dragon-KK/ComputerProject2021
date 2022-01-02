class ResourceManager:
    def __init__(self):
        self.Resources = {

        }

    def __getattr__(self, name):
        return self.Resources.get(name)

    def AddResource(self, resource):
        pass

    def RemoveResource(self, resource):
        pass

    def __add__(self, resource):
        self.AddResource(resource)
        return self

    def __sub__(self, resource):
        self.RemoveResource(resource)
        return self