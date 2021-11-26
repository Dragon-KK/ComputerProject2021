from ..utils import page
import tkinter as tk
from ..utils.custom import TextBox, Frame
from ..utils.page import container
from ._localMultiplayer import settings,play
"""
Instead of usig a container for child pages, just import a function that is called on render this is mucch easier
"""


class localMultiplayer(page.definition):

    def __init__(self, *args, **kwargs):
        self.activePage = "settings"
        self.args = []
        self.onEnd = print
        super().__init__(*args, **kwargs)
        

    def navigate(self,location,*args):
        self.elements['container'].destroy()
        self.args = args
        
        if location == "play":
            self.onEnd()
            for i in self.container.child_nodes:i.destroy()
            self.container.child_nodes.clear()
            self.activePage = 'play'
            self.render()
        elif location == 'settings':
            self.onEnd()
            for i in self.container.child_nodes:i.destroy()
            self.container.child_nodes.clear()
            self.activePage = 'settings'
            self.render()
        elif location == "mainMenu":
            self.navigateTo("mainMenu")
        else:
            print("Error")

    def onDestruction(self):
        print("Closing local multiplayer")
        for i in self.container.child_nodes:i.destroy()
        self.container.child_nodes.clear()
        self.onEnd()

    def render(self):
        self.elements['container'] = Frame(self.container).updateStyles(
            top = '0:px',left = '0:px',width = '100:w%',height = '100:h%'
        )
        if self.activePage == 'settings':        
            self.onEnd = settings.render(self.elements['container'], *self.args, goTo = self.navigate)
        elif self.activePage == 'play':
            self.onEnd = play.render(self.elements['container'], *self.args, goTo = self.navigate)
        
        
        self.container.draw()
