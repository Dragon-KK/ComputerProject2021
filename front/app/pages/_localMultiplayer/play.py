from ...utils.custom import TextBox,Frame,TextInput,Arena

from ...utils import fileManager

from ...common.tools import Vector

from ..engine import drawing as shapes

from ..engine.pong import GameSettings,Ball,Game,Player,Wall,WinZone


def render(container, gameSettings, goTo = print):

    container.updateStyles(background = {'color' : 'black'})

    elements = {}

    elements['Arena'] = Arena(container).updateStyles(

        top='10:h%',height = '90:h%',left='0:w%',width = '100:w%',

        border = {'color' : '#707070', 'size' : 3}
    )

    


    def pause(*args):
        game.forceQuit()
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


    # This is why we have over 50 files
    # This is clean and easy to configure
    game = Game(
        arena,
        gameSettings,
        None,
        walls = {
            'top' : Wall(arena,vertical=False, p1=Vector('0:px', '0:px'),p2=Vector('100:w%', '0:px')),
            'bottom' : Wall(arena,vertical=False, p1=Vector('0:px', '100:h%'),p2=Vector('100:w%', '100:h%')),
            'left' : Wall(arena,vertical=True, p1=Vector('0:px', '0:px'),p2=Vector('0:px', '100:h%')),
            'right' : Wall(arena,vertical=True, p1=Vector('100:w%', '0:h%'),p2=Vector('100:w%', '100:h%')),
            },
        winZones={},
        balls=[
            Ball(
                arena,
                walls = ['top', 'bottom','left','right'],
                winZones = [],
                acceleration=10,
                initialSpeed=100
            )
        ]

    )

    # This part looks ugly but you win some you lose some ig
    def onEnd():
        game.forceQuit()
    return onEnd