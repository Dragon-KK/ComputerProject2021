from App.UI import Window,Styles
from App.UI.Elements import div
from App.Core.DataTypes.Standard import Vector
from App.Views.MainMenu import Document
import ctypes

# To improve resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)

w = Window(
    resizable=True,
    title="Pong",
    windowSize=Vector(1000, 600)
)
 


w.Document = Document
w.Run()