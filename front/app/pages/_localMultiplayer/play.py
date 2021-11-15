from ...utils.custom import TextBox,Frame,TextInput,Arena

from ...utils import fileManager

from ...common.tools import Vector

from ..engine import drawing as shapes

from ..engine.pong import GameSettings,Ball,Game,Player,Wall,WinZone

from ..engine.physics import world
from ..engine.util import Daemon

from ..engine import playerManagers as PlayerManager

PHYSICSFPS = 30
p1Score = 0
p2Score = 0
def render(container, gameSettings, goTo = print):
    global p1Score
    global p2Score
    p1Score = 0
    p2Score = 0
    container.updateStyles(background = {'color' : 'black'})


    elements = {}
    elements['Arena'] = Arena(container).updateStyles(
        top='10:h%',height = '90:h%',left='0:w%',width = '100:w%',
        border = {'color' : '#707070', 'size' : 3}
    )

    def pause(*args):
        if physics.paused:
            game.cont()
            physics.cont()
        else:
            game.pause()
            physics.pause()
        return

    def updateScores(p1,p2):

        elements['scoreCounter']['p1'].text = p1
        elements['scoreCounter']['p2'].text = p2

        elements['scoreCounter']['p1'].update()
        elements['scoreCounter']['p2'].update()


    elements['pause'] = TextBox(container,text = "l l").updateStyles(
        right='1:w%',height = '3:w%',top='3:h%',width = '3:w%',
        border = {'color' : 'white', 'size' : 2, 'radius' : 10},
        font = {'size' : 15, 'color' : 'white', 'style' : 'ariel'}
    ).addEventListener("<Button-1>", pause)

    elements['scoreCounter'] = {
        'p1' : TextBox(container, text = 0).updateStyles(
            height = '9:h%', top = '0:px', width = '30:w%',left='19:w%',
            font = {'style' : 'ariel', 'color' : 'white', 'size' : 10 }
        ),
        'p2' : TextBox(container, text = 0).updateStyles(
            height = '9:h%', top = '0:px', width = '30:w%',left='51:w%',
            font = {'style' : 'ariel', 'color' : 'white', 'size' : 10 }
        )
    }   

    arena = elements['Arena']    

    sectionizer = arena.registerItem(
        shapes.line(
            Vector('50:vw', '0:vh'),
            Vector('50:vw', '100:vh'),
            absolute = True,
            dash=(4,1),
            size = 2,
            color = "#303030"
        )
    )
    def createRound():
        # This is why we have over 50 files
        # This is clean and easy to configure
        return Game(
        arena,
        gameSettings,
        None,
        fps=16,
        walls = {
            'top' : Wall(arena,vertical=False, p1=Vector('0:px', '0:px'),p2=Vector('100:w%', '0:px')),
            'bottom' : Wall(arena,vertical=False, p1=Vector('0:px', '100:h%'),p2=Vector('100:w%', '100:h%')),
            },
        winZones={            
            'left' : WinZone(PlayerManager.player2,arena,vertical=True, p1=Vector('0:px', '0:px'),p2=Vector('0:px', '100:h%')),
            'right' : WinZone(PlayerManager.player1,arena,vertical=True, p1=Vector('100:w%', '0:h%'),p2=Vector('100:w%', '100:h%')),
        },
        balls=[
            Ball(
                arena,
                walls = ['top', 'bottom'],
                winZones = ['left','right'],
                acceleration=10,
                initialSpeed=300
            )
        ]
    )
    
    def roundEnd(res):
        global p1Score
        global p2Score
        print("Round Over ",res)
        physics.pause()
        game.pause()
        if res == PlayerManager.player1:p1Score += 1
        elif res == PlayerManager.player2:p2Score += 1
        updateScores(p1Score, p2Score)

          
    game = createRound()    
    World = world(game, roundEnd)
    physics = Daemon(arena.getTkObj(),PHYSICSFPS, World.work)
    
    # This part looks ugly but you win some you lose some ig
    def onEnd():
        game.forceQuit()
        physics.pause()
    return onEnd