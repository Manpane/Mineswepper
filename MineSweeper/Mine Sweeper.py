import sys
import random,math
import pygame
import time
import threading
pygame.init()
pygame.font.init()
class Color():
    RED=(200,0,0)
    GREEN = (0,200,0)
    BLUE = (0,0,200)
    GRAY=(200,200,200)
    UNCLICKED_GREEN = (151,198,43)
    ONE_TEXT = (36,50,215)
    TWO_TEXT=(243,145,17)
    THREE_TEXT=(213,38,117)
    FOUR_TEXT = (164,30,221)
    ORANGE = (235, 158, 52)
    WIN_COLOR=(193, 232, 228)
    WHITE=(255,255,255)
    BLACK=(0,0,0)

SCREEN_WIDTH = 400
SCREEN_BOTTOM_GAP = 50
SCREEN_HEIGHT = 400 + SCREEN_BOTTOM_GAP

class Board():
    width=10
    height=10
    clicks=0
    cubeWidth=0
    cubeHeight=0
    def __init__(self):
        self.cubeWidth = int(SCREEN_WIDTH/self.width)
        self.cubeHeight = int((SCREEN_HEIGHT - SCREEN_BOTTOM_GAP)/self.height)
        self.fontStyle = pygame.font.Font("freesansbold.ttf",int((self.cubeWidth+self.cubeHeight)*0.5))
        self.board = self.newBoard()
        self.setNeighbours()
        self.mineNumbers = math.floor((self.width*self.height)/10)
        self.wonGame = False
    def __repr__(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j],end=" ")
            print(end="\n\n")
        return ""

    def newBoard(self):
        board=[]
        for i in range(self.height):
            board.append([])
            for j in range(self.width):
                board[i].append(Cube(Dimensions(j*self.cubeWidth,i*self.cubeHeight,self.cubeWidth,self.cubeHeight),self.fontStyle))
        return board

    def setNeighbours(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i>0:
                    self.board[i][j].neighbours.append(self.board[i-1][j])
                    if j>0:
                        self.board[i][j].neighbours.append(self.board[i-1][j-1])
                    if j<self.width-1:
                        self.board[i][j].neighbours.append(self.board[i-1][j+1])
                if i<self.height-1:
                    self.board[i][j].neighbours.append(self.board[i+1][j])
                    if j<self.width-1:
                        self.board[i][j].neighbours.append(self.board[i+1][j+1])
                    if j>0:
                        self.board[i][j].neighbours.append(self.board[i+1][j-1])
                if j<self.width-1:
                    self.board[i][j].neighbours.append(self.board[i][j+1])
                if j>0:
                    self.board[i][j].neighbours.append(self.board[i][j-1])
    def draw(self):
        if not self.wonGame:
            clicks=0
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.board[i][j].draw()
                    if (not self.board[i][j].isMine) and (self.board[i][j].clickedMe):
                        clicks+=1
            if clicks==(self.width*self.height)-self.mineNumbers:
                self.wonGame = True
        else:
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].isMine:
                        self.board[i][j].draw(won=True)
    def getNewMinePosition(self,mines):
        while True:
            newMinePos = (  random.randint(0,self.height-1)  ,  random.randint(0,self.width-1)   )
            if newMinePos not in mines:
                break
        return newMinePos
    def setMines(self,minesList):
        mines=[tuple(mine) for mine in minesList]
        for i in range(self.mineNumbers):
            minePosition = self.getNewMinePosition(mines)
            self.board[minePosition[0]][minePosition[1]]
            self.board[ minePosition[0] ] [ minePosition[1] ].isMine=True
            mines.append(minePosition)
