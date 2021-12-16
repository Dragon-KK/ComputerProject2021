class EntityHolder(list):
    def __init__(self,container, Styles  = {}):
        super().__init__()
        self.Styles = Styles
        self.Container = container

    def AddEntity(self,entity):
        self.append(entity)
        entity.SetStyles(self.Styles.get(entity.Tag, {}))
        self.Container.Children += entity.Sprite

    def RemoveEntity(self, entity):
        if entity in self:
            self.remove(entity)
            self.Container.Children -= entity.Sprite

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