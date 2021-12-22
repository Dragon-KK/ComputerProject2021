from .div import div
from ..Styles import Style
from ..Base.Util import States
from ...Core.DataTypes.UI import EventListener

# TODO
# Overflow Hidden
# Overflow Scroll
# Overflow Ellipse
# Max len

def floatCheck(curr, proposed, allowNegative):
    return proposed.isnumeric() or (proposed == '.' and '.' not in curr) or (proposed == '-' and len(curr) == 0 and allowNegative)

def intCheck(curr, proposed, allowNegative):
    return proposed.isnumeric() or (proposed == '-' and len(curr) == 0 and allowNegative)

def isSpecial(proposed):
    return proposed in ['\x08', '\n', '\r']

class input(div):   

    def __init__(self,*args,Type=str,allowNegative = True, placeHolder = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.Type = Type
        self.allowNegative = allowNegative
        self.__value = ""
        self.PlaceHolder = placeHolder
        self.EventListeners += EventListener("!Key", self.__OnKeyInput)

    def __OnKeyInput(self, e):
        if States.KeyboardFocused not in self.State:return
        char = e.args[0].char

        if (isSpecial(char)):
            if char == '\x08':
                self.__value = str(self.__value)[:-1]
                if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=self.Value, fill = self.Styles.ForegroundColor if not self.__IsShowingPlaceholder else self.Styles.PlaceHolderForegroundColor)

        elif (self.Type == str) or (self.Type == int and intCheck(self.__value, char, self.allowNegative)) or (self.Type == float and floatCheck(self.__value, char, self.allowNegative)):
            self.__value += char            
            # Basically just update the value
            if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=self.Value, fill = self.Styles.ForegroundColor if not self.__IsShowingPlaceholder else self.Styles.PlaceHolderForegroundColor)


    def _Render(self):
        self._CanvasIDs += self.Window.Document.create_polygon(self._GetVisualRectBox(),width=self.Styles.BorderStroke,outline=self.Styles.BorderColor,fill=self.Styles.BackgroundColor, smooth=True)
        self._CanvasIDs += self.Window.Document.create_text(
            self.ComputedStyles.TopLeft.x + self.Styles.BorderStroke,
            self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize, 
            text=self.Value, 
            fill=self.Styles.ForegroundColor if not self.__IsShowingPlaceholder else self.Styles.PlaceHolderForegroundColor,
            anchor = 'w',
            font = (
                self.Styles.FontStyle,
                self.ComputedStyles.FontSize
            ),
            width = self.ComputedStyles.Size.x
        )

    def _Update(self, updateRender = True):
        if updateRender:
            textID = self._CanvasIDs.list[1]
            boxID = self._CanvasIDs.list[0]

            # Item config our text item
            self.Window.Document.itemconfig(
                textID,
                fill=self.Styles.ForegroundColor if not self.__IsShowingPlaceholder else self.Styles.PlaceHolderForegroundColor,
                anchor='w',
                font = (
                    self.Styles.FontStyle,
                    self.ComputedStyles.FontSize
                ),
                width = self.ComputedStyles.Size.x
            )

            # Move our text
            self.Window.Document.moveto(
                textID,
                self.ComputedStyles.TopLeft.x + self.Styles.BorderStroke,
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize, 
            )
            
            # Move our box
            self.Window.Document.coords(boxID,*self._GetVisualRectBox()) 

            # Item config our box       
            self.Window.Document.itemconfig(
                boxID,
                width=self.Styles.BorderStroke,
                outline=self.Styles.BorderColor,
                fill=self.Styles.BackgroundColor
            )

    # region Text
    @property
    def Value(self):
        if not self.__value:
            self.__IsShowingPlaceholder = True
            return self.PlaceHolder if self.PlaceHolder else self.Type()
        try:
            self.__IsShowingPlaceholder = False
            return self.Type(self.__value)
        except:
            self.__IsShowingPlaceholder = True
            return self.PlaceHolder if self.PlaceHolder else self.Type()
    @Value.setter
    def Value(self, value):
        self.__value = str(value)
        # self._CanvasIDs.list[1] holds the canvasID for our text item
        if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=str(value))
    # endregion
