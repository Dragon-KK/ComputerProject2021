from ...utils.custom import TextBox,Frame,TextInput,Arena

from ...utils import fileManager,audioManager

from ...common.tools import Vector

from ..engine import drawing as shapes

from ..engine.pong import GameSettings,Ball,Game,Player,Wall,WinZone

from ..engine.physics import world
from ...utils.daemon import Daemon
from ..engine import playerManager
from .._common import settings as settingsScreen

PHYSICSFPS = 20
p1Score = 0
p2Score = 0
def render(container, gameSettings : GameSettings, goTo = print):
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
    def showCont(*args):
        if elements.get('PauseContainer'):
            elements['PauseContainer'].destroy()
            del elements['PauseContainer']
        elements['ContinueButton'] = TextBox(container,text="Continue").updateStyles(
            left="40:w%",width="20:w%",height="10:h%",top="45:h%",background={'color':'blue'},font={'size':15,'color':'white'}
        ).addEventListener('<Button-1>', cont)
        elements['ContinueButton'].draw()
    def pause(*args):
        game.pause()
        physics.pause()
        elements['PauseContainer'] = Frame(container).updateStyles(
            top='0:px',left='0:px',height="100:h%",width='100:w%',background={'color':None}
        )
        settingsScreen.render(elements['PauseContainer'], showCont)
        elements['PauseContainer'].draw()

    


    def cont(*args):
        elements['ContinueButton'].destroy() if elements.get('ContinueButton') else 0
        del elements['ContinueButton']
        game.cont()
        physics.cont()

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
        playerManager.localMultiplayer(
            Player( arena,   {
                            "verticalWall" : Wall(arena,
                                                p1=Vector('1:w%','35:h%'),
                                                p2=Vector('1:w%','65:h%'),
                                                size=5,
                                                color="white"
                                            )
                            }, 
                    playerManager.LEFTPLAYER, 
                    Vector("-35:h%", "35:h%")), 
            Player( arena,   {
                            "verticalWall" : Wall(arena,
                                                p1=Vector('99:w%','35:h%'),
                                                p2=Vector('99:w%','65:h%'),
                                                size=5,
                                                color="white"
                                            )
                            }, 
                    playerManager.LEFTPLAYER, 
                    Vector("-35:h%", "35:h%")),
            arena)
            ,
        fps=21,
        walls = {
            'top' : Wall(arena,vertical=False, 
                p1=Vector('0:px', '0:px'),
                p2=Vector('100:w%', '0:px')),
            'bottom' : Wall(arena,vertical=False, 
                p1=Vector('0:px', '100:h%'),
                p2=Vector('100:w%', '100:h%')),
            },
        winZones={     
            'left' : WinZone(playerManager.RIGHTPLAYER,arena,vertical=True, 
                p1=Vector('0:px', '0:px'),
                p2=Vector('0:px', '100:h%')),
            'right' : WinZone(playerManager.LEFTPLAYER,arena,vertical=True, 
                p1=Vector('100:w%', '0:h%'),
                p2=Vector('100:w%', '100:h%')),
        },
        balls=[
            Ball(
                arena,
                walls = ['top', 'bottom'],
                winZones = ['left','right'],
                acceleration=gameSettings.difficultySlope,
                initialSpeed=gameSettings.speed
            )
        ]
    )
    
    def roundEnd(res):
        global p1Score
        global p2Score
        print("Round Over ",res)
        physics.pause()
        game.pause()
        if res == playerManager.LEFTPLAYER:p1Score += 1
        elif res == playerManager.RIGHTPLAYER:p2Score += 1
        # TODO
        # Check for win logic goes here

        # TODO
        # Make and screen
        # Make pause screen
        # Then only multiplayer is left : )
        updateScores(p1Score, p2Score)
        showCont()
    elements['navigationButtons'] = {

        'goBack' : TextBox(container, text = "back").updateStyles(

            top = '5:h%', left = '3:w%', width = '10:w%', height = '5:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'},

            border = {'size' : 2, 'color' : 'white', 'radius' : 5}

        ).addEventListener('<Button-1>', lambda n: goTo('mainMenu'))
    }
    game = createRound()    
    World = world(game, roundEnd)
    physics = Daemon(arena.getTkObj(),PHYSICSFPS, World.work)

    game.pause()
    physics.pause()

    elements['ContinueButton'] = TextBox(container,text="Continue").updateStyles(
            left="40:w%",width="20:w%",height="10:h%",top="45:h%",background={'color':'blue'},font={'size':15,'color':'white'}
        ).addEventListener('<Button-1>', cont)
    # This part looks ugly but you win some you lose some ig
    def onEnd():
        game.forceQuit()
        physics.pause()
    return onEnd