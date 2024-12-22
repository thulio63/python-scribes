import time
import os
import math

class Canvas():
    checkSpots = []

    def __init__(self, width, height):
        """Initialize the canvas."""
        self._x = width
        self._y = height
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    def setPos(self, pos, mark):
        try:
            self._canvas[round(pos[0])][round(pos[1])] = mark
        except:
            #check = input(f"{pos} is out of bounds. Do you understand?")
            
            self.checkSpots.append(pos)
            #self._canvas[math.floor(pos[0])][math.floor(pos[1])] = mark

    def bonk(self, pos: list, dir:list): #needs rethinking
        returns = [1, 1]
        if self.horizontalCheck(pos, dir):
            returns[0] *= -1

        self.verticalCheck(pos, dir)

    def horizontalCheck(self, pos:list): #not finished
        posCheck = pos
        if (posCheck[0] + self.direction[0] > self.canvas._x) or (posCheck[0] + self.direction[0] < 0):
            #self.direction[0] *= -1
            return True
        else: return False

    def verticalCheck(self, pos:list): #not finished
        posCheck = pos
        if (posCheck[1] + self.direction[1] > self.canvas._y) or (posCheck[1] + self.direction[1] < 0):
            #self.direction[1] *= -1    
            return True
        else: return False

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self):
        self.clear()
        for y in range(self._y):
            print([' '.join([col[y] for col in self._canvas])])
            #add [] inside print() for visible border
        
endingPos = [0,0]

def _logEndPos(pos: list): #makes scribes follow from previous scribes
    global endingPos 
    endingPos = pos
    
class TerminalScribe:

    fresh = True

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        #self.pos = [0, 0] #start in top left
        self.pos = [(self.canvas._x / 2), self.canvas._y / 2]
        
        self.framerate = 0.05
        self.direction = [0.0, 0.0]
        self.willBonk = True
        #myCanvas.clear()

        self.mark = '*'
        self.trail = '.'

    def drawLine(self, size: int, angle: int, currentPos):        
        self.pos = currentPos #chains lines together
        
        self.canvas.setPos(self.pos, self.mark) 
        self._face(angle)
        self._forward(size)

        _logEndPos(self.pos)
        self._clearMark()        

    def drawSquare(self, size: int, currentPos: list= [0,0]):
        #for rectangles (self, width: int, height: int) swap "size" with width and height
        if currentPos == [0, 0]:
            self.pos = [(int((self.canvas._x - size) / 2)), (int((self.canvas._y - size) / 2))]
        else:
            self.pos = currentPos
        self.canvas.setPos(self.pos, self.mark) 

        self._right(size-1)
        #changes direction before resuming
        self._face(180)    
        self._forward(size - 1) #height for rect 
        #changes direction before resuming
        self._face(270)
        self._forward(size-1) #width for rect
        #changes direction before resuming
        self._face(0)
        self._forward(size-1) #height for rect 

        _logEndPos(self.pos)
        self._clearMark()

    def drawFunction(self, identity: str):
        if identity == "sin":
            self._drawSin()
        elif identity == "cos":
            self._drawCos()
        elif identity == "tan":
            self._drawTan()

        pass

    def _drawSin():
        pass

    def _drawCos():
        pass

    def _drawTan():
        pass

    def _bonk(self, pos: list):
        """Makes the scribe bounce off of walls.""" 
        posCheck = pos
        if (posCheck[0] + self.direction[0] > self.canvas._x) or (posCheck[0] + self.direction[0] < 0):
            self.direction[0] *= -1
            
        if (posCheck[1] + self.direction[1] > self.canvas._y) or (posCheck[1] + self.direction[1] < 0):
            self.direction[1] *= -1    

    def _face(self, degrees):
        """Tells the scribe what direction to move in."""
        #use degrees to set angle - multiply radians by 2 to create easier numbers? need to address int v float
        radians = math.radians(degrees)
        self.direction = [math.sin(radians), -(math.cos(radians))]              

    def _forward(self, spaces: int):
        """Sends the scribe forward in it's given direction."""
        for i in range(spaces):
            self.canvas.setPos(self.pos, self.trail)
            #self.canvas.bonk(self.pos, self.direction) #attaches wall bounce to canvas instead of self
            if self.willBonk:
                self._bonk(self.pos)
            self.pos = [self.pos[0] + self.direction[0], self.pos[1] + self.direction[1]]           
            self.canvas.setPos(self.pos, self.mark)
            self.canvas.print()
            time.sleep(self.framerate)

    def _right(self, spaces):
        self._face(90) 
        self._forward(spaces) #width for rect

    def _down(self, spaces):
        self._face = 180
        self._forward(spaces)

    def _left(self, spaces):
        self._face = 270
        self._forward(spaces)

    def _up(self, spaces):
        self._face = 360
        self._forward(spaces)

    def _clearMark(self):
        self.canvas.setPos(self.pos, self.trail)
        self.canvas.print()

    def createScribe(name: str, shape: str, size: int = 5, angle: int = 90):
        """Adding a scribe to a list of dictionaries."""
        newScribe = {"Name":name, "Size":size}
        if angle == 0:
            angle = 360
        match shape.lower(): #determines what shape to store in dict
            case "line":
                func = "line"
            case "square":
                func = "square"
                #checks size to see if it fits/is an int
                if type(size) != int or size < 1 or size > myCanvas._x:
                    while True:
                        try:
                            newSize = int(input(f"{name}'s size is invalid. Please provide a new size:\n"))
                        except ValueError:
                            continue
                        if newSize < 1 or newSize > myCanvas._x:
                            continue
                        else:
                            newScribe["Size"] = newSize
                            break
            case "form" | "formula":
                func = "formula" 
                #asks for ident to use
                while True:
                    formula = input(f"Which of the trigonometric identities should {name} graph?\n")
                    if formula.lower() == "sin":
                        newScribe["Calc"] = "sin"
                        break
                    elif formula.lower() == "cos":
                        newScribe["Calc"] = "cos"
                        break
                    elif formula.lower() == "tan":
                        newScribe["Calc"] = "tan"
                        break
                    else: continue

            case _:
                #asks for apology if shape is invalid
                while True:
                    data = input(f"{name} will not draw this filth! Apologize!\n")                    
                    if data.lower() != "sorry" or "srry":
                        continue
                    else: #kills self if you apologize, lol
                        os._exit(1) #figure this out later, maybe just a vscode thing

        newScribe["Function"] = func
        
        if angle:
            newScribe["Angle"] = angle
        for i in scribesList:
            if newScribe["Name"] == i["Name"]:
                #maybe undo this to allow for auto-naming?
                return print("There is already a scribe with this name!") 
        scribesList.append(newScribe)

    def summonScribe(name: str):
        """Tells specified scribe to make its shape."""
        #return print(scribesList)
        #startPos = [myCanvas._x / 2, myCanvas._y / 2]
        startPos = endingPos        
        summoned = TerminalScribe(myCanvas) #edit into prev to choose canvas size
        if (TerminalScribe.fresh): #trying to make lines start at center, failing
            summoned.pos = [summoned.canvas._x / 2, summoned.canvas._y / 2]
            TerminalScribe.fresh = False
        size = 1
        angle = 90
        for i in scribesList: #sends scribes to work depending on name and function
            if i["Name"] == name:
                match i["Function"]:
                    case "square":
                        size = i["Size"]                        
                        summoned.drawSquare(size, startPos)
                    case "line":
                        size = i["Size"]
                        angle = i["Angle"]                    
                        summoned.drawLine(size, angle, startPos)
                    case "formula":
                        purpose = i["Calc"]
                        summoned.drawFunction(purpose)

