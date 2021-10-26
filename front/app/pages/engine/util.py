class Daemon:
    def __init__(self,tk, interval, slave, *args, **kwargs):
        self.interval = interval
        self.args = args
        self.tk = tk
        self.loopID = tk.after(interval, self.work)
        self.kwargs = kwargs
        self.slave = slave
        self.paused = False

    def pause(self):
        self.paused = True
        self.tk.after_cancel(self.loopID)

    def cont(self):
        self.paused = False
        self.work()   
    

    def work(self):
        if self.paused:return
        self.slave(*self.args,**self.kwargs)
        self.loopID = self.tk.after(self.interval,self.work)