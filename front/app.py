# Imports
import tkinter as tk # this is the thing that lets us handle GUI easily
from app.pages import mainMenu,freePlay,localMultiplayer,onlineMultiplayer,aboutUs
from app.utils import page
from app.common.tools import Vector # Import Vector

# References -
# pong gameplay : https://www.ponggame.org/
# classes in python : https://www.w3schools.com/python/python_classes.asp/ 
# tkinter canvas : https://www.tutorialspoint.com/python/tk_canvas.htm/
# how to edit markdown files : https://www.youtube.com/watch?v=HUBNt18RFbo

# this is the file with the most comments 
# its also the file where the least stuff happens :D

WINDOW_SIZE = Vector(800, 500) # The size of the window

# < set {root} >
root = tk.Tk() # Initialize the window
root.geometry(f'{WINDOW_SIZE.x}x{WINDOW_SIZE.y}') # Set size of the window
root.title("Pong") # Setting the title to the window
root.resizable(0,0) # We dont want it to be resizable
# < />

# < set {app} >
app = page.container(root, WINDOW_SIZE, {
    "mainMenu" : mainMenu.mainMenu,
    "aboutUs" : aboutUs.aboutUs,
    "freePlay" : freePlay.freePlay,
    "localMultiplayer" : localMultiplayer.localMultiplayer,
    "onlineMultiplayer" : onlineMultiplayer.onlineMultiplayer
})
app.open("mainMenu")

def onClose():
    app.destroy() # I destroy the current page
    root.destroy() # I close the window

root.protocol("WM_DELETE_WINDOW", onClose) # When user closes the window, I want to do some extra stuff

root.mainloop() # Start running window