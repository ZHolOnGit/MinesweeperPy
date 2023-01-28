#Minesweeper, this should be fine

import pygame
import math
import random
import IM
import tkinter as tk

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NBLUE = (0, 0, 128)
TURQUOISE = (64, 224, 208)
DGREY = (47,79,79)
clock = pygame.time.Clock()


Width = 800

win = pygame.display.set_mode((Width,Width))
pygame.init()

class Square:
    def __init__(self,row,col,total_rows,width):#width is width of square
        self.col = col
        self.row = row
        self.total_rows = total_rows
        self.width = width
        self.x = col * width
        self.y = row * width
        self.colour = GREY
        self.neighbors = []
        self.mine = False
        self.mine_close = 0
        self.flagged = False
        self.Text_col = None

    def get_pos(self):
        return self.col,self.row

    def is_mine(self):
        return self.mine

    def update_neighbors (self,grid):
        self.neighbors = []
        if self.row >0 and self.col>0:
            self.neighbors.append(grid[self.col-1][self.row-1])#north west
        if self.row > 0:
            self.neighbors.append(grid[self.col][self.row-1])#north
        if self.row > 0 and self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.col+1][self.row-1]) #north east
        if self.col < self.total_rows - 1:
            self.neighbors.append(grid[self.col+1][self.row])#east
        if self.col < self.total_rows - 1 and self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.col+1][self.row + 1])#southeast
        if self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.col][self.row+1])#south
        if self.col > 0 and self.row < self.total_rows - 1:
            self.neighbors.append(grid[self.col -1][self.row +1])#south west
        if self.col > 0:
            self.neighbors.append(grid[self.col-1][self.row])#west

    def draw_rect(self,win):
        pygame.draw.rect(win,self.colour,(self.x,self.y,self.width,self.width))
        if self.colour == BLACK and self.mine_close!=0:
            self.Mine_Text(win)
        if self.flagged == True:
            win.blit(IM.FLAG,(self.x,self.y))

    def Mine_Text(self,win):
        smallText = pygame.font.Font("BERN.ttf",30)
        Mnum = str(self.mine_close)
        TextSurf = smallText.render(Mnum,True,self.Text_col)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((self.x+self.width//2,self.y+self.width//2))
        win.blit(TextSurf,TextRect)
        
    def Find_Near(self):
        for neighbor in self.neighbors:
            if neighbor.mine == True:
                self.mine_close +=1
        if self.mine_close != 0:
            self.Text_col_find()
        if self.mine == True:
            self.mine_close = 0
        
    def Text_col_find(self):
        if self.mine_close == 1:
            self.Text_col = BLUE
        elif self.mine_close == 2:
            self.Text_col = GREEN
        elif self.mine_close == 3:
            self.Text_col = RED
        elif self.mine_close == 4:
            self.Text_col = NBLUE
        else:
            self.Text_col = TURQUOISE
            
    def Show_Mine(self,win):
        if self.mine == True:
            win.blit(IM.MINE,(self.x,self.y))
            
    def Show_N(self,win):
        i = 0
        for spot in self.neighbors:
            i+=1
            if spot.colour == GREY:
                pygame.draw.circle(win,RED,(spot.x+spot.width//2,spot.y+self.width//2),5)
        pygame.display.update()
        
def draw_grid(win,rows,width):
    gap = width//rows
    for i in range (rows):
        pygame.draw.line(win,WHITE,((i*gap),0),(i*gap,width))
    for i in range (rows):
        pygame.draw.line(win,WHITE,(0,(i*gap)),(width,i*gap))

    
def draw(win,grid,rows,width,flags):
    win.fill(BLACK)
    for row in grid:
        for spot in row:
            spot.draw_rect(win)
    draw_grid(win,rows,width)
    Flag_counter(flags,win,width)
    pygame.display.update()

def Show_Mine(rows,grid,win):
    for row in grid:
        for spot in row:
            spot.Show_Mine(win)
        
    pygame.display.update()
    
def Make_Grid(rows,width,mines):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            Sq = Square(j,i,rows,gap)
            grid[i].append(Sq)
    i = 0
    while i != mines:
        x,y = random.randint(0,rows-1),random.randint(0,rows-1)
        Sq = grid[x][y]
        if Sq.mine == False:
            Sq.mine = True
            i+=1
            
    for row in grid:
        for spot in row:
            spot.update_neighbors(grid)
    for row in grid:
        for spot in row:
            spot.Find_Near()
    return grid

def Algo(grid,Sq,win,rows,width,flags):#on click, update neighbors, Find near,
    OpenSet = []
    OpenSet.append(Sq)
    while (len(OpenSet)) != 0:
        Sq = OpenSet[0]
        OpenSet.pop(0)     
        if Sq.mine_close != 0:
            Sq.colour = BLACK
        else:
            Sq.colour = BLACK
            for neighbor in Sq.neighbors:
                if neighbor.mine_close != 0:
                    neighbor.colour = BLACK
                else:
                    if neighbor.colour != BLACK:  
                        OpenSet.append(neighbor)
    draw(win,grid,rows,width,flags)

def text_objects(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def Win_Check(grid,rows,mines,win,width):
    i = 0
    for row in grid:
        for spot in row:
            if spot.mine == True and spot.flagged == True:
                i += 1
    if i == mines:
        Game_Over(win,False,width,rows,mines)

def Button(msg,x,y,w,h,ic,ac,action,width,rows,mines):
    global intro
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            intro = False
            action(win,width,rows,mines)
    else:
        pygame.draw.rect(win,ic,(x,y,w,h))

    smallText = pygame.font.Font('BERN.ttf',20)
    textSurf, textRect = text_objects(msg,smallText)
    textRect.center = ( (x+(w//2)),(y+h//2))
    win.blit(textSurf, textRect)

def Game_Intro():
    win = pygame.display.set_mode((800,800))
    intro = True
    win.fill(BLACK)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        win.blit(IM.BG,(0,0))
        Button("Beginner",300,300,200,100,BLACK,GREY,Main,450,9,10)
        Button("Intermediate",300,400,200,100,BLACK,GREY,Main,800,16,40)
        Button("Expert",300,500,200,100,BLACK,GREY,Main,1000,20,99)
        Button("Custom",300,600,200,100,BLACK,GREY,Custom_game,0,0,0)
        clock.tick(10)
        pygame.display.update()

def Custom_game(win,width,rows,mines):
    Custom()

def Flag_counter(flags,win,width):
    flags = str(flags)
    smallText = pygame.font.Font('BERN.ttf',30)
    textSurf, textRect = text_objects(flags,smallText)
    textRect.center = (25,width+25)
    win.blit(textSurf, textRect)
    pygame.display.update()
    

def Game_Over(win,player,width,rows,mines):
    print("HIT MINE")
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_y:
                    over  = False
                    Main(win,width,rows,mines)
        largeText = pygame.font.Font('BERN.ttf',30)
        if player == True:
            TextSurf, TextRect = text_objects(f"You have hit a mine, play again y or n?",largeText)
        else:
            TextSurf, TextRect = text_objects(f"You have won!!, play again y or n?",largeText)
            
        TextRect.center = ((width//2,width//2))
        win.blit(TextSurf,TextRect)
        pygame.display.update()
        clock.tick(15)
        
def Get_Click(pos,width,rows):
    gap = width//rows
    x,y = pos
    col = x//gap
    row = y//gap
    return col,row

def Tk_done():
    global entry1,entry2,window,intro
    Rows = entry1.get()
    Mines = entry2.get()
    Rows,Mines = int(Rows),int(Mines)
    if Rows > 20 or Mines > (Rows*Rows):
        print ("please choose smaller values")
        Custom()
    else:
        intro = False
        window.destroy()
        Main(win,Rows*50,Rows,Mines)

        
def Custom():
    global entry1,entry2,window
    window = tk.Tk()
    label = tk.Label(window,
                     text = "Custom Game",
                        fg = "white",
                        bg = "blue",
                        width = 10,
                        height = 1)
    
    frame_a = tk.Frame()
    frame_b = tk.Frame()
    frame_c = tk.Frame()

    labelR = tk.Label(master = frame_a,text = "Rows")
    labelM = tk.Label(master = frame_b,text = "Mines")

    entry1 = tk.Entry(master = frame_a)
    entry2 = tk.Entry(master = frame_b)

    button = tk.Button(master = frame_c,text = "Enter", command = Tk_done)

    label.pack()
    labelR.pack()
    labelM.pack()
    entry1.pack()
    entry2.pack()
    button.pack()
    frame_a.pack()
    frame_b.pack()
    frame_c.pack()
    
    window.mainloop()
    

def Main (win,width,rows,mines):
    win = pygame.display.set_mode((width,width+50))
    grid = Make_Grid(rows,width,mines)
    running = True
    flags = mines
    draw(win,grid,rows,width,flags)
    

    while running:
        draw(win,grid,rows,width,flags)
        pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #IM_Button(width//2 - 25,width,50,50,width,rows,mines)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    Main(win,width,rows,mines)
            if click[0]:
                if pos[1] < width:
                    col,row = Get_Click(pos,width,rows)
                    Sq = grid[col][row]
                    if Sq.colour == GREY:
                        Algo(grid,Sq,win,rows,width,flags)
                        
                    if Sq.mine == True:
                        Show_Mine(rows,grid,win)
                        Game_Over(win,True,width,rows,mines)
            if click[1]:
                if pos[1] < width:
                    col,row = Get_Click(pos,width,rows)
                    Sq = grid[col][row]
                    Sq.Show_N(win)
                
            if click[2]:
                if pos[1] < width:
                    col,row = Get_Click(pos,width,rows)
                    Sq = grid[col][row]
                    if Sq.flagged == True:
                        Sq.flagged = False
                        flags += 1
                    else:  
                        Sq.flagged = True
                        flags -=1
                    Win_Check(grid,rows,mines,win,width)
                
    clock.tick(60)
    pygame.display.update()
    
Game_Intro()
 
