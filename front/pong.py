import tkinter as tk
from helpers import Vector
import drawingtools
from keyboardinput import BindKeyDown
# < Some constants >
fps = 10 # Number of frames per second
xOffset = 20 # Distance from the edge of the screen player is drawn
paddleSpeed = Vector(0, 5)
# < Some declarations >
p1CanvasID = -1
p2CanvasID = -1
middleSectionLineCanvasID = -1
def Pong(root : tk.Tk,canvas : tk.Canvas, size : Vector):
    '''
    Deals with the main working of our app\n    
    Params :\n
    root (tk.Tk) - The root of out app (the window object)
    canvas (tk.Canvas) - The canvas on whice we can draw the game on\n   
    size (Vector) - The size of the canvas\n
    ''' 
    # < Defining players >
    playerRenderInfo = {
        "size" : Vector(20,60),
        "color" : "white"
    }
    # Player 1
    player1 = {
        'position' : Vector(xOffset, size.y / 2)
    }

    # Player 2
    player2 = {
        'position' : Vector(size.x - xOffset, size.y / 2)
    }
    # ---
    

    # < Called once at the start, renders some items that stay forever >
    def InitialRender():
        global middleSectionLineCanvasID
        global p1CanvasID
        global p2CanvasID
        # Draw the middle line
        middleSectionLineCanvasID = canvas.create_line(size.x / 2, 0, size.x / 2, size.y,fill = "white",dash=(3, 1),tags="splitDistance")

        p1CanvasID = drawingtools.draw_rectangle_with_centre(canvas, player1['position'], playerRenderInfo['size'])
        p2CanvasID = drawingtools.draw_rectangle_with_centre(canvas, player2['position'], playerRenderInfo['size'])
        


    # < Renders the game > | To be used whenever some update is made
    def Render():
        global p1CanvasID
        global p2CanvasID
        # !!! Note !!!
        # Canvas origin is not in the centre, it is the top left
        canvas.delete(p1CanvasID,p2CanvasID) # delete drawing done in previous frame
        p1CanvasID = drawingtools.draw_rectangle_with_centre(canvas, player1['position'], playerRenderInfo['size'])
        p2CanvasID = drawingtools.draw_rectangle_with_centre(canvas, player2['position'], playerRenderInfo['size'])
        

    # < Called every frame, Handles logic and rendering >
    def HandleFrame():
        # Called every {1000 / fps} milliseconds
        root.after(int(1000 / fps), HandleFrame)

    # < Called when a key is pressed >
    def keydown(key):
        
        if key == "Up":
            if (player2['position'] - paddleSpeed - (playerRenderInfo['size'] / 2)).y > 0:
                player2['position'] -= paddleSpeed
                Render()
        elif key == "Down":
            if (player2['position'] + paddleSpeed + (playerRenderInfo['size'] / 2)).y < size.y:
                player2['position'] += paddleSpeed
                Render()
        elif key == "w":
            if (player1['position'] - paddleSpeed - (playerRenderInfo['size'] / 2)).y > 0:
                player1['position'] -= paddleSpeed
                Render()
        elif key == "s":
            if (player1['position'] + paddleSpeed + (playerRenderInfo['size'] / 2)).y < size.y:
                player1['position'] += paddleSpeed
                Render()

    # < Adding keybinds >
    keybind = BindKeyDown(root, msdelay=10)
    keybind.bindKey("Up",keydown)
    keybind.bindKey("Down",keydown)
    keybind.bindKey("w",keydown)
    keybind.bindKey("s",keydown)
    # ---

    InitialRender() # paint the initial screen
    HandleFrame() # start the actual logic
    


if __name__ == "__main__": # just for debugging
    import app