from ..Elements import div

class Canvas(div):
    '''
    The element that can interact with our Engine
    '''
    # region
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

    # endregion

    # region canvas methods
    def CreateCircle(self, centre, radius, **kwargs):
        centre += self.ComputedStyles.TopLeft
        return self.Window.Document.create_oval(centre.x - radius,centre.y + radius, centre.x + radius, centre.y - radius,fill='white')

    def UpdateItem(self, itemId, **kwargs):
        print('updating item',itemId)

    def MoveItem(self, itemId, displacement):
        print('moving item',itemId,displacement)
    # endregion

        


