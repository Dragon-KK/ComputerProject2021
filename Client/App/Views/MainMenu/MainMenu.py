from ...Core.DataTypes.UI import EventListener
from ...Core.DataTypes.Standard import Vector
from ...UI.Base import Document as doc
from ...UI.Components import *
from ...UI.Elements import *

class Document(doc):
    Name = "Pong/MainMenu"
    MinSize = Vector(500, 500)
    StyleSheet = "Styles/MainMenu.json"

    def NavigateTo(self, destination):
        if destination == "LocalMultiplayer":
            from ..LocalMultiplayer import Document as LocalMultiplayer
            self.Window.Document = LocalMultiplayer
        elif destination == "OnlineMultiplayer":
            from ..OnlineMultiplayer import Document as OnlineMultiplayer
            self.Window.Document = OnlineMultiplayer
        elif destination == "AboutUs":
            from ..AboutUs import Document as AboutUs
            self.Window.Document = AboutUs
        elif destination == "Arcade":
            from ..Arcade import Document as Arcade
            self.Window.Document = Arcade

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)        
        self.Children += container

        # Title
        container.Children += label(name=".title",text="PONG")        

        # region LocalMultiplayer Button
        LocalMultiplayerButton = label(name=".navigationButton", text="Local")
        LocalMultiplayerButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("LocalMultiplayer"))
        LocalMultiplayerButton.Styles.Set(
            "Position", ("37:w%", "70:h%")
        )
        container.Children += LocalMultiplayerButton
        # endregion

        # region OnlineMultiplayer Button
        OnlineMultiplayerButton = label(name=".navigationButton", text="Online")
        OnlineMultiplayerButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("OnlineMultiplayer"))
        OnlineMultiplayerButton.Styles.Set(
            "Position", ("63:w%", "70:h%")
        )
        container.Children += OnlineMultiplayerButton
        # endregion

        # region AboutUs Button
        AboutUsButton = label(name=".navigationButton", text="About")
        AboutUsButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("AboutUs"))
        AboutUsButton.Styles.Set(
            "Position", ("37:w%", "85:h%")
        )
        container.Children += AboutUsButton
        # endregion

        # region Arcade Button
        ArcadeButton = label(name=".navigationButton", text="Arcade")
        ArcadeButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs:self.NavigateTo("Arcade"))
        ArcadeButton.Styles.Set(
            "Position", ("63:w%", "85:h%")
        )
        container.Children += ArcadeButton
        # endregion
