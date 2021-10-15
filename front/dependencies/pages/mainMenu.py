from ..utils import page
import tkinter as tk
from ..utils.custom import Button
class mainMenu(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onDestruction(self):
        print("am die")


    def render(self):
        def tmp(a):
            self.elements['button'].undraw()
        self.container.config(background='black')
        self.elements['button'] = Button(self.container,text='yo')\
        .updateStyles(
            top=100,right=10,width=60,height=30,
            font = {'color' : 'black', 'size' : 20, 'style' : 'Ariel'},
            background = { 'color' : 'white' },
            border = {'radius' : 20, 'color' : 'white'}
        ).addEventListener('<Button-1>', tmp)
        self.elements['child'] = Button(self.elements['button'],
        text="Hello")\
        .updateStyles(
            top=100,left=10,width=60,height=30,
            font = {'color' : 'black', 'size' : 20, 'style' : 'Ariel'},
            background = { 'color' : 'white' },
            border = {'radius' : 20, 'color' : 'white'}
        )
        self.container.draw()
