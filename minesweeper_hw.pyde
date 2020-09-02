
import random
path = os.getcwd()
class Tiles:
    def __init__ (self,r,c,v, cnt):
        self.r=r #row coordinate
        self.c=c #column coordinate
        self.v=v # 0-8 or mine
        self.status="hidden" #hiden or uncovered
        self.cnt = cnt # a value for each tile so I can assign the mines and make sure it doesn't pickthe same location
        self.img=loadImage(path+"/images/"+"tile"+".png") #covered tile image
    def display(self): #main display function/changes the pic when status changes
        if self.status=="hidden":
            image(self.img,self.r*50, self.c*50)
            stroke(0)
        elif self.status!="hidden":
            image(self.img2,self.r*50, self.c*50)
class Minesweeper:
    def __init__(self):
        self.numCols=8
        self.numRows=8
        self.numMines=10
        self.tiles=[] #stores all tiles
        self.state="play" #if state is win it displays win image/if it's loss it diplays gameover/if it's play it calls normal display function
        self.imgwin=loadImage(path+"/images/win.png") #displayed when there is a win/uploaded it on nyuclasses with homework
        self.imgloss=loadImage(path+"/images/gameover.png") #displayed when there is loss
        cnt=0
        for r in range(self.numRows): #makes board
            for c in range(self.numCols):
                self.tiles.append(Tiles(r,c,0,cnt))
                cnt+=1
    def display(self): #displays tiles
        for x in self.tiles:
            x.display()
    def getTile(self,r,c): #gets tile from self.tiles list
        for x in self.tiles:
            if r == x.r and c == x.c:
                return x    
    def assignMines(self): 
        all_tiles = list(range(1, (self.numRows*self.numCols)+1)) 
        mines_tile_num = random.sample(all_tiles, self.numMines) # a list of random numbers with values that are the cnt attributes of the tiles / makes sure each mine is unique
        for x in self.tiles:
            if x.cnt in mines_tile_num:
                x.v = "mine"
                x.img2 = loadImage(path+"/images/"+"mine"+".png")
    def setNumbers(self):
        for x in self.tiles:
            counter=0
            if x.v != "mine": #if the value isn't a mine loop through neighbours (check first if within board) and then increment the counter if mine is found
                neighbours=[[-1,0],[1,0],[0,-1],[0,1],[-1,1],[-1,-1],[1,-1],[1,1]]
                for n in neighbours:
                    if 0<=x.r+n[0]<=self.numRows-1 and 0<=x.c+n[1]<=self.numCols-1:
                        nT = self.getTile(x.r+n[0],x.c+n[1])
                        if nT.v == "mine":
                            counter+=1
                            x.v=counter   
            x.img2 = loadImage(path+"/images/"+str(x.v)+".png")#the number of the counter is the value of the tile and the number of surrounding mines
            
    
    def game(self,tile): #if value is btw 1-8 uncover it and append it to the opened tiles list (so I can later implemet win condition)
        if tile.v in range(1,9):
            tile.status="uncovered"
        elif tile.v == 0: #if value is 0 or empty uncover it and append it but also open all surrounding tiles and call the function again on each empty neighbour
            tile.status="uncovered"
            neighbours=[[-1,0],[1,0],[0,-1],[0,1],[-1,1],[-1,-1],[1,-1],[1,1]]
            for n in neighbours:
                if 0<=tile.r+n[0]<=self.numRows-1 and 0<=tile.c+n[1]<=self.numCols-1:
                    nT = self.getTile(tile.r+n[0],tile.c+n[1])
                    if nT.status=="hidden":
                        self.game(nT)
    def win(self):#if all tiles are opened and are not mines that means that only means are left
        cnt=0
        for x in self.tiles:
            if x.status=="uncovered" and x.v!="mine":
                cnt+=1
        if cnt==(self.numRows*self.numCols)-self.numMines:
            for x in self.tiles:
                x.status="uncovered"
                self.state="win"
        
    def click(self):
        if self.state=="play":
            r = mouseX // 50
            c = mouseY // 50
            cT = self.getTile(r,c)
            if cT.v=="mine": #uncovers all the remaining mines and ends game
                for x in self.tiles:
                    if x.v=="mine":
                        x.status="uncovered"
                self.state="loss"
            else:
                self.game(cT) #calls game function if tile clicked is not a mine
                
p=Minesweeper()

def setup():
    size(p.numRows*50,p.numCols*50)
    p.assignMines()
    p.setNumbers()
def draw():
    if p.state=="play":
        p.display()
    elif p.state=="win":
        p.display()
        image(p.imgwin,100,100,200,200)
    else:
        p.display()
        image(p.imgloss,100,100,200,200)

def mouseClicked():
    p.click()
    p.win()
