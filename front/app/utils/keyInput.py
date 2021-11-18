from .daemon import Daemon
class inputWatcher:
    def __init__(self, tkObj,callBackInterval = 20):
        self.daemon = Daemon(tkObj, callBackInterval, self.broadcast)
        self.binds = {}
        self.downs = set()

    def bind(self, keyCode, callBack):
        self.binds[keyCode] = callBack

    def keyEvent(self,e):
        if e.keySym in self.binds:
            self.downs.add(e.keysym)

    def broadcast(self, dt = 0):
        for i in self.downs:
            self.binds[i](i)
        self.downs.clear()

    def pause(self):
        self.daemon.pause()

    def cont(self):
        self.daemon.cont()