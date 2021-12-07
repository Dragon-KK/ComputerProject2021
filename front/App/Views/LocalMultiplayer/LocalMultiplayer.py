from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...UI import Styles
from ...Core.DataTypes.Standard import Vector


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.d = div(
            styles=Styles.Style(
                Size=("60:w%", "50:h%"),
                Position=("50:w%", "50:h%"),
                CornerRadius="10:vw",
                OriginType=4,
                BackgroundColor="Red",
                BorderColor="Green",
                BorderStroke=5
            )
        )
        def bclick2(e):
            from ..MainMenu import Document as MainMenu
            print("bclick2")
            self.Window.Document = MainMenu

        def bclick(e):
            print("bclick1")
            self.d.Styles\
                .Set("Size" ,("20:w%", "50:h%"))\
                .Set("Position", ("50:w%","50:h%"))
            self.d.AddEventListener("<Button-3>", bclick2)
        self.d.AddEventListener("<Button-1>", bclick)
        self.Children += self.d
