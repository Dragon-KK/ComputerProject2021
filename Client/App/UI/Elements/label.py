from .div import div
from tkinter import font as tkFont

class label(div):
    def __init__(self,*args,text = "My Text", **kwargs):
        super().__init__(*args, **kwargs)
        self.__text = text

    def _Render(self):
        #, font=(self.css.font['style'], self.css.font['size'])
        super()._Render()
        self._CanvasIDs += self.Window.Document.create_text(
            self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2) + self.ComputedStyles.Padding[0],
            self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) + self.ComputedStyles.Padding[1], 
            text=self.Text, 
            fill=self.Styles.ForegroundColor  if "Visible" in self.State else "",
            anchor='center',
            justify='center',
            font = (
                self.Styles.FontStyle,
                self.ComputedStyles.FontSize
            ),
            width = self.ComputedStyles.Size.x
        )

    def _Update(self, updateRender = True):
        super()._Update(updateRender=updateRender)
        if updateRender and self._CanvasIDs.list:
            textID = self._CanvasIDs.list[1]
            self.Window.Document.itemconfig(
                textID,
                fill=self.Styles.ForegroundColor if "Visible" in self.State else "",
                anchor='center',
                justify='center',
                font = (
                    self.Styles.FontStyle,
                    self.ComputedStyles.FontSize
                ),
                width=self.ComputedStyles.Size.x
            )

            textSize = tkFont.Font(self.Window.Document, family=self.Styles.FontStyle,size = self.ComputedStyles.FontSize).measure(self.Text)

            self.Window.Document.moveto(
                textID,
                self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2) - (textSize / 2) + self.ComputedStyles.Padding[0],
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize + self.ComputedStyles.Padding[1], 
            )

    # region Text
    @property
    def Text(self):
        return self.__text
    @Text.setter
    def Text(self, value):
        self.__text = value

        # self._CanvasIDs.listp[1] holds the canvasID for our text item
        if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=value)
    # endregion