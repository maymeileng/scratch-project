from block import*

class CodeHolder(object):
    def __init__(self, width, height):
        self.cx = width // 2.36-width//5-width//12
        self.cy = (height-height//50)-(height-height//50-height//9)//2
        self.width = width // 12
        self.height = (height-height//50-height//9)//2
        self.allBlocks = []
        self.text = "Motion"
        self.blockcx = width//16
        cy = self.cy-self.height + 60
        self.organizer = Organizer(width,height)
        self.allBlocks += [CodeBlock(self.blockcx, cy, "#f45f42", "move 10 steps")]
        self.allBlocks += [CodeBlock(self.blockcx, cy+50, "#f45f42", "rotate 15 degrees")]
        self.allBlocks += [CodeBlock(self.blockcx, cy+100, "#f45f42", "go to random position")]
        self.show = False
        self.button = None
        self.DIYbuttons = []
        self.titleButton = AnotherButton(50,self.cy-self.height-20,50,20,"Code")
        self.titleButton.pressed = True
        
    def update(self):
        cy = self.cy-self.height + 60
        self.allBlocks = []
        self.show = False
        for type in self.organizer.types:
            if type[2]:
                name = type[0]
                color = type[1]
                self.text = name
                if name == "Motion":
                    self.allBlocks += [CodeBlock(self.blockcx, cy, color, "move 10 steps")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+50, color, "rotate 15 degrees")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+100, color, "go to random position")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+150, color, "if on edge, bounce")]
                elif name == "Looks":
                    self.allBlocks += [CodeBlock(self.blockcx, cy, color, "change size by 10")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+50, color, "show")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+100, color, "hide")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+150, color, "next costume")]
                elif name == "Sound":
                    self.allBlocks += [AudioBlock(self.blockcx, cy, color, "start sound")]
                    self.allBlocks += [AudioBlock(self.blockcx, cy+50, color, "stop sound")]
                elif name == "Events":
                    self.allBlocks += [CodeBlock(self.blockcx, cy, color, "when play clicked")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+50, color, "when this sprite clicked")]
                    self.allBlocks += [CodeBlock(self.blockcx, cy+100, color, "when space key pressed")]
                elif name == "Control":
                    self.allBlocks += [CodeBlock(self.blockcx, cy, color, "wait 1 seconds")]
                    self.allBlocks += [OperationalBlock(self.blockcx, cy + 50, color, "forever")]
                    #self.allBlocks += [OperationalBlock(self.blockcx, cy+150, color, "if___then")]
                elif name == "My Blocks": 
                    self.show = True
                    self.button = MakeButton(self.blockcx,cy,color,"Make a Block")
        
    def draw(self, canvas):
        self.titleButton.draw(canvas)
        #round_rectangle(canvas, self.cx - self.width, self.cy - self.height, self.cx + self.width, self.cy + self.height, fill="white",outline="#eaeaea",width=1)
        if self.titleButton.pressed:
            canvas.create_rectangle(self.cx - self.width, self.cy - self.height+1, self.cx + self.width, self.cy + self.height, fill="white",outline="")
            canvas.create_text(self.cx-self.width+11,self.cy-self.height+20,text=self.text,font="Helvetica 13 bold",anchor=W)
            for block in self.allBlocks:
                block.draw(canvas)
            if self.show:
                self.button.draw(canvas)
                for block in self.DIYbuttons:
                    block.draw(canvas)
            self.organizer.draw(canvas)
        
class Organizer(object):
    def __init__(self,width,height):
        self.cy = (height-height//50)-(height-height//50-height//9)//2
        self.width = (width // 2.36-width//5-width//12-width // 12)//2
        self.cx = self.width
        self.r = self.width//2.5
        self.height = height//25
        self.rHeight = height
        self.lineHeight = (height-height//50-height//9)//2
        self.types = [["Motion","#f45f42",True],["Looks","#f4d341",False],["Sound","#c1f43f",False],["Events","#7a80f4",False],["Control","#945fc6",False],["My Blocks","#fc8f8f",False]]
        
    def isPressed(self,x,y):
        if x <= self.cx+self.width and x >= self.cx-self.width:
            if y<= self.cy+self.lineHeight and y>= self.cy-self.lineHeight:
                y = y - self.rHeight//9
                index = y//(self.height*2)
                if index < len(self.types):
                    for type in self.types:
                        if type[2]:
                            type[2] = False
                    self.types[index][2] = True
                    return True
        return False
    
    def draw(self,canvas):
        canvas.create_rectangle(self.cx - self.width, self.cy - self.lineHeight, self.cx + self.width, self.cy + self.lineHeight, fill="white",outline="#dbdbdb")
        #canvas.create_line(self.cx + self.width,self.cy-self.lineHeight,self.cx+self.width,self.cy+self.lineHeight,fill="#dbdbdb")
        count = 0
        cy = self.cy-self.lineHeight+self.height-7
        for type in self.types:
            if type[2]:
                canvas.create_rectangle(self.cx-self.width,self.cy-self.lineHeight+self.height*2*(count),self.cx+self.width,self.cy-self.lineHeight+self.height*2*(count+1),fill="#ededed",outline="")
            canvas.create_oval(self.cx-self.r,cy-self.r,self.cx+self.r,cy+self.r,fill=type[1],outline="")
            canvas.create_text(self.cx,cy+self.r+2,text=type[0],font="Helvetica",anchor=N)
            count += 1
            cy += self.height*2
        