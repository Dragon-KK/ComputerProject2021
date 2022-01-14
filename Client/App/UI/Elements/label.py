from .div import div
from tkinter import font as tkFont

class label(div):
    def __init__(self,*args,text = "My Text", **kwargs):
        kwargs['elemName'] = kwargs.get('elemName', 'label')
        super().__init__(*args, **kwargs)
        self.__text = text

    def _Render(self):
        super()._Render()
        self._CanvasID.text=self.Window.Document.create_text(
            self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2) + self.ComputedStyles.Padding[0],
            self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) + self.ComputedStyles.Padding[1], 
            text=self.Text, 
            fill=self.Styles.ForegroundColor  if "Visible" in self.State else "",
            anchor='center',
            justify='center',
            font = (
                self.Styles.FontStyle,
                self.ComputedStyles.FontSize,
                self.Styles.FontType
            ),
            width = self.ComputedStyles.Size.x
        )
        
        textSize = tkFont.Font(self.Window.Document, family=self.Styles.FontStyle,size = self.ComputedStyles.FontSize,weight = self.Styles.FontType).measure(self.Text)

        self.Window.Document.moveto(
                self._CanvasID.text,
                self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2) - (textSize / 2) + self.ComputedStyles.Padding[0],
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - (self.ComputedStyles.FontSize * 1.25) + self.ComputedStyles.Padding[1], 
            )

    def _Update(self):
        super()._Update()
        if self._CanvasID.text is None:return
            
        textID = self._CanvasID.text
        self.Window.Document.itemconfig(
            textID,
            fill=self.Styles.ForegroundColor if "Visible" in self.State else "",
            anchor='center',
            justify='center',
            font = (
                self.Styles.FontStyle,
                self.ComputedStyles.FontSize,
                self.Styles.FontType
            ),
            width=self.ComputedStyles.Size.x
        )

        textSize = tkFont.Font(self.Window.Document, family=self.Styles.FontStyle,size = self.ComputedStyles.FontSize,weight = self.Styles.FontType).measure(self.Text)

        self.Window.Document.moveto(
            textID,
            self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2) - (textSize / 2) + self.ComputedStyles.Padding[0],
            self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - (self.ComputedStyles.FontSize * 1.25) + self.ComputedStyles.Padding[1], 
        )

    # region Text
    @property
    def Text(self):
        return self.__text
    @Text.setter
    def Text(self, value):
        self.__text = value

        # self._CanvasIDs.listp[1] holds the canvasID for our text item
        if self._CanvasID.text is not None:self.Window.Document.itemconfig(self._CanvasID.text,text=value)
    # endregion