from .div import div
from ...Core.DataTypes.UI import EventListener
from ...Core.DataTypes.Standard import Vector

'''
For scrolling up in the y direction anything with a bottom y value that goes above the padding cutoff will be set to invisible
For scrolling down in the y direction anything with a top y value that goes below the padding cutoff will be set to invisible
'''

class ListBox(div):
    '''For now scrolling is only done in the direction of the listbox'''
    def __init__(self, *args, vertical = True,  scrollable = True, scrollSensitivity = 20, **kwargs):
        kwargs['elemName'] = kwargs.get('elemName', 'ListBox')
        super().__init__(*args, **kwargs)
        self.__IsVertical = vertical # Is the ListBox for vertical items
        self.Scrollable = scrollable # Allow scrolling in the y directions        
        self.__ContentSize = Vector(0, 0) # The size of our content

        self.EventListeners += EventListener("!Scroll", self.__OnScroll)
        self.EventListeners += EventListener("<Enter>", lambda *args,**kwargs: self.GainFocus())    
        self.EventListeners += EventListener("<Leave>", lambda *args,**kwargs: self.LoseFocus())

        self.__Scroller = ListBoxScroller(scrollSensitivity=scrollSensitivity)


    def __OnScroll(self, e):
        if not self.Scrollable:return
        if e.sender == self: # If i am the focused element
            self.__Scroller.Scroll(1 if e.args[0].delta < 0 else -1 if e.args[0].delta>0 else 0)
            if abs(self.__Scroller.LastCurrent - self.__Scroller.Current) < 1:return
            self.Update(float('inf'), ReRender=True)


    #region dirty shit

    def __GetPaddingRectBox(self, topleft, size, cornerRadius):
        # Same as in Element.py
        w = size.x
        h = size.y
        x = topleft.x
        y = topleft.y
        r1,r2,r3,r4 = cornerRadius

        # Putting the points 2 times seems to give slightly better results
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

    def __UpdatePaddingCutoff(self, boxID, rect):
        # Move our box
        self.Window.Document.coords(boxID,*rect) 

        # Item config our box           
        self.Window.Document.itemconfig(
            boxID,
            fill=self.Styles.BackgroundColor
        )

    def OnChildrenChanged(self, added = None, removed = None):pass

    def Render(self):
        '''Make sure is same as Element.py'''
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
        
        self.State.OnStateChanged = self._OnStateChange
        self.ClassList.OnClassListChange = self._OnClassChange
        # Render our children


        NextChildPosition = Vector(self.ComputedStyles.Padding[0], self.ComputedStyles.Padding[1]) # The position of the next child
        RestIsHidden = False
        if self.__IsVertical:
            maxWidth = 0
            for child in self.Children:
                child.Styles.Position = (NextChildPosition.x, NextChildPosition.y)
                child.Render()
                if child.ComputedStyles.Size.x + self.ComputedStyles.Padding[0] > maxWidth:maxWidth = child.ComputedStyles.Size.x + self.ComputedStyles.Padding[0]
                
                if not ((child.ComputedStyles.TopLeft.y + child.ComputedStyles.Size.y > self.ComputedStyles.TopLeft.y + self.ComputedStyles.Padding[1]) and (child.ComputedStyles.TopLeft.y < self.ComputedStyles.TopLeft.y + self.ComputedStyles.Size.y - self.ComputedStyles.Padding[1])):
                    child.State -= "Visible"
                NextChildPosition += (0, child.ComputedStyles.Size.y + self.ComputedStyles.Gap.y)
            
            # Now add the padding cutoff
            # The top part
            self._CanvasID._topPad = self.Window.Document.create_polygon(self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, 0), Vector(self.ComputedStyles.Size.x - self.Styles.BorderStroke, self.ComputedStyles.Padding[1]), (self.ComputedStyles.CornerRadius[0], self.ComputedStyles.CornerRadius[1], 0 ,0)),width=0,outline="",fill=self.Styles.BackgroundColor, smooth=True)
            # The bottom part
            self._CanvasID._bottomPad = self.Window.Document.create_polygon(self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, self.ComputedStyles.Size.y - self.ComputedStyles.Padding[1]), Vector(self.ComputedStyles.Size.x - self.Styles.BorderStroke, self.ComputedStyles.Padding[1]), (0,0,self.ComputedStyles.CornerRadius[2], self.ComputedStyles.CornerRadius[3])),width=0,outline="",fill=self.Styles.BackgroundColor, smooth=True)

            self.__ContentSize = Vector(maxWidth, NextChildPosition.y - self.ComputedStyles.Gap.y)
            self.__Scroller.Max = self.__ContentSize.y - self.ComputedStyles.Size.y + self.ComputedStyles.Padding[1] + 2
        else:
            maxHeight = 0
            for child in self.Children:
                child.Styles.Position = (NextChildPosition.x, NextChildPosition.y)
                child.Render()
                if child.ComputedStyles.Size.y + self.ComputedStyles.Padding[1] > maxHeight:maxHeight = child.ComputedStyles.Size.y + self.ComputedStyles.Padding[1]
                if not ((child.ComputedStyles.TopLeft.x + child.ComputedStyles.Size.x > self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0]) and (child.ComputedStyles.TopLeft.x < self.ComputedStyles.TopLeft.x + self.ComputedStyles.Size.x - self.ComputedStyles.Padding[0])):
                    child.State -= "Visible"
                NextChildPosition += (child.ComputedStyles.Size.x + self.ComputedStyles.Gap.x, 0)

            # Now add the padding cutoff
            # The left part
            self._CanvasID._leftPad = self.Window.Document.create_polygon(self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, 0), Vector(self.ComputedStyles.Padding[0],self.ComputedStyles.Size.y), (self.ComputedStyles.CornerRadius[0], 0, 0 ,self.ComputedStyles.CornerRadius[3])),width=0,outline="",fill=self.Styles.BackgroundColor, smooth=True)
            # The right part
            self._CanvasID._rightPad = self.Window.Document.create_polygon(self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke + self.ComputedStyles.Size.x - self.ComputedStyles.Padding[0], 0), Vector(self.ComputedStyles.Padding[0],self.ComputedStyles.Size.y), (0,self.ComputedStyles.CornerRadius[2],self.ComputedStyles.CornerRadius[2], 0)),width=0,outline="",fill=self.Styles.BackgroundColor, smooth=True)
            self.__ContentSize = Vector(NextChildPosition.x - self.ComputedStyles.Gap.x, maxHeight)
            self.__Scroller.Max = self.__ContentSize.x - self.ComputedStyles.Size.x + self.ComputedStyles.Padding[0] + 2

        self.EventListeners.Set()

    def Update(self, propogationDepth=0):
        self.ComputeStyles() # Compute styles
        self._Update() # Update
        self._UpdateBlock()
        # Now we need to set the position for each of our children
        NextChildPosition = Vector(self.ComputedStyles.Padding[0], self.ComputedStyles.Padding[1]) # The position of the next child
        if self.__IsVertical:
            NextChildPosition += (0, -self.__Scroller.Current)
            maxWidth = 0
            for child in self.Children:
                child.Styles.Position = (NextChildPosition.x, NextChildPosition.y)
                if "Visible" not in child.State:child.State += "Visible"
                child.Update(propogationDepth = propogationDepth - 1)
                if child.ComputedStyles.Size.x + self.ComputedStyles.Padding[0] > maxWidth:maxWidth = child.ComputedStyles.Size.x + self.ComputedStyles.Padding[0]
                NextChildPosition += (0, child.ComputedStyles.Size.y + self.ComputedStyles.Gap.y)
                if not ((child.ComputedStyles.TopLeft.y + child.ComputedStyles.Size.y > self.ComputedStyles.TopLeft.y + self.ComputedStyles.Padding[1]) and (child.ComputedStyles.TopLeft.y < self.ComputedStyles.TopLeft.y + self.ComputedStyles.Size.y - self.ComputedStyles.Padding[1])):
                    child.State -= "Visible"
                

            # Update our padding cutoff
            self.__UpdatePaddingCutoff(self._CanvasID._topPad, self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, 0), Vector(self.ComputedStyles.Size.x - self.Styles.BorderStroke, self.ComputedStyles.Padding[1]), (self.ComputedStyles.CornerRadius[0], self.ComputedStyles.CornerRadius[1], 0 ,0)))
            self.__UpdatePaddingCutoff(self._CanvasIDs._bottomPad, self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, self.ComputedStyles.Size.y - self.ComputedStyles.Padding[1]), Vector(self.ComputedStyles.Size.x - self.Styles.BorderStroke, self.ComputedStyles.Padding[1]), (0,0,self.ComputedStyles.CornerRadius[2], self.ComputedStyles.CornerRadius[3])))
            self.__ContentSize = Vector(maxWidth, NextChildPosition.y - self.ComputedStyles.Gap.y + self.__Scroller.Current)
            self.__Scroller.Max = self.__ContentSize.y - self.ComputedStyles.Size.y + self.ComputedStyles.Padding[1] + 2
        else:
            maxHeight = 0
            NextChildPosition += (-self.__Scroller.Current, 0)
            for child in self.Children:
                child.Styles.Position = (NextChildPosition.x, NextChildPosition.y)
                if "Visible" not in child.State:child.State += "Visible"
                child.Update(propogationDepth = propogationDepth - 1, ReRender = ReRender)
                if child.ComputedStyles.Size.y + self.ComputedStyles.Padding[1] > maxHeight:maxHeight = child.ComputedStyles.Size.y + self.ComputedStyles.Padding[1]
                if not ((child.ComputedStyles.TopLeft.x + child.ComputedStyles.Size.x > self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0]) and (child.ComputedStyles.TopLeft.x < self.ComputedStyles.TopLeft.x + self.ComputedStyles.Size.x - self.ComputedStyles.Padding[0])):
                    child.State -= "Visible"
                NextChildPosition += (child.ComputedStyles.Size.x + self.ComputedStyles.Gap.x, 0)
            self.__UpdatePaddingCutoff(self._CanvasIDs._leftPad, self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, 0), Vector(self.ComputedStyles.Padding[0],self.ComputedStyles.Size.y), (self.ComputedStyles.CornerRadius[0], 0, 0 ,self.ComputedStyles.CornerRadius[3])))
            self.__UpdatePaddingCutoff(self._CanvasID._rightPad, self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke + self.ComputedStyles.Size.x - self.ComputedStyles.Padding[0], 0), Vector(self.ComputedStyles.Padding[0],self.ComputedStyles.Size.y), (0,self.ComputedStyles.CornerRadius[2],self.ComputedStyles.CornerRadius[2], 0)))
            self.__ContentSize = Vector(NextChildPosition.x - self.ComputedStyles.Gap.x + self.__Scroller.Current, maxHeight)
            self.__Scroller.Max = self.__ContentSize.x - self.ComputedStyles.Size.x + self.ComputedStyles.Padding[0] + 2 

    def Update(self, propogationDepth=0, ReRender=True):
        super().Update(propogationDepth=0,ReRender=ReRender)
        if not propogationDepth:return

        # Now we need to set the position for each of our children
        NextChildPosition = Vector(self.ComputedStyles.Padding[0], self.ComputedStyles.Padding[1]) # The position of the next child
        if self.__IsVertical:
            NextChildPosition += (0, -self.__Scroller.Current)
            maxWidth = 0
            for child in self.Children:
                child.Styles.Position = (NextChildPosition.x, NextChildPosition.y)
                if "Visible" not in child.State:child.State += "Visible"
                child.Update(propogationDepth = propogationDepth - 1, ReRender = ReRender)
                if child.ComputedStyles.Size.x + self.ComputedStyles.Padding[0] > maxWidth:maxWidth = child.ComputedStyles.Size.x + self.ComputedStyles.Padding[0]
                NextChildPosition += (0, child.ComputedStyles.Size.y + self.ComputedStyles.Gap.y)
                if not ((child.ComputedStyles.TopLeft.y + child.ComputedStyles.Size.y > self.ComputedStyles.TopLeft.y + self.ComputedStyles.Padding[1]) and (child.ComputedStyles.TopLeft.y < self.ComputedStyles.TopLeft.y + self.ComputedStyles.Size.y - self.ComputedStyles.Padding[1])):
                    child.State -= "Visible"
                

            # Update our padding cutoff
            self.__UpdatePaddingCutoff(self._CanvasIDs.list[1], self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, 0), Vector(self.ComputedStyles.Size.x - self.Styles.BorderStroke, self.ComputedStyles.Padding[1]), (self.ComputedStyles.CornerRadius[0], self.ComputedStyles.CornerRadius[1], 0 ,0)))
            self.__UpdatePaddingCutoff(self._CanvasIDs.list[2], self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, self.ComputedStyles.Size.y - self.ComputedStyles.Padding[1]), Vector(self.ComputedStyles.Size.x - self.Styles.BorderStroke, self.ComputedStyles.Padding[1]), (0,0,self.ComputedStyles.CornerRadius[2], self.ComputedStyles.CornerRadius[3])))
            self.__ContentSize = Vector(maxWidth, NextChildPosition.y - self.ComputedStyles.Gap.y + self.__Scroller.Current)
            self.__Scroller.Max = self.__ContentSize.y - self.ComputedStyles.Size.y + self.ComputedStyles.Padding[1] + 2
        else:
            maxHeight = 0
            NextChildPosition += (-self.__Scroller.Current, 0)
            for child in self.Children:
                child.Styles.Position = (NextChildPosition.x, NextChildPosition.y)
                if "Visible" not in child.State:child.State += "Visible"
                child.Update(propogationDepth = propogationDepth - 1, ReRender = ReRender)
                if child.ComputedStyles.Size.y + self.ComputedStyles.Padding[1] > maxHeight:maxHeight = child.ComputedStyles.Size.y + self.ComputedStyles.Padding[1]
                if not ((child.ComputedStyles.TopLeft.x + child.ComputedStyles.Size.x > self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0]) and (child.ComputedStyles.TopLeft.x < self.ComputedStyles.TopLeft.x + self.ComputedStyles.Size.x - self.ComputedStyles.Padding[0])):
                    child.State -= "Visible"
                NextChildPosition += (child.ComputedStyles.Size.x + self.ComputedStyles.Gap.x, 0)
            self.__UpdatePaddingCutoff(self._CanvasIDs.list[1], self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke, 0), Vector(self.ComputedStyles.Padding[0],self.ComputedStyles.Size.y), (self.ComputedStyles.CornerRadius[0], 0, 0 ,self.ComputedStyles.CornerRadius[3])))
            self.__UpdatePaddingCutoff(self._CanvasIDs.list[2], self.__GetPaddingRectBox(self.ComputedStyles.TopLeft + (self.Styles.BorderStroke + self.ComputedStyles.Size.x - self.ComputedStyles.Padding[0], 0), Vector(self.ComputedStyles.Padding[0],self.ComputedStyles.Size.y), (0,self.ComputedStyles.CornerRadius[2],self.ComputedStyles.CornerRadius[2], 0)))
            self.__ContentSize = Vector(NextChildPosition.x - self.ComputedStyles.Gap.x + self.__Scroller.Current, maxHeight)
            self.__Scroller.Max = self.__ContentSize.x - self.ComputedStyles.Size.x + self.ComputedStyles.Padding[0] + 2
    #endregion

class ListBoxScroller:
    def __init__(self, scrollSensitivity = 10):
        self.__Min = 0
        self.__Max = 100
        self.Current = 0
        self.ScrollSensitivity = scrollSensitivity

        self.LastCurrent = 0

    def Scroll(self, dir):
        self.LastCurrent = self.Current
        self.Current += dir * self.ScrollSensitivity
        self.Current = max(self.Current, self.Min)
        self.Current = min(self.Current, self.Max)

    @property
    def Max(self):
        """The Max property."""
        return self.__Max
    @Max.setter
    def Max(self, value):
        self.__Max = max(value, self.Min)

    @property
    def Min(self):
        """The Min property."""
        return self.__Min
    @Min.setter
    def Min(self, value):
        self.__Min = min(value, self.Max)