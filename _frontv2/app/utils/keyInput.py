from .daemon import Daemon
class inputWatcher:
    def __init__(self, tkObj,callBackInterval = 20):
        
        self.binds = {}
        tkObj.bind_all("<KeyPress>",self.keyDown)
        tkObj.bind_all("<KeyRelease>",self.keyUp)
        self.tkObj = tkObj
        self.downs = set()
        self.daemon = Daemon(tkObj, callBackInterval, self.broadcast)

    def bind(self, keyCode, callBack ,spclCode = None):
        self.binds[spclCode if spclCode else keyCode] = callBack

    def keyUp(self,e):
        if e.keysym in self.downs:
            self.downs.remove(e.keysym)  

    def keyDown(self,e):
        if e.keysym in self.binds:
            self.downs.add(e.keysym)

    def broadcast(self, dt = 0):
        for i in self.downs:
            self.binds[i](i)
        

    def pause(self):
        self.daemon.pause()

    def cont(self):
        self.daemon.cont()