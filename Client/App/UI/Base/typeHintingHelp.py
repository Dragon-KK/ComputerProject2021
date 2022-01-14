from ...Core.DataTypes.Standard import Vector
from ..Base import Document
from ..Helper import ResourceManager
class Window:
    '''Create a new window'''

    def __init__(self, resizable = False, title = "New Window", windowSize = Vector(300,300)):
        self.Title:str = ""
        self.Document : Document = None
        self.MinSize : Vector = Vector(0,0)
        self.ViewPort : Vector = Vector(0,0)
        self.Resources = ResourceManager()
        # # Add Resources
        # self.Resources += Resources.Storage()
        # self.Resources += Resources.Audio()
        # self.Resources += Resources.Images()

        # self.Intervals = IntervalContainer(self)
        # self.Timeouts = TimeoutContainer(self)

        Console.info("Initializing Window")

    def ChangeDocument(self, newDocument):
        # self.Resources.RemoveAll()
        # self.Timeouts.EndAll()
        # self.Intervals.EndAll()
        self.Document.Destroy() if self.Document else None # Destroy the document
        self._tkRoot.after(10, self.__InstantiateDocument, newDocument)


    

    
