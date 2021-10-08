import tkinter as tk
from ._custom.util import rect
from ._custom import styleArgs as css

class container(tk.Canvas):
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clientRect = rect(size)

class element:
    def __init__(self, parent : element, **kwargs):
        self.parent = parent
        self.renderInfo = {}
        self.css = {
            'position' : css.default,
            'display' : css.default,
            'grid' : None,
            'flex' : None,
            'width' : 0,
            'height' : 0,
            'border' : None,
            'padding' : None,
            'margin' : None,
            'top' : None,
            'left' : None,
            'bottom' :None,
            'right' : None,
            'zIndex' : 1
        }
        self.children =  []

    def getAbsolutePosition():
        pass

    def render(self):
        
        '''
        Called when element is to be rendered
        '''
        pass

    def updateStyles(self, **kwargs):
        self.css.update(kwargs)

    def addEventListener(self, event, callback):
        '''
        Binds and
        '''
        return self


class Frame(element):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

    

class Button(element):
    def __init__(
        self,
        parent : Frame,
        borderRadius = [0, 0, 0, 0],
        text = "button",
        command = lambda:0,
        **kwargs ):
        pass
