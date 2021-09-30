import tkinter as tk
from helpers import Vector
from pong import Pong
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

# < Background >
canvas = tk.Canvas(root,background = "black") # background is going to be a Canvas on the {root} with background black
canvas.place(x = 0, y = 0, width = WINDOW_SIZE.x,height = WINDOW_SIZE.y) # We place the background at 0,0 with width = window's width and height = window's height
# ---

Pong(root, canvas, WINDOW_SIZE) # Refer to pong.py for this function

root.mainloop() # Start running window