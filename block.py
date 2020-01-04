from tkinter import *
from codearea import *
import pyaudio
import wave
from threading import Thread
from PIL import ImageTk,Image 
import sys
class CodeBlock(object):
    def __init__(self, cx, cy, color, text="", pressed=False):
        self.cx = cx
        self.cy = cy
        self.color = color
        self.text = text
        length = 0
        spaces = 0
        for c in self.text:
            if c != " ":
                length += 1
            else:
                spaces += 1
        numSpace = spaces // 2
        self.width = (length+1) * 8 + numSpace
        self.height = 15
        self.pressed = pressed
        self.mouseX = 0
        self.mouseY = 0
        self.shadow = False
        self.otherWidth = 0
        
    def __repr__(self):
        return "%s" %self.text
        
    def __eq__(self,other):
        return self.cx == other.cx and self.cy == other.cy and self.text == other.text
    
    def draw(self, canvas):
        if self.shadow:
            canvas.create_rectangle(self.cx,self.cy+self.height,self.cx+self.otherWidth,self.cy+self.height*3,fill="#dbdbdb",outline="")
        canvas.create_rectangle(self.cx,self.cy-self.height,self.cx+self.width,self.cy+self.height, fill=self.color, outline="")
        canvas.create_text(self.cx+5,self.cy,text = self.text, font = "Helvetica", anchor=W,fill="white")
    
    def isPressed(self, x, y):
        if x <= self.cx + self.width and x >= self.cx:
            if y <= self.cy + self.height and y >= self.cy - self.height:
                self.pressed = True
                return True
        return False
    
    def isPlaced(self, x, y, width, height):
        if self.cx >= x - width and self.cx + self.width <= x + width:
            if self.cy - self.height >= y - height and self.cy + self.height <= y + height:
                return True
        return False
        
    def isBelow(self, other):
        if other.cx+other.width >= self.cx + 15 and other.cx <= self.cx + other.width - 15:
            if other.cy-other.height >= self.cy+self.height-5 and other.cy+other.height <= self.cy + self.height*3 + 15:
                self.otherWidth = other.width
                return True
        return False
        
class DIYBlock(CodeBlock):
    def __init__(self,cx,cy,color,text,moveable,pressed=False):
        super().__init__(cx,cy,color,text,pressed)
        self.moveable = moveable

class TextBox(object):
    def __init__(self,cx,cy,width,height,color="white",default=""):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.default = default
        self.color = color
        self.text = ""
        self.cursor = self.text + "I"
        self.pressed = False
        self.show = False
        self.blink = False
        self.finalized = False
        
    def isPressed(self,x,y):
        if x <= self.cx + self.width and x >= self.cx-self.width:
            if y <= self.cy + self.height and y >= self.cy - self.height:
                return True
        return False
        
    def draw(self,canvas):
        if self.show:
            self.cursor = self.text + "I"
            canvas.create_rectangle(self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill=self.color,outline="")
            if self.finalized:
                canvas.create_text(self.cx-self.width+10,self.cy,text=self.text,font = "Helvetica 20", anchor=W)
            elif not self.pressed:
                canvas.create_text(self.cx-self.width+10,self.cy,text=self.default,font = "Helvetica 20", anchor=W,fill="#a7b2c6")
            elif self.pressed:
                canvas.create_text(self.cx-self.width+10,self.cy,text=self.text,font = "Helvetica 20", anchor=W)
                # canvas.create_text(self.cx-self.width,self.cy,text=self.cursor,font = "Helvetica 30", anchor=W)
                if self.blink:
                    canvas.create_text(self.cx-self.width+10,self.cy,text=self.cursor,font = "Helvetica 20", anchor=W)
                    #canvas.create_rectangle(self.cx-self.width+self.numSpace,self.cy-self.height,self.cx-self.width+5+self.numSpace,self.cy+self.height,fill="black")

