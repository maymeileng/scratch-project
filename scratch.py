from tkinter import *
import module_manager
module_manager.review()
from block import*
from backdrop import*
import time
from codeholder import *
from codearea import CodeArea
from sprite import Sprite
import copy
import pickle
from PIL import ImageTk,Image 
import random
import pyaudio
import wave
from threading import Thread
import sys
import string
from costume import*
from spriteholder import *
import os
####################################
# Customize any of these functions:
####################################

class Animate(object):
    def __init__(self, width, height):
        self.cx = (width-width//1.6)//2 + width//1.6
        self.cy = width//7+height//9
        self.width = width//5.6
        self.height = width//7
    
    def draw(self, canvas):
        round_rectangle(canvas, self.cx-self.width, self.cy-self.height, self.cx+self.width, self.cy + self.height,fill="white",outline="#dbdbdb",width=1)
    
        
def init(data):
    data.login = True 
    data.users = dict()
    data.currUser = None
    data.filename = "users"
    data.nameBox = TextBox(data.width//2,data.height//3+2*data.height//40-15,data.width//7,data.height//40,"white","enter username")
    data.nameBox.show = True
    data.password = TextBox(data.width//2,data.height//3+5*data.height//40+15,data.width//7,data.height//40,"white","enter password")
    data.password.show = True
    data.codeHolder = CodeHolder(data.width, data.height)
    data.blocks = []
    data.appear = False
    data.animate = Animate(data.width, data.height)
    data.sprite = None
    data.codeArea = None
    data.sprites = []
    data.sprites.append([Sprite(data.animate.cx,data.animate.cy,90,130,"trash.png")])
    data.sprites[0].append(Sprite(data.animate.cx,data.animate.cy,90,130,"trash2.png"))
    data.sprites.append([Sprite(data.animate.cx,data.animate.cy,100,155,"can1.png")])
    data.sprites[1].append(Sprite(data.animate.cx,data.animate.cy,100,155,"can2.png"))
    data.sprites[1].append(Sprite(data.animate.cx,data.animate.cy,100,155,"can3.png"))
    data.playButton = Button(data.width//1.58+17.5,data.height//10-20,40,40,"flag.png")
    data.stopButton = Button(data.width//1.58+55,data.height//10-20,35.5,36.5,"stop.png")
    data.logo = Button(50,20,71,29,"logo.png")
    data.movingBlocks = []
    data.backdropHolder = BackdropHolder(data.width,data.height)
    data.w = None
    data.count = 0
    data.pressed = 0
    data.clicked = 0
    data.counter = 0
    data.textbox = TextBox(data.width//2,data.height//3,data.width//5,data.height//35)
    data.window = Window(data.width,data.height,"pink.png")
    data.rgbIm = None
    data.backdrops = ["rainforest.png"]
    data.backdrops = []
    data.cy = data.codeHolder.cy-data.codeHolder.height + 60 + 50
    data.spriteHolder = SpriteHolder(data.width,data.height)
    cx = data.spriteHolder.width//4+data.spriteHolder.cx-data.spriteHolder.width+7
    for sprites in data.sprites:
        data.spriteHolder.sprites += [SpriteButton(cx,data.spriteHolder.cy-data.spriteHolder.height+data.spriteHolder.width//4+7,sprites[0].width//2.5,sprites[0].height//2.5,sprites[0].ogimg,data.spriteHolder.width//4,data.width,data.height)]
        cx += data.spriteHolder.width//2 + 7
    data.spriteHolder.sprites[0].pressed = True
    data.newSprite = copy.copy(data.sprites[0][0])
    data.costume = CostumeScreen(data.newSprite,data.width,data.height,data.sprites[0])
    data.costume.sprite.ogimg = data.sprites[0][0].ogimg
    data.costume.sprite.update()
    data.myBlocks = None
    data.moreBlocks = None
    data.name = "new.png"
    data.nameNum = 0
    data.saveButton = AnotherAnotherButton(data.width-30,20,25,20,"Save")
    data.fill = False
def getNums(command):
    result = ""
    for c in command:
        if c.isdigit():
            result += c
    return int(result)

def translate(event, data):
    for i in range(len(data.sprites)):
        for blockGroup in data.spriteHolder.sprites[i].codeArea.placedBlocks:
            if "when" in str(blockGroup[0]) and len(blockGroup)>1:
                for block in blockGroup:
                    if "play clicked" in str(block):
                        index = data.sprites[i][0].costumeNum
                        translateMore(data, blockGroup[1:],data.sprites[i][index])

def translateMore(data, blockGroup,sprite):
    count = 0
    for block in blockGroup:
        if type(block) == AudioBlock:
            count += 1
    for block in blockGroup:
        if "move" in str(block) and "steps" in str(block):
            if sprite.inBounds(data.animate.cx, data.animate.cy, data.animate.width, data.animate.height):
                sprite.move(getNums(str(block)))
        if "random position" in str(block):
            sprite.cx = random.randint(data.animate.cx-data.animate.width+sprite.width//2,data.animate.cx+data.animate.width-sprite.width//2)
            sprite.cy = random.randint(data.animate.cy-data.animate.height+sprite.height//2,data.animate.cy+data.animate.height-sprite.height//2)
        if "rotate" in str(block):
            if sprite.inBounds(data.animate.cx, data.animate.cy, data.animate.width, data.animate.height):
                sprite.rotate(getNums(str(block)))
        if "size" in str(block):
            #if sprite.inBounds(data.animate.cx, data.animate.cy, data.animate.width*getNums(str(block))//5, data.animate.height*getNums(str(block))//5):
            if sprite.height < data.animate.height:
                sprite.resize(getNums(str(block)))
        if "show" in str(block):
            sprite.show = True
        if "hide" in str(block):
            sprite.show = False
        if "forever" in str(block):
            sprite.keepGoing = True
            data.myBlocks = blockGroup[1:]
        if "if on edge" in str(block):
            steps = 0
            for block in data.myBlocks:
                if "move 10 steps" in str(block):
                    steps += 10
            if sprite.direction == 1:
                if not sprite.inBounds(data.animate.cx-steps, data.animate.cy, data.animate.width, data.animate.height):
                    sprite.flip()
                    sprite.direction *= -1
            elif sprite.direction  == -1:
                if not sprite.inBounds(data.animate.cx+steps, data.animate.cy, data.animate.width, data.animate.height):
                    sprite.flip()
                    sprite.direction *= -1
        if "wait 1 seconds" in str(block):
            data.counter = 0
            index = blockGroup.index(block)
            sprite.wait = True
            data.moreBlocks = blockGroup[index+1:]
            break
        if "next costume" in str(block):
            for sprites in data.sprites:
                if sprite in sprites:
                    if sprites[0].costumeNum == len(sprites)-1:
                        sprites[0].costumeNum = 0
                    else:
                        sprites[0].costumeNum += 1
        if type(block) == AudioBlock:
            if "start" in str(block):
                data.w = WavePlayer("goldlink.wav")
                data.w.play()
            if "stop" in str(block):
                data.w.stop()
        if type(block) == DIYBlock:
            for blockGroup in data.codeArea.placedBlocks:
                if str(blockGroup[0]) == str(block):
                    translateMore(data,blockGroup[1:],sprite) 
            
def mousePressed(event, data):
    if data.login:
        if data.nameBox.isPressed(event.x,event.y):
            data.nameBox.pressed = True
            data.password.pressed = False
            data.nameBox.finalized = False
            if data.password.text != "":
                data.password.finalized = True
        if data.password.isPressed(event.x,event.y):
            data.nameBox.pressed = False
            data.password.pressed = True
            data.password.finalized = False
            if data.nameBox.text != "":
                data.nameBox.finalized = True
    if not data.login:
        if data.saveButton.isPressed(event.x,event.y):
            savedDict = dict()
            # placedBlocks = None
            # images = None 
            for i in range(len(data.spriteHolder.sprites)):
                placedBlocks = data.spriteHolder.sprites[i].codeArea.placedBlocks
                spritetype = data.sprites[i]
                images = []
                for sprite in spritetype:
                    images += [sprite.ogimg]
                print("placedblocks",placedBlocks)
                print("images",images)
                savedDict[i] = (placedBlocks,images)
            try:
                data.userDict[data.currUser] = savedDict
            except:
                print("NO ENTER")
                data.userDict = dict()
                data.userDict[data.currUser] = savedDict
            outfile = open("save","wb")
            pickle.dump(data.userDict,outfile)
            outfile.close()
            print("END")
        #if data.logo.isPressed(event.x,event.y):
            # infile = open("save","rb")
            # myDict = pickle.load(infile)
            # infile.close()
            # for key in myDict:
            #     data.spriteHolder.sprites[key].codeArea.placedBlocks = myDict[key]
        for sprite in data.spriteHolder.sprites:
            if sprite.isPressed(event.x,event.y):
                sprite.pressed = True
                index = data.spriteHolder.sprites.index(sprite)
                index2 = data.sprites[index][0].costumeNum
                data.sprite = data.sprites[index][index2]
                data.codeArea = sprite.codeArea
                data.costume.updateCostumes(data.sprites[index],data.width,data.height)
                if data.costume.button.pressed: 
                    data.costume.button.pressed = True
                for otherSprite in data.spriteHolder.sprites:
                    if otherSprite != sprite:
                        otherSprite.pressed = False
            if sprite.pressed:
                index = data.spriteHolder.sprites.index(sprite)
                index2 = data.sprites[index][0].costumeNum
                data.sprite = data.sprites[index][index2]
                data.codeArea = sprite.codeArea
                #data.costume.updateCostumes(data.sprites[index],data.width,data.height)
                # data.costume.sprite.ogimg = sprite.ogimg
                # data.costume.sprite.update()
                # data.costume.updateCostumes(data.sprites[index],data.width,data.height)
                if data.costume.button.pressed:
                    for costume in data.costume.costumes:
                        if costume.isPressed(event.x,event.y):
                            costume.pressed = True
                            for otherCostume in data.costume.costumes:
                                if costume != otherCostume:
                                    otherCostume.pressed = False
                        if costume.pressed:
                            data.costume.sprite.ogimg = costume.ogimg
                            data.costume.sprite.update()
        if not data.costume.button.pressed:
            if data.codeHolder.show:
                for block in data.codeHolder.DIYbuttons:
                    if block.isPressed(event.x,event.y):
                        data.appear = True
                        data.blocks += [DIYBlock(block.cx,block.cy,block.color,block.text,True)]
            for block in data.codeHolder.allBlocks:
                if block.isPressed(event.x,event.y):
                    data.appear = True
                    if type(block) == OperationalBlock:
                        data.blocks += [OperationalBlock(block.cx,block.cy,block.color,block.text,True)]
                    elif type(block) == AudioBlock:
                        data.blocks += [AudioBlock(block.cx,block.cy,block.color,block.text,True)]
                    elif type(block) == DIYBlock:
                        data.blocks += [DIYBlock(block.cx,block.cy,block.color,block.text,True)]
                    else:
                        data.blocks += [CodeBlock(block.cx, block.cy, block.color, block.text, True)]
                    if len(data.blocks) != 0:
                        data.blocks[0].mouseX = event.x - block.cx
                        data.blocks[0].mouseY = event.y - block.cy
            updatedBlocks = copy.deepcopy(data.codeArea.placedBlocks)
            for blockGroup in data.codeArea.placedBlocks:
                if len(blockGroup) == 1:
                    for block in blockGroup:
                        if block.isPressed(event.x,event.y):
                            print("block",block)
                            data.appear = True
                            data.blocks += [block]
                            print("group",blockGroup)
                            print(updatedBlocks.index(blockGroup))
                            data.blocks[-1].mouseX = event.x - block.cx
                            data.blocks[-1].mouseY = event.y - block.cy
                            updatedBlocks.remove(blockGroup)
                    print("data.blocks",data.blocks)
                    if len(data.blocks) > 1:
                        updatedBlocks.append([data.blocks[0]])
                        data.blocks = data.blocks[1:]
                elif blockGroup[0].isPressed(event.x, event.y):
                    for block in blockGroup:
                        data.blocks += [block]
                    data.appear = True
                    for block in data.blocks:
                        block.mouseX = event.x - block.cx
                        block.mouseY = event.y - block.cy
                    updatedBlocks.remove(blockGroup)
                else:
                    if blockGroup in updatedBlocks:
                        index1 = updatedBlocks.index(blockGroup)
                        for block in blockGroup:
                            if block.isPressed(event.x,event.y):
                                if blockGroup.index(block) == len(blockGroup)-1:
                                    data.appear = True
                                    data.blocks += [block]
                                    data.blocks[0].mouseX = event.x - block.cx
                                    data.blocks[0].mouseY = event.y - block.cy
                                    updatedBlocks[index1].remove(block)
                                else:
                                    index2 = blockGroup.index(block)
                                    updatedBlocks.append(blockGroup[0:index2])
                                    updatedBlocks.append(blockGroup[index2+1:len(blockGroup)])
                                    updatedBlocks.remove(blockGroup)
                                    data.appear = True
                                    data.blocks += [blockGroup[index2]]
                                    data.blocks[0].shadow = False
                                    data.blocks[0].mouseX = event.x - block.cx
                                    data.blocks[0].mouseY = event.y - block.cy
            data.codeArea.placedBlocks = updatedBlocks
            print(data.codeArea.placedBlocks)
            if data.codeHolder.button != None and data.codeHolder.show and data.codeHolder.button.isPressed(event.x,event.y):
                data.codeHolder.button.pressed = False
                data.window.show = True
                data.textbox.show = True
                data.textbox.default = "enter block name"
            if data.textbox.isPressed(event.x,event.y):
                data.textbox.pressed = True
            if data.window.button.isPressed(event.x,event.y):
                data.window.button.pressed = True
        if data.playButton.isPressed(event.x,event.y):
            for sprites in data.sprites:
                for sprite in sprites:
                    data.sprite.keepGoing = False
                    data.sprite.wait = False
            data.count += 1
            if data.w != None and data.count > 1:
                data.w.stop()
            data.playButton.pressed = True
            translate(event, data)
        if data.stopButton.isPressed(event.x,event.y):
            if data.w != None:
                data.w.stop()
            data.playButton.pressed = False
        if data.playButton.pressed:
            for i in range(len(data.sprites)):
                for blockGroup in data.spriteHolder.sprites[i].codeArea.placedBlocks:
                    if blockGroup[0].text == "when this sprite clicked" and len(blockGroup) > 1:
                        index = data.sprites[i][0].costumeNum
                        if data.sprites[i][index].isPressed(event.x,event.y):
                            data.clicked += 1
                            if audioIn(blockGroup) and data.w != None and data.clicked > 1:
                                data.w.stop()
                            translateMore(data,blockGroup[1:],data.sprites[i][index])
        for backdrop in data.backdropHolder.backdrops:
            if backdrop.isPressed(event.x,event.y):
                backdrop.pressed = True
        if data.window.button.pressed:
            data.window.show = False
            data.textbox.show = False
            data.window.button.pressed = False
            data.codeHolder.DIYbuttons += [DIYBlock(data.width//16, data.cy, "#fc8f8f",data.textbox.text,True)]
            data.codeArea.placedBlocks.append([DIYBlock(data.width//4.3,data.height//7,"#fc8f8f",data.textbox.text,False)])
            data.cy += 50
            data.textbox.text = ""
        if data.costume.button.isPressed(event.x,event.y):
            data.costume.button.pressed = True
            data.codeHolder.titleButton.pressed = False
        if data.costume.button.pressed:
            if data.codeHolder.titleButton.isPressed(event.x,event.y):
                data.costume.button.pressed = False
            if data.costume.wheel.isPressed(event.x,event.y):
                x = event.x -abs((data.costume.wheel.cx-data.costume.wheel.width//2))
                y = event.y - (data.costume.wheel.cy-data.costume.wheel.height//2)
                r,g,b,a = data.costume.wheel.img.getpixel((x,y))
                data.rgb1 = (r,g,b,a)
            if data.costume.sprite.isPressed(event.x,event.y) and data.costume.colorPicker!=None:
                for i in range(len(data.spriteHolder.sprites)):
                    if data.spriteHolder.sprites[i].pressed and i == 0:
                        data.name = "new"
                        break
                    else:
                        data.name = "newer"
                for i in range(len(data.costume.costumes)):
                    if data.costume.costumes[i].pressed:
                        data.nameNum = i
                data.name += str(data.nameNum) + ".png"
                print(data.name)
                floodfill(data,event.x,event.y,data.rgb1)
                data.costume.sprite.ogimg = data.name
                data.costume.sprite.update()
                for i in range(len(data.costume.costumes)):
                    if data.costume.costumes[i].pressed and i == 0:
                        data.costume.costumes[i].ogimg = data.name
                        data.costume.costumes[i].update()
                        for spritebutton in data.spriteHolder.sprites:
                            if spritebutton.pressed:
                                spritebutton.ogimg = data.name
                                spritebutton.update()
                                index = data.spriteHolder.sprites.index(spritebutton)
                                data.sprites[index][i].ogimg = data.name
                                data.sprites[index][i].update()
                    elif data.costume.costumes[i].pressed:
                        data.costume.costumes[i].ogimg = data.name
                        data.costume.costumes[i].update()
                        for spritebutton in data.spriteHolder.sprites:
                            if spritebutton.pressed:
                                index = data.spriteHolder.sprites.index(spritebutton)
                                data.sprites[index][i].ogimg = data.name
                                data.sprites[index][i].update()
        if data.codeHolder.organizer.isPressed(event.x,event.y):
            data.codeHolder.update()

def floodfill(data,x,y,rgb1):
    data.rgbIm = data.costume.sprite.img
    x = x - (data.costume.sprite.cx-data.costume.sprite.width//2)
    y = y - (data.costume.sprite.cy-data.costume.sprite.height//2)
    r, g, b, a = data.rgbIm.getpixel((x,y))
    rgb2 = (r,g,b,a)
    visited = set()
    data.rgbIm = floodfillWrapper(data,x,y,rgb1,rgb2,visited)
    
sys.setrecursionlimit(600000)

# modified from 112 website
def floodfillWrapper(data,x,y,rgb1,rgb2,visited):
    if x<=1 or y<=1 or x>=180 or y >=260:
        data.rgbIm.save(data.name)
        return 
    elif (x,y) in visited:
        return
    r,g,b,a = data.rgbIm.getpixel((x,y))
    r2,g2,b2,a2=rgb2
    if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
        data.rgbIm.putpixel((int(x),int(y)),rgb1)
        if not (x-1,y) in visited:
            r,g,b,a=data.rgbIm.getpixel((x-1,y))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x)-1,int(y)),rgb1)
        if not (x,y-1) in visited:
            r,g,b,a=data.rgbIm.getpixel((x,y-1))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x),int(y)-1),rgb1)
        if not (x+1,y) in visited:
            r,g,b,a=data.rgbIm.getpixel((x+1,y))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x)+1,int(y)),rgb1)
        if not (x,y+1) in visited:
            r,g,b,a=data.rgbIm.getpixel((x,y+1))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x),int(y)+1),rgb1)
        if not (x-1,y-1) in visited:
            r,g,b,a=data.rgbIm.getpixel((x-1,y-1))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x)-1,int(y)-1),rgb1)
        if not (x+1,y+1) in visited:
            r,g,b,a=data.rgbIm.getpixel((x+1,y+1))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x)+1,int(y)+1),rgb1)
        if not (x-1,y+1) in visited: 
            r,g,b,a=data.rgbIm.getpixel((x-1,y+1))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x)-1,int(y)+1),rgb1)
        if not (x+1,y-1) in visited:
            r,g,b,a=data.rgbIm.getpixel((x+1,y-1))
            if abs(r-r2) < 20 and abs(g-g2) < 20 and abs(b-b2) < 20 and abs(a-a2) < 20:
                data.rgbIm.putpixel((int(x)+1,int(y)-1),rgb1)
        visited.add((x,y))
        visited.add((x-1,y-1))
        visited.add((x-1,y))
        visited.add((x+1,y))
        visited.add((x-1,y+1))
        visited.add((x+1,y+1))
        visited.add((x,y-1))
        visited.add((x,y+1))
        visited.add((x+1,y-1))
        data.rgbIm.save(data.name)
    else:
        visited.add((x,y))
        return 
    floodfillWrapper(data,x-2,y,rgb1,rgb2,visited)
    floodfillWrapper(data,x+2,y,rgb1,rgb2,visited)
    floodfillWrapper(data,x,y-2,rgb1,rgb2,visited)
    floodfillWrapper(data,x,y+2,rgb1,rgb2,visited)

