from App.UI import Window
from App.Core.DataTypes.Standard import Vector
from App.Views.MainMenu import MainMenu
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
MyWindow.ChangeDocumentTo(MainMenu)

# Run window
MyWindow.Run()
# eeeez game done. gn5