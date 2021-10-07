import tkinter as tk
from ..common.helpers import Vector
from ..common import drawingtools
from ..common.keyboardinput import BindKeyDown
from . import physics as world
from . import constants as cmd
renderLoopID = -1
logicLoopID = -1
paused = True

def resetGlobalScope():
    global paused
    paused = True

def PongRound(root : tk.Tk,canvas : tk.Canvas, size : Vector, onRoundEnd = print):
    '''
    Deals with the main working of our app\n    
    Params :\n
    root (tk.Tk) - The root of out app (the window)
    canvas (tk.Canvas) - The canvas on which we can draw the game on\n   
    size (Vector) - The size of the canvas\n
    ''' 
    # < Some constants >
    logicDelay = 10 # ms between each Frame
    renderDelay = 1 # ms between each render
    canvasIDS = { # Given by canvas when we draw stuff
        "p1" : -1, # for player1 (left side)
        "p2" : -1, # for player2 (right side)
        "ball" : -1, # ball
        "middleSectionLineCanvasID" : -1 # for the middle division line thingy
    }
    
    result = {
        "victorySide" : 0,
        "reason" : "Unkown Reason"
    }
    
    # < Defining ball >
    ball = {
        'position' : Vector(size.x/2, size.y/2),
        'direction' : Vector(3,4).normalized(),
        'size' : Vector(10,10),
        'ballSpeed' : 6,
        'displacement' : Vector(0,0),
        'collisionConst' : -3
    }

    # < Defining players >
    playerInfo = {
        'color' : "white",
        'paddleSpeed' : 5,
        'xOffset' : 13
    }
    # Player 1
    player1 = {
        'position' : Vector(playerInfo['xOffset'], size.y / 2),
        'size' : Vector(20,80),
        'displacement' : Vector(0,0),
        'dir' : 0
    }

    # Player 2
    player2 = {
        'position' : Vector(size.x - playerInfo['xOffset'], size.y / 2),
        'size' : Vector(20,80),
        'displacement' : Vector(0,0),
        'dir' : 0
    }
    # ---
    
    def End(): # Called when the round ends
        global renderLoopID
        global logicLoopID
        
        root.after_cancel(renderLoopID) # I no longer want to render stuff
        root.after_cancel(logicLoopID) # I no longer want to do logic
        keybinds.pause() # I no longer need to listen for keypress
        canvas.delete("all") # Clear the canvas so it can be reused
        
        onRoundEnd(result) # onRoundEnd is a function given by local_multiplayer

    # < Called once at the start, renders some items that stay forever >
    def InitialRender():
        # Draw the middle line
        canvasIDS["middleSectionLineCanvasID"] = canvas.create_line(size.x / 2, 0, size.x / 2, size.y,fill = "white",dash=(3, 1),tags="splitDistance")

        canvasIDS['p1'] = drawingtools.draw_rectangle_with_centre(canvas, player1['position'], player1['size'])
        canvasIDS['p2'] = drawingtools.draw_rectangle_with_centre(canvas, player2['position'], player2['size'])
        
        canvasIDS['ball'] = drawingtools.draw_rectangle_with_centre(canvas, ball['position'], ball['size'])


    # < Renders the game > | To be used whenever some update is made
    def Render():
        global renderLoopID
        # !!! Note !!!
        # Canvas origin is not in the centre, it is the top left
        
        # Move all the items by displacement
        drawingtools.moveItem(canvas, canvasIDS['p1'], player1['displacement'])
        drawingtools.moveItem(canvas, canvasIDS['p2'], player2['displacement'])
        drawingtools.moveItem(canvas, canvasIDS['ball'], ball['displacement'])
        player1['displacement'] = Vector(0,0)
        player2['displacement'] = Vector(0,0)
        ball['displacement'] = Vector(0,0)
        renderLoopID = root.after(renderDelay, Render)

    # < Called every frame, Handles logic and rendering >
    def HandleFrame():
        # Called every {1000 / fps} milliseconds
        global paused
        global logicLoopID
        
        if paused:return # should never really happen, but if it does this is another check

        if (world.hasCrossedHorizontalWalls(ball, (0, size.x))):
            if ball["position"].x < 0:
                result["victorySide"] = 2
                result["reason"] = "GOAL!"
            else:
                result["victorySide"] = 1
                result["reason"] = "GOAL!"
            End()
            return
        if (world.isCollidingVerticalWalls(ball, (0, size.y))):
            ball['direction'].y *= -1
        
        isColliding,collidingBody = world.lookForCollisionWithPaddles(ball, player1, player2)
        if (isColliding):
            currVel = ball['direction'] * ball['ballSpeed']
            #print(collidingBody['dir'],currVel.y)
            ball['direction'] = Vector(-currVel.x, currVel.y + (collidingBody['dir'] * ball["collisionConst"])).normalized()
        ball['position'] += ball['direction'] * ball['ballSpeed']
        ball['displacement'] += ball['direction'] * ball['ballSpeed']
        logicLoopID = root.after(logicDelay, HandleFrame)

    # < Called when a key is pressed >
    def onKeydown(key):
        # Origin is top left of screen
        up = Vector(0,-1)
        down = Vector(0,1)

        # Note that player['dir'] is used when ball collides with paddle
        if key == "Up":
            if (player2['position'] + up * playerInfo['paddleSpeed'] - (player2['size'] / 2)).y > 0:
                player2['displacement'] += up * playerInfo['paddleSpeed']
                player2['position'] += up * playerInfo['paddleSpeed']
                player2['dir'] = 1
        elif key == "Down":
            if (player2['position'] + down * playerInfo['paddleSpeed'] + (player2['size'] / 2)).y < size.y:
                player2['displacement'] += down * playerInfo['paddleSpeed']
                player2['position'] += down * playerInfo['paddleSpeed']
                player2['dir'] = -1
        elif key == "w":
            if (player1['position'] + up * playerInfo['paddleSpeed'] - (player1['size'] / 2)).y > 0:
                player1['displacement'] += up * playerInfo['paddleSpeed']
                player1['position'] += up *playerInfo['paddleSpeed']
                player1['dir'] = 1
        elif key == "s":
            if (player1['position'] + down * playerInfo['paddleSpeed'] + (player1['size'] / 2)).y < size.y:
                player1['displacement'] += down * playerInfo['paddleSpeed']
                player1['position'] += down * playerInfo['paddleSpeed']
                player1['dir'] = -1
    # < Called when a key is released >
    def onKeyUp(key):
        # Origin is top left of screen
        if key == "Up" or key == "Down":
            player2['dir'] = 0
        elif key == "w" or key == "s":
                player1['dir'] = 0


    # < Adding keybinds >
    keybinds = BindKeyDown(root, msdelay=20)
    keybinds.bindKey("Up",down=onKeydown, up=onKeyUp)
    keybinds.bindKey("Down",down=onKeydown, up=onKeyUp)
    keybinds.bindKey("w",down=onKeydown, up=onKeyUp)
    keybinds.bindKey("s",down=onKeydown, up=onKeyUp)
    # ---

    InitialRender() # paint the initial screen
    
    def pauseGame():
        global renderLoopID
        global logicLoopID
        global paused
        # Refer to 'End' for what these do
        paused = True
        root.after_cancel(renderLoopID)
        root.after_cancel(logicLoopID)
        keybinds.pause()
        return True
        
    def continueGame():
        global logicLoopID
        global renderLoopID
        global paused
        # Refer to 'End' for what these do
        paused = False
        keybinds.cont()
        renderLoopID = root.after(renderDelay, Render)
        logicLoopID = root.after(logicDelay, HandleFrame)
        return True

    def interface(c): # A way for the window to speak to the round
        if c == cmd.FORCE_QUIT:
            End()
            return True
        elif c == cmd.GET_STATE:
            global paused
            return paused
        elif c == cmd.PAUSE:
            return pauseGame()
        elif c == cmd.CONTINUE:
            return continueGame()
        else:
            return "Invalid Command!"

    return interface
