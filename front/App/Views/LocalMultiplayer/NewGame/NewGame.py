from ....Core.DataTypes.UI import Interval, EventListener
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.Components import *
from ....UI.Elements import *


class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/LocalMultiplayer/NewGame"
    StyleSheet = "Styles/LocalMultiplayer/NewGame.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += container

        

        
