from .div import div
from ..Styles import Style
class label(div):
    def __init__(self,*args,text = "My Text",ResizeCorrectionConst = 2, **kwargs):
        super().__init__(*args, **kwargs)
        self.__text = text
        self.ResizeCorrectionConst = ResizeCorrectionConst

    def _Render(self):
        #, font=(self.css.font['style'], self.css.font['size'])
        self._CanvasIDs += self.Window.Document.create_polygon(self._GetVisualRectBox(),width=self.Styles.BorderStroke,outline=self.Styles.BorderColor,fill=self.Styles.BackgroundColor, smooth=True)
        self._CanvasIDs += self.Window.Document.create_text(
            self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2),
            self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2), 
            text=self.Text, 
            fill=self.Styles.ForegroundColor, 
            anchor='center',
            justify='center',
            font = (
                self.Styles.FontStyle,
                self.ComputedStyles.FontSize
            )
        )

    def _Update(self, updateRender = True):
        if updateRender:
            
            textID = self._CanvasIDs.list[1]
            boxID = self._CanvasIDs.list[0]

            # Move our text
            self.Window.Document.moveto(
                textID,
                self.ComputedStyles.TopLeft.x + (self.ComputedStyles.Size.x/2) - len(self.Text) * self.ComputedStyles.FontSize / self.ResizeCorrectionConst,
                self.ComputedStyles.TopLeft.y + (self.ComputedStyles.Size.y/2) - self.ComputedStyles.FontSize, 
            )
            # Item config our text item
            self.Window.Document.itemconfig(
                textID,
                fill=self.Styles.ForegroundColor,
                anchor='center',
                justify='center',
                font = (
                    self.Styles.FontStyle,
                    self.ComputedStyles.FontSize
                )
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
    def Text(self):
        return self.__text
    @Text.setter
    def Text(self, value):
        self.__text = value

        # self._CanvasIDs.listp[1] holds the canvasID for our text item
        if len(self._CanvasIDs.list) == 2:self.Window.Document.itemconfig(self._CanvasIDs.list[1],text=value)
    # endregion