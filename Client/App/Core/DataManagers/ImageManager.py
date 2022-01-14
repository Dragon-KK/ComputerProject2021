from PIL import Image, ImageTk
from .FileManager import FileManager

class ImageManager:
    ImagePath = FileManager.MediaPath.joinpath("Images")
    @staticmethod
    def ResizedImage(img, resolution):
        # Since all our images are tiny we really dont need anti aliasing
        # But ideally we would use Image.ANTIALIASING instead as the images look cleaner
        return img.resize((int(resolution.x), int(resolution.y)), 1) # second param basically tells it to use antialiasing

    @staticmethod
    def TkImage(img):
        return ImageTk.PhotoImage(img)

    @staticmethod
    def ProcessedImage(img, resolution):
        return ImageManager.TkImage(ImageManager.ResizedImage(img, resolution))

    @staticmethod
    def Load(path):
        '''Path is relative to images folder'''
        return Image.open(ImageManager.ImagePath.joinpath(path))
