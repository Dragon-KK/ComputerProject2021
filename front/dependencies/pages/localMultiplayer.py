from ..utils import page
import tkinter as tk
from ..utils.custom import TextBox, Frame
from ..utils.page import container
from ._localMultiplayer import settings


class localMultiplayer(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def goBack(self,*args):
        print(1)
        self.c.destroy()
        self.navigateTo('mainMenu')

    def onDestruction(self):
        print("am die")

    def render(self):
        print(self.container)
        self.container.config(background='black')
        self.c = container(self.container, (0,0), {
            'Settings' : settings.Settings,
            'goBack' : self.goBack
        })
        self.c.open('Settings')
        self.container.draw()