class Dimensions():
    def __init__ (self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
class Cube():
    def __init__(self,dimensions,fontStyle):
        self.dimensions = dimensions
        self.rect = pygame.Rect(self.dimensions.x+1,self.dimensions.y+1,self.dimensions.width-2,self.dimensions.height-2)
        self.isMine = False
        self.color = Color.UNCLICKED_GREEN
        self.textColor=Color.RED
        self.neighbours = []
        self.mineFulNeighbours = 0
        self.fontStyle = fontStyle
        self.flagged = False
        self.number=self.fontStyle.render("",True,self.textColor)
        self.clickedMe=False
    def draw(self,won=False):
        if won:
            pygame.draw.rect(screen,Color.WIN_COLOR,self.rect)
            return
        pygame.draw.rect(screen,self.color,self.rect)
        if self.flagged:
            self.number=self.fontStyle.render("F",True,Color.RED)
        else:
            self.number=self.fontStyle.render("",True,Color.RED)
            if self.clickedMe:
                if self.mineFulNeighbours==1:
                    self.number=self.fontStyle.render("1",True,Color.ONE_TEXT)
                elif self.mineFulNeighbours==2:
                    self.number=self.fontStyle.render("2",True,Color.TWO_TEXT)
                elif self.mineFulNeighbours==3:
                    self.number=self.fontStyle.render("3",True,Color.THREE_TEXT)
                elif self.mineFulNeighbours==4:
                    self.number=self.fontStyle.render("4",True,Color.FOUR_TEXT)
                elif self.mineFulNeighbours==0:
                    self.number=self.fontStyle.render("",True,Color.FOUR_TEXT)
                else:
                    self.number=self.fontStyle.render(str(self.mineFulNeighbours),True,Color.RED)
        
        screen.blit(self.number,(  self.dimensions.x+int(Board.cubeWidth/3),self.dimensions.y+int(Board.cubeHeight/2.5)  ))
        if self.clickedMe and self.isMine:
            pygame.draw.rect(screen,Color.GRAY,(self.dimensions.x+5,self.dimensions.y+5,self.dimensions.width-10,self.dimensions.height-10))

    def clicked(self):
        if not self.clickedMe and not self.flagged:
            self.clickedMe = True
            self.color=(200,200,200)
            if self.isMine:
                self.color = (200,0,0)
                return "Game Over"
            for each in self.neighbours:
                if each.isMine:
                    self.mineFulNeighbours+=1
            if self.mineFulNeighbours==0:
                for each in self.neighbours:
                    if not each.clickedMe:
                        each.clicked()
    def flaggedButton(self):
        if self.flagged:
            self.flagged=False
            return
        if not self.clickedMe:
            self.flagged=True

    def __repr__(self):
        return str(self.isMine)
class Button():
    def __init__(self,text:str,dimensions:Dimensions,fontSize:int,color:Color):
        self.text = text
        self.backgroundColor = Color.BLACK
        self.color = color
        self.dimensions = dimensions
        self.dimensions.width = (len(text)-1)*(fontSize-1)
        self.dimensions.height = fontSize
        self.font = pygame.font.Font("freesansbold.ttf",fontSize)
        self.actualText = self.font.render(text,True,self.color)
    def render(self):
        pygame.draw.rect(screen,self.backgroundColor,(self.dimensions.x-1,self.dimensions.y-2,self.dimensions.width-2,self.dimensions.height+4))
        screen.blit(self.actualText,(self.dimensions.x,self.dimensions.y))
    def isClicked(self,x,y):
        return (x>self.dimensions.x and x<self.dimensions.x+self.dimensions.width and y>self.dimensions.y and y<self.dimensions.y+self.dimensions.height)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption(("Mine Sweeper"))
try:
    pygame.display.set_icon(pygame.image.load("bomb.png"))
except Exception as e:
    pass

def renderPostGame(board):
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j].isMine:
                board.board[i][j].color = Color.RED
                time.sleep(0.05)
