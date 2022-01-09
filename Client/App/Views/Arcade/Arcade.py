from ...UI.Base import Document as doc
from ...Core.Diagnostics.Debugging import Console

class Document(doc):
    Name = "Pong/Arcade"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .NewGame import Document as NewGame
        Console.info("Redirecting to new arcade game")
        self.Window.Document = NewGame
