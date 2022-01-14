from ...Core.Diagnostics.Debugging import Console

class Children(list):
    def __init__(self, parent,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Parent = parent
        self.OnChildrenChanged = lambda *args,**kwargs:0

    def __iadd__(self, other):
        if other in self:
            Console.error(f"{other} is already a child of me")
            return self
        self.append(other)
        other._SetParent(self.Parent) # Set its parent
        other.Render() # Render it
        self.OnChildrenChanged(added = other)
        return self

    def __isub__(self, other):
        self.Remove(other)        

    def Remove(self, item):
        if item in self:
            self.remove(item)
            self.OnChildrenChanged(removed = item)