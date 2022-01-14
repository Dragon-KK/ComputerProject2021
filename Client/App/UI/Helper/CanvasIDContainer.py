class CanvasIDContainer:
    def __init__(self):
        self.IDs = {}

    def __getattr__(self, name):
        if name == 'ALL' : return list(self.IDs.values())
        return self.IDs.get(name)

    def __setattr__(self, name, value):
        if name == "IDs":
            self.__dict__["IDs"] = value
        else:
            self.IDs[name] = value