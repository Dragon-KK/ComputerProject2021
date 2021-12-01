import tkinter as tk
from ._custom.util import rect # we dont even use this but it sounded cool so i kept it in
from ._custom.styling import options,css
from ..common.tools import Vector # If we didnt have our Vector class the code wouldve been 10 times worse
from ..utils import imageManager
# I just added stuff as i needed (without commenting)
# Half of this is probably useless
# But now im too deep in i cant go through and exactly figure out the best way to do things


class element: # This is an element
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
        self.renderInfo['viewport'] = self.parent.renderInfo['viewport']
        self.onDraw()
        for event in self.events:
            self.parent.addChildEventListener(self.canvasIDs, event, lambda *args:self.onEvent(event,*args))
        for i in self.child_nodes:
            i.draw()
    def onDraw(self):
        return

    def update(self):
        self.reDraw()
        for event in self.events:
            self.parent.addChildEventListener(self.canvasIDs, event, lambda *args:self.onEvent(event,*args))
        

    def reDraw(self):
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

    def onEvent(self,event, args, propagate = False):
        if propagate:
            for i in self.child_nodes:i.onEvent(event,args,propagate = True)
        self.events.get(event, lambda n:0)(args)



    def _getRenderPoints(self):
        return []

    def getAbsoluteValue(self,query, **kwargs): # Best function
        wrt = kwargs.get('wrt', self.parent)
        x = query.split(':')
        if len(x) != 2:
            print(f"{query} doesnt have ':' properly")
            return 0
        val,unit = x
        try:
            if unit == 'px':
                return float(val)
            elif unit == 'w%':
                return float(val) * wrt.renderInfo['size'].x / 100
            elif unit == 'h%':
                return float(val) * wrt.renderInfo['size'].y / 100
            elif unit == 'vw':
                return float(val) * wrt.renderInfo['viewport'].x / 100
            elif unit == 'vh':
                return float(val) * wrt.renderInfo['viewport'].y / 100
            else:
                return 0
        except Exception as e:
            print(e)
            return 0
    def updateFocus(self,elem):
        self.parent.updateFocus(elem)

    def getTkObj(self): # Most obviously redundant function
        return self.parent.getTkObj()

    def getCanvas(self):
        return self.parent.getCanvas()

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

class container(tk.Canvas): # this is a container
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.css = css()
        self.bind_all("<Key>", self.onKey)
        self.child_nodes = []
        self.renderInfo = {
            'position' : Vector(0, 0)
        }
        
        self.focuesedElement = None

    def getTkObj(self):
        return self

    def getCanvas(self):
        return self

    def updateFocus(self,elem):
        if self.focuesedElement:self.focuesedElement._unfocus()
        self.focuesedElement = elem

    def onKey(self,e):
        for i in self.child_nodes:i.onEvent('<Key>',e,propagate = True)

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
        self.renderInfo['viewport'] = Vector(self.css.width,self.css.height)

    def addChildEventListener(self, canvasID, event, callback):
        for i in canvasID:
            self.tag_bind(canvasID[i], event, callback)

    def appendChild(self, child : element):
        self.child_nodes.append(child)


class Frame(element): # ig i shouldve just named it div but Frame sounds more pythonic
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
            x1 = self.css.origin.x
            x2 = x1 + w
        if self.css.top != None:
            y = self.getAbsoluteValue(self.css.top)
            
            y1 = y + self.css.origin.y
            y2 = y1 + h
        elif self.css.bottom != None:
            y = self.getAbsoluteValue(self.css.bottom)
            y2 = self.parent.renderInfo['size'].y - y + self.css.origin.y
            y1 = y2 - h
        else:
            y1 = self.css.origin.y
            y2 = y1 + h
        radius =  self.css.border['radius']


        self.clientRect = [ # The points on our shape. tkinter does the rest :D
                x1+radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1
        ]
    def reDraw(self): # Ive interchanged draw and render and im too lazy to fix it
        self.undrawChild(self.canvasIDs.values())
        self.onDraw()

    
    def onDraw(self):
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], dash = self.css.border['dash'],tag='button', smooth=True)
        

class TextBox(Frame): # Label wouldve been a more pythonic name 
    def __init__(
        self,
        parent : element,
        text = "Text",
        **kwargs ):
        super().__init__(parent,**kwargs)
        self.text = text

    
            
    def onDraw(self):
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], tag='button', smooth=True)
        self.canvasIDs['text'] = self.create_text(self.clientRect[-2] + w/2, self.clientRect[-1] + h/2, text=self.text, tags="button", fill=self.css.font['color'], font=(self.css.font['style'], self.css.font['size']), justify="center")

class ImageBox(Frame):
    def __init__(self,*args, img=None, **kwargs):
        self.img = img
        self.photoImage = None
        super().__init__(*args,**kwargs)

    def relativeToCentreCorrection(self,w,h):
        w/=2
        h/=2
        for i in range(0,len(self.clientRect),2):self.clientRect[i] -= w
        for i in range(1,len(self.clientRect),2):self.clientRect[i] -= h

    def onDraw(self):
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.relativeToCentreCorrection(w,h) # ImageBoxs dont take left corner and right corner they take centre of element so we correct it here
        
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.photoImage = imageManager.tkImage(self.img.resize((int(w),int(h))))
        self.canvasIDs['img'] = self.create_image(self.clientRect[-2], self.clientRect[-1],anchor='nw',image = self.photoImage)
        