def mouseDragged(event, data):
    for movingBlock in data.blocks:
        movingBlock.cx = -movingBlock.mouseX + event.x
        movingBlock.cy = -movingBlock.mouseY + event.y
        for blockGroup in data.codeArea.placedBlocks:
            if blockGroup[-1].isBelow(movingBlock):
                blockGroup[-1].shadow = True
            else:
                blockGroup[-1].shadow = False
            
def mouseReleased(event, data):
    if data.appear:
        if len(data.blocks) > 1 and data.blocks[0].pressed:
            if data.blocks[0].isPlaced(data.codeArea.cx, data.codeArea.cy, data.codeArea.width, data.codeArea.height):
                data.codeArea.placedBlocks += [data.blocks]
        if not (len(data.blocks) > 1 and data.blocks[0].pressed):
            for blockGroup in data.codeArea.placedBlocks:
                index = data.codeArea.placedBlocks.index(blockGroup)
                updatedBlocks = []
                data.appear = False    
                if len(data.blocks) != 0:
                    newBlocks = copy.copy(data.blocks)
                    for movingBlock in data.blocks:
                        if blockGroup[-1].isBelow(movingBlock):
                            # if data.fill:
                            #     print("here")
                            #     for blockGroup in data.codeArea.placedBlocks:
                            #         for block in blockGroup:
                            #             if type(block) == OperationalBlock:
                            #                 index = blockGroup.index(block)
                            #                 block.update(blockGroup[index+1:])
                            if type(blockGroup[-1]) == OperationalBlock:
                                movingBlock.cx = blockGroup[-1].cx + 10
                                movingBlock.cy = blockGroup[-1].cy+movingBlock.height*2
                                blockGroup[-1].dy += 10
                                # data.fill = True
                            else:
                                movingBlock.cx = blockGroup[-1].cx
                                movingBlock.cy = blockGroup[-1].cy+movingBlock.height*2
                            blockGroup[-1].shadow = False
                            movingBlock.pressed = False
                            blockGroup+=[movingBlock]
                            newBlocks.remove(movingBlock)
                            break
                        elif index == len(data.codeArea.placedBlocks) - 1 and movingBlock.isPlaced(data.codeArea.cx, data.codeArea.cy, data.codeArea.width, data.codeArea.height):
                            updatedBlocks.append([movingBlock])
                            movingBlock.pressed = False
                            newBlocks.remove(movingBlock)
                    data.blocks = newBlocks
                    for block in updatedBlocks:
                        data.codeArea.placedBlocks.append(block)
                        updatedBlocks = []
            if data.blocks != [] and len(data.codeArea.placedBlocks) == 0 and data.blocks[0].isPlaced(data.codeArea.cx, data.codeArea.cy, data.codeArea.width, data.codeArea.height):
                data.codeArea.placedBlocks.append([data.blocks[0]])
        updatedBlocks = copy.deepcopy(data.codeArea.placedBlocks)
        for blockGroup in data.codeArea.placedBlocks:
            if blockGroup == []:
                updatedBlocks.remove(blockGroup)
        data.codeArea.placedBlocks = updatedBlocks
        print(data.codeArea.placedBlocks)
    data.blocks = []
