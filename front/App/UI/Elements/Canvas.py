from ..Elements import div

class Canvas(div):
    '''
    The element that can interact with our Engine
    '''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def OnRender(self):
        pass
        
    def RegisterSprite(self, sprite):
        self.Children += sprite

    def RemoveSprite(self, sprite):
        self.Children -= sprite

    def _Render(self):
        super()._Render()
        self.OnRender()

    

        


