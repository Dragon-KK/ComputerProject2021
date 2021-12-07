from ...Core.DataTypes.UI import EventListener
from ...Core.DataTypes.Standard import Vector
from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...UI import Styles

class Document(doc):
    Name = "Pong/MainMenu"
    MinSize = Vector(500, 100)
    StyleSheet = "Styles/MainMenu.json"

    def NavigateTo(self, destination):
        pass
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Title
        self.Children += label(name=".title",text="PONG",ResizeCorrectionConst=1.6)
        
        # region LocalMultiplayer Button
        LocalMultiplayerButton = label(name=".navigationButton", text="Local")
        LocalMultiplayerButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("LocalMultiplayer"))
        LocalMultiplayerButton.Styles.Set(
            "Position", ("30:w%", "60:h%")
        )
        self.Children += LocalMultiplayerButton
        # endregion
        # region OnlineMultiplayer Button
        OnlineMultiplayerButton = label(name=".navigationButton", text="Online")
        OnlineMultiplayerButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("OnlineMultiplayer"))
        OnlineMultiplayerButton.Styles.Set(
            "Position", ("70:w%", "60:h%")
        )
        self.Children += OnlineMultiplayerButton
        # endregion
        # region AboutUs Button
        AboutUsButton = label(name=".navigationButton", text="About")
        AboutUsButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("AboutUs"))
        AboutUsButton.Styles.Set(
            "Position", ("30:w%", "80:h%")
        )
        self.Children += AboutUsButton
        # endregion
        # region Arcade Button
        Arcadebutton = label(name=".navigationButton", text="Arcade")
        Arcadebutton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("Arcade"))
        Arcadebutton.Styles.Set(
            "Position", ("70:w%", "80:h%")
        )
        self.Children += Arcadebutton
        # endregion

