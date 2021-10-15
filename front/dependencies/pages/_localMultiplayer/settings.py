from ...utils.page import childPage
from ...utils.custom import TextBox,Frame
class Settings(childPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        return

    def onDestroy(self):
        print("I have died")

    def render(self):
        self.container.updateStyles(background = {'color' : 'black'})

        self.elements['navigationButtons'] = {
            'goBack' : TextBox(self.container, text = "back").updateStyles(
                top = '5:h%', left = '3:w%', width = '10:w%', height = '5:h%',
                font = {'color' : 'white', 'size' : 10},
                border = {'size' : 2, 'color' : 'white', 'radius' : 5}
            ).addEventListener('<Button-1>', lambda n: self.navigateTo('goBack'))
        }
        def a(e):
            print(e)

        self.elements['title'] = TextBox(self.container, text='Local Multiplayer')\
            .updateStyles(
                top = '5:h%', left = '30:w%', width = '40:w%', height = '5:h%',
                font = {'color' : 'white', 'size' : 30}
            ).addEventListener("<w>", a)
        

        self.elements['Frame'] = Frame(self.container).updateStyles(
            top = '15:h%', left = '3:w%', width = '94:w%', height = '80:h%',
            border = {'color' : '#28292f','size' : 2}
        )
        
        