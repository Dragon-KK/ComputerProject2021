from ..Core.Diagnostics.Debugging import Console
from ..Core.DataTypes.Standard import Vector
# These are just some arbitrary values
class Positions:
    Left = -1
    TopLeft = 0.5
    Top = 1
    TopRight = 1.5
    Right = 2
    BottomRight = 2.5
    Bottom = 3
    BottomLeft = 3.5
    Centre = 4

class Style:
    # The priority order in which the styles must be computed
    PriorityOrder = [
        "OriginType",
        "Size",
        "Position",
        "CornerRadius",
        "Visible",
        "BackgroundColor",
        "ForegroundColor",
        "BorderColor",
        "BorderStroke",
        "FontSize",
        "FontStyle"
    ]

    def __getattr__(self, name):
        return self.__dict__.get(name, None) # If a property isnt set just return None and dont give error

    def OnUpdate(self):
        # Needs to be overwritten by element
        return

    def __init__(self, **kwargs):        
        for key in kwargs.keys():self.Set(key, kwargs[key])

    def Set(self, propName, newValue, update = True):
        if propName not in Style.PriorityOrder: # If the property name is not recognized just ditch it
            Console.error(f"Invalid property name {propName}")
            return self
        if propName == "OriginType":
            if Positions.__dict__.get(newValue):
                newValue = Positions.__dict__.get(newValue) 
          
        self.__dict__[propName] = newValue
        if update:self.OnUpdate() # The element will change the OnUpdate function when its ready
        return self

    @classmethod
    def FromJson(cls, styles):
        if styles.get("OriginType"):
            if Positions.__dict__.get(styles["OriginType"]):
                styles["OriginType"] = Positions.__dict__.get(styles["OriginType"])
        return cls(**styles)
