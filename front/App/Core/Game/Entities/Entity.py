class Entity:
    '''Anything that is added to our game'''
    # Entity is one of the intersections between engine and ui

    def __init__(self, dynamic = False):
        self.Dynamic = dynamic

    def Draw(self):
        '''Called every frame'''
        pass