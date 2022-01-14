from .Root import Root
from ...Core.DataTypes.UI import Event
from tkinter import Canvas
from ...Core.DataTypes.Standard import Vector
from ...Core.Diagnostics.Debugging import Console
from ..Helper import ComputedStyles,States,EventHandler
from ...Core.DataTypes.UI import Event,ContentContainer


# The intersection between tkinter and our custom thing
class Document(Root, Canvas):    
    '''Every window has 1 active document'''

    Name = "Default"
    MinSize = Vector(500,350)
    StyleSheet = "Styles/DefaultStyles.json"
    ResourceKey = "None"
            
    def __init__(self, window):

        cstyles = ComputedStyles()
        cstyles.Size = window.ViewPort

        Canvas.__init__(self,window._tkRoot,bg="black") # Init canvas        
        Root.__init__(self,window,cstyles,self.StyleSheet) # Init root
        # Load resources
        self.Window.Resources.Images.LoadResources(self.ResourceKey)
        self.place(relx = 0,rely = 0,relheight =1, relwidth = 1) # tkinter stuff

        self._FocusedElement = None
        self._KeyboardFocusedElement = None

    @property
    def FocusedElement(self):
        """The FocusedElement property."""
        return self._FocusedElement
    @FocusedElement.setter
    def FocusedElement(self, value):
        if self._FocusedElement:
            self._FocusedElement.OnFocusLoss()
        self._FocusedElement = value
        if value:value.OnFocusGain()

    @property
    def KeyboardFocusedElement(self):
        """The FocusedElement property."""
        return self._KeyboardFocusedElement
    @KeyboardFocusedElement.setter
    def KeyboardFocusedElement(self, value):
        if self._KeyboardFocusedElement:
            self._KeyboardFocusedElement.OnKeyboardFocusLoss()
        self._KeyboardFocusedElement = value
        if value:value.OnKeyboardFocusGain()

    def _Destroy(self):
        pass

    def Destroy(self):
        Console.info(f"Closing Document {self.Name}")
        self._Destroy()
        self.Remove() # Element.Remove
        self.destroy() # Canvas.destroy

    def _RemoveVisual(self, canvasIDs):
        self.delete(*canvasIDs)