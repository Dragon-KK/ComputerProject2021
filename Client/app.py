from App.UI import Window
from App.Core.DataTypes.Standard import Vector
from App.Views.MainMenu import Document
import ctypes

# To improve resolution
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# Create a window
MyWindow = Window(
    resizable=True,
    title="Pong",
    windowSize=Vector(1000, 600)
)

# Set document
MyWindow.Document = Document

# Run window
MyWindow.Run()
import threading
print(threading.active_count()) # Just a sanity check
# eeeez game done. gn