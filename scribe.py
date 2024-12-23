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
        
class Format:
    end = '\033[0m'
    underline = '\033[4m'

endingPos = [0,0]

def _logEndPos(pos: list): #makes scribes follow from previous scribes
    global endingPos 
    endingPos = pos
    
class TerminalScribe:

    fresh = True
    scribesList = []
    shapes = "line", "square", "function", "ln", "sq", "func"

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        #self.pos = [0, 0] #start in top left
        self.pos = [(self.canvas._x / 2), self.canvas._y / 2]
        
        self.framerate = 0.05
        self.direction = [0.0, 0.0]
        self.willBonk = True
        #myCanvas.clear()

        self.name = ""
        self.mark = '*'
        self.trail = '.'      

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
                #checks size to see if it fits the canvas/is an int
                if type(size) != int or size < 1 or size > myCanvas._x:
                    while True:
                        try:
                            newSize = int(input(f"{name}'s size is invalid. Please provide a valid size:\n"))
                        except ValueError:
                            continue
                        if newSize < 1 or newSize > myCanvas._x:
                            continue
                        else:
                            newScribe["Size"] = newSize
                            break
            case "func" | "function":
                formList = ["sin", "sine", "cos", "cosine", "tan", "tangent"]
                func = "formula" 
                #asks for ident to use
                formula = input(f"Which of the trigonometric identities should {name} graph?\n").lower()
                #ask for what to take func of in future? assign input to some x variable
                if formula.lower() not in formList:
                    while True:
                        try:
                            newFormula = input(f"That is not a valid identity. Please enter a valid identity:\n").lower()
                        except Exception:
                            continue
                        if newFormula not in formList:
                            continue
                        else: 
                            formula = newFormula
                            break
                if formula == "sin" or formula == "sine":
                    newScribe["Calc"] = "sin" #will make sin graph
                elif formula == "cos" or formula == "cosine":
                    newScribe["Calc"] = "cos" #will make cos graph
                elif formula == "tan" or formula == "tangent":
                    newScribe["Calc"] = "tan" #will make tan graph               
            case _:
                #asks for apology if shape is invalid
                while True:
                    data = input(f"{name} will not draw this filth! Apologize!\n")                    
                    if data.lower() != "sorry" or "sry":
                        continue
                    else: #kills self if you apologize, lol
                        os._exit(1) #figure this out later, maybe just a vscode thing

        newScribe["Function"] = func
        
        if angle:
            newScribe["Angle"] = angle
        for i in TerminalScribe.scribesList:
            if newScribe["Name"] == i["Name"]:
                #maybe undo this to allow for auto-naming?
                return print("There is already a scribe with this name!") 
        
        TerminalScribe.scribesList.append(newScribe)

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
        for i in TerminalScribe.scribesList: #sends scribes to work depending on name and function
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

class LineScribe(TerminalScribe):
    def __init__(self, name: str, length: int, angle: int, currentPos: list = [0,0]):
        super().__init__(myCanvas)
        self.name = name
        self.length = length
        self.angle = angle
        self.currentPos = currentPos
        

    def draw(self, size: int, angle: int, currentPos):        
        self.pos = currentPos #chains lines together
        
        self.canvas.setPos(self.pos, self.mark) 
        self._face(angle)
        self._forward(size)

        _logEndPos(self.pos)
        self._clearMark()    

class SquareScribe(TerminalScribe):

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
    
    def draw(self, size: int, currentPos: list= [0,0]):
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

    """In interactive mode, user creates scribe. new <name> SquareScribe 
    object is created. On order to run, code <name>.draw(*args)"""

    
class FunctionScribe(TerminalScribe):
    def draw(self, identity: str):
        self.pos = [0, int(self.canvas._y / 2)]
        if identity == "sin":
            self._drawSin()
        elif identity == "cos":
            self._drawCos()
        elif identity == "tan":
            self._drawTan()

    def _drawSin(self):
        self.canvas.setPos(self.pos, self.mark)
        yVar = int(self.canvas._y / 2)
        for i in range(self.canvas._x):
            self.canvas.setPos(self.pos, self.trail)        
            self.pos = [i, math.sin(i) * (yVar / math.pi) + yVar]
            self.canvas.setPos(self.pos, self.mark) 
            self.canvas.print()
            time.sleep(self.framerate)
        self._clearMark()

    def _drawCos(self):
        self.canvas.setPos(self.pos, self.mark)
        yVar = int(self.canvas._y / 2)
        for i in range(self.canvas._x):
            self.canvas.setPos(self.pos, self.trail)        
            self.pos = [i, math.cos(i) * (yVar / math.pi) + yVar]
            self.canvas.setPos(self.pos, self.mark) 
            self.canvas.print()
            time.sleep(self.framerate)
        self._clearMark()

    def _drawTan(self):
        self.canvas.setPos(self.pos, self.mark)
        yVar = int(self.canvas._y / 2)
        for i in range(self.canvas._x):
            self.canvas.setPos(self.pos, self.trail)
            self.pos = [i, math.tan(i) * (yVar / math.pi) + yVar]
            if self.pos[1] > self.canvas._y:
                self.pos[1] = self.canvas._y - 1
            if self.pos[1] < 0:
                self.pos[1] = 0
            self.canvas.setPos(self.pos, self.mark) 
            self.canvas.print()
            time.sleep(self.framerate)
        self._clearMark()

