import time
import os
import math
import operator

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
    """Allows for different text formatting effects when printed."""
    end = '\033[0m'
    underline = '\033[4m'
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'

    def colorMark(markColor):
        
        pass
  
class TerminalScribe:

    fresh = True
    scribesList = []
    shapes = "line", "square", "function", "ln", "sq", "func"
    endingPos = [0,0]

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.pos = [0, 0] #start in top left
        #self.pos = [(self.canvas._x / 2), self.canvas._y / 2] #start in center
        
        self.framerate = 0.05
        self.direction = [0.0, 0.0]
        self.willBonk = True
        self.type = ""
        #myCanvas.clear()

        #make interactive?
        self.name = ""
        self.mark = '*'
        self.trail = '.'      

    def _logEndPos(pos: list): #makes scribes follow from previous scribes
        #global endingPos 
        TerminalScribe.endingPos = pos

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

    def createScribe():
        """Adding a scribe to a master list."""
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
                    scribeName = input("\nThere is already a scribe with this name! Choose another:\n")
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

            case "square" | "sq":
                scribeType = "square"
                #ensure size is an int above 0 and below canvas boundaries
                while True:
                    try:
                        lineLen = int(input(f"\nHow long should {scribeName}'s sides be?\t"))
                    except Exception:
                        print("\nThat is not a valid length; please ensure your answer is an int.")
                        continue
                    
                    if lineLen < 1:
                        print("Your answer cannot be smaller than 1.\n")
                        continue
                    if lineLen > myCanvas._x or lineLen > myCanvas._y:
                        print(f"Your answer cannot be larger than the canvas, which is {myCanvas._x} units wide and {myCanvas._y} units tall.\n")
                        continue

                    else: break
                #checks if square should be centered
                isCentered = input(f"Should {scribeName} be centered on the canvas?\t").lower()
                ansCent = True
                while ansCent:
                    match isCentered:
                        case "y" | "yes":
                            ansCent = False
                            _centered = True
                            break
                        case "n" | "no":
                            ansCent = False
                            _centered = False
                            break
                        case _:
                            isCentered = input("Please answer yes or no:\n\t").lower()
                            continue
                #scribe is created and added to master list
                scribe = SquareScribe(scribeName, lineLen, _centered)
                TerminalScribe.scribesList.append(scribe)

                #perhaps indicate if square is centered?
                buildMore = input(f"\nYou have created a scribe named {scribeName} that will draw a {scribeType} with {lineLen} unit long sides. Would you like to make more scribes?\n\t").lower()

            case "function" | "func":
                scribeType = "function"
                buildFunc = True
                while buildFunc:
                    try:
                        myFunc = input(f"\nWhat does y= in {scribeName}'s function?\t")
                    except Exception: #IDK HOW TO TEST FOR THIS FUCK
                        print("\nThat is not a valid length; please ensure your answer is an int.")
                        continue
                    else: break
                #scribe is created and added to master list
                scribe = FunctionScribe(scribeName, myFunc)
                TerminalScribe.scribesList.append(scribe)

                buildMore = input(f"\nYou have created a scribe named {scribeName} that will draw a {scribeType} where y = {myFunc}. Would you like to make more scribes?\n\t").lower()
            case _:
                pass
            #fill out with drawing different shapes

        #asks to continue, catches anything but yes or no
        ansBuild = True
        while ansBuild:
            match buildMore:
                case "y" | "yes":
                    ansBuild = False
                    TerminalScribe.createScribe()
                    break
                case "n" | "no":
                    ansBuild = False
                    break
                case _:
                    buildMore = input("Please answer yes or no:\n\t").lower()
                    continue

    def sendScribe():
        drawing = True
        print("\nWhich scribe would you like to summon? The following scribes are currently ready to be summoned:")
        for i in TerminalScribe.scribesList:
            print(i.name)
        commandName = input("")
        while drawing: 
            for i in TerminalScribe.scribesList:
                if i.name == commandName:
                    if i.type == "line":
                        i.draw(i.length, i.angle, TerminalScribe.endingPos)
                        drawing = False       
                    elif i.type == "square":
                        i.draw(i.size, i.centered)
                        drawing = False 
                    elif i.type == "function":
                        i.draw(i.function)
                        drawing = False 
            if drawing: 
                commandName = input("\nThere is no scribe with such a name. Please name an existing scribe:\t")
                continue

