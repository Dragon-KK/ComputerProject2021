import tkinter as tk
from pages.common.helpers import Vector
from pages import local_multiplayer
from time import sleep
# References -
# pong gameplay : https://www.ponggame.org/
# classes in python : https://www.w3schools.com/python/python_classes.asp/ 
# tkinter canvas : https://www.tutorialspoint.com/python/tk_canvas.htm/
# how to edit markdown files : https://www.youtube.com/watch?v=HUBNt18RFbo

WINDOW_SIZE = Vector(800, 500) # The size of the window

# < Root >
root = tk.Tk() # Initialize window
root.geometry(f'{WINDOW_SIZE.x}x{WINDOW_SIZE.y}') # Set size of the window
root.resizable(0,0) # We dont want it to be resizable
# ---
local_multiplayer.load(root,WINDOW_SIZE)


root.mainloop() # Start running window