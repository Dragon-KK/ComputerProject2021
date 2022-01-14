from ...UI.Base import Document as doc
from ...UI.Elements import div,img
from ...Core.DataTypes.UI import EventListener
from ...UI.CustomElements import AspectRatioPreservedContainer

class Document(doc):
    StyleSheet = "Styles/MainMenu/MainMenu.json"
    ResourceKey = "MainMenu"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        d= img(self.Window.Resources.Images.Background,classes = ".background")
        def addcls(e):
            d.ClassList -= ".test"
        d.EventListeners += EventListener("<Button-1>", addcls)
        self.Children+=d