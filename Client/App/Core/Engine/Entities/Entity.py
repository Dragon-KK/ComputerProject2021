class Entity:
    '''
    Some thing
    An Item that is in our game
    '''

    def __init__(self, sprite, dynamic = True, tag = "default"):
        self.Sprite = sprite # is basically a App.UI.Components.Sprite
        self.Dynamic = dynamic # Whether the thing should be updated every frame or not
        # Note that on events like window resize or state change sprite.Update will automatically be called

        self.Tag = tag

    def Reset(self):
        '''Called when world is reset'''
        pass

    def SetStyles(self, Styles):
        self.Sprite.Styles.__dict__.update(Styles)

    def Render(self):
        if not self.Dynamic:return # If im not dynamic dont frameupdate
        self.Sprite.FrameUpdate()