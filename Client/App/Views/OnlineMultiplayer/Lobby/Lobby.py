from ....Core.DataTypes.UI import Interval, EventListener
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.Components import *
from ....UI.Elements import *

'''
In the lobby you connect to the server and can communicate to get another partner to play
Once you get the partners address it is saved in Storage
Then game is opened

In game the connection is made with the address saved in storage
and the game is started then
'''

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/OnlineMultiplayer/Lobby"
    StyleSheet = "Styles/OnlineMultiplayer/Lobby.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += container

        listbox = ListBox(name = ".listbox")
        container.Children += listbox
        
        for _ in range(12):
            listbox.Children += label(name = ".testItem", text = f"Item {_ + 1}")

        

        
