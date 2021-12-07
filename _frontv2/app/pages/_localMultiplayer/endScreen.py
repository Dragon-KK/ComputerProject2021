from ...utils.page import childPage

from ...utils.custom import TextBox,Frame,TextInput
from ...utils import fileManager
from ..engine.pong import GameSettings

def render(container, goTo = print):
    elements ={}

    def onEnd():
        print("Closing End Screen")

    return onEnd