from ..utils import page
import tkinter as tk

class mainMenu(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onDestruction(self):
        print("am die")


    def render(self):
        self.container.config(background = "black")
        self.elements['title'] = tk.Label(self.container, text = "Hello World")
        self.elements['title'].place(relx = 0.3, relwidth = 0.4,rely = 0.1,relheight = 0.2)

        self.elements['buttons'] = {
            'Play' : tk.Button(self.container,text="Play",command=lambda:print("Hello"))
        }
        self.elements['buttons']['Play'].pack()
