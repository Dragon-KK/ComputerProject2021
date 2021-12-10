from .Root import Root
from ...Core.DataTypes.UI import Event
from tkinter import Canvas
from ...Core.DataTypes.Standard import Vector
from ...Core.Diagnostics.Debugging import Console
from ..Styles import Style
from .Util.StyleParser import ComputedStyles
from .Util import States,EventHandler
from ...Core.DataTypes.UI import Event,ContentContainer


# The intersection between tkinter and our custom thing
class Document(Root, Canvas):    
    '''Every window has 1 active document'''

    Name = "Default"
    MinSize = Vector(0, 0)
    StyleSheet = "Styles/DefaultStyles.json"

    def __init__(self, window):

        cstyles = ComputedStyles()
        cstyles.Size = window.ViewPort

        self.Content = ContentContainer()

        Root.__init__(self, window,cstyles,self.StyleSheet) # Init root
        Canvas.__init__(self,window._tkRoot,bg="white") # Init canvas

        self.EventHandler = EventHandler(self)
        self.place(relx = 0,rely = 0,relheight =1, relwidth = 1) # tkinter stuff
        
        self.__FocusedElement = None # No element is focused at the beginning
        self.__KeyboardFocusedElement = None # No element is focused at the beginning

    def Render(self):
        '''Renders the element and its children'''        
        for child in self.Children:
            child.Render()
        self.InitialRenderDone = True
        self.EventHandler.SetEventListeners()

    @property
    def FocusedElement(self):
        return self.__FocusedElement

    @FocusedElement.setter
    def FocusedElement(self,value):
        if self.FocusedElement:
            self.FocusedElement.LoseFocus()
        self.__FocusedElement = value
        value.State += States.Focused

    @property
    def KeyboardFocusedElement(self):
        return self.__KeyboardFocusedElement

    @KeyboardFocusedElement.setter
    def KeyboardFocusedElement(self,value):
        if self.KeyboardFocusedElement:
            self.KeyboardFocusedElement.LoseKeyboardFocus()
        self.__KeyboardFocusedElement = value
        value.State += States.KeyboardFocused
        


    def Destroy(self):
        Console.info(f"Closing Document {self.Name}")
        self.Remove() # Element.Remove
        self.destroy() # Canvas.destroy

    def __OnKeyEvent(self, e):
        for listener in self.__KeyEventListeners:
            listener(e)

    def _AddEventListenerForElement(self,code,element):
        if code == "<Key>":
            self.__KeyEventListeners.append(lambda *args,**kwargs:self._CallChildEvent(element, code, args, kwargs))
        else:
            for Id in element._CanvasIDs.list:
                self.tag_bind(Id, code,lambda *args,**kwargs: self._CallChildEvent(element,code,args,kwargs))

    def _CallChildEvent(self, element, eventCode, args,kwargs):
        '''Sends the event to the children listening'''
        element.OnEvent(
            Event(element, eventCode, *args, **kwargs)
        )

    def _RemoveVisual(self, canvasIDs):
        self.delete(*canvasIDs)
