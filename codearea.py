from PIL import ImageTk,Image 
class CodeArea(object):
    def __init__(self, width, height,img):
        self.cx = width // 2.36
        self.cy = (height-height//50)-(height-height//50-height//9)//2
        self.width = width // 5
        self.height = (height-height//50-height//9)//2
        self.lineHeight = (height-height//50-height//9)//2
        self.placedBlocks = []
        self.img = Image.open(img)
        #self.img.putalpha(128)
        self.img = self.img.resize((40, 60), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
        
    def draw(self, canvas):
        round_rectangle(canvas, self.cx - self.width, self.cy - self.height+2, self.cx + self.width, self.cy + self.height,fill="white",outline="")
        canvas.create_line(self.cx-self.width,self.cy-self.lineHeight,self.cx-self.width,self.cy+self.lineHeight,fill="#dbdbdb")
        canvas.create_image(self.cx+self.width-25,self.cy-self.height+38,image=self.tkImg)
        #canvas.create_rectangle(self.cx - self.width, self.cy - self.height, self.cx + self.width, self.cy + self.height, fill="white")
        # for blockGroup in self.placedBlocks:
        #     for index in range(len(self.placedBlocks)-1,-1,-1):
        #         print(blockGroup[index])
        #         blockGroup[index].draw(canvas)
        for blockGroup in self.placedBlocks:
            for block in blockGroup:
                block.draw(canvas)

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