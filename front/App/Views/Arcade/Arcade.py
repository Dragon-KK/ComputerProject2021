from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...Core.DataTypes.Standard import Vector
from PIL import Image

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/Arcade"
    ResourceKey = "Arcade"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Children += img(self.Window.Resources.Images.Arcade.Play,name=".img")

    def Destroy(self):
        super().Destroy()
