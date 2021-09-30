import tkinter as tk
from helpers import Vector
import drawingtools
from keyboardinput import BindKeyDown

def Pong(root : tk.Tk,canvas : tk.Canvas, size : Vector):
    '''
    Deals with the main working of our app\n    
    Params :\n
    root (tk.Tk) - The root of out app (the window)
    canvas (tk.Canvas) - The canvas on which we can draw the game on\n   
    size (Vector) - The size of the canvas\n
    ''' 
    # < Some constants >
    delay = 10 # ms between each Frame
    canvasIDS = { # Given by canvas when we draw stuff
        "p1" : -1, # for player1 (left side)
        "p2" : -1, # for player2 (right side)
        "ball" : -1, # ball
        "middleSectionLineCanvasID" : -1 # for the middle division line thingy
    }
    
    # < Defining ball >
    ball = {
        'position' : Vector(size.x/2, size.y/2),
        'direction' : Vector(3,4).normalized()
    }
    ballInfo = {
        'radius' : 10,
        'ballSpeed' : 2
    }

    # < Defining players >
    playerInfo = {
        'size' : Vector(20,80),
        'color' : "white",
        'paddleSpeed' : 5,
        'xOffset' : 20
    }
    # Player 1
    player1 = {
        'position' : Vector(playerInfo['xOffset'], size.y / 2)
    }

    # Player 2
    player2 = {
        'position' : Vector(size.x - playerInfo['xOffset'], size.y / 2)
    }
    # ---
    

    # < Called once at the start, renders some items that stay forever >
    def InitialRender():
        # Draw the middle line
        canvasIDS["middleSectionLineCanvasID"] = canvas.create_line(size.x / 2, 0, size.x / 2, size.y,fill = "white",dash=(3, 1),tags="splitDistance")

        canvasIDS['p1'] = drawingtools.draw_rectangle_with_centre(canvas, player1['position'], playerInfo['size'])
        canvasIDS['p2'] = drawingtools.draw_rectangle_with_centre(canvas, player2['position'], playerInfo['size'])
        
        canvasIDS['ball'] = drawingtools.draw_circle_with_centre(canvas, ball['position'], ballInfo['radius'])


    # < Renders the game > | To be used whenever some update is made
    def Render():
        # !!! Note !!!
        # Canvas origin is not in the centre, it is the top left
        canvas.delete(canvasIDS['p1'],canvasIDS['p2']) # delete drawing done in previous frame
        canvasIDS['p1'] = drawingtools.draw_rectangle_with_centre(canvas, player1['position'], playerInfo['size']) # Drawing player1
        canvasIDS['p2'] = drawingtools.draw_rectangle_with_centre(canvas, player2['position'], playerInfo['size']) # Drawing player2
        
        canvas.delete(canvasIDS['ball'])
        canvasIDS['ball'] = drawingtools.draw_circle_with_centre(canvas, ball['position'], ballInfo['radius'])

    # < Called every frame, Handles logic and rendering >
    def HandleFrame():
        # Called every {1000 / fps} milliseconds
        
        ball['position'] += ball['direction'] * ballInfo['ballSpeed']
        Render()
        root.after(delay, HandleFrame)

    # < Called when a key is pressed >
    def onKeydown(key):
        # Origin is top left of screen
        up = Vector(0,-1)
        down = Vector(0,1)
        if key == "Up":
            if (player2['position'] + up * playerInfo['paddleSpeed'] - (playerInfo['size'] / 2)).y > 0:
                player2['position'] += up * playerInfo['paddleSpeed']
        elif key == "Down":
            if (player2['position'] + down * playerInfo['paddleSpeed'] + (playerInfo['size'] / 2)).y < size.y:
                player2['position'] += down * playerInfo['paddleSpeed']
        elif key == "w":
            if (player1['position'] + up * playerInfo['paddleSpeed'] - (playerInfo['size'] / 2)).y > 0:
                player1['position'] += up *playerInfo['paddleSpeed']
        elif key == "s":
            if (player1['position'] + down * playerInfo['paddleSpeed'] + (playerInfo['size'] / 2)).y < size.y:
                player1['position'] += down * playerInfo['paddleSpeed']

    # < Adding keybinds >
    keybinds = BindKeyDown(root, msdelay=10)
    keybinds.bindKey("Up",onKeydown)
    keybinds.bindKey("Down",onKeydown)
    keybinds.bindKey("w",onKeydown)
    keybinds.bindKey("s",onKeydown)
    # ---

    InitialRender() # paint the initial screen
    HandleFrame() # start the actual logic cycle
    


if __name__ == "__main__": # just for debugging
    import app