from .Util import ComputeStyles,EventListenersHolder, CanvasIDContainer, Children , StateHolder, States
from ..Styles import Style
from ...Core.DataTypes.UI import EventListener,ContentContainer
import inspect
class Element:
    # TODO
    # handle text overflow
    # Just have a rough take on how big a string will be and handle according to that

    # TODO
    # SetTimout and SetInterval

    # TODO
    # html knockoff is done :)
    # see how to make background transparent

    def __init__(self, name="."):
        self.Parent = None
        self.__name = name
        self.InitialRenderDone = False  # Just for some checks
        self.Children = Children(self)  # The children of this element
        self.Window = None
        self.Content = ContentContainer()

        self.State = StateHolder()
        self.State += "Visible"
        self.State.OnChange = self.UpdateBasedOnStyleSheet
        self._CanvasIDs = CanvasIDContainer()  # Storing the tkinter canvas ids

        self._Styles = Style()  # How the element looks
        self._ComputedStyles = None  # Computed Styles
        self.EventListeners = EventListenersHolder(self)

        self.__STYLE_UNITS = {}

        self.EventListeners += EventListener("<Enter>", lambda *args,**kwargs: self.__OnMouseEnter())
        self.EventListeners += EventListener("<Button-1>", lambda *args,**kwargs: self.GainKeyboardFocus())        
        self.EventListeners += EventListener("<Leave>", lambda *args,**kwargs: self.__OnMouseExit())

    def __OnMouseEnter(self):
        self.State += States.Hovered

    def __OnMouseExit(self):
        self.State -= States.Hovered

    def LoseFocus(self):
        self.State -= States.Focused

    def LoseKeyboardFocus(self):
        self.State -= States.KeyboardFocused

    def GainKeyboardFocus(self):
        self.Window.Document.KeyboardFocusedElement = self

    def GainFocus(self):
        self.Window.Document.FocusedElement = self

    def _SetParent(self, parent):
        if self.Parent:
            raise ValueError(f"{self} already has a parent")
        else:
            self.Parent = parent  # The parent
            self.Window = parent.Window  # Gets hold of the window object

    def UpdateBasedOnStyleSheet(self, removed = []):
        # Possibility of none type error here be careful
        self.__SetStylesBasedOnSheet(removed = removed)
        self.Update(ReRender=True)

    def __SetStylesBasedOnSheet(self,removed = []):
        styleSheet = self.Window.Document.GetStylesByClassName(self.Name)

        for style in styleSheet:
            # Removed the styles that have been set by state
            if style['State'] in removed:
                for prop in style['Styles'].keys():
                    if self.Styles.__dict__.get(prop):
                        del self.Styles.__dict__[prop]           
            
    
        for style in styleSheet:            
            if style['State'] in self.State:
                for prop in style['Styles'].keys():
                    self.Styles.Set(prop, style['Styles'][prop], update=False)
            
        
        self.Update(ReRender=False)

    def Render(self, UpdateStyleSheet = True, ReRenderChildren = True):
        '''Renders the element and its children'''
        if self.InitialRenderDone:
            # If i have already been rendered once i need to first delete my previous render
            self.Window.Document._RemoveVisual(self._CanvasIDs.list)
            self._CanvasIDs.clear()
        else:
            pass

        if UpdateStyleSheet:self.__SetStylesBasedOnSheet()

        
        self._Render()  # In case an inherited class has to do some extra stuff on render

        if ReRenderChildren:
            for child in self.Children:
                child.Render()


        # We need to add all the event listeners set till now (since we needed the canvas ids to set them it can only be done now)
        # Set our event listeners
        self.EventListeners.Set()
        self.InitialRenderDone = True

    def _Remove(self):
        pass

    def Remove(self):
        '''Removes the element and its children visually'''
        self._Remove()
        if self._CanvasIDs.list:self.Window.Document._RemoveVisual(self._CanvasIDs.list)
        self.Parent.Children.Remove(self)
        self._CanvasIDs.clear()
        for child in self.Children:
            child.Remove()  # Removes every child

        self.EventListeners.RemoveAll()

    def SetStyleUnits(self):
        
        self.__STYLE_UNITS = self._GetStyleUnits()

    def ComputeStyles(self):
        self._ComputedStyles = ComputeStyles(self.Styles, self)
        

    def Update(self, propogationDepth=0, ReRender=True):
        self.ComputeStyles()
        self.SetStyleUnits()      
        self._Update(updateRender=ReRender)  # In case an inherited class has to do some extra stuff on update        
        if propogationDepth:  # How deep do we want to update our stuff
            for child in self.Children:
                child.Update(propogationDepth = propogationDepth - 1,ReRender= ReRender)

        # FIXME
        # So
        # I have no clue why doing it once doesnt work but if we do our thing twice bang everything is fine
        # It should be ok cause we dont have that many elements but this is something to check

        # region braindamage
        self._Update(updateRender=ReRender)
        self.SetStyleUnits()
        if propogationDepth:  # How deep do we want to update our stuff
            for child in self.Children:
                child.Update(propogationDepth = propogationDepth - 1,ReRender= ReRender)
        # endregion

    # region ComputedStyles
    @property
    def ComputedStyles(self):
        if self._ComputedStyles:
            return self._ComputedStyles
        else:
            self.ComputeStyles()
            return self._ComputedStyles
    # endregion

    # region Styles
    @property
    def Styles(self):
        return self._Styles

    @Styles.setter
    def Styles(self, value):
        self._Styles = value
        self.ComputeStyles()
        self.Update(propogationDepth=float('inf'))
    # endregion

    # region Name
    @property
    def Name(self):
        return self.__name

    @Name.setter
    def Name(self, value):
        self.__name = value
        if self.InitialRenderDone:
            tmp = self.Window.Document.GetStylesByClassName(self.Name)
            for prop in tmp:
                self.Styles.Set(prop, tmp[prop])
            self.Update()
    # endregion

    @property
    def STYLE_UNITS(self):
        if self.__STYLE_UNITS:
            return self.__STYLE_UNITS
        else:
            self.SetStyleUnits()
            return self.__STYLE_UNITS
    
    def _GetStyleUnits(self):
        return self.Parent.STYLE_UNITS

    
    

    def _Render(self):
        '''Called when element is to be rendered. ! Inheritors must overwrite this function to render themselves'''
        pass

    def _Update(self, updateRender = True):
        '''Called when element is to be updated. ! Inheritors must overwrite this function to update themselves'''
        pass