creating = True
#begins program with user input

#make canvas first!
myCanvas = Canvas(50, 50) #make input

#greeting
print("Welcome! Let's make some scribes together :)")
while creating:
    if len(TerminalScribe.scribesList) == 0:
        scribeName = input("\nWhat would you like to name your first scribe?\n")
    else: scribeName = input("\nWhat would you like to name this scribe?\n")
    naming = True
    while naming:
        if len(TerminalScribe.scribesList) == 0:
            naming = False
        for i in TerminalScribe.scribesList:
            #add .lower() after both to ignore cases in name matching
            if i.name == scribeName:
                #if this name has already been added
                scribeName = input("\nThere is already a scribe with this name! Choose another:")
                continue
            else: 
                naming = False

    scribeType = input(f"\nWhat would you like {scribeName} to draw? \nFor now, choose between a line, a square, or a function.\n").lower()
    shaping = True
    while shaping:
        if scribeType not in TerminalScribe.shapes:
            scribeType = input("\nThat is not a valid shape; please choose one of the listed options.\n")
            continue
 
        else: 
            shaping = False

    match scribeType:
        case "line" | "ln":
            scribeType = "line"
            #ensure length is an int above 0
            while True:
                try:
                    lineLen = int(input(f"\nHow long should {scribeName} be?\t"))
                except Exception:
                    print("\nThat is not a valid length; please ensure your answer is an int.")
                    continue
                
                if lineLen < 1:
                    print("Your answer cannot be smaller than 1.\n")
                    continue
                else: break
            #dictates angle of line
            while True:
                try:
                    lineAng = int(input(f"What angle (in degrees) should {scribeName} be?\t"))
                except Exception:
                    print("\nThat is not a valid angle; please ensure your answer is an int.\n")
                    continue
                break
            
            #scribe is created and added to master list
            scribe = LineScribe(scribeName, lineLen, lineAng)
            TerminalScribe.scribesList.append(scribe)

            buildMore = input(f"\nYou have created a scribe named {scribeName} that will draw a {lineAng} degree {scribeType}. Would you like to make more scribes?\n\t").lower()
            #asks to continue, catches anything but yes or no
            ansBuild = True
            while ansBuild:
                match buildMore:
                    case "y" | "yes":
                        ansBuild = False
                        break
                    case "n" | "no":
                        ansBuild = False
                        creating = False
                        break
                    case _:
                        buildMore = input("Please answer yes or no:\n\t").lower()
                        continue

        case "square" | "sq":
            pass
        case "function" | "func":
            pass
        case _:
            pass
        #fill out with drawing different shapes
    
    

#once all scribes are created, run specified scribe/other functions to be added (list them, run multiple, whatever)
drawing = True
commandName = input("\nWhich scribe would you like to summon?\t")
while drawing: 
    for i in TerminalScribe.scribesList:
        if i.name == commandName:
            i.draw(i.length, i.angle, i.currentPos)
            drawing = False           
        else: 
            commandName = input("\nThere is no scribe with such a name. Please name an existing scribe:\t")
            continue
prompt = input(f"Would you like to {Format.underline}summon{Format.end} another scribe, {Format.underline}create{Format.end} a new scribe, or {Format.underline}quit{Format.end}?\n").lower()
choosing = True
while choosing:
    match prompt:
        case "summon" | "s":
            choosing = False
            pass
        case "create" | "c":
            choosing = False
            pass
        case "quit" | "q":
            choosing = False
            print("yayayayAYAYAYAYAY YOU'RE FREE!!!!!")
            break
        case _:
            prompt = input(f"That is not a valid response. You can {Format.underline}summon{Format.end}, {Format.underline}create{Format.end}, or {Format.underline}quit{Format.end}.\n").lower()
            continue
    #fill match case to redirect

    

print(Canvas.checkSpots)