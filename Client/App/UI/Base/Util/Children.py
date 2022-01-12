from ....Core.Diagnostics.Debugging import Console

class Children(list):
    def __init__(self, parent,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Parent = parent

    def __iadd__(self, other):
        try:
            if other in self:
                Console.error(f"{other} is already a child of me")
                return self
            self.append(other)
            other._SetParent(self.Parent)
            if self.Parent.InitialRenderDone:
                other.Render()
                self.Parent.Update(propogationDepth=float('inf'), ReRender=True)
        except Exception as e:
            print(e)
            raise TypeError(f"Cannot add type {type(other)} as child")

        return self

    def __isub__(self, other):
        self.Remove(other)

    def Remove(self, item):
        if item in self:
            self.remove(item)