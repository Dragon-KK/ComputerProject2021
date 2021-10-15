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
        self.canvasIDs = {}
        self.events = {}
        self.clientRect = []

    def undraw(self):
        for i in self.child_nodes:
            i.undraw()
        self.parent.undrawChild(self.canvasIDs.values())
        self.events.clear()
        self.canvasIDs.clear()

    def undrawChild(self,ids):
        self.parent.undrawChild(ids)

    def draw(self):
        self.onDraw()
        for event in self.events:
            self.parent.addChildEventListener(self.canvasIDs, event, lambda *args:self.onEvent(event,*args))
        for i in self.child_nodes:
            i.draw()
    def onDraw(self):
        return

    def create_image(self,*args,**kwargs):
        return self.parent.create_image(*args,**kwargs)
    def create_polygon(self,*args,**kwargs):
        return self.parent.create_polygon(*args,**kwargs)

    def create_text(self,*args,**kwargs):
        return self.parent.create_text(*args,**kwargs)

    def appendChild(self,child):
        self.child_nodes.append(child)
        return self

    def onEvent(self,event, args):
        self.events.get(event, lambda n:0)(args)

    def updateAbsolutePosition(self):
        pass

    def _getRenderPoints(self):
        return []

    def updateAbsoluteSize(self):
        pass

    def updateStyles(self, **kwargs):
        self.css.set(**kwargs)
        return self

    def addEventListener(self, event, callback):
        '''
        Binds and
        '''
        self.events[event] = callback
        return self

    def addChildEventListener(self,canvasID,event, callback):
        self.parent.addChildEventListener(canvasID, event, callback)

class container(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.css = css()
        self.child_nodes = []

    def draw(self):
        for i in self.child_nodes:
            i.draw() 

    def undrawChild(self,ids):
        for i in ids:
            self.delete(i)
        
    def activate(self):
        self.update()
        self.css.set(height = self.winfo_height(), width = self.winfo_width(), origin = Vector(0,0))

    def addChildEventListener(self, canvasID, event, callback):
        for i in canvasID:
            self.tag_bind(canvasID[i], event, callback)

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
            
    def onDraw(self):
        self._getRenderPoints()

        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], tag='button', smooth=True)
        self.canvasIDs['text'] = self.create_text(self.clientRect[-2] + self.css.width/2, self.clientRect[-1] + self.css.height/2, text=self.text, tags="button", fill=self.css.font['color'], font=(self.css.font['style'], self.css.font['size']), justify="center")
