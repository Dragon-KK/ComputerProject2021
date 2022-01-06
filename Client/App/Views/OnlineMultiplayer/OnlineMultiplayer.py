from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...Core.DataTypes.Standard import Vector


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/OnlineMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Children += label(name=".title",text="Online Mult")

        self.Children += input(name=".input", maxLength=10,placeHolder="Enter some text")
