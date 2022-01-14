from ...Core.DataTypes.UI import Event

class EventHandler:
    '''
    For the document
    '''

    def __init__(self, doc):
        self.Document = doc
        self.nextListenerID = 0
        self.Listeners = {}
        self.Document.focus_set()
        self.Document.bind('<KeyPress>', self.__OnKeyEvent)
        self.Document.bind('<KeyRelease>', self.__OnKeyEvent)
        self.Document.bind('<MouseWheel>', self.__OnScrollEvent)

    
        

    def AddEventListener(self, code, element):
        if not self.Listeners.get(code):
            self.Listeners[code] = [element]
        else:
            self.Listeners[code].append(element)

    def RemoveEventListeners(self, element):
        for listeners in self.Listeners.values():
            if element in listeners:
                listeners.remove(element)

    def RemoveAllEventListeners(self):
        self.Listeners = {}

    def CallEvent(self,element,code,args,kwargs):
        if self.Listeners.get(code):
            if element in self.Listeners[code]:
                element.EventListeners.Call(Event(
                    element,
                    code,
                    *args,
                    **kwargs
                )
            )

    def __OnKeyEvent(self, e):
        if self.Listeners.get("!Key"):
            for element in self.Listeners['!Key']:
                element.EventListeners.Call(Event(
                    self.Document.KeyboardFocusedElement,
                    "!Key",
                    e
                ))
    def __OnScrollEvent(self, e):
        if self.Listeners.get("!Scroll"):
            for element in self.Listeners['!Scroll']:
                element.EventListeners.Call(Event(
                    self.Document.FocusedElement,
                    "!Scroll",
                    e
                ))

    def SetEventListeners(self):
        for code in self.Listeners.keys():
            self.SetEventListenerForCode(code)
    def SetEventListenerForCode(self,code,element = None):
        if code == "!Key":
            pass
        elif code == "!Scroll":
            pass
        else:
            if not element:
                for element in self.Listeners[code]:
                    self.SetEventListenerForCodeAndElement(code, element)
            else:
                if element in self.Listeners[code]:
                    self.SetEventListenerForCodeAndElement(code, element)

    def SetEventListenersForElement(self, elem):
        for code in self.Listeners.keys():
            self.SetEventListenerForCode(code)
                
    def SetEventListenerForCodeAndElement(self,code,element):
        
        for ID in element._CanvasID.ALL:
            self.Document.tag_bind(
                ID,
                code, 
                lambda *args,**kwargs:
                    self.CallEvent(element, code, args, kwargs)
            )


class EventListenerContainer:
    def __init__(self, elem):
        self.element = elem
        self.HasBeenSet = False
        self.eventListeners = {}
        self.nextListenerID = 0

    def Call(self, event):
        
        listeners = self.eventListeners.get(event.Code, {})
        KEYS = list(listeners.keys())
        for i in KEYS:
            if not listeners.get(i):continue
            listeners[i].Callback(event)


    def AddEventListener(self, eventListener):
        if not self.eventListeners.get(eventListener.Code):
            self.eventListeners[eventListener.Code] = {}
        self.eventListeners[eventListener.Code][self.nextListenerID] = eventListener
        self.nextListenerID += 1
        if self.HasBeenSet:
            self.element.Window.Document.EventHandler.AddEventListener(eventListener.Code, self.element)
            if self.element.InitialRenderDone:self.element.Window.Document.EventHandler.SetEventListenersForElement(self.element)
        return self.nextListenerID - 1

    def __add__(self, eventListener):
        if not self.eventListeners.get(eventListener.Code):
            self.eventListeners[eventListener.Code] = {}
        self.eventListeners[eventListener.Code][self.nextListenerID] = eventListener
        self.nextListenerID += 1
        if self.HasBeenSet:
            self.element.Window.Document.EventHandler.AddEventListener(eventListener.Code, self.element)
            if self.element.InitialRenderDone:self.element.Window.Document.EventHandler.SetEventListenersForElement(self.element)
        return self

    def Remove(self, ID):
        for code in self.eventListeners:
            if self.eventListeners[code].get(ID):
                del self.eventListeners[code][ID]
                break

    def __sub__(self, eventListener):
        
        if self.eventListeners.get(eventListener.Code):
            for i in self.eventListeners[eventListener.Code]:
                if self.eventListeners[eventListener.Code][i] == eventListener:
                    del self.eventListeners[eventListener.Code][i]
                    break
        return self

    def RemoveAll(self):
        self.element.Window.Document.EventHandler.RemoveEventListeners(self.element)

    def Set(self):        
        if self.HasBeenSet:
            self.RemoveAll()
        self.HasBeenSet = True
        for code in self.eventListeners.keys():
            self.element.Window.Document.EventHandler.AddEventListener(code, self.element)
        if self.element.InitialRenderDone:self.element.Window.Document.EventHandler.SetEventListenersForElement(self.element)