def mouseMoved(event, data): pass   
def keyPressed(event, data): 
    if data.playButton.pressed:
        for i in range(len(data.sprites)):
            for blockGroup in data.spriteHolder.sprites[i].codeArea.placedBlocks:
                if blockGroup[0].text == "when space key pressed" and len(blockGroup) > 1:
                    if event.keysym == "space":
                        data.pressed += 1
                        if audioIn(blockGroup) and data.w != None and data.pressed > 1:
                            data.w.stop()
                        index2 = data.sprites[i][0].costumeNum
                        translateMore(data,blockGroup[1:],data.sprites[i][index2])
    if data.textbox.pressed:
        if event.keysym in string.ascii_letters:
            data.textbox.text += event.keysym
        elif event.keysym == "space":
            data.textbox.text += " "
        elif event.keysym == "BackSpace":
            data.textbox.text = data.textbox.text[:-1]
    if data.nameBox.pressed:
        if event.keysym in string.ascii_letters:
            data.nameBox.text += event.keysym
        elif event.keysym == "space":
            data.nameBox.text += " "
        elif event.keysym == "BackSpace":
            data.nameBox.text = data.nameBox.text[:-1]
        elif event.keysym == "Return":
            data.nameBox.pressed = False
            data.nameBox.finalized = True
            data.password.pressed = True
    if data.password.pressed:
        if event.keysym in string.ascii_letters:
            data.password.text += event.keysym
        elif event.keysym == "space":
            data.password.text += " "
        elif event.keysym == "BackSpace":
            data.password.text = data.password.text[:-1]
        if event.keysym == "Return" and data.password.text!="":
            data.currUser = data.nameBox.text
            try:
                infile = open(data.filename,"rb")
                data.users = pickle.load(infile)
                print(data.users)
                infile.close()
                if data.nameBox.text in data.users:
                    if data.users[data.nameBox.text] == data.password.text:
                        infile = open("save","rb")
                        data.userDict = pickle.load(infile)
                        print(data.userDict)
                        infile.close()
                        oldDict = data.userDict[data.currUser]
                        for key in oldDict:
                            data.spriteHolder.sprites[key].codeArea.placedBlocks = oldDict[key][0]
                            data.spriteHolder.sprites[key].ogimg = oldDict[key][1][0]
                            data.spriteHolder.sprites[key].update()
                            for i in range(len(data.sprites[key])):
                                data.sprites[key][i].ogimg = oldDict[key][1][i]
                                #data.costume.costumes[key][i].ogimg = data.sprites[key][i].ogimg
                                #data.costume.costumes[key][i].update()
                                data.sprites[key][i].update()
                        for i in range(len(data.sprites)-1,-1,-1):
                            data.costume.updateCostumes(data.sprites[i],data.width,data.height)
                            #for costume in data.costumes:
                                
                                # if "new" in oldDict[key][1][i]:
                                #     data.costume.costumes[key][i].ogimg = data.sprites[key][i].ogimg
                                #     data.costume.costumes[key][i].update()
                                #     #print("hello")
                        data.login = False
                elif data.nameBox.text not in data.users:
                    data.users[data.nameBox.text] = data.password.text
                    infile = open("save","rb")
                    data.userDict = pickle.load(infile)
                    infile.close()
                    data.login = False
                data.filename = "users"
                outfile = open(data.filename,"wb")
                pickle.dump(data.users,outfile)
                outfile.close()
            except:
                print('NO ENTER!!!')
                if data.nameBox.text in data.users:
                    if data.users[data.nameBox.text] == data.password.text:
                        data.login = False
                if data.nameBox.text not in data.users:
                    data.users[data.nameBox.text] = data.password.text
                    data.login = False
                data.filename = "users"
                outfile = open(data.filename,"wb")
                pickle.dump(data.users,outfile)
                outfile.close()
            
