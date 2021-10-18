from ...utils.page import childPage
from ...utils.custom import TextBox,Frame
def render(container, goTo = print):

    container.updateStyles(background = {'color' : 'black'})
    elements ={}
    elements['navigationButtons'] = {
        'goBack' : TextBox(container, text = "back").updateStyles(
            top = '5:h%', left = '3:w%', width = '10:w%', height = '5:h%',
            font = {'color' : 'white', 'size' : 10},
            border = {'size' : 2, 'color' : 'white', 'radius' : 5}
        ).addEventListener('<Button-1>', lambda n: goTo('mainMenu'))
    }    

    elements['title'] = TextBox(container, text='Local Multiplayer')\
        .updateStyles(
            top = '5:h%', left = '30:w%', width = '40:w%', height = '5:h%',
            font = {'color' : 'white', 'size' : 30}
        )
    

    elements['Frame'] = Frame(container).updateStyles(
        top = '15:h%', left = '3:w%', width = '94:w%', height = '80:h%',
        border = {'color' : '#28292f','size' : 2}
    ).addEventListener("<Button-1>", print)

    elements['TextBox'] = TextBox(elements['Frame']).updateStyles(
        top='3:h%',left = '3:w%', width = '20:w%', height = '5:w%',
        border = {'color' : 'white','size' : 2}
    )
        