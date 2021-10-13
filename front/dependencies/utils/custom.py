import tkinter as tk
from ._custom.util import rect
from ._custom.styling import options,css
from ..common.tools import Vector


class container(tk.Canvas):
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clientRect = []

class element:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.renderInfo = {}
        self.css = css()
        self.css.set(**(kwargs.get('css', {})))
        self.child_nodes =  []

        self.parent.appendChild(self)
    def create_image(self,*args,**kwargs):
        return self.parent.create_image(*args,**kwargs)
    def create_polygon(self,*args,**kwargs):
        return self.parent.create_polygon(*args,**kwargs)

    def create_text(self,*args,**kwargs):
        return self.parent.create_text(*args,**kwargs)

    def appendChild(self,child):
        self.child_nodes.append(child)

    def updateAbsolutePosition(self):
        pass

    def _getRenderPoints(self):
        return []

    def updateAbsoluteSize(self):
        pass
    def render(self):        
        '''
        Called when element is to be rendered
        '''
        pass

    def updateStyles(self, **kwargs):
        self.css.set(**kwargs)
        pass

    def addEventListener(self, event, callback):
        '''
        Binds and
        '''
        return self


class container(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.css = css()
        self.child_nodes = []
        
        
    def activate(self):
        self.update()
        self.css.set(height = self.winfo_height(), width = self.winfo_width(), origin = Vector(0,0))


    def appendChild(self, child : element):
        self.child_nodes.append(child)

    

class Button(element):
    def __init__(
        self,
        parent : tk.Canvas,
        borderRadius = [0, 0, 0, 0],
        text = "button",
        command = lambda:0,
        **kwargs ):
        super().__init__(parent,**kwargs)
        self.elemID = -1
        self.textID = -1
        self.text = text

    def _getRenderPoints(self):
        if not (self.css.width and self.css.height):return []
        x1,x2,y1,y2 = 0,0,0,0
        if self.css.left != None:
            x1 = self.css.left
            x2 = x1 + self.css.width
        elif self.css.right != None:
            x2 = self.parent.css.width - self.css.right
            x1 = x2 - self.css.width
        else:
            return []
        if self.css.top != None:
            y1 = self.css.top
            y2 = y1 + self.css.height
        elif self.css.bottom != None:
            y2 = self.parent.css.height - self.css.bottom
            y1 = y2 - self.css.height
        else:
            return []
        radius =  self.css.border['radius']
        # src for how to make rounded elements : https://stackoverflow.com/a/44100075/15993687
        self.clientRect =  [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
            
    def draw(self):
        self._getRenderPoints()

        self.elemID = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], tag='button', smooth=True)
        self.textID = self.create_text(self.clientRect[-2] + self.css.width/2, self.clientRect[-1] + self.css.height/2, text=self.text, tags="button", fill=self.css.font['color'], font=(self.css.font['style'], self.css.font['size']), justify="center")
