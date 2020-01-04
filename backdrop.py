from PIL import ImageTk,Image 
class Backdrop(object):
    def __init__(self,x,y,width,height,bigWidth,bigHeight,img):
        self.cx = x
        self.cy = y
        self.width = width//2
        self.height = height//2
        self.bigWidth = bigWidth//2
        self.bigHeight = bigHeight//2
        #self.color = color
        self.img = Image.open(img)
        self.tkImg = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.tkImg)
        self.pressed = False
    def draw(self,canvas,width,height,x,y):
        canvas.create_image(self.cx,self.cy,image=self.tkImg)
        #canvas.create_rectangle(self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill=self.color)
        #round_rectangle(canvas,self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill=self.color,outline="#dbdbdb",width=1)
        if self.pressed:
            #round_rectangle(canvas,x-self.bigWidth,y-self.bigHeight,x+self.bigWidth,y+self.bigHeight,fill=self.color,outline="#dbdbdb",width=1)
            self.img = self.img.resize((int(self.bigWidth), int(self.bigHeight)), Image.ANTIALIAS)
            self.tkImg = ImageTk.PhotoImage(self.img)
            canvas.create_image(x,y,image=self.tkImg)
    def isPressed(self, x, y):
        if x <= self.cx + self.width//2 and x >= self.cx-self.width//2:
            if y <= self.cy + self.height//2 and y >= self.cy - self.height//2:
                return True
        return False
        
        
class BackdropHolder(object):
    def __init__(self, width, height):
        self.width = width//25
        self.height = (height-height//9-2*width//7-height//50)//2+7
        self.cx = width - self.width - 0.05*width//4.5
        self.cy = height-self.height+10
        self.margin = self.width//15
        self.backdrops = []
        # self.x = self.cx - self.width + self.margin
        # self.y = self.cy - 
        
    def draw(self,canvas):
        round_rectangle(canvas,self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill="white", outline="#dbdbdb",width=1)
        
        
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