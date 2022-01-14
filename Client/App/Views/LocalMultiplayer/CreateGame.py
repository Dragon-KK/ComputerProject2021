from ...UI.Base import Document
from ...UI.Elements import div,img,label,radio,input
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer

class CreateGame(Document):
    Name = "Pong/LocalMultiplayer/CreateGame"
    StyleSheet = "Styles/LocalMultiplayer/CreateGame.json"
    ResourceKey = "LocalMultiplayer"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # region Background
        container = AspectRatioPreservedContainer() # The container
        self.Children += container # Add child
        background = img(self.Window.Resources.Images.Background,classes = ".background") # The background
        container.Children += background # Add child
        # endregion

        # title
        title = label(text="Local Multiplayer", classes = ".title")
        background.Children += title

        # region goHomeButton
        goHomeButton = img(self.Window.Resources.Images.Home, classes = ".goHome .imgButton")
        goHomeButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("MainMenu"))
        background.Children += goHomeButton
        # endregion

        self.SelectDifficultyBox = div(classes = ".selectionBox")
        background.Children += self.SelectDifficultyBox
        self.PopulateDifficultyBox()

        self.SelectWinCriteriaBox = div(classes = ".selectionBox", states = [])
        background.Children += self.SelectWinCriteriaBox
        self.PopulateWinCriteriaBox()

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

        startButton = label(text="Select", classes = ".startButton")
        startButton.EventListeners += EventListener("<Button-1>", lambda e:self.ShowWinCriteriaBox())
        self.SelectDifficultyBox.Children += startButton

    def ShowWinCriteriaBox(self):
        self.SetSettingsFromDifficultyLevel()
        self.Window.Title += f" ({self.OptionsRadio.SelectedElement.Text})"
        self.SelectDifficultyBox.Remove()
        self.SelectWinCriteriaBox.State += "Visible"

    def PopulateWinCriteriaBox(self):
        self.Duece = self.Window.Resources.Storage.LocalMultiplayer['GameSettings']['Duece']
        raceTo = self.Window.Resources.Storage.LocalMultiplayer['GameSettings']['WinCondition']

        mintitle = label(classes = ".miniTitle", text = "Select Win Criteria")
        self.SelectWinCriteriaBox.Children += mintitle

        startButton = label(text="Start", classes = ".startButton")
        startButton.EventListeners += EventListener("<Button-1>", lambda e:self.NavigateTo("PlayGame"))
        self.SelectWinCriteriaBox.Children += startButton

        allowDuece = label(classes = ".allowDueceToggles" + (" .confirmGreen" if self.Duece else ""),text = "Allow Duece" if self.Duece else "No Duece")
        allowDuece.EventListeners += EventListener("<Button-1>", lambda e:ToggleDueceSelect())
        self.SelectWinCriteriaBox.Children += allowDuece

        self.winConditionInput = input(classes = '.winCondInp',Type=int,allowNegative=False,placeHolder="Race to ? Eg: 5",maxLength=3)
        self.SelectWinCriteriaBox.Children += self.winConditionInput

        def ToggleDueceSelect():
            if self.Duece:
                allowDuece.Text = "No Duece"
                allowDuece.ClassList.RemoveClass(".confirmGreen")
            else:
                allowDuece.Text = "Allow Duece"
                allowDuece.ClassList.AddClass(".confirmGreen")
            self.Duece = not self.Duece

    def NavigateTo(self, dest):
        if dest == "MainMenu":
            from ..MainMenu import MainMenu
            self.Window.ChangeDocumentTo(MainMenu)
        elif dest == "PlayGame":
            self.SetSettings()
            from .PlayGame import PlayGame
            self.Window.ChangeDocumentTo(PlayGame)

    def SetSettings(self):
        curr = self.Window.Resources.Storage.LocalMultiplayer['GameSettings']
        curr['Duece'] = self.Duece
        v = self.winConditionInput.Value
        curr['WinCondition'] = v if v > 0 else 5
        self.Window.Resources.Storage.LocalMultiplayer['GameSettings'] = curr
        

    def SetSettingsFromDifficultyLevel(self):
        difficulty = self.OptionsRadio.SelectedElement.Text
        if difficulty == "Beginner":
            self.Window.Resources.Storage.LocalMultiplayer['GameSettings'] = {
                "Difficulty" : 40,
                "DifficultySlope" : 0,
                "BallCount" : 1,
                "Duece" : self.Duece,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.LocalMultiplayer['Difficulty'] = 'Beginner'
        elif difficulty == "Novice":
            self.Window.Resources.Storage.LocalMultiplayer['GameSettings'] = {
                "Difficulty" : 40,
                "DifficultySlope" : 0.01,
                "BallCount" : 1,
                "Duece" : self.Duece,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.LocalMultiplayer['Difficulty'] = 'Novice'
        elif difficulty == "Amateur":
            self.Window.Resources.Storage.LocalMultiplayer['GameSettings'] = {
                "Difficulty" : 30,
                "DifficultySlope" : 0.1,
                "BallCount" : 1,
                "Duece" : self.Duece,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.LocalMultiplayer['Difficulty'] = 'Amateur'
        elif difficulty == "Expert":
            self.Window.Resources.Storage.LocalMultiplayer['GameSettings'] = {
                "Difficulty" : 30,
                "DifficultySlope" : 0.1,
                "BallCount" : 2,
                "Duece" : self.Duece,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.LocalMultiplayer['Difficulty'] = 'Expert'         
        elif difficulty == "Impossible":
            self.Window.Resources.Storage.LocalMultiplayer['GameSettings'] = {
                "Difficulty" : 40,
                "DifficultySlope" : 0.01,
                "BallCount" : 5,
                "Duece" : self.Duece,
                "WinCondition" : 0,
            }
            self.Window.Resources.Storage.LocalMultiplayer['Difficulty'] = 'Impossible'