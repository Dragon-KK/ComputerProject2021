import tkinter as tk
from ._custom.util import rect
from ._custom.styling import options,css
from ..common.tools import Vector




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

    def setKeyInput(self,callback):
        self.parent.setKeyInput(callback)

    def destroy(self):
        for i in self.child_nodes:
            i.destroy()
        self.parent.undrawChild(self.canvasIDs.values())
        self.events.clear()
        self.canvasIDs.clear()

    def undrawChild(self,ids):
        self.parent.undrawChild(ids)

    def draw(self):
        self.css.origin = self.parent.renderInfo.get('position', Vector(0,0))
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



    def _getRenderPoints(self):
        return []

    def getAbsoluteValue(self,query):
        val,unit = query.split(':')
        if unit == 'px':
            return int(val)
        elif unit == 'w%':
            return int(val) * self.parent.renderInfo['size'].x / 100
        elif unit == 'h%':
            return int(val) * self.parent.renderInfo['size'].y / 100
        else:
            return 0


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
        self.bind_all("<Key>", self.onKey)
        self.child_nodes = []
        self.renderInfo = {
            'position' : Vector(0, 0)
        }

    def onKey(self,e):
        print(self,self.child_nodes)

    def draw(self):
        for i in self.child_nodes:
            i.draw() 

    def undrawChild(self,ids):
        for i in ids:
            self.delete(i)
        
    def activate(self):
        self.update()
        self.css.set(height = self.winfo_height(), width = self.winfo_width(), origin = Vector(0,0))
        self.renderInfo['size'] = Vector(self.css.width,self.css.height)

    def addChildEventListener(self, canvasID, event, callback):
        for i in canvasID:
            self.tag_bind(canvasID[i], event, callback)

    def appendChild(self, child : element):
        self.child_nodes.append(child)

class Frame(element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def _getRenderPoints(self):
        if not (self.css.width and self.css.height):return []
        x1,x2,y1,y2 = 0,0,0,0
        h = self.getAbsoluteValue(self.css.height)
        w = self.getAbsoluteValue(self.css.width)
        if self.css.left != None:
            x = self.getAbsoluteValue(self.css.left)
            

            x1 = x + self.css.origin.x
            x2 = x1 + w
        elif self.css.right != None:
            x = self.getAbsoluteValue(self.css.right)
            x2 = self.parent.renderInfo['size'].x - x + self.css.origin.x
            x1 = x2 - w
        else:
            return []
        if self.css.top != None:
            y = self.getAbsoluteValue(self.css.top)
            
            y1 = y + self.css.origin.y
            y2 = y1 + h
        elif self.css.bottom != None:
            y = self.getAbsoluteValue(self.css.bottom)
            y2 = self.parent.renderInfo['size'].y - y + self.css.origin.y
            y1 = y2 - h
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
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], tag='button', smooth=True)
        

class TextBox(element):
    def __init__(
        self,
        parent : element,
        text = "Text",
        **kwargs ):
        super().__init__(parent,**kwargs)
        self.text = text

    def _getRenderPoints(self):
        if not (self.css.width and self.css.height):return []
        x1,x2,y1,y2 = 0,0,0,0
        h = self.getAbsoluteValue(self.css.height)
        w = self.getAbsoluteValue(self.css.width)
        if self.css.left != None:
            x = self.getAbsoluteValue(self.css.left)
            

            x1 = x + self.css.origin.x
            x2 = x1 + w
        elif self.css.right != None:
            x = self.getAbsoluteValue(self.css.right)
            x2 = self.parent.renderInfo['size'].x - x + self.css.origin.x
            x1 = x2 - w
        else:
            return []
        if self.css.top != None:
            y = self.getAbsoluteValue(self.css.top)
            
            y1 = y + self.css.origin.y
            y2 = y1 + h
        elif self.css.bottom != None:
            y = self.getAbsoluteValue(self.css.bottom)
            y2 = self.parent.renderInfo['size'].y - y + self.css.origin.y
            y1 = y2 - h
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
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], tag='button', smooth=True)
        self.canvasIDs['text'] = self.create_text(self.clientRect[-2] + w/2, self.clientRect[-1] + h/2, text=self.text, tags="button", fill=self.css.font['color'], font=(self.css.font['style'], self.css.font['size']), justify="center")
