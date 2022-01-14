from ...UI.Base import Document
from ...UI.Elements import div,img,label
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer

class MainMenu(Document):
    Name = "Pong/MainMenu"
    StyleSheet = "Styles/MainMenu/MainMenu.json"
    ResourceKey = "MainMenu"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # region Background
        container = AspectRatioPreservedContainer() # The container
        self.Children += container # Add child
        background = img(self.Window.Resources.Images.Background,classes = ".background") # The background
        container.Children += background # Add child
        # endregion

        # title
        title = label(text="PONG", classes = ".title")
        background.Children += title

        # region Navigation buttons
        onlineButton = label(text="Online Multiplayer", classes = ".navigationButton .onlineButton")
        localButton = label(text="Local Multiplayer", classes = ".navigationButton .localButton")
        arcadeButton = label(text="Arcade", classes = ".navigationButton .arcadeButton")
        quitButton = label(text="Quit", classes = ".navigationButton .quitButton")

        onlineButton.EventListeners += EventListener("<Button-1>", lambda e: self.NavigateTo('Online'))
        localButton.EventListeners += EventListener("<Button-1>", lambda e: self.NavigateTo('Local'))
        arcadeButton.EventListeners += EventListener("<Button-1>", lambda e: self.NavigateTo('Arcade'))
        quitButton.EventListeners += EventListener("<Button-1>", lambda e: self.QuitGame())

        background.Children += onlineButton
        background.Children += localButton
        background.Children += arcadeButton
        background.Children += quitButton
        # endregion

    def QuitGame(self):
        self.Window.Quit()

    def NavigateTo(self, dest):
        if dest == "Online":
            pass
        elif dest == "Local":
            from ..LocalMultiplayer import CreateGame
            self.Window.ChangeDocumentTo(CreateGame)
        elif dest == "Arcade":
            from ..Arcade import CreateGame
            self.Window.ChangeDocumentTo(CreateGame)