class Button(object):
    
    def __init__(self, cx, cy, width, height,img):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.img = Image.open(img)
        self.img = self.img.resize((int(width), int(height)), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
        self.pressed = False
    
    def isPressed(self,x,y):
        if x <= self.cx + self.width//2 and x >= self.cx - self.width//2:
            if y <= self.cy + self.height//2 and y >= self.cy - self.height//2:
                return True
        return False
    
    def draw(self,canvas):
        canvas.create_image(self.cx,self.cy,image=self.tkImg)
        
class SpriteButton(Button):

    def __init__(self,cx,cy,width,height,img,boxWidth,swidth,sheight):
        self.ogimg = img
        self.codeArea = CodeArea(swidth,sheight,img)
        super().__init__(cx,cy,width,height,img)
        self.boxWidth = boxWidth
        self.show = False
        
    def __eq__(self,other):
        return self.cx == other.cx and self.cy == other.cy and self.img == other.img
    
    def update(self):
        self.img = Image.open(self.ogimg)
        self.img = self.img.resize((int(self.width), int(self.height)), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
    
    def isPressed(self,x,y):
        if x <= self.cx + self.boxWidth and x >= self.cx - self.boxWidth:
            if y <= self.cy + self.boxWidth and y >= self.cy - self.boxWidth:
                return True
        return False
        
    def draw(self,canvas):
        if self.pressed:
            round_rectangle(canvas,self.cx-self.boxWidth,self.cy-self.boxWidth,self.cx+self.boxWidth,self.cy+self.boxWidth,fill="white",outline="#4D97FE",width=3)
        else:
            round_rectangle(canvas,self.cx-self.boxWidth,self.cy-self.boxWidth,self.cx+self.boxWidth,self.cy+self.boxWidth,fill="white",outline="#dbdbdb")
        canvas.create_image(self.cx,self.cy,image=self.tkImg)

class AnotherButton(object):
    def __init__(self,cx,cy,width,height,text,color="white"):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.text = text
        self.color =color
        self.pressed = False
        
    def isPressed(self, x,y):
        if x <= self.cx + self.width and x >= self.cx-self.width:
            if y <= self.cy + self.height and y >= self.cy - self.height:
                self.pressed = True
                return True
        return False
        
    def draw(self,canvas):
        if self.pressed:
            canvas.create_rectangle(self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill=self.color,outline="#dbdbdb")
            canvas.create_text(self.cx,self.cy,text = self.text, font = "Helvetica 13 bold", anchor=CENTER,fill="#4D97FE")
        else:
            canvas.create_rectangle(self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill="#c7d5ed",outline="#dbdbdb")
            canvas.create_text(self.cx,self.cy,text = self.text, font = "Helvetica 13 bold", anchor=CENTER,fill="#a7b2c6")
        
class AnotherAnotherButton(AnotherButton):
    def __init__(self,cx,cy,width,height,text,color="white"):
        super().__init__(cx,cy,width,height,text,color)
        
    def draw(self,canvas):
        canvas.create_rectangle(self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill="#4D97FE",outline="")
        canvas.create_text(self.cx,self.cy,text = self.text, font = "Helvetica 13 bold", anchor=CENTER,fill="white")
        
class AnotherAnotherAnotherButton(AnotherButton):
    def __init__(self,cx,cy,width,height,text,color="white"):
        super().__init__(cx,cy,width,height,text,color)
        
    def draw(self,canvas):
        canvas.create_rectangle(self.cx-self.width,self.cy-self.height,self.cx+self.width,self.cy+self.height,fill="#f44268",outline="")
        canvas.create_text(self.cx,self.cy,text = self.text, font = "Helvetica 13 bold", anchor=CENTER,fill="white")

class MakeButton(object):
    def __init__(self,cx,cy,color,text,pressed=False):
        self.cx = cx
        self.cy = cy
        self.color = color
        self.text = text
        self.pressed = pressed
        self.width = len(self.text) * 8
        self.height = 15
        
    def isPressed(self,x,y):
        if x <= self.cx + self.width and x >= self.cx:
            if y <= self.cy + self.height and y >= self.cy - self.height:
                self.pressed = True
                return True
        return False
    
    def draw(self,canvas):
        canvas.create_rectangle(self.cx,self.cy-self.height,self.cx+self.width,self.cy+self.height, fill=self.color, outline="")
        canvas.create_text(self.cx+5,self.cy,text = self.text, font = "Helvetica", anchor=W,fill="white")

class Window(object):
    def __init__(self,sWidth,sHeight,img):
        self.sWidth = sWidth
        self.sHeight = sHeight
        self.wx = sWidth//2
        self.wy = sHeight//2
        self.img = Image.open(img)
        self.img.putalpha(128)
        self.img = self.img.resize((sWidth, sHeight), Image.ANTIALIAS)
        self.tkImg = ImageTk.PhotoImage(self.img)
        self.wWidth = sWidth//4
        self.wHeight = sHeight//4
        self.button = AnotherAnotherAnotherButton(sWidth//2,sHeight//1.5,sWidth//30,sHeight//45,"ok")
        self.show = False
                        
    def draw(self,canvas):
        if self.show:
            #canvas.create_rectangle(0,0,self.sWidth,self.sHeight,fill="#fc8f8f",stipple="gray50")
            canvas.create_image(self.wx,self.wy,image=self.tkImg)
            canvas.create_rectangle(self.wx-self.wWidth,self.wy-self.wHeight,self.wx+self.wWidth,self.wy+self.wHeight,fill="#fc8f8f",outline="#f44268")
            self.button.draw(canvas)
    
class AudioBlock(CodeBlock):
    def __init__(self,cx,cy,color,text,pressed=False):
        super().__init__(cx,cy,color,text,pressed)

# modified from https://stackoverflow.com/questions/38302606/python-multithreading-play-multiple-sine-waves-simultaneously
class WavePlayer(Thread) :
    CHUNK = 1024
    def __init__(self,file,loop=True) :
        Thread.__init__(self)
        self.file = file
        self.loop = loop
    
    def run(self):
        wf = wave.open(self.file, 'rb')
        player = pyaudio.PyAudio()
        stream = player.open(format = player.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)
        data = wf.readframes(self.CHUNK)
        while self.loop :
            stream.write(data)
            data = wf.readframes(self.CHUNK)
        if data == b'' : 
            wf.rewind()
            data = wf.readframes(self.CHUNK)
        stream.close()
        player.terminate()
    
    def play(self) :
        self.start()
    
    def stop(self) :
        self.loop = False

class OperationalBlock(CodeBlock):
    def __init__(self, cx, cy, color, text, pressed=False):
        super().__init__(cx, cy, color, text, pressed)
        self.dy = 50
        #self.fill = False
        
    def update(self,blocks):
        if len(blocks) != 0:
            print(len(blocks))
            self.dy = 30*len(blocks)+60
        else:
            self.dy = 50
    
    def draw(self,canvas):
        super().draw(canvas)
        canvas.create_rectangle(self.cx,self.cy+self.height,self.cx+10,self.cy+self.height+self.dy,fill=self.color,outline="")
        canvas.create_rectangle(self.cx,self.cy-self.height+self.dy,self.cx+self.width,self.cy+self.height+self.dy, fill=self.color, outline="")

class InputBlock(CodeBlock):
    def __init__(self,cx,cy,color,text,input,pressed=False):
        super().__init__(cx,cy,color,text,pressed)
        self.input = input
        
    def draw(self,canvas):
        super().draw(canvas)


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