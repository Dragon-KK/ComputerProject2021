from .Util import ComputeStyles,CanvasIDContainer,Children
from ...Core.DataManagers import FileManager
from ..Styles import Style
class Root:
    '''Like an element but without a parent'''
    def __init__(self, window, computedStyles, stylePath):
        self.Parent = None # The parent of this element
        
        self.InitialRenderDone = False # Just for some checks
        self.Children = Children(self) # The children of this element
        self.Window = window # Gets hold of the window object

        self._CanvasIDs = CanvasIDContainer()

        self.Styles = FileManager.ReadJson(stylePath)

        self.__ComputedStyles = computedStyles # Computed Styles


    def GetStylesByClassName(self, name):
        return self.Styles.get(name, [])  
   
 
    

        
            
    def Remove(self):
        '''Removes the element and its children visually'''
        self.Window.Document._RemoveVisual(self._CanvasIDs.list)
        self._CanvasIDs.clear()
        for child in self.Children:
            child.Remove() # Removes every child

    def Update(self, propogationDepth = 0):
        self.__ComputedStyles.Size = self.Window.ViewPort
        if propogationDepth: # Probably not needed but meh why not
            for child in self.Children:
                child.Update(propogationDepth - 1)
    
    # region ComputedStyles
    @property
    def ComputedStyles(self):
        return self.__ComputedStyles
    # endregion