class TextInput(Frame): # we shouldve just made an imput element and give it the type of input in the args, it wouldve been more 'future proof'
    def __init__(self, *args, numeric = False,**kwargs):
        self.value = ""
        super().__init__(*args,**kwargs)
        self.focused = False
        self.addEventListener("<Key>", self.onKey)
        self.addEventListener("<Button-1>", self._focus)
        self.borderColor = None
        self.Numeric = numeric
        
    def _focus(self,e):
        self.updateFocus(self)
        self.focused =True
        self.updateStyles(border = {'color' : "green"})
        self.update()

    def _unfocus(self):
        self.focused = False
        self.updateStyles(border = {'color' : self.borderColor})
        self.update()
    def onKey(self, e):
        if not self.focused:return
        if e.char == '\x08':
            self.value = self.value[:-1]
        elif e.char == '\r' or e.char == '\n':
            self._unfocus()
        else:
            self.value += e.char if not self.Numeric or e.char.isnumeric() else ''
        self.update()


    def onDraw(self):
        
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], tag='button', smooth=True)
        self.canvasIDs['text'] = self.create_text(self.clientRect[-2] + w/2, self.clientRect[-1] + h/2, text=self.value, fill=self.css.font['color'], font=(self.css.font['style'], self.css.font['size']), justify = None)
        

class Arena(Frame): # ?
    # canvas sounded too lame, arena > canvas
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.canvas : tk.Canvas = self.getCanvas()
        self.items = {

        }
        self.itemNumber = 0
        self.queries = []

    def answerQueries(self):
        for item in self.queries:
            if item['queryType'] == 'absolute_wrt_self':
                item['callback'](self.getAbsoluteValue(item['query'], wrt=self))

    def query(self,queryType, query, callback):
        self.queries.append({'queryType':queryType,'query':query,'callback':callback})

    def registerItem(self,item):
        self.items[self.itemNumber] = item
        self.itemNumber += 1
        return self.itemNumber - 1

    def updateItem(self, itemID, **kwargs):
        if not self.items.get(itemID):return False
        self.items[itemID].update(**kwargs)
        return True

    


    def delete(self,ID):
        if ID in self.items:
            self.canvas.delete(self.items[ID].canvasID)
            del self.canvasIDs[ID]
            del self.items[ID]
            return True
        else:
            return False
    
    def onDraw(self):
        w = self.getAbsoluteValue(self.css.width)
        h = self.getAbsoluteValue(self.css.height)
        self._getRenderPoints()
        self.renderInfo['position'] = Vector(self.clientRect[-2], self.clientRect[-1])
        self.renderInfo['size'] = Vector(w, h)
        self.canvasIDs['container'] = self.create_polygon(self.clientRect,width=self.css.border['size'],outline=self.css.border['color'],fill=self.css.background['color'], dash = self.css.border['dash'],tag='button', smooth=True)
        self.answerQueries()
        self.render(first = True)

    def renderItem(self, item):
        if item.type == 'line':
            p1 = Vector(self.getAbsoluteValue(item.p1.x, wrt = self), self.getAbsoluteValue(item.p1.y, wrt = self)) 
            p2 = Vector(self.getAbsoluteValue(item.p2.x, wrt = self), self.getAbsoluteValue(item.p2.y, wrt = self))
            if not item.absolute:
                p1 += self.renderInfo['position']
                p2 += self.renderInfo['position']
            item.absoluteInfo['p1'] = p1
            item.absoluteInfo['p2'] = p2
            item.absoluteInfo['color'] = item.color
            item.canvasID =  self.canvas.create_line(p1.x,p1.y,p2.x,p2.y,fill = item.color, dash = item.dash, width = item.size)
            item.init()
            
        
        elif item.type == 'circle':
            c = Vector(self.getAbsoluteValue(item.c.x, wrt = self), self.getAbsoluteValue(item.c.y, wrt = self))
            r = self.getAbsoluteValue(item.r, wrt = self)
            if not item.absolute:
                c += self.renderInfo['position']
            item.absoluteInfo['position'] = c
            item.absoluteInfo['radius'] = r
            item.canvasID = self.canvas.create_oval(c.x - r, c.y - r,c.x + r, c.y + r, fill = item.color)
            #item.canvasID = self.canvas.create_rectangle(c.x - r, c.y - r,c.x + r, c.y + r, fill = item.color, tag='ball')
            item.init()
            
        else:
            print("Invalid Item")
            return -1

        return item.canvasID

    def moveItem(self, itemID, amount):
        self.canvas.move(self.canvasIDs[itemID],amount.x,amount.y)


    def render(self, first = False):
        def _render():
            for i in self.items:
                self.canvasIDs[i] = self.renderItem(self.items[i])
        
        if first:
            _render()
        else:
            toDel = []
            for i in self.items:
                toDel.append(self.canvasIDs[i])
                del self.canvasIDs[i]
            self.undrawChild(toDel)
            _render()
    

        