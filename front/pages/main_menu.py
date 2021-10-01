from time import sleep
from . import page_index as pages
import tkinter as tk
Container = None
def unload():
    Container.destroy()



def load(root,size,navigateTo):
    global Container
    Container = tk.Label(root, background = "black")
    Container.place(x = 0,y = 0,relwidth = 1, relheight = 1)

    title = tk.Label(Container,background="black",text = "PONG",fg="white")
    title.place(relx = 0.3,rely = 0.2,relheight = 0.2,relwidth = 0.4)

    modesContainer = tk.Label(Container, background="#111111")
    modesContainer.place(relx = 0.1,relwidth = 0.8,rely = 0.6,relheight = 0.2)

    local_multiplayer = tk.Button(modesContainer,text="Local Multiplayer", background="white",command=lambda:navigateTo(pages.LOCAL_MULTIPLAYER))
    local_multiplayer.grid()