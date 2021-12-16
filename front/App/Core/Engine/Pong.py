from . import World
from . import Entities

class Pong:
    '''
    Deals with world physics and adding entitites
    '''
    def __init__(
        self,
        worldContainer,
        gameSettings, # Settings
        players = [],
        balls = [], 
        walls = [],
        goals = []
        ):
        self.World = World(worldContainer)

    '''
    Idea :
        Isolate updating renders completely
        Just takes in list of entities and renders them

    World has jsonify and dejsonify inbuilt
    players are just entities
    Pong class doesnt store anything it just acts as the medium

    ** The entities itself just contain stuff they arent really doing any logic by themselves, physics will handle everything **
    '''