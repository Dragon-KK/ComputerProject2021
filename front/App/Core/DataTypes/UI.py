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

# Just an empty class
class ContentContainer:
    pass
