from block import*
from PIL import ImageTk,Image,ImageDraw
class CostumeScreen(object):
    def __init__(self,sprite,width,height,costumes):
        self.sprite = sprite
        self.cx = width//10 + (width//1.6-width//10)//2
        self.cy = (height-height//50)-(height-height//50-height//9)//2
        self.width = (width//1.6-width//10)//2
        self.height = (height-height//50-height//9)//2
        self.lineHeight = (height-height//50-height//9)//2
        self.sprite.cx = self.cx
        self.sprite.cy = self.cy
        self.sprite.resize(10)
        self.button = AnotherButton(200,self.cy-self.height-20,100,20,"Costumes")
        self.x = width // 20
        self.y = (height-height//50)-(height-height//50-height//9)//2
        self.w = width // 20
        self.h = (height-height//50-height//9)//2
        self.colors = ["#f4426e","#a32745","#fca4a4","#ff8f89","#ff4f4f"]
        self.colorPicker = []
        self.color = None
        self.wheel = Button(self.cx,height//6,int(self.width*1.3),self.height//8,"scale.png")
        cy = self.cy-self.height+70
        self.costumes = []
        for costume in costumes:
            self.costumes += [SpriteButton((self.cx-self.width)//2,cy,48,69,costume.ogimg,60,width,height)]
            cy += 130
        self.costumes[0].pressed = True
    def draw(self, canvas):
        if self.button.pressed:
            round_rectangle(canvas, self.cx - self.width, self.cy - self.height+2, self.cx + self.width, self.cy + self.height,fill="white",outline="")
            round_rectangle(canvas, self.x - self.w, self.y - self.h+2, self.x + self.w, self.y + self.h,fill="white",outline="")
            canvas.create_line(self.cx-self.width,self.cy-self.lineHeight,self.cx-self.width,self.cy+self.lineHeight,fill="#dbdbdb")
            self.sprite.draw(canvas)
            self.wheel.draw(canvas)
            for costume in self.costumes:
                costume.draw(canvas)
        self.button.draw(canvas)
        
    def updateCostumes(self,costumes,width,height):
        self.costumes = []
        cy = self.cy-self.height+70
        for costume in costumes:
            self.costumes += [SpriteButton((self.cx-self.width)//2,cy,48,69,costume.ogimg,60,width,height)]
            cy += 130
        self.costumes[0].pressed = True
        
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
        