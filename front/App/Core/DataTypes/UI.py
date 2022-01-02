class Event:
    def __init__(self, sender, code, *args, **kwargs):
        self.sender = sender
        self.code = code
        self.args = args
        self.kwargs = kwargs

class EventListener:
    def __init__(self, code, callback):
        self.Code = code
        self.Callback = callback

class Timeout:
    def __init__(self, delay, callback):
        self.Delay = delay
        self.Callback = callback
        self._ID = -1

class Interval:
    def __init__(self, delay, callback):
        self.Delay = delay
        self.Callback = callback
        self._ID = -1

class Resource:
    def __init__(self, name):
        self.Name = name

    def Unload(self):
        '''Called when resource is removed'''
        pass

    def Load(self):
        '''Called when the resource is added'''
        pass

# Just an empty class
class ContentContainer:
    pass

