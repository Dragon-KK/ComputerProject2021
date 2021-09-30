import tkinter as tk
from .common.helpers import Vector
from time import sleep
from ._local_multiplayer import pong
from ._local_multiplayer import constants as cmd

root = None
canvas = None
currentScore = {
    1 : 0,
    2 : 0
}
Round = None
def load(_root : tk.Tk, WINDOW_SIZE : Vector):
    global root
    global Round
    global canvas
    
    root = _root
    # Ignore the comments with code in it, i just kept it just in case i want to debug something
    # WINDOW_SIZE.x -= 30
    # def onClick():
    #     x = Round(cmd.GET_STATE)
    #     if x:
    #         print("I am paused")
    #         Round(cmd.CONTINUE)
    #     else:
    #         print("I am not paused")
    #         Round(cmd.PAUSE)

    # debug_button = tk.Button(root,command=onClick,text="Pause")
    # debug_button.place(x = WINDOW_SIZE.x, y = 0, width=30,height=30)


    # < Canvas >
    canvas = tk.Canvas(root,background = "black") # background is going to be a Canvas on the {root} with background black
    canvas.place(x = 0, y = 0, width = WINDOW_SIZE.x,height = WINDOW_SIZE.y) # We place the background at 0,0 with width = window's width and height = window's height
    # ---

    # < Score Counter >
    p1Score = tk.Label(root, background = "black",text = "0", fg ="white")
    p1Score.place(x = WINDOW_SIZE.x / 2 - 50, y = 10, width = 20, height = 20)

    p2Score = tk.Label(root, background = "black",text = "0", fg="white")
    p2Score.place(x = WINDOW_SIZE.x / 2 + 30, y = 10, width = 20, height = 20)
    # ---
    
    def onRoundEnd(res):
        global Round
        global currentScore
        currentScore[res['victorySide']] += 1
        print(f"{res['reason']}")
        print(f"player {res['victorySide']} has won the round")
        p1Score.config(text = str(currentScore[1]))
        p2Score.config(text = str(currentScore[2]))
        Round = pong.PongRound(root, canvas, WINDOW_SIZE, onRoundEnd = onRoundEnd)

    Round = pong.PongRound(root, canvas, WINDOW_SIZE, onRoundEnd = onRoundEnd) # Refer to pong.py for this function

def end():
    Round(cmd.FORCE_QUIT)
