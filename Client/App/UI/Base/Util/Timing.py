# class EventListenersHolder:

#     def __init__(self, elem):
#         self.element = elem
#         self.HasBeenSet = False
#         self.eventListeners = {}
#         self.nextListenerID = 0

#     def Call(self, event):
#         listeners = self.eventListeners.get(event.code, {})
#         KEYS = list(listeners.keys())
#         for i in KEYS:
#             if not listeners.get(i):continue
#             listeners[i].Callback(event)


#     def AddEventListener(self, eventListener):
#         if not self.eventListeners.get(eventListener.Code):
#             self.eventListeners[eventListener.Code] = {}
#         self.eventListeners[eventListener.Code][self.nextListenerID] = eventListener
#         self.nextListenerID += 1
#         return self.nextListenerID - 1

#     def __add__(self, eventListener):
#         if not self.eventListeners.get(eventListener.Code):
#             self.eventListeners[eventListener.Code] = {}
#         self.eventListeners[eventListener.Code][self.nextListenerID] = eventListener
#         self.nextListenerID += 1
#         return self

#     def Remove(self, ID):
#         for code in self.eventListeners:
#             if self.eventListeners[code].get(ID):
#                 del self.eventListeners[code][ID]
#                 break

#     def __sub__(self, eventListener):
        
#         if self.eventListeners.get(eventListener.Code):
#             for i in self.eventListeners[eventListener.Code]:
#                 if self.eventListeners[eventListener.Code][i] == eventListener:
#                     del self.eventListeners[eventListener.Code][i]
#                     break
#         return self

#     def RemoveAll(self):
#         self.element.Window.Document.EventHandler.RemoveEventListeners(self.element)

#     def Set(self):        
#         if self.HasBeenSet:
#             self.RemoveAll()
#         self.HasBeenSet = True
#         for code in self.eventListeners.keys():
#             self.element.Window.Document.EventHandler.AddEventListener(code, self.element)
#         if self.element.InitialRenderDone:self.element.Window.Document.EventHandler.SetEventListenersForElement(self.element)
from ....Core.DataTypes.UI import Interval,Timeout

class IntervalContainer:
    def __init__(self, window):
        self.Window = window
        self.root = window._tkRoot
        self.Intervals = []


    def CallInterval(self, interval):
        if interval not in self.Intervals:return
        interval.Callback()
        interval._ID = self.root.after(interval.Delay, self.CallInterval, interval)

    def SetInterval(self, delay, callback):
        interval = Interval(delay, callback)
        self.Intervals.append(interval)
        interval._ID = self.root.after(delay, self.CallInterval, interval)
        return interval

    def __add__(self, interval):
        self.Intervals.append(interval)
        interval._ID = self.root.after(interval.Delay, self.CallInterval, interval)
        return self

    def __sub__(self, interval):
        self.root.after_cancel(interval._ID)
        if interval in self.Intervals:
            self.Intervals.remove(interval)
        return self

    def CancelInterval(self, interval):
        self.root.after_cancel(interval._ID)
        if interval in self.Intervals:
            self.Intervals.remove(interval)

    def EndAll(self):
        for interval in self.Intervals:
            self.root.after_cancel(interval._ID)
        self.Intervals.clear()

class TimeoutContainer:
    def __init__(self, window):
        self.Window = window
        self.root = window._tkRoot
        self.Timeouts = []

    def CallTimeout(self, timeout):
        timeout.Callback()
        if timeout in self.Timeouts:
            self.Timeouts.remove(timeout)

    def CancelTimout(self, timeout):
        self.root.after_cancel(timout._ID)
        if timeout in self.Timeouts:
            self.Timeouts.remove(timeout)

    def SetTimeout(self, delay, callback):
        timeout = Timeout(delay, callback)
        self.Timeouts.append(timeout)
        timeout._ID = self.root.after(delay, self.CallTimeout, timeout)
        return timeout

    def __add__(self, timeout):
        self.Timeouts.append(timeout)
        timeout._ID = self.root.after(timeout.Delay, self.CallTimeout, timeout)
        return self

    def __sub__(self, timeout):
        self.root.after_cancel(timout._ID)
        if timeout in self.Timeouts:
            self.Timeouts.remove(timeout)
        return self

    def EndAll(self):
        for timeout in self.Timeouts:
            self.root.after_cancel(timeout._ID)