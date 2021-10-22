from ...utils.page import childPage

from ...utils.custom import TextBox,Frame,TextInput,Arena
from ...utils import fileManager
from ..engine.pong import GameSettings,Ball,Game,Player

def render(container, gameSettings, goTo = print):
    container.updateStyles(background = {'color' : 'black'})
    elements = {}
    elements['Arena'] = Arena(container).updateStyles(
        top='10:h%',height = '89:h%',left='0.5:w%',width = '99:w%',
        border = {'color' : 'white', 'size' : 2, 'dash' : (1,1)}
    )

    def pause(*args):
        print(gameSettings)
        return

    elements['pause'] = TextBox(container,text = "l l").updateStyles(
        right='1:w%',height = '3:w%',top='3:h%',width = '3:w%',
        border = {'color' : 'white', 'size' : 2, 'radius' : 10},
        font = {'size' : 15, 'color' : 'white', 'style' : 'ariel'}
    ).addEventListener("<Button-1>", pause)

    