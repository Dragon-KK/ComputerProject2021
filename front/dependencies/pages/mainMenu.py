from ..utils import page
import tkinter as tk
from ..utils.custom import TextBox, Frame


class mainMenu(page.definition):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def onDestruction(self):
        print("am die")

    def render(self):
        self.container.config(background='black')

        self.elements['buttonContainer'] = Frame(self.container)\
            .updateStyles(
                bottom='15:h%', left='30:w%', width='40:w%', height='25:h%',
                background={'color': None}
            )
        self.elements['title'] = TextBox(self.container, text = "PONG")\
        .updateStyles(
            top='10:h%', left='30:w%', width='40:w%',height='20:h%',
            font={'color': 'white','size' : 60 }
        )
        self.elements['buttons'] = {
            'playLocalButton' : TextBox(self.elements['buttonContainer'], text="LOCAL")\
                .updateStyles(
                    top='0:px', left='0:px', width='48:w%', height='55:h%',
                    font={'color': 'white', 'size': 20, 'style': 'Ariel'},
                    background={'color': None},
                    border={'radius': 30,'size' : 3, 'color': 'white'}
                ).addEventListener('<Button-1>', lambda n:print("Play Local")),
            'playOnineButton' : TextBox(self.elements['buttonContainer'], text="ONLINE")\
                .updateStyles(
                    top='0:px', left='52:w%', width='48:w%', height='55:h%',
                    font={'color': 'white', 'size': 20, 'style': 'Ariel'},
                    background={'color': None},
                    border={'radius': 30,'size' : 3, 'color': 'white'}
                ).addEventListener('<Button-1>', lambda n:print("Play Online")),
            'freePlayButton' : TextBox(self.elements['buttonContainer'], text="Free Play")\
                .updateStyles(
                    top='65:h%', left='52:w%', width='48:w%', height='35:h%',
                    font={'color': 'white', 'size': 20, 'style': 'Ariel'},
                    background={'color': None},
                    border={'radius': 10,'size' : 3, 'color': 'white'}
                ).addEventListener('<Button-1>', lambda n:print("Play Online")),
            'aboutUsButton' : TextBox(self.elements['buttonContainer'], text="About Us")\
                .updateStyles(
                    top='65:h%', left='0:w%', width='48:w%', height='35:h%',
                    font={'color': 'white', 'size': 20, 'style': 'Ariel'},
                    background={'color': None},
                    border={'radius': 10,'size' : 3, 'color': 'white'}
                ).addEventListener('<Button-1>', lambda n:print("Play Online")),
        }
        self.container.draw()
