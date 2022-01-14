from ..Helper import ComputedStyles,Children,EventHandler
from ...Core.DataManagers import FileManager
from ..Base.typeHintingHelp import Window
class Root:
    '''Like an element but without a parent'''
    def __init__(self, window : Window, computedStyles, stylePath, elementStylesPath = "Styles/ElementStyles.json"):
        self.Parent = None # The parent of this element
        
        self.InitialRenderDone = False # Just for some checks
        self.Children = Children(self) # The children of this element
        self.Window = window # Gets hold of the window object

        self.Styles = FileManager.ReadJson(stylePath)
        self.ElementStyles = FileManager.ReadJson(elementStylesPath)

        self.__STYLE_UNITS = {}
        self.EventHandler = EventHandler(self)
        self.__ComputedStyles = computedStyles # Computed Styles

    def _GetStyleUnits(self):
        return {
            "em" : self.__ComputedStyles.Size.x / 100
        }
    @property
    def STYLE_UNITS(self):
        """The STYLE_UNITS property."""
        return self._GetStyleUnits()

    def GetStylesByClassName(self, name):
        return self.Styles.get(name, []) 

    def GetStylesByElement(self, elementName):
        return self.ElementStyles.get(elementName, [])

    def Render(self):
        '''Renders the element and its children'''        
        self.InitialRenderDone = True
        for child in self.Children:
            child.Render()
        self.EventHandler.SetEventListeners()
            
    def Remove(self):
        '''Removes the element and its children visually'''
        for child in self.Children:
            child.Remove() # Removes every child

    def Update(self, propogationDepth = 0, **kwargs):
        self.__ComputedStyles.Size = self.Window.ViewPort
        
        if propogationDepth: # Probably not needed but meh why not
            for child in self.Children:
                child.Update(propogationDepth = propogationDepth - 1)
    
    # region ComputedStyles
    @property
    def ComputedStyles(self):
        return self.__ComputedStyles
    # endregion
