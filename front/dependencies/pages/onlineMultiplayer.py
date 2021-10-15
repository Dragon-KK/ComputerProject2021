from ..utils import page
import tkinter as tk
from ..utils.custom import TextBox, Frame


class onlineMultiplayer(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onDestruction(self):
        print("am die")

    def render(self):
        self.container.config(background='black')

        
        self.elements['title'] = TextBox(self.container, text = "Online")\
        .updateStyles(
            top='10:h%', left='30:w%', width='40:w%',height='20:h%',
            font={'color': 'white','size' : 60 }
        )
        self.container.draw()
