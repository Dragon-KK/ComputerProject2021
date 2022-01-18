from ..Helper import ClassList,Children,StateHolder,Styles,ComputedStyles,EventListenerContainer,CanvasIDContainer
from .typeHintingHelp import Window
from ...Core.DataTypes.UI import EventListener
class Element:

    def __init__(self, elemName = "element", classes = ".default", states = ['Visible']):
        self.Parent : Element = None
        self.Window : Window = None

        self.__ElemName = elemName

        self.Children = Children(self)

        self.ClassList = ClassList()
        for Cls in classes.split(" "):self.ClassList += Cls

        self.State = StateHolder()
        self.__ReleventStates = set()
        for state in states:self.State += state

        self.Styles = Styles()
        self._ComputedStyles = ComputedStyles()

        self.StyleSheet = []

        self._CanvasID = CanvasIDContainer()

        self.EventListeners = EventListenerContainer(self)

        self.InitialRenderDone = False

        self.EventListeners += EventListener("<Button-1>", lambda e:self.GainKeyboardFocus())
        self.EventListeners += EventListener("<Enter>", lambda e:self.__OnMouseEnter())
        self.EventListeners += EventListener("<Leave>", lambda e:self.__OnMouseExit())

    def OnFocusGain(self):
        self.State += "Focused"

    def OnFocusLoss(self):
        self.State -= 'Focused'

    def GainFocus(self):
        self.Window.Document.FocusedElement = self

    def LoseFocus(self):
        self.Window.Document.FocusedElement = None

    def OnKeyboardFocusGain(self):
        self.State += "KeyboardFocused"

    def OnKeyboardFocusLoss(self):
        self.State -= 'KeyboardFocused'

    def GainKeyboardFocus(self):
        self.Window.Document.KeyboardFocusedElement = self

    def LoseKeyboardFocus(self):
        self.Window.Document.KeyboardFocusedElement = None

    def __OnMouseEnter(self):
        self.State += "Hovered"

    def __OnMouseExit(self):
        self.State -= "Hovered"



    def _SetParent(self, parent):
        if self.Parent:
            raise ValueError(f"{self} already has a parent")
        else:
            self.Parent = parent  # The parent
            self.Window = parent.Window  # Gets hold of the window object
            if "Visible" not in self.Parent.State:
                self.State -= "Visible"

    def Remove(self):
        '''Removes the element and its children visually'''
        if not self.Parent:return
        self._Remove()
        if self._CanvasID.ALLNOEXCEPTION:self.Window.Document._RemoveVisual(self._CanvasID.ALLNOEXCEPTION)
        for child in self.Children + []: # TO createa  seperate object
            child.Remove()  # Removes every child
        self.EventListeners.RemoveAll()
        self.Parent.Children.Remove(self)
        self.Parent = None


    def Render(self):
        '''Renders the element and its children'''
        if (not self.Parent) or not self.Parent.InitialRenderDone:return # If my parent hasnnt been rendered dont go forward

        if self.InitialRenderDone:
            # If i have already been rendered once i need to first delete my previous render
            self.Window.Document._RemoveVisual(self._CanvasID.ALL)

        self.SetStyleSheet() # Set our stylesheet
        self.SetStylesByStyleSheet() # Set our styles based on the stylesheet
        self.ComputeStyles() # Compute our styles
        self._Render()  # In case an inherited class has to do some extra stuff on render
        self._RenderBlock()
        self.InitialRenderDone = True
        self.EventListeners.Set()
        self.State.OnStateChanged = self._OnStateChange
        self.ClassList.OnClassListChange = self._OnClassChange
        # Render our children
        for child in self.Children:
            child.Render()

    def Update(self, propogationDepth=0):
        self.ComputeStyles() # Compute styles
        self._Update() # Update
        self._UpdateBlock()
        if propogationDepth:  # How deep do we want to update our stuff
            for child in self.Children:
                child.Update(propogationDepth = propogationDepth - 1)       

    # region Styles
    def SetStylesByStyleSheet(self, removedState = "", removedClass = ""):
        
        if removedClass:
            self.__ReleventStates.clear()
            for i in self.StyleSheet[removedClass]:
                for propname in i['Styles']:self.Styles.Remove(propname)
        if removedState:
            for i in self.StyleSheet[self.__ElemName]:
                if i['State'] == removedState:
                    for propname in i['Styles']:self.Styles.Remove(propname)
            for n in self.ClassList:
                for i in self.StyleSheet[n]:
                    if i['State'] == removedState:
                        for propname in i['Styles']:self.Styles.Remove(propname)


        for i in self.StyleSheet[self.__ElemName]:
            self.__ReleventStates.add(i['State'])
            if i['State'] in self.State:
                self.Styles.__dict__.update(i['Styles'])
        for n in self.ClassList:
            if n == removedClass:continue
            for i in self.StyleSheet[n]:
                self.__ReleventStates.add(i['State'])
                if i['State'] in self.State:
                    self.Styles.__dict__.update(i['Styles'])

    def _OnClassChange(self, added = "", removed = ""):
        if added:
            self.StyleSheet[added] = self.Window.Document.GetStylesByClassName(added)
            self.SetStylesByStyleSheet()
        else:
            self.SetStylesByStyleSheet(removedClass=removed)
            del self.StyleSheet[removed]
        self.Update()

    def _OnStateChange(self, added = "", removed = ""):
        if added:
            if added.stateName in self.__ReleventStates:
                self.SetStylesByStyleSheet()
                self.Update()
            if added == 'Visible':
                for child in self.Children:child.State += 'Visible'
        else:
            if removed.stateName in self.__ReleventStates:
                self.SetStylesByStyleSheet(removedState=removed)
                self.Update()
            if removed == 'Visible':
                for child in self.Children:child.State -= 'Visible'
            
    
    def SetStyleSheet(self):
        self.StyleSheet = {
            self.__ElemName : self.Window.Document.GetStylesByElement(self.__ElemName)
        }
        for name in self.ClassList:
            self.StyleSheet[name] = self.Window.Document.GetStylesByClassName(name)
            

    def ComputeStyles(self):
        self._ComputedStyles = ComputedStyles.FromStyles(self.Styles, self)

    @property
    def ComputedStyles(self):
        """The ComputedStyles property."""
        if self._ComputedStyles:
            return self._ComputedStyles
        else:
            self.ComputeStyles()
            return self._ComputedStyles

    def _GetStyleUnits(self):
        return self.Parent.STYLE_UNITS
    @property
    def STYLE_UNITS(self):
        """The STYLE_UNITS property."""
        return self._GetStyleUnits()
    # endregion

    def _Render(self):
        '''Called when element is to be rendered. ! Inheritors must overwrite this function to render themselves'''
        pass

    def _Update(self):
        '''Called when element is to be updated. ! Inheritors must overwrite this function to update themselves'''
        pass

    def _Remove(self):
        pass

    def _GetVisualRectBox(self):
        w = self.ComputedStyles.Size.x
        h = self.ComputedStyles.Size.y
        x = self.ComputedStyles.TopLeft.x
        y = self.ComputedStyles.TopLeft.y
        r1,r2,r3,r4 = self.ComputedStyles.CornerRadius

        # https://stackoverflow.com/a/69092113
        # Putting the points 2 times seemw to give slightly better results
        return [
            x+r1, y,
            x+r1, y,
            x + w - r2, y,
            x + w - r2, y,
            x + w, y,
            x + w, y + r2,
            x + w, y + r2,
            x + w, y + h - r3,
            x + w, y + h - r3,
            x + w, y + h,
            x + w- r3, y + h,
            x + w- r3, y + h,
            x + r4, y + h,
            x + r4, y + h,
            x, y + h,
            x, y + h - r4,
            x, y + h - r4,
            x, y + r1,
            x, y + r1,
            x, y
        ]

    def _RenderBlock(self):
        self._CanvasID._block = self.Window.Document.create_polygon(self._GetVisualRectBox(),outline="",fill="", smooth=True)

    def _UpdateBlock(self):
        if self._CanvasID._block is None:return
        self.Window.Document.coords(self._CanvasID._block,*self._GetVisualRectBox())