class LineScribe(TerminalScribe):
    def __init__(self, name: str, length: int, angle: int, currentPos: list = [0,0]):
        super().__init__(myCanvas)
        self.name = name
        self.length = length
        self.angle = angle
        self.pos = currentPos
        self.type = "line"
        

    def draw(self, size: int, angle: int, currentPos):        
        self.pos = currentPos #chains lines together
        
        self.canvas.setPos(self.pos, self.mark) 
        self._face(angle)
        self._forward(size)

        TerminalScribe._logEndPos(self.pos)
        self._clearMark()    

class SquareScribe(TerminalScribe):
    def __init__(self, name: str, size: int, centered: bool = True, currentPos: list = [0,0]):
        super().__init__(myCanvas)
        self.name = name
        self.size = size
        self.centered = centered
        self.pos = currentPos
        self.type = "square"

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
    
    def draw(self, size: int, centered: bool):
        #for rectangles (self, width: int, height: int) swap "size" with width and height

        if centered:
            self.centered = True
            self.pos = [(int((self.canvas._x - size) / 2)), (int((self.canvas._y - size) / 2))]
        else:
            self.pos = TerminalScribe.endingPos
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

        TerminalScribe._logEndPos(self.pos)
        self._clearMark()

    """In interactive mode, user creates scribe. new <name> SquareScribe 
    object is created. On order to run, code <name>.draw(*args)"""
  
class FunctionScribe(TerminalScribe):
    def __init__(self, name: str, function):
        super().__init__(myCanvas)
        self.name = name
        self.pos = []
        self.type = "function"
        self.function = function
        
           
    def draw(self, function):
        yVar = int(self.canvas._y / 2)
        #calculate x and y coordinates in for loop
        for i in range(self.canvas._x):
            if self.pos is not []: #ignores on first calc, then displays afterwards
                self.canvas.setPos(self.pos, self.trail)   
            yVal = self.calculate(i, function)     
            self.pos = [i, yVal]
            self.canvas.setPos(self.pos, self.mark) 
            self.canvas.print()
            time.sleep(self.framerate)
        self._clearMark()
        

    def calculate(self, calcX: int, function: str): #doesn't do trig or pi
        #operators that can be parsed
        ops = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,
            '%' : operator.mod,
            '**': operator.pow
               }
        
        errors = []
        x = calcX
        list = function.split()
        addList = []

        #turns x into int
        for i in range(len(list)): 
            if list[i] == "x":
                list[i] = x

        #turns int strings to ints
        for INT in range(len(list)):
            try: list[INT] = int(list[INT])
            except: errors.append(f"{INT} is not an INT")

        #turn operators into ops
        for OP in range(len(list)):
            if list[OP] in ops: list[OP] = ops[list[OP]]

        it = 0
        iterations = int((len(list) - 1) / 2)
        while it < iterations:
            addList.append(list[1](list[0], list[2]))
            list.pop(0)
            list.pop(0)
            list[0] = addList[it]
            it += 1

        return addList[-1]

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

#begins program with user input

#make canvas first!
myCanvas = Canvas(20, 20) #make input

#greeting
print("Welcome! Let's make some scribes together :)")

TerminalScribe.createScribe()
    
TerminalScribe.sendScribe()

prompt = input(f"Would you like to {Format.underline}summon{Format.end} another scribe, {Format.underline}create{Format.end} a new scribe, or {Format.underline}quit{Format.end}?\n").lower()
choosing = True
while choosing:
    match prompt:
        case "summon" | "s":
            #choosing = False
            TerminalScribe.sendScribe()
            prompt = input(f"Would you like to {Format.underline}summon{Format.end} another scribe, {Format.underline}create{Format.end} a new scribe, or {Format.underline}quit{Format.end}?\n").lower()
            continue
        case "create" | "c":
            #choosing = False
            TerminalScribe.createScribe()
            prompt = "summon"
            continue
        case "quit" | "q":
            choosing = False
            print("yayayayAYAYAYAYAY YOU'RE FREE!!!!!")
            break
        case _:
            prompt = input(f"That is not a valid response. You can {Format.underline}summon{Format.end}, {Format.underline}create{Format.end}, or {Format.underline}quit{Format.end}.\n").lower()
            continue
    #fill match case to redirect

    

if len(Canvas.checkSpots) is not 0: print(Canvas.checkSpots)