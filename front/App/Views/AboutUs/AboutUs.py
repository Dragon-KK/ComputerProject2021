from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...Core.DataTypes.Standard import Vector


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Children += label(name=".title",text="About")
