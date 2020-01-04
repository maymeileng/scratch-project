class SpriteHolder(object):
    def __init__(self,width,height):
        self.width = (width-3*height//50-2*(width//25)-width//1.6)//2+4
        self.cx = width//1.6+height//50+self.width-3
        self.height = (height-height//9-2*width//7-height//50)//2+7
        self.cy = height-self.height+10
        self.sprites = []
        
    def draw(self,canvas):
        round_rectangle(canvas,self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill="white",outline="#dbdbdb")
        for sprite in self.sprites:
            sprite.draw(canvas)
        
def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)