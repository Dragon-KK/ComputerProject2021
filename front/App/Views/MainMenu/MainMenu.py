from ...Core.DataTypes.UI import EventListener
from ...Core.DataTypes.Standard import Vector
from ...UI.Base import Document as doc
from ...UI.Elements import *
from ...UI.Components import *
from ...UI import Styles

class Document(doc):
    Name = "Pong/MainMenu"
    MinSize = Vector(500, 100)
    StyleSheet = "Styles/MainMenu.json"

    def NavigateTo(self, destination):
        print("Lcik")    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        c = div(name=".container")
        container = AspectRatioPreservedContainer(aspectRatio=16/9)        
        self.Children += c
        c.Children += container
        # Title
        container.Children += label(name=".title",text="PONG",ResizeCorrectionConst=1.6)        

        # region LocalMultiplayer Button
        LocalMultiplayerButton = label(name=".navigationButton", text="Local", ResizeCorrectionConst=2.53)
        LocalMultiplayerButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("LocalMultiplayer"))
        LocalMultiplayerButton.Styles.Set(
            "Position", ("30:w%", "60:h%")
        )
        container.Children += LocalMultiplayerButton
        # endregion

        # region OnlineMultiplayer Button
        OnlineMultiplayerButton = label(name=".navigationButton", text="Online",  ResizeCorrectionConst=2.5)
        OnlineMultiplayerButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("OnlineMultiplayer"))
        OnlineMultiplayerButton.Styles.Set(
            "Position", ("70:w%", "60:h%")
        )
        container.Children += OnlineMultiplayerButton
        # endregion

        # region AboutUs Button
        AboutUsButton = label(name=".navigationButton", text="About", ResizeCorrectionConst=2.2)
        AboutUsButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("AboutUs"))
        AboutUsButton.Styles.Set(
            "Position", ("30:w%", "80:h%")
        )
        container.Children += AboutUsButton
        # endregion

        # region Arcade Button
        ArcadeButton = label(name=".navigationButton", text="Arcade", ResizeCorrectionConst=2.28)
        ArcadeButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("Arcade"))
        ArcadeButton.Styles.Set(
            "Position", ("70:w%", "80:h%")
        )
        container.Children += ArcadeButton
        # endregion
