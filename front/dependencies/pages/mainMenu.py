from ..utils import page
import tkinter as tk
from ..utils.custom import Button
class mainMenu(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onDestruction(self):
        print("am die")


    def render(self):
        self.container.config(background='black')
        self.elements['button'] = Button(self.container,
        css = {
            'top' : 100, 'right' : 10, 'width' : 60, 'height' : 30,
            'font' : {'color' : 'black', 'style' : 'Times'},
            'background' : { 'color' : None },
            'border':{'radius' : 20, 'color' : 'white'}
        },
        text='yo'
        )
        self.elements['button'].draw()
