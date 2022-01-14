from ...Core.DataTypes.Standard import Vector
from ...Core.Diagnostics.Debugging import Console



class Styles:
    PriorityOrder = [
        "OriginType",
        "Size",
        "Position",
        "CornerRadius",
        "BackgroundColor",
        "ForegroundColor",
        "BorderColor",
        "BorderStroke",
        "FontSize",
        "FontStyle",
        "Padding",
        "FontType",
        "PlaceHolderForegroundColor",
        "Gap"
    ]
    Default = {
        "OriginType" : 'TopLeft',
        "Size" : (0,0),
        "Position" : (0,0),
        "CornerRadius" : "0",
        "BackgroundColor" : None,
        "ForegroundColor" : None,
        "PlaceHolderForegroundColor" : "gray",
        "BorderColor" : "Black",
        "BorderStroke" : 1,
        "FontSize" : "1:em",
        "FontStyle" : "Montserrat",
        "FontType" : "bold",
        "Padding" : "0:em",
        "Gap" : "0"

    }
    def __init__(self):
        self.OriginType = "TopLeft",
        self.Size = (0,0)
        self.Position = (0,0)
        self.CornerRadius = "0"
        self.BackgroundColor = ""
        self.ForegroundColor = ""
        self.PlaceHolderForegroundColor = "gray"
        self.BorderColor = ""
        self.BorderStroke = 0
        self.FontSize = "1:em"
        self.FontStyle = "Montserrat"
        self.FontType = "bold"
        self.Padding = "0:em"
        self.Gap = "0:em"

    def Remove(self, name):
        if name in self.PriorityOrder:
            self.__dict__[name] = self.Default[name]

    @classmethod
    def FromJson(cls, styles):
        retVal = cls()
        for propName in styles:
            retVal.__dict__[propName] = styles[propName]
        return retVal

