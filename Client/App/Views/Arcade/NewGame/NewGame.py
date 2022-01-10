from ....Core.DataTypes.UI import Interval, EventListener
from ....Core.DataTypes.UI import EventListener
from ....Core.DataTypes.Standard import Vector
from ....UI.Base import Document as doc
from ....UI.Components import *
from ....UI.Elements import *

class Document(doc):
    MinSize = Vector(1000, 500)
    Name = "Pong/Arcade/NewGame"
    ResourceKey = "Arcade"
    StyleSheet = "Styles/Arcade/NewGame.json"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config(bg="black") # Let the background be black

        # Container (since we want our page to preserve aspect ratio)
        container = AspectRatioPreservedContainer(name=".container",aspectRatio=16/9)
        self.Children += container

        # Title
        title = label(name = ".title", text = "Settings")
        container.Children += title

        # ContentContainer
        contentContainer = div(name = ".contentContainer")
        container.Children += contentContainer

        # region content
        
        # Go Home
        def GoHome():
            from ...MainMenu import Document as MainMenu
            self.Window.Document = MainMenu
        GoBackButton = img(self.Window.Resources.Images.Arcade.Home, name = ".goHome")
        GoBackButton.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs:GoHome())
        container.Children += GoBackButton

        # region DifficultySelector
        difficultySelectorContainer = div(name = ".difficultySelectorContainer")
        contentContainer.Children += difficultySelectorContainer

        difficultySelectorLabel = label(name = ".optionSelectorLabel", text="Difficulty")
        self.difficultySelectorInput = input(name = ".optionSelectorInput",Type = float,maxLength = 12, allowNegative=False)
        self.difficultySelectorInput.Value = self.Window.Resources.Storage.Arcade['GameSettings']['Difficulty']

        difficultySelectorContainer.Children += difficultySelectorLabel
        difficultySelectorContainer.Children += self.difficultySelectorInput        
        # endregion
        # region DifficultySlopeSelector
        difficultySlopeSelectorContainer = div(name = ".difficultySlopeSelectorContainer")
        contentContainer.Children += difficultySlopeSelectorContainer

        difficultySlopeSelectorLabel = label(name = ".optionSelectorLabel", text="Difficulty Slope")
        self.difficultySleopSelectorInput = input(name = ".optionSelectorInput", Type = float,maxLength = 12, allowNegative=False)
        self.difficultySleopSelectorInput.Value = self.Window.Resources.Storage.Arcade['GameSettings']['DifficultySlope']

        difficultySlopeSelectorContainer.Children += difficultySlopeSelectorLabel
        difficultySlopeSelectorContainer.Children += self.difficultySleopSelectorInput        
        # endregion
        # region BallCountSelector
        ballCountSelectorContainer = div(name = ".ballCountSelectorContainer")
        contentContainer.Children += ballCountSelectorContainer

        ballCountSelectorLabel = label(name = ".optionSelectorLabel", text="Ball Count")
        self.ballCountSelectorInput = input(name = ".optionSelectorInput", Type = int,maxLength = 12, allowNegative=False)
        self.ballCountSelectorInput.Value = self.Window.Resources.Storage.Arcade['GameSettings']['BallCount']

        ballCountSelectorContainer.Children += ballCountSelectorLabel
        ballCountSelectorContainer.Children += self.ballCountSelectorInput        
        # endregion
        
        # Start button
        startButton = label(".startButton", text = "Start")
        startButton.EventListeners += EventListener("<Button-1>", lambda *args, **kwargs : self.StartRound())
        contentContainer.Children += startButton

        # endregion

    def GetSettings(self):
        return {
            'Difficulty' : self.difficultySelectorInput.Value,
            'DifficultySlope' : self.difficultySleopSelectorInput.Value,
            'BallCount' : self.ballCountSelectorInput.Value,
            'Duece' : False,
            'WinCondition' : 1
        }

    def StartRound(self):
        settings = self.GetSettings()
        self.Window.Resources.Storage.Arcade['GameSettings'] = settings
        from ..Game import Document as Game
        self.Window.Document = Game 

        

        
