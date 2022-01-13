from .div import div
from ..Base.Util import States
from ...Core.DataTypes.UI import EventListener
from tkinter.font import Font

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

    def __init__(self,*args,Type=str,allowNegative = True, placeHolder = None,maxLength = float('inf'), **kwargs):
        super().__init__(*args, **kwargs)
        self.Type = Type
        self.MaximumInputLength = maxLength
        self.allowNegative = allowNegative
        self.__value = ""
        self.PlaceHolder = placeHolder
        self.EventListeners += EventListener("!Key", self.__OnKeyInput)

    def __OnKeyInput(self, e):
        if States.KeyboardFocused not in self.State:return
        if str(e.args[0].type) != "KeyPress":return

        char = e.args[0].char

        if (isSpecial(char)):
            if char == '\x08':
                self.__value = str(self.__value)[:-1]
                if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=self.__value if self.__value else self.PlaceHolder if self.PlaceHolder else self.Type(), fill = self.Styles.ForegroundColor if self.__value else self.Styles.PlaceHolderForegroundColor)

        elif len(self.__value) < self.MaximumInputLength and ((self.Type == str) or (self.Type == int and intCheck(self.__value, char, self.allowNegative)) or (self.Type == float and floatCheck(self.__value, char, self.allowNegative))):
            self.__value += char            
            # Basically just update the value
            if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=self.__value if self.__value else self.PlaceHolder if self.PlaceHolder else self.Type(), fill = self.Styles.ForegroundColor if self.__value else self.Styles.PlaceHolderForegroundColor)


    def _Render(self):
        super()._Render()
        self._CanvasIDs += self.Window.Document.create_text(
            self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0],
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize + self.ComputedStyles.Padding[1],
            text=self.__value if self.__value else self.PlaceHolder if self.PlaceHolder else self.Type(), 
            fill=self.Styles.ForegroundColor if self.__value else self.Styles.PlaceHolderForegroundColor,
            anchor = 'w',
            font = (
                self.Styles.FontStyle,
                self.ComputedStyles.FontSize,
                self.Styles.FontType
            )
        )
        self.Window.Document.moveto(
                self._CanvasIDs.list[1],
                self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0],
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize + self.ComputedStyles.Padding[1]
            )

    def _Update(self, updateRender = True):
        super()._Update(updateRender=updateRender)
        if updateRender:
            textID = self._CanvasIDs.list[1]

            # Item config our text item
            self.Window.Document.itemconfig(
                textID,
                fill=self.Styles.ForegroundColor if self.__value else self.Styles.PlaceHolderForegroundColor,
                anchor='w',
                font = (
                    self.Styles.FontStyle,
                    self.ComputedStyles.FontSize,
                    self.Styles.FontType
                )
            )

            # Move our text
            self.Window.Document.moveto(
                textID,
                self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0],
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize + self.ComputedStyles.Padding[1], 
            )

    # region Text
    @property
    def Value(self):
        try:
            return self.Type(self.__value)
        except:
            return self.Type()
    @Value.setter
    def Value(self, value):
        self.__value = str(value)
        # self._CanvasIDs.list[1] holds the canvasID for our text item
        if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=str(value))
    # endregion
