from PIL import ImageTk,Image 
class Sprite(object):
    def __init__(self,cx,cy,width,height,img):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.angle = 0
        self.ogimg = img
        self.img = Image.open(img)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
        self.show = True
        self.keepGoing = False
        self.direction = 1
        self.wait = False
        self.costumeNum = 0
    def draw(self,canvas):
        if self.show:
            canvas.create_image(self.cx,self.cy,image=self.tkImg)
    
    def update(self):
        self.img = Image.open(self.ogimg)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
        
    def move(self, steps):
        self.cx += steps*self.direction
        
    def flip(self):
        self.img = Image.open(self.ogimg)
        if self.direction == 1:
            self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
    
    def rotate(self,angle):
        self.angle += angle
        self.img = Image.open(self.ogimg)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.tkImg = self.img.rotate(self.angle,expand=True)
        self.tkImg = ImageTk.PhotoImage(self.tkImg)
        
    def resize(self,scale):
        scale = scale//5
        self.width *= scale
        self.height *=scale
        self.img = Image.open(self.ogimg)
        self.img = self.img.resize((self.width, self.height), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
        
        
    def isPressed(self, x, y):
        if x <= self.cx + self.width//2 and x >= self.cx-self.width//2:
            if y <= self.cy + self.height//2 and y >= self.cy - self.height//2:
                return True
        return False
        
    def inBounds(self, cx, cy, width, height):
        if self.cx + self.width//2 <= cx + width and self.cx - self.width//2 >= cx - width:
            if self.cy + self.height//2 <= cy + height and self.cy - self.height//2 >= cy - height:
                return True
        return False