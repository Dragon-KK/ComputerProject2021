from ...Core.DataTypes.Standard import Vector
from ...UI.Base import Document as doc
from ...UI.Components import *
from ...UI.Elements import *
from ...UI import Styles


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer/NewGame"
    StyleSheet = "Styles/LocalMultiplayer.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
