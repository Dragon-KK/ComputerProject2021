from .div import div
from ...Core.DataTypes.UI import EventListener

class radio(div):
    def __init__(self,*args, **kwargs):
        kwargs['elemName'] = kwargs.get('elemName', 'radio')
        super().__init__(*args, **kwargs)
        
        self._SelectedElement = None
        self.SelectEvent = EventListener("<Button-1>", self.OnSelect)

    def OnSelect(self, e):
        self.SelectedElement = e.Sender

    def _Render(self):
        self.Children.OnChildrenChanged = self.OnChildrenChanged
        for child in self.Children:
            child.EventListeners += self.SelectEvent

    @property
    def SelectedElement(self):
        """The SelectedElement property."""
        return self._SelectedElement
    @SelectedElement.setter
    def SelectedElement(self, value):
        if value == self.SelectedElement:return
        if self._SelectedElement:
            self._SelectedElement.State -= "RadioSelected"
        self._SelectedElement = value
        if value:value.State += "RadioSelected"

    def OnChildrenChanged(self, added = None, removed = None):
        if removed:
            if removed == self.SelectedElement:
                self._SelectedElement = None
        else:
            added.EventListeners += self.SelectEvent

