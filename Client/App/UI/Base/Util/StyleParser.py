from ....Core.DataTypes.Standard import Vector
from .Styles import Positions,Style
from ....Core.Diagnostics.Debugging import Console
class ComputedStyles:
    def __init__(self):
        self.Size = Vector(0, 0) # width, height
        self.Position = Vector(0, 0) # x, y
        self.Origin = Vector(0, 0) # x, y
        self.TopLeft = Vector(0, 0) # x, y
        self.FontSize = 10
        self.SelfOriginType = Positions.TopLeft # Position
        self.CornerRadius = (0, 0, 0, 0) # (topleft, topright, bottomright, bottomleft)
        self.ImagePadding = (0, 0, 0, 0) # (left, up, right, down)
        self.Visible = True


def ComputeStyles(styles, element):
    def GetUnitMultiplyer(unit):
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
    def GetComputedValue(value):
        if type(value) == float or type(value) == int:
            return value
        if type(value) == str:
            try:
                return float(value)
            except ValueError:
                try:
                    val,unit = value.split(":")
                    return float(val) * GetUnitMultiplyer(unit)
                except:
                    Console.error(f"Invalid type of value {value} on {element}")
        else:
            Console.error(f"Invalid type for value {value} on {element}")
        # If the value is faulty just return 0
        return 0

    retVal = ComputedStyles()
    dic = styles.__dict__
    for propName in Style.PriorityOrder:
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
        elif propName == 'ImagePadding':
            try:
                x = dic[propName].split(',')
                if len(x) == 1:
                    r = GetComputedValue(x[0])
                    retVal.ImagePadding = (r,r,r,r)
                elif len(x) == 4:
                    retVal.ImagePadding = (GetComputedValue(x[0]),GetComputedValue(x[1]),GetComputedValue(x[2]),GetComputedValue(x[3]))
            except Exception:
                Console.error(f'Invalid style for {element} | "{propName}" : {dic[propName]} : ',errorLevel="UI 1")
                continue
        elif propName == 'Visibile':
            retVal.Visible = dic[propName]
        else:
            continue
    retVal.Origin = element.Parent.ComputedStyles.TopLeft
    offset = Vector(0, 0)
    # region setOffset
    if retVal.SelfOriginType == Positions.Bottom:
        offset = Vector(-retVal.Size.x/2, -retVal.Size.y)
    elif retVal.SelfOriginType == Positions.BottomLeft:
        offset = Vector(0, -retVal.Size.y)
    elif retVal.SelfOriginType == Positions.BottomRight:
        offset = Vector(-retVal.Size.x, -retVal.Size.y)
    elif retVal.SelfOriginType == Positions.Centre:
        offset = Vector(-retVal.Size.x/2, -retVal.Size.y/2)
    elif retVal.SelfOriginType == Positions.Left:
        offset = Vector(0, -retVal.Size.y/2)
    elif retVal.SelfOriginType == Positions.Right:
        offset = Vector(-retVal.Size.x, -retVal.Size.y/2)
    elif retVal.SelfOriginType == Positions.Top:
        offset = Vector(-retVal.Size.x/2, 0)
    elif retVal.SelfOriginType == Positions.TopRight:
        offset = Vector(-retVal.Size.x, 0)
    else:
        offset = Vector(0, 0)    
    # endregion

    retVal.TopLeft = retVal.Origin + retVal.Position + offset
    
    return retVal