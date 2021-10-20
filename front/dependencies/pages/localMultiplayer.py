from ..utils import page
import tkinter as tk
from ..utils.custom import TextBox, Frame
from ..utils.page import container
from ._localMultiplayer import settings
"""
Instead of usig a container for child pages, just import a function that is called on render this is mucch easier
"""


class localMultiplayer(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def navigate(self,location,*args):
        self.elements['container'].destroy()
        if location == "play":
            print(args[0])
            self.navigateTo("mainMenu")
        elif location == "mainMenu":
            self.navigateTo(location)
        else:
            print("Error")

    def onDestruction(self):
        print("am die")

    def render(self):
        self.container.config(background='black')
        self.elements['container'] = Frame(self.container).updateStyles(
            top = '0:px',left = '0:px',width = '100:w%',height = '100:h%'
        )
        settings.render(self.elements['container'], goTo = self.navigate)
        self.container.draw()
