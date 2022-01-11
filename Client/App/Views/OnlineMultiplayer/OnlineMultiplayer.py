from ...Core.Diagnostics.Debugging import Console
from ...UI.Base import Document as doc


class Document(doc):
    Name = "Pong/OnlineMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .Lobby import Document as Lobby
        Console.info("Redirecting to online multiplayer lobby")
        self.Window.Document = Lobby
