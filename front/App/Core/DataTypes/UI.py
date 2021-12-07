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