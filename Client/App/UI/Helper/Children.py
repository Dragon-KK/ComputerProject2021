from ...Core.Diagnostics.Debugging import Console

class Children(list):
    def __init__(self, parent,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Parent = parent
        self.OnChildrenChanged = lambda *args,**kwargs:0

    def Add(self, other, notify  = True):
        if other in self:
            Console.error(f"{other} is already a child of me")
            return self
        self.append(other)
        other._SetParent(self.Parent) # Set its parent
        other.Render() # Render it
        if notify:self.OnChildrenChanged(added = other)
    def __iadd__(self, other):
        self.Add(other)
        return self

    def __isub__(self, other):
        self.Remove(other)        

    def Remove(self, item, notify = True):
        if item in self:
            self.remove(item)
            if notify:self.OnChildrenChanged(removed = item)