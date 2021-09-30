import tkinter as tk
class BindKeyDown:
    '''
    The keydown even in tkinter/windows (? idk) is shitty so this is a tmp fix
    '''
    def __init__(self,root : tk.Tk, msdelay = 100):
        root.bind_all("<KeyPress>", self.onKeyPressed) # whenever a key is pushed down, self.onKeyPressed is called
        root.bind_all("<KeyRelease>", self.onKeyRelease) # sem
        self.root = root # keep track of root
        self.toWatch = {} # dictionary with keysymbol : callback
        self.isDown = set() # set of all keys currently down
        self.paused = False # to pause all key events
        self.msdelay = msdelay # delat between each keydown callback
        self.callbackLoop() # start da loop

    def callbackLoop(self):
        if self.paused : return
        #print(self.isDown)
        for i in self.isDown: # for every key that is currently pushed
            self.toWatch[i][0](i) # call the callback
        self.root.after(self.msdelay, self.callbackLoop) # after msdelay call this function again

    def pause(self): # pauses all key events
        self.paused = True
    def cont(self): # continues all key events
        self.paused = False
        self.callbackLoop()
    def bindKey(self,keysym, down = print, up = lambda k:0): # bind a new key to keydown
        self.toWatch[keysym] = (down,up)
    def unbindKey(self,keysym): # unbind a key
        if not self.toWatch.get(keysym):return
        self.toWatch.__delitem__(keysym)
    def onKeyPressed(self,e):
        #print(e.keysym, self.toWatch)
        if e.keysym in self.toWatch:
            self.isDown.add(e.keysym)
    def onKeyRelease(self,e):
        if e.keysym in self.isDown:
            self.isDown.remove(e.keysym)

            if not self.paused:self.toWatch[e.keysym][1](e.keysym)
            
        