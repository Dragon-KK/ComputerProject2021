from . import custom as customTK
from typing import Dict
class definition:

    def __init__(self, root, pageSize, navigator):
        self.root = root # Store this (i refer to this as parent sometimes)
        self.container = customTK.container(root) # Each page has a container which contains all the other elements
        self.container.place(relx = 0, rely = 0, relwidth = 1, relheight = 1) # Place it to fill the whole parent
        self.container.activate()
        self.pageSize = pageSize # Store this
        self.navigateTo = navigator # A way to talk to whoever initialized this page
        self.elements = {} # A dict of all elements in the page
        self.render()

    def onDestruction(self):
        '''
        Return True if destruction is to be continued
        To be overloaded by child if needed
        '''
        
        return True

    def destroy(self, force = False):
        '''
        Called on destruction, returns false if destruction is aborted

        Params\n
        force : bool -> if True destroys regardless of self.onDestruction 
        '''
        destructionAccepted = self.onDestruction()
        if force or destructionAccepted:
            self.container.destroy()
            return True
        else:
            return False

    def render(self):
        '''
        Called when the page is ready to be rendered
        '''
        pass

class container:
    '''
    Deals with keeping track of sibling pages and some other basic stuff

    Params:\n
    root : tk.Element -> The parent
    size : Vector -> the size
    pages : {
        name : page
    } -> A dict with all sibling pages
    '''
    def __init__(self, root, size ,pages : Dict[str, definition]):
        self.pages = pages
        self.root = root
        self.size = size
        self.currentActive = definition(root, size, self.open)

    def open(self, pageName, force = True):
        if not self.pages.get(pageName):return False
        if not self.currentActive.destroy(force = force):
            return False
        self.currentActive = self.pages[pageName](self.root, self.size, self.open)

    def destroy(self):
        self.currentActive.destroy(force=True)