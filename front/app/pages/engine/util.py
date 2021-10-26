from time import time as time
# Honestly idk what a daemon actually does
# But i think usually daemons are used to manage threads and stuff
# The use of the class below is somewhat similar and plus the name sounds cool
class Daemon:
    def __init__(self,tk, interval, slave, *args, **kwargs):
        self.interval = interval
        self.args = args
        self.tk = tk
        self.loopID = tk.after(interval, self.work)
        self.kwargs = kwargs
        self.slave = slave
        self.paused = False
        self.last = 0

    def pause(self):
        self.paused = True
        self.tk.after_cancel(self.loopID)
        self.last = 0

    def cont(self):
        self.paused = False
        self.work()  
    

    def work(self):
        if self.paused:return
        if not self.last:
            dt = 0.0000000001 # idk why i put this number it shouldnt really matter 
            self.last = time()
        else:
            tmp = time()
            dt = tmp - self.last
            self.last = tmp
        self.slave(*self.args,dt = dt,**self.kwargs)
        self.loopID = self.tk.after(self.interval,self.work)

# we have atleast 6 util.py files lol i should probably use more descriptive names but util.py sounds professional so...