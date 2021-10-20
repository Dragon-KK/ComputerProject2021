from ...utils.page import childPage

from ...utils.custom import TextBox,Frame,TextInput

from ..engine.pong import GameSettings

def render(container, goTo = print):


    container.updateStyles(background = {'color' : 'black'})

    elements ={}

    elements['navigationButtons'] = {

        'goBack' : TextBox(container, text = "back").updateStyles(

            top = '5:h%', left = '3:w%', width = '10:w%', height = '5:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'},

            border = {'size' : 2, 'color' : 'white', 'radius' : 5}

        ).addEventListener('<Button-1>', lambda n: goTo('mainMenu'))

    }

    def unfocusInputs(*args):

        container.updateFocus(None)
    

    def start(*args):

        speed = elements['Speed']['input'].value

        difficulty = elements['difficultySlope']['input'].value
        winCond = elements['winCondInput']['input'].value
        print(difficulty,winCond)
        if not speed:
            elements['Speed']['input'].updateStyles(border = {'color' : 'red'})
            elements['Speed']['input'].update()

        if not difficulty:
            elements['difficultySlope']['input'].updateStyles(border = {'color' : 'red'})

            elements['difficultySlope']['input'].update()
        if winCond == '':
            elements['winCondInput']['input'].updateStyles(border = {'color' : 'red'})

            elements['winCondInput']['input'].update()

        if speed and difficulty and winCond:

            setting = GameSettings(difficulty= speed,difficultySlope=difficulty,winCondition=winCond)
            goTo('play',setting)



    elements['title'] = TextBox(container, text='Local Multiplayer') .updateStyles(

            top = '5:h%', left = '30:w%', width = '40:w%', height = '5:h%',

            font = {'color' : 'white', 'size' : 30, 'style' : 'ariel'}

        ).addEventListener('<Button-1>',unfocusInputs)
    
    



    elements['Frame'] = Frame(container).updateStyles(

        top = '15:h%', left = '3:w%', width = '94:w%', height = '80:h%',

        border = {'color' : '#28292f','size' : 2}

    )
    


    container.addEventListener('<Button-1>',unfocusInputs)

    elements['Frame'].addEventListener('<Button-1>',unfocusInputs)


    elements['SettingsContainers'] = {

        'Speed' : Frame(elements['Frame']).updateStyles(

            top='3:h%',left = '3:w%', width = '40:w%', height = '5:w%',

            border = {'color' : '#303030', 'size' : 2}

        ),

        'winCondInput' : Frame(elements['Frame']).updateStyles(

            top='15:h%',left = '3:w%', width = '40:w%', height = '5:w%',

            border = {'color' : '#303030', 'size' : 2}

        ),

        'difficultySlope' : Frame(elements['Frame']).updateStyles(

            top='27:h%',left = '3:w%', width = '40:w%', height = '5:w%',

            border = {'color' : '#303030', 'size' : 4}

        )

    }


    elements['Speed'] = {

        "label" : TextBox(elements['SettingsContainers']['Speed'], text="Speed").updateStyles(

            top = '0:px',left = '0:px', width = '50:w%', height = '100:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'}

        ),

        "input" : TextInput(elements['SettingsContainers']['Speed'], numeric=True).updateStyles(

        top = '0:px',left = '50:w%', width = '50:w%', height = '100:h%',

        border = {'radius' : 10,'size' : 2},

        font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'})

    }

    elements['winCondInput'] = {

        "label" : TextBox(elements['SettingsContainers']['winCondInput'], text="Race to").updateStyles(

            top = '0:px',left = '0:px', width = '50:w%', height = '100:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'}

        ),

        "input" : TextInput(elements['SettingsContainers']['winCondInput'], numeric=True).updateStyles(

        top = '0:px',left = '50:w%', width = '50:w%', height = '100:h%',

        border = {'radius' : 10,'size' : 2},

        font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'})

    }
    

    elements['difficultySlope'] = {

        "label" : TextBox(elements['SettingsContainers']['difficultySlope'], text="Difficulty").updateStyles(

            top = '0:px',left = '0:px', width = '50:w%', height = '100:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'}

        ),

        "input" : TextInput(elements['SettingsContainers']['difficultySlope'], numeric=True).updateStyles(

        top = '0:px',left = '50:w%', width = '50:w%', height = '100:h%',

        border = {'radius' : 10,'size' : 2},

        font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'})

    }


    elements['start'] = TextBox(elements['Frame'], text = "Start").updateStyles(

        bottom = "2.5:h%", right = "2.5:w%",height = "7.5:h%", width = "10:w%",

        border = {'color' : '#303030', 'size' : 2, 'radius' : 10},

        font = {'color' : 'white','size' : 10, 'style' : 'ariel'}

    ).addEventListener('<Button-1>', start)