#Not sure how to bundle these with the module. Will give thought.
scribesList = []
shapes = "line", "square", "formula"
myCanvas = Canvas(20, 20)


""" 
# def createScribe(name: str, shape: str, size: int, angle: int = 90): 
#     Adding a scribe to a list of dictionaries.
#     if angle == 0:
#         angle = 360
#     match shape.lower():
#         case "line":
#             func = "line"
#         case "square":
#             func = "square"
#         case "rect" | "rectangle":
#             func = "square"
#         case _:
#             return print("This is not an accepted shape!")
    
#     newScribe = {"Name":name, "Size":size, "Function":func}
#     if angle:
#         newScribe["Angle"] = angle
#     for i in scribesList:
#         if newScribe["Name"] == i["Name"]:
#             return print("There is already a scribe with this name!")
#     scribesList.append(newScribe)

# def summonScribe(name: str):
#     Tells specified scribe to make its shape.
#     #return print(scribesList)
#     startPos = endingPos
#     summoned = TerminalScribe(myCanvas) #edit into prev to choose canvas size
#     size = 1
#     angle = 90
#     for i in scribesList:
#         if i["Name"] == name:
#             match i["Function"]:
#                 case "square":
#                     size = i["Size"]
#                     summoned.drawSquare(size, startPos)
#                 case "line":
#                     size = i["Size"]
#                     angle = i["Angle"]                    
#                     summoned.drawLine(size, angle, startPos)
"""

TerminalScribe.createScribe("billy", "line", 24, 70)
TerminalScribe.createScribe("frank", "line", 15, 30)
# TerminalScribe.createScribe("sam", "line", 2, 180)
TerminalScribe.createScribe("jack", "square", 8)
TerminalScribe.createScribe("sinx", "form")

# TerminalScribe.summonScribe("billy")
# TerminalScribe.summonScribe("frank")
# TerminalScribe.summonScribe("sam")
TerminalScribe.summonScribe("jack")

# for i in scribesList:
#     TerminalScribe.summonScribe(i["Name"])
print(Canvas.checkSpots)