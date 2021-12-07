from ...utils.page import childPage
from ...utils.custom import TextBox,Frame,TextInput

def render(container, Return = print,audioManager = None):
    elements = {}
    elements['navigationButtons'] = {

        'goBack' : TextBox(container, text = "back").updateStyles(

            top = '5:h%', left = '3:w%', width = '10:w%', height = '5:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'},

            border = {'size' : 2, 'color' : 'white', 'radius' : 5}

        ).addEventListener('<Button-1>', Return)

    }

    def unfocusInputs(*args):
        container.updateFocus(None)    	

    elements['Frame'] = Frame(container).updateStyles(

        top = '15:h%', left = '3:w%', width = '94:w%', height = '80:h%',

        border = {'color' : '#28292f','size' : 2}

    )
    elements['title'] = TextBox(elements['Frame'], text='Settings') .updateStyles(

            top = '5:h%', left = '30:w%', width = '40:w%', height = '5:h%',

            font = {'color' : 'white', 'size' : 30, 'style' : 'ariel'}

        ).addEventListener('<Button-1>',unfocusInputs)
    
    

    
    


    # container.addEventListener('<Button-1>',unfocusInputs)
    # elements['Frame'].addEventListener('<Button-1>',unfocusInputs)


    elements['SettingsContainers'] = {
         'Music' : Frame(elements['Frame']).updateStyles(

            top='39:h%',left = '3:w%', width = '40:w%', height = '5:w%',

            border = {'color' : '#303030', 'size' : 4}

        ),

    }

    
    def MusicClick(*args):
        audioManager.stopBGMusic() if audioManager.bgMusicIsPlaying else audioManager.startBGMusic()
        elements['Music']['input'].text = "Yes" if audioManager.bgMusicIsPlaying else "No"
        
        elements['Music']['input'].update()
    
    elements['Music'] = {

        "label" : TextBox(elements['SettingsContainers']['Music'], text="Music").updateStyles(

            top = '0:px',left = '0:px', width = '50:w%', height = '100:h%',

            font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'}

        ),

        "input" : TextBox(elements['SettingsContainers']['Music'], text = "Yes" if audioManager.bgMusicIsPlaying else "No").updateStyles(

        top = '0:px',left = '50:w%', width = '50:w%', height = '100:h%',
        background = {'color' : '#202020'},
        border = {'radius' : 10,'size' : 2},

        font = {'color' : 'white', 'size' : 10, 'style' : 'ariel'}).addEventListener("<Button-1>", MusicClick)
    }

    def onEnd():
        print("Closing Main Settings")

    return onEnd