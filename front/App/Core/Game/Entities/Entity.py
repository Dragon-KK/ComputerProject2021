class Entity:
    '''Anything that is added to our game'''
    # Entity is one of the intersections between engine and ui

    def __init__(self, dynamic = False, tag = "default"):
        self.Dynamic = dynamic
        self.Canvas = None
        self.Sprite = None
        self.Tag = tag
        self.Styles = {}

    def Render(self):
        if self.Sprite:self.Sprite.Render()

    def Remove(self):
        pass

    def SetStyles(self, json):
        self.Styles.update(json)
        if self.Sprite:self.Sprite.SetStyles(self.Styles)

    def Update(self,*args,OnlyDynamic = False, **kwargs):
        '''Called every frame if its dynamic else called only when needed'''
        if (OnlyDynamic and not self.Dynamic):
            pass
        else:
            if self.Sprite:self.Sprite.Update()

    def _SetParent(self, canvas):
        self.Canvas = canvas
        print("up")