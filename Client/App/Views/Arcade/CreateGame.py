from ...UI.Base import Document
from ...UI.Elements import div,img,label,radio
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer

class CreateGame(Document):
    Name = "Pong/Arcade/CreateGame"
    StyleSheet = "Styles/Arcade/CreateGame.json"
    ResourceKey = "Arcade"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # region Background
        container = AspectRatioPreservedContainer() # The container
        self.Children += container # Add child
        background = img(self.Window.Resources.Images.Background,classes = ".background") # The background
        container.Children += background # Add child
        # endregion

        # title
        title = label(text="Arcade", classes = ".title")
        background.Children += title

        # region goHomeButton
        goHomeButton = img(self.Window.Resources.Images.Home, classes = ".goHome .imgButton")
        goHomeButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("MainMenu"))
        background.Children += goHomeButton
        # endregion

        self.SelectDifficultyBox = div(classes = ".selectionBox")
        background.Children += self.SelectDifficultyBox
        self.PopulateDifficultyBox()

    def PopulateDifficultyBox(self):
        mintitle = label(classes = ".miniTitle", text = "Select Difficulty")
        self.SelectDifficultyBox.Children += mintitle
        self.OptionsRadio = radio(classes = ".optionsRadio")
        self.SelectDifficultyBox.Children += self.OptionsRadio

        self.OptionsRadio.Children += label(text = "Beginner",classes = ".option .lvl1")
        self.OptionsRadio.Children += label(text = "Novice",classes = ".option .lvl2")
        self.OptionsRadio.Children += label(text = "Amateur",classes = ".option .lvl3")
        self.OptionsRadio.Children += label(text = "Expert",classes = ".option .lvl4")
        self.OptionsRadio.Children += label(text = "Impossible",classes = ".option .lvl5")

        self.OptionsRadio.SelectedElement = self.OptionsRadio.Children[0]

        startButton = label(text="Start", classes = ".startButton")
        startButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("PlayGame"))
        self.SelectDifficultyBox.Children += startButton


    def NavigateTo(self, dest):
        if dest == "MainMenu":
            from ..MainMenu import MainMenu
            self.Window.ChangeDocumentTo(MainMenu)
        elif dest == "PlayGame":
            self.SetSettings()
            from .PlayGame import PlayGame
            self.Window.ChangeDocumentTo(PlayGame)

    def SetSettings(self):
        difficulty = self.OptionsRadio.SelectedElement.Text
        if difficulty == "Beginner":
            self.Window.Resources.Storage.Arcade['GameSettings'] = {
                "Difficulty" : 40,
                "DifficultySlope" : 0,
                "BallCount" : 1,
                "Duece" : False,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.Arcade['Difficulty'] = 'Beginner'
        elif difficulty == "Novice":
            self.Window.Resources.Storage.Arcade['GameSettings'] = {
                "Difficulty" : 40,
                "DifficultySlope" : 0.01,
                "BallCount" : 1,
                "Duece" : False,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.Arcade['Difficulty'] = 'Novice'
        elif difficulty == "Amateur":
            self.Window.Resources.Storage.Arcade['GameSettings'] = {
                "Difficulty" : 30,
                "DifficultySlope" : 0.1,
                "BallCount" : 1,
                "Duece" : False,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.Arcade['Difficulty'] = 'Amateur'
        elif difficulty == "Expert":
            self.Window.Resources.Storage.Arcade['GameSettings'] = {
                "Difficulty" : 30,
                "DifficultySlope" : 0.1,
                "BallCount" : 2,
                "Duece" : False,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.Arcade['Difficulty'] = 'Expert'         
        elif difficulty == "Impossible":
            self.Window.Resources.Storage.Arcade['GameSettings'] = {
                "Difficulty" : 40,
                "DifficultySlope" : 0.01,
                "BallCount" : 5,
                "Duece" : False,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.Arcade['Difficulty'] = 'Impossible'