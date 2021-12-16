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

    def Initialize(self):
        '''Anything that must be done before after rendering but before game starts must be done here'''
        pass

    def SetStyles(self, Styles):
        for prop in Styles:
            self.Sprite.Styles.Set(prop, Styles[prop])

    def Render(self):
        if not self.Dynamic:return
        self.Sprite.Update(updateRender = True)