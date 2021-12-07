from ...Core.DataTypes.UI import EventListener
from ...Core.DataTypes.Standard import Vector
from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...UI import Styles

class Document(doc):
    Name = "Pong/MainMenu"
    MinSize = Vector(500, 100)
    StyleSheet = "Styles/MainMenu.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Title
        self.Children += label(name=".title",text="PONG",ResizeCorrectionConst=1.6)
        
        