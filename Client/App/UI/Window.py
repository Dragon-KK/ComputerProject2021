from .Base.Util import IntervalContainer, TimeoutContainer
from ..Core.Diagnostics.Debugging import Console
from ..Core.DataTypes.Standard import Vector
from .Base.Util.Resources import ResourceManager
from .Base import Document
from ..Core import Resources
import tkinter as tk
class Window:
    '''Create a new window'''

    def __init__(self, resizable = False, title = "New Window", windowSize = Vector(300,300)):
        self._tkRoot = tk.Tk() # Store root of out tkinter window

        self.__viewPort = windowSize
        self._tkRoot.geometry(f'{self.__viewPort.x}x{self.__viewPort.y}') # Set size of the window
        self._tkRoot.wm_attributes("-transparentcolor", "#000001")
        self.__minSize = Vector(0,0)

        self.Title = title # Sets title
        self._Document = None

        self.Resources = ResourceManager()
        # Add Resources
        self.Resources += Resources.Storage()
        self.Resources += Resources.Audio()
        self.Resources += Resources.Images()
        self.Resources += Resources.Networking()

        self.Intervals = IntervalContainer(self)
        self.Timeouts = TimeoutContainer(self)

        if not resizable: self._tkRoot.resizable(0,0) # This makes the window unresizable

        self._tkRoot.protocol("WM_DELETE_WINDOW", self.OnClose)
        self._tkRoot.bind("<Configure>", self.OnResize)

        Console.info("Initializing Window")

    def Run(self):
        Console.info("Showing Window")
        self._tkRoot.mainloop() # Starts UI loop

    def OnResize(self,event):
        if(event.widget == self._tkRoot and (self.ViewPort.x != event.width or self.ViewPort.y != event.height)):
            # If the window is resized, i update my viewport
            self.ViewPort = Vector(event.width, event.height)

    def OnClose(self):
        self.Resources.RemoveAll()
        self.Document.Destroy() if self.Document else None # Destroy the document
        self.Timeouts.EndAll()
        self.Intervals.EndAll()
        self._tkRoot.destroy() # Destroy the tkinter window
        Console.info("Closing Window")

    def __InstantiateDocument(self, docConstructor):
        Console.info(f"Rendering document {docConstructor.Name}")
        self._Document = docConstructor(self)
        # The minimum size of the window is given by the document it is rendering
        self.MinSize = self._Document.MinSize
        
        self._Document.Render()

    #region Document
    @property
    def Document(self):
        return self._Document
    @Document.setter
    def Document(self, docConstructor):
        if self.Document:
            self.Document.Destroy()
        self.Timeouts.SetTimeout(1, lambda : self.__InstantiateDocument(docConstructor)) # THis is to avoid long error messages
    #endregion


    # region ViewPort
    @property
    def ViewPort(self):
        return self.__viewPort
    @ViewPort.setter
    def ViewPort(self, value):
        self.__viewPort = value
        if self.Document:
            # When my viewport is updated i need to update all the elements on the document
            self.Document.Update(float('inf'))    
    #endregion ViewPort

    # region MinSize
    @property
    def MinSize(self):
        return self.__minSize
    @MinSize.setter
    def MinSize(self, value):
        self.__minSize = value

        # Sets the minimum size of the tkinter window
        self._tkRoot.minsize(self.__minSize.x,self.__minSize.y)
    #endregion Minsize
    
    # region Title
    @property
    def Title(self):
        return self._tkRoot.title()
    @Title.setter
    def Title(self, value):
        self._tkRoot.title(value)
    # endregion

    
