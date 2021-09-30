'''
A body is defined as:
{
    type : c | r (Circle or Rectangle)
    position : Vector,
    velocity : Vector,
    
    if c{
        radius : number
    }
    if r{
        size : Vector
    }
}
'''
def body(info, Type):
    if Type == 'c':
        return {
            'type' : 'c',
            'position' : info['position'],
            'radius' : info['radius']            
        }
    elif Type == 'r':
        return {
            'type' : 'r',
            'position' : info['position'],
            'size' : info['size']
        }
def hasCrossedHorizontalWalls(body, constraints):
    if body['type'] == 'c':
        return (body['position'].x + body['radius'] <= constraints[0]) or (body['position'].x - body['radius'] >= constraints[1])
    elif body['type'] == 'r':
        return (body['position'].x + (body['size'].x/2) <= constraints[0]) or (body['position'].x - (body['size'].x/2) >= constraints[1]) or ()
    else:
        raise RuntimeError("Physics Error : Invalid Body")

def isCollidingVerticalWalls(body, constraints):

    if body['type'] == 'c':
        return (body['position'].y - body['radius'] <= constraints[0]) or (body['position'].y + body['radius'] >= constraints[1])
    elif body['type'] == 'r':
        return (body['position'].y - (body['size'].y/2) <= constraints[0]) or (body['position'].y + (body['size'].y/2) >= constraints[1]) or ()
    else:
        raise RuntimeError("Physics Error : Invalid Body")
    

