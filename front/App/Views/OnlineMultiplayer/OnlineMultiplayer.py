from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...UI import Styles
from ...Core.DataTypes.Standard import Vector


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/OnlineMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Children += label(name=".title",text="Online Mult",ResizeCorrectionConst=1.6)

        self.Children += input(name=".input", placeHolder="Enter some text")
