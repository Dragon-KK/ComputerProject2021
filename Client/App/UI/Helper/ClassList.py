class ClassList(list):
    def __init__(self):
        self.OnClassListChange = lambda *args,**kwargs:0

    def AddClass(self,Cls, notify = True):
        if Cls not in self:
            self.append(Cls)
            if notify:self.OnClassListChange(added = self[-1])

    def RemoveClass(self, Cls, notify = True):
        if Cls in self:
            self.remove(Cls)
            if notify:self.OnClassListChange(removed = Cls)
        return self

    def __add__(self, other):
        self.AddClass(other)
        return self

    def __sub__(self,other):
        self.RemoveClass(other)
        return self

    def __iadd__(self, other):
        self.AddClass(other)
        return self

    def __isub__(self,other):
        self.RemoveClass(other)
        return self