def main():
    startingTime = time.time()
    board = Board()
    Board.clicks=0
    gameOut=False
    EasyButton = Button("Easy",Dimensions(1,SCREEN_HEIGHT-SCREEN_BOTTOM_GAP+20,0,0),15,Color.WHITE)
    MidButton = Button("Normal",Dimensions(EasyButton.dimensions.x+EasyButton.dimensions.width+5,SCREEN_HEIGHT-SCREEN_BOTTOM_GAP+20,0,0),15,Color.WHITE)
    HardButton = Button("Hard",Dimensions(MidButton.dimensions.x+MidButton.dimensions.width+5,SCREEN_HEIGHT-SCREEN_BOTTOM_GAP+20,0,0),15,Color.WHITE)
    quitButton = Button("QUIT",Dimensions(SCREEN_WIDTH-100,SCREEN_HEIGHT-SCREEN_BOTTOM_GAP+25,0,0),18,Color.RED)
    running = True
    newFOnt = pygame.font.Font("freesansbold.ttf",40)
    outText = newFOnt.render("Game Over",True,Color.BLACK)
    winText = newFOnt.render("You Won!",True,(108,32,97))
    playAgain = False
    gameQuitted = False
    timeFont = pygame.font.Font("freesansbold.ttf",14)
    timeToDisplay=0
    while running:
        screen.fill((100,100,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if not gameOut:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==1:
                        MposX , MposY = pygame.mouse.get_pos()
                        if quitButton.isClicked(MposX,MposY):
                            gameOut=True
                            gameQuitted = True
                            break
                        boardX=math.floor(MposX/board.cubeWidth)
                        boardY=math.floor(MposY/board.cubeHeight)
                        if boardY<Board.height and Board.clicks==0:
                            board.setMines([(boardY,boardX),(boardY-1,boardX),(boardY+1,boardX),(boardY-1,boardX-1),(boardY-1,boardX+1),(boardY+1,boardX+1),(boardY+1,boardX-1),(boardY,boardX-1),(boardY,boardX+1)])
                            Board.clicks+=1
                        if boardY<Board.height and board.board[boardY][boardX].clicked():
                            gameOut = True
                    if event.button==3:
                        MposX , MposY = pygame.mouse.get_pos()
                        boardX=math.floor(MposX/board.cubeWidth)
                        boardY=math.floor(MposY/board.cubeHeight)
                        try:
                            board.board[boardY][boardX].flaggedButton()
                        except:
                            pass
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        MposX,MposY = pygame.mouse.get_pos()
                        if EasyButton.isClicked(MposX,MposY):
                            Board.width = 10
                            Board.height = 10
                            EasyButton.backgroundColor = Color.GRAY
                            MidButton.backgroundColor = Color.BLACK
                            HardButton.backgroundColor = Color.BLACK
                            return
                        if MidButton.isClicked(MposX,MposY):
                            Board.width = 17
                            Board.height = 17
                            EasyButton.backgroundColor = Color.BLACK
                            MidButton.backgroundColor = Color.GRAY
                            HardButton.backgroundColor = Color.BLACK
                            return
                        if HardButton.isClicked(MposX,MposY):
                            Board.width = 25
                            Board.height =25
                            EasyButton.backgroundColor = Color.BLACK
                            MidButton.backgroundColor = Color.BLACK
                            HardButton.backgroundColor = Color.GRAY
                            return
        board.draw()
        if not gameQuitted and not gameOut:
            timeToDisplay = int(time.time()-startingTime)
        if not gameQuitted:
            screen.blit(timeFont.render(f"Time : {timeToDisplay}",True,Color.WHITE),(SCREEN_WIDTH-100,SCREEN_HEIGHT-SCREEN_BOTTOM_GAP+5))
        quitButton.render()
        EasyButton.render()
        MidButton.render()
        HardButton.render()
        if gameOut:
            threading.Thread(target=renderPostGame,args=(board,),daemon=False).start()
            if not gameQuitted:
                screen.blit(outText,(100,100))
            for line in board.board:
                for cube in line:
                    if cube.flagged and not cube.isMine:
                        cube.flaggedButton()
        if board.wonGame:
            gameOut =True
            gameQuitted = True
            threading.Thread(target=renderPostGame,args=(board,),daemon=False).start()
            winText = newFOnt.render(f"You Won! Time {timeToDisplay} s.",True,(108,32,97))
            screen.blit(winText,(10,100))
        pygame.display.update()
while True:
    main()
