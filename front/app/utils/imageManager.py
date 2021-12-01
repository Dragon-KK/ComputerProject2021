from pathlib import Path
from PIL import ImageTk,Image
IMG_SOURCE = Path(__file__).parent.parent.joinpath('media/Images')

def loadImage(filename):
    return Image.open(IMG_SOURCE.joinpath(filename))

def tkImage(img):
    return ImageTk.PhotoImage(img)