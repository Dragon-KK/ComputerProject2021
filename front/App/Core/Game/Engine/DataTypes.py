class EntityHolder(list):
    def __init__(self):
        super().__init__()

    def AddEntity(self,entity):
        self.append(entity)

    def RemoveEntity(self, entity):
        if entity in self:
            self.remove(entity)

    def __add__(self, entity):
        self.AddEntity(entity)
        return self
    def __iadd__(self, entity):
        self.AddEntity(entity)
        return self

    def __sub__(self, entity):
        self.RemoveEntity(entity)
        return self
    def __isub__(self, entity):
        self.RemoveEntity(entity)
        return self