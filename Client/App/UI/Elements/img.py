from .div import div
from ...Core.DataManagers import ImageManager

class img(div):
    def __init__(self, img, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.Image = img # A PIL.Image object
        self.__PhotoImage = None
        self.__PhotoSize = None

    def _Render(self):
        super()._Render()
        if self.ComputedStyles.Size.x <=0 or self.ComputedStyles.Size.y <= 0:return
        self.__PhotoSize = self.ComputedStyles.Size - (self.ComputedStyles.Padding[2] + self.ComputedStyles.Padding[1], self.ComputedStyles.Padding[3] + self.ComputedStyles.Padding[1])
        self.__PhotoImage = ImageManager.ProcessedImage(self.Image, self.__PhotoSize)
        self._CanvasIDs += self.Window.Document.create_image(self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0], self.ComputedStyles.TopLeft.y + self.ComputedStyles.Padding[1],anchor='nw',image = self.__PhotoImage)

    def _Update(self, updateRender = True):
        if len(self._CanvasIDs.list) < 2:return
        super()._Update(updateRender=updateRender)
        imgId = self._CanvasIDs.list[1]
        if self.ComputedStyles.Size.x <= 0 or self.ComputedStyles.Size.y <= 0:
            self.__PhotoSize = None
            self.Window.Document.itemconfig(
                imgId,
                image = ''
            )
            return

        if updateRender:
            
            if self.__PhotoSize != self.ComputedStyles.Size:
                # Resize the img again
                self.__PhotoSize = self.ComputedStyles.Size - (self.ComputedStyles.Padding[2] + self.ComputedStyles.Padding[1], self.ComputedStyles.Padding[3] + self.ComputedStyles.Padding[1])
                self.__PhotoImage = ImageManager.ProcessedImage(self.Image, self.__PhotoSize)
                
                self.Window.Document.itemconfig(
                    imgId,
                    image = self.__PhotoImage
                )

                self.Window.Document.moveto(
                    imgId,
                    self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0],
                    self.ComputedStyles.TopLeft.y + self.ComputedStyles.Padding[1], 
                )
            else:
                self.Window.Document.moveto(
                    imgId,
                    self.ComputedStyles.TopLeft.x + self.ComputedStyles.Padding[0],
                    self.ComputedStyles.TopLeft.y + self.ComputedStyles.Padding[1], 
                )
