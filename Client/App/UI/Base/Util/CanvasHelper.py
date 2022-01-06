class CanvasIDContainer:

    def __init__(self):
        self.list = []

    def __add__(self,other):
        self.list.append(other)
        return self

    def clear(self):
        self.list.clear()