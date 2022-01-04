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
        self.__PhotoSize = self.ComputedStyles.Size
        self.__PhotoImage = ImageManager.ProcessedImage(self.Image, self.__PhotoSize)
        self._CanvasIDs += self.Window.Document.create_image(self.ComputedStyles.TopLeft.x, self.ComputedStyles.TopLeft.y,anchor='nw',image = self.__PhotoImage)

    def _Update(self, updateRender = True):
        super()._Update(updateRender=updateRender)
        if updateRender:
            imgId = self._CanvasIDs.list[1]
            if self.__PhotoSize != self.ComputedStyles.Size:
                # Resize the img again
                self.__PhotoSize = self.ComputedStyles.Size
                self.__PhotoImage = ImageManager.ProcessedImage(self.Image, self.__PhotoSize)
                
                self.Window.Document.itemconfig(
                    imgId,
                    image = self.__PhotoImage
                )

                self.Window.Document.moveto(
                    imgId,
                    self.ComputedStyles.TopLeft.x,
                    self.ComputedStyles.TopLeft.y, 
                )
            else:
                self.Window.Document.moveto(
                    imgId,
                    self.ComputedStyles.TopLeft.x,
                    self.ComputedStyles.TopLeft.y, 
                )