class ComputedStyles:
    def __init__(self):
        self.Size = Vector(0, 0) # width, height
        self.Position = Vector(0, 0) # x, y relative to parent
        self.Origin = Vector(0, 0) # x, y the topleft of the parent
        self.TopLeft = Vector(0, 0) # x, y absolute
        self.FontSize = 10 # Fontsize
        self.SelfOriginType = "TopLeft" # Position
        self.CornerRadius = (0, 0, 0, 0) # (topleft, topright, bottomright, bottomleft)
        self.Padding = (0, 0, 0, 0) # (left, up, right, down)
        self.Gap = Vector(0, 0) # x,y

    @staticmethod
    def GetUnitMultiplyer(unit, element):
        if unit == "px": # pixel
            return 1
        elif unit == "vw": # viewport width
            return element.Window.ViewPort.x / 100
        elif unit == "vh": # viewport height
            return element.Window.ViewPort.y / 100
        elif unit == "h%": # height %
            return element.Parent.ComputedStyles.Size.y / 100
        elif unit == "w%": # width %
            return element.Parent.ComputedStyles.Size.x / 100
        elif unit == "em": # emphemeral unit
            return element.STYLE_UNITS['em']
        else:
            Console.error(f"Invalid unit {unit} on {element}")
            return 0

    @staticmethod
    def GetComputedValue(value, element):
        if type(value) == float or type(value) == int:
            return value
        if type(value) == str:
            try:
                return float(value)
            except ValueError:
                try:
                    val,unit = value.split(":")
                    return float(val) * ComputedStyles.GetUnitMultiplyer(unit,element)
                except:
                    Console.error(f"Invalid type of value {value} on {element}")
        else:
            Console.error(f"Invalid type for value {value} on {element}")
        # If the value is faulty just return 0
        return 0


    @classmethod
    def FromStyles(cls,styles,element):
        retVal = ComputedStyles()
        dic = styles.__dict__
        GetComputedValue = lambda n:ComputedStyles.GetComputedValue(n, element)
        
        for propName in Styles.PriorityOrder:
            if not dic.get(propName):continue
            if propName == 'Size':
                try:
                    retVal.Size = Vector(GetComputedValue(dic[propName][0]), GetComputedValue(dic[propName][1]))
                except Exception:
                    Console.error(f'Invalid style for {element} | {"{propName}" : {dic[propName]} : }')
                    continue
            elif propName == 'Position':
                try:
                    retVal.Position = Vector(GetComputedValue(dic[propName][0]), GetComputedValue(dic[propName][1]))
                except Exception:
                    Console.error(f'Invalid style for {element} | {"{propName}" : {dic[propName]} : }')
                    continue
            elif propName == 'OriginType':
                retVal.SelfOriginType = dic[propName]
            elif propName == 'CornerRadius':
                try:
                    x = dic[propName].split(',')
                    if len(x) == 1:
                        r = GetComputedValue(x[0])
                        retVal.CornerRadius = (r,r,r,r)
                    elif len(x) == 4:
                        retVal.CornerRadius = (GetComputedValue(x[0]),GetComputedValue(x[1]),GetComputedValue(x[2]),GetComputedValue(x[3]))
                except Exception:
                    Console.error(f'Invalid style for {element} | "{propName}" : {dic[propName]} : ',errorLevel="UI 1")
                    continue
            elif propName == 'FontSize':
                retVal.FontSize = int(GetComputedValue(dic[propName]))
            elif propName == 'Gap':
                try:
                    x = dic[propName].split(',')
                    if len(x) == 1:
                        r = GetComputedValue(x[0])
                        retVal.Gap = Vector(r,r)
                    elif len(x) == 2:
                        r1 = GetComputedValue(x[0])
                        r2 = GetComputedValue(x[1])
                        retVal.Gap = Vector(r1,r2)
                except Exception:
                    Console.error(f'Invalid style for {element} | {"{propName}" : {dic[propName]} : }')
                    continue
            elif propName == 'Padding':
                try:
                    x = dic[propName].split(',')
                    if len(x) == 1:
                        r = GetComputedValue(x[0])
                        retVal.Padding = (r,r,r,r)
                    elif len(x) == 2:
                        r1 = GetComputedValue(x[0])
                        r2 = GetComputedValue(x[1])
                        retVal.Padding = (r1,r2,r1,r2)
                    elif len(x) == 4:
                        retVal.Padding = (GetComputedValue(x[0]),GetComputedValue(x[1]),GetComputedValue(x[2]),GetComputedValue(x[3]))
                except Exception:
                    Console.error(f'Invalid style for {element} | "{propName}" : {dic[propName]} : ',errorLevel="UI 1")
                    continue
            else:
                continue
        retVal.Origin = element.Parent.ComputedStyles.TopLeft
        offset = Vector(0, 0)
        # region setOffset
        if retVal.SelfOriginType == 'Bottom':
            offset = Vector(-retVal.Size.x/2, -retVal.Size.y)
        elif retVal.SelfOriginType == 'BottomLeft':
            offset = Vector(0, -retVal.Size.y)
        elif retVal.SelfOriginType == 'BottomRight':
            offset = Vector(-retVal.Size.x, -retVal.Size.y)
        elif retVal.SelfOriginType == 'Centre':
            offset = Vector(-retVal.Size.x/2, -retVal.Size.y/2)
        elif retVal.SelfOriginType == 'Left':
            offset = Vector(0, -retVal.Size.y/2)
        elif retVal.SelfOriginType == 'Right':
            offset = Vector(-retVal.Size.x, -retVal.Size.y/2)
        elif retVal.SelfOriginType == 'Top':
            offset = Vector(-retVal.Size.x/2, 0)
        elif retVal.SelfOriginType == 'TopRight':
            offset = Vector(-retVal.Size.x, 0)
        else:
            offset = Vector(0, 0)    
        # endregion

        retVal.TopLeft = retVal.Origin + retVal.Position + offset
        
        return retVal