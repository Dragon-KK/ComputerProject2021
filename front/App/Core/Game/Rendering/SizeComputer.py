from ...DataTypes.Standard import Vector


def Parse(self, Object, Canvas):
    def GetUnitMultiplier(unit):
        return {
            'em' : Canvas.STYLE_UNITS['em'],
            'w%' : Canvas.ComputedStyles.Size.x / 100,
            'h%' : Canvas.ComputedStyles.Size.y / 100,
            'vw' : Canvas.Window.ViewPort.x / 100,
            'vh' : Canvas.Window.ViewPort.y / 100
        }.get(unit, 0)

    t = type(Object)
    if t == int:
        return Object
    elif t == tuple or t == list():
        return t(Parse(item) for item in Object)
    elif t == Vector:
        return Vector(Parse(Object.x), Parse(Object.y))
    elif t == str:
        value,unit = Object.split(':')
        value = float(value)
        return value * GetUnitMultiplier(unit)
