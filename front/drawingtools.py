def draw_rectangle_with_centre(canvas, position, size, fill="white"):
    # canvas.createRectangle takes (x1,y1,x2,y2)
    # x1,y1 and x2,y2 are the coordinates of opposite corners of the rectangle
    return canvas.create_rectangle(position.x - size.x/2, position.y + size.y/2, position.x + size.x/2, position.y - size.y/2, fill = fill)

def move_rectangle_with_centre(canvas, canvasID, position, size, fill="white"):
    canvas.moveto(canvasID, position.x - size.x/2, position.y - size.y/2)
def move_circle_with_centre(canvas, canvasID, position, radius, fill="white"):
    canvas.moveto(canvasID, position.x - radius, position.y - radius)

def moveItem(canvas, canvasID, displacement):
    canvas.move(canvasID, displacement.x,displacement.y)


def draw_circle_with_centre(canvas, position, radius, fill="white"):
    return canvas.create_oval(position.x - radius,position.y - radius,position.x+radius,position.y +radius,fill=fill)