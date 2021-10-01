import tkinter as tk
from pages.common.helpers import Vector
from pages import local_multiplayer,main_menu
from pages import  page_index as pages
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

__pages = {
    pages.MAIN_MENU : main_menu,
    pages.LOCAL_MULTIPLAYER : local_multiplayer
}

current = None
def goTo(page):
    global current
    global root
    global WINDOW_SIZE
    if current:
        current.unload()
        print("Finished deload")
    current = __pages.get(page)
    current.resetGlobalScope()
    current.load(root, WINDOW_SIZE + Vector(0,0), goTo)
    

goTo(pages.MAIN_MENU)

root.mainloop() # Start running window