def audioIn(blocks):
    for block in blocks:
        if "sound" in str(block):
            return True
    return False
            
def timerFired(data): 
    data.counter += 1
    if data.counter % 4 == 0:
        data.textbox.blink = not data.textbox.blink
        data.nameBox.blink = not data.nameBox.blink
        data.password.blink = not data.password.blink
    if data.playButton.pressed:
        for sprites in data.sprites:
            index = sprites[0].costumeNum
            sprite = sprites[index]
            if sprite.wait and sprite.keepGoing:
                if data.counter % 10 == 0:
                    sprite.wait = False
                    print("moreBlocks",data.moreBlocks)
                    if len(data.moreBlocks) == 0:
                        data.moreBlocks = data.myBlocks
                    translateMore(data,data.moreBlocks,sprite)
            elif sprite.keepGoing:
                print("myBlocks",data.myBlocks)
                translateMore(data,data.myBlocks,sprite)
            elif sprite.wait:
                if data.counter % 10 == 0:
                    sprite.wait = False
                    translateMore(data,data.moreBlocks,sprite)

# taken from https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
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

def redrawAll(canvas, data):
    if data.login:
        canvas.create_rectangle(0,0,data.width,data.height,fill="#4D97FE",outline="")
        data.nameBox.draw(canvas)
        data.password.draw(canvas)
    if not data.login:
        canvas.create_rectangle(0, 0,data.width, data.height, fill="#e8f1ff",width=0)
        canvas.create_rectangle(0,0,data.width,data.height//20,fill="#4D97FE",outline="")
        round_rectangle(canvas,-10,data.height//9,data.width//1.6,data.height-data.height//50,fill="white", outline="#dbdbdb",width=1)
        data.playButton.draw(canvas)
        data.stopButton.draw(canvas)
        #data.codeArea.draw(canvas)
        data.backdropHolder.draw(canvas)
        data.spriteHolder.draw(canvas)
        data.animate.draw(canvas)
        for sprites in data.sprites:
            index = sprites[0].costumeNum
            sprite = sprites[index]
            sprite.draw(canvas)
        for spritebutton in data.spriteHolder.sprites:
            if spritebutton.pressed:
                spritebutton.codeArea.draw(canvas)
                #index = data.spriteHolder.sprites.index(spritebutton)
                #data.sprites[index].draw(canvas)
        data.codeHolder.draw(canvas)
        for backdrop in data.backdropHolder.backdrops:
            backdrop.draw(canvas,data.animate.width,data.animate.height,data.animate.cx,data.animate.cy)
        if data.appear:
            for movingBlock in data.blocks:
                movingBlock.draw(canvas)
        #data.sprite.draw(canvas)
        data.logo.draw(canvas)
        y = data.backdropHolder.cy - 230
        width = data.backdropHolder.width*2 - data.backdropHolder.margin*2
        height = int(width//1.5)
        # for color in ["orange","yellow"]:
        for backdrop in data.backdrops:
            data.backdropHolder.backdrops += [Backdrop(data.backdropHolder.cx,y,width,height,data.animate.width*2,data.animate.height*2,backdrop)]
            y += data.backdropHolder.backdrops[0].height+50
        data.costume.draw(canvas)
        data.saveButton.draw(canvas)
        data.window.draw(canvas)
        data.textbox.draw(canvas)
    

# taken from 110 website
class Struct(object): pass

def run(width=300, height=300):
    def redrawAllWrapper():
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, width, height, fill="white", width=0)
        redrawAll(canvas, data)
        canvas.update()

    def callFn(fn, event=None):
        if (fn == 'mousePressed'): data._mouseIsPressed = True
        elif (fn == 'mouseReleased'): data._mouseIsPressed = False
        if ('mouse' in fn): data._lastMousePosn = (event.x, event.y)
        if (fn in globals()):
            if (fn.startswith('key')):
                c = event.key = event.char
                if ((c in [None, '']) or (len(c) > 1) or (ord(c) > 255)):
                    event.key = event.keysym
                elif (c == '\t'): event.key = 'Tab'
                elif (c in ['\n', '\r']): event.key = 'Enter'
                elif (c == '\b'): event.key = 'Backspace'
                elif (c == chr(127)): event.key = 'Delete'
                elif (c == chr(27)): event.key = 'Escape'
                elif (c == ' '): event.key = 'Space'
                if (event.key.startswith('Shift')): return
            args = [data] if (event == None) else [event, data]
            globals()[fn](*args)
            redrawAllWrapper()

    def timerFiredWrapper():
        callFn('timerFired')
        data._afterId1 = root.after(data.timerDelay, timerFiredWrapper)
        
    def mouseMotionWrapper():
        if (((data._mouseIsPressed == False) and (data._mouseMovedDefined == True)) or
            ((data._mouseIsPressed == True ) and (data._mouseDragDefined == True))):
            event = Struct()
            event.x = root.winfo_pointerx() - root.winfo_rootx()
            event.y = root.winfo_pointery() - root.winfo_rooty()
            if ((data._lastMousePosn !=  (event.x, event.y)) and
                (event.x >= 0) and (event.x <= data.width) and
                (event.y >= 0) and (event.y <= data.height)):
                fn = 'mouseDragged' if (data._mouseIsPressed == True) else 'mouseMoved'
                callFn(fn, event)
        data._afterId2 = root.after(data.mouseMovedDelay, mouseMotionWrapper)

    # Set up data and call init
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.mouseMovedDelay = 50 # ditto
    data._mouseIsPressed = False
    data._lastMousePosn = (-1, -1)
    data._mouseMovedDefined = 'mouseMoved' in globals()
    data._mouseDragDefined = 'mouseDragged' in globals()
    data._afterId1 = data._afterId2 = None
    # create the root and the canvas
    root = Tk()
    root.title("Trash")
    root.resizable(width=False,height=False)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event: callFn('mousePressed', event))
    # root.bind("<B1-Motion>", lambda event: callFn('mouseDragged', event))
    root.bind("<B1-ButtonRelease>", lambda event: callFn('mouseReleased', event))
    root.bind("<Key>", lambda event: callFn('keyPressed', event))
    # initialize, start the timer, and launch the app
    callFn('init')
    if ('timerFired' in globals()): timerFiredWrapper()
    if (data._mouseMovedDefined or data._mouseDragDefined): mouseMotionWrapper()
    root.mainloop()  # blocks until window is closed
    if (data._afterId1): root.after_cancel(data._afterId1)
    if (data._afterId2): root.after_cancel(data._afterId2)
    if data.w != None: data.w.stop()
    print("bye!")

run(1420, 830)
