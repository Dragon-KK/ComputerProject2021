from ...Core.Diagnostics.Debugging import Console
from ...UI.Base import Document as doc

class Document(doc):
    '''This is just used for redirecting'''
    Name = "Pong/LocalMultiplayer"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
    def Render(self):
        from .NewGame import Document as NewGame
        Console.info("Redirecting to new game : )")
        self.Window.Document = NewGame
        
