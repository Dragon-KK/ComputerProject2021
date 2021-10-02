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
    # if body['type'] == 'c':
    #     return (body['position'].x + body['radius'] <= constraints[0]) or (body['position'].x - body['radius'] >= constraints[1])
    # elif body['type'] == 'r':
    #     return (body['position'].x + (body['size'].x/2) <= constraints[0]) or (body['position'].x - (body['size'].x/2) >= constraints[1]) or ()
    # else:
    #     raise RuntimeError("Physics Error : Invalid Body")
    return (body['position'].x + (body['size'].x/2) <= constraints[0]) or (body['position'].x - (body['size'].x/2) >= constraints[1])

def isCollidingVerticalWalls(body, constraints):

    # if body['type'] == 'c':
    #     return (body['position'].y - body['radius'] <= constraints[0]) or (body['position'].y + body['radius'] >= constraints[1])
    # elif body['type'] == 'r':
    #     return (body['position'].y - (body['size'].y/2) <= constraints[0]) or (body['position'].y + (body['size'].y/2) >= constraints[1]) or ()
    # else:
    #     raise RuntimeError("Physics Error : Invalid Body")
    return (body['position'].y - (body['size'].y/2) <= constraints[0]) or (body['position'].y + (body['size'].y/2) >= constraints[1])

def lookForCollisionWithPaddles(ball, p1,p2):
    
    if ball['direction'].x < 0:
        # First check if im withing the y range of the paddle
        if ball['position'].y - ball['size'].y/2 < p1['position'].y + p1['size'].y/2 and ball['position'].y + ball['size'].y/2 > p1['position'].y - p1['size'].y/2:
            # Now chekc if im in the correct x position
            if ball['position'].x - ball['size'].x/2 < p1['position'].x + p1['size'].x/2:
                return True, p1
    else:
        if ball['position'].y - ball['size'].y/2 < p2['position'].y + p2['size'].y/2 and ball['position'].y + ball['size'].y/2 > p2['position'].y - p2['size'].y/2:
            # Now chekc if im in the correct x position
            if ball['position'].x + ball['size'].x/2 > p2['position'].x - p2['size'].x/2:
                return True, p2
    return False, None