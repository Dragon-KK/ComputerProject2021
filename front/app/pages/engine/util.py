from time import time as time
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
            dt = 0.0000000001
            self.last = time()
        else:
            tmp = time()
            dt = tmp - self.last
            self.last = tmp
        self.slave(*self.args,dt = dt,**self.kwargs)
        self.loopID = self.tk.after(self.interval,self.work)