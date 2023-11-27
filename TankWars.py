import random as rand
import math
from cmu_graphics import *

def onAppStart(app):
    app.pause=False
    app.stepsPerSecond=1
    app.width=800
    app.height=800
    app.mazeHeight=600
    app.mazeWidth=600
    resetApp(app)

def resetApp(app):
    app.timer=0
    app.score=(0,0)
    app.rows=rand.randint(3,8)
    app.cols=rand.randint(3,8)
    app.maze=[[0]*app.cols for _ in range (app.rows)]
    app.startLocation=((rand.randrange(app.rows),rand.randrange(app.cols)))
    generateMaze(app)
    #set of lines to draw in maze (walls of maze)
    app.drawSet=mazeWalls(app)
    
def gameReset(app):
    onAppStart(app)

def redrawAll(app):
    drawLabel(f"Score:{app.score[0]}-{app.score[1]}",350,75,align='center',size=16)
    drawMaze(app) # call function to draw maze

# draw the maze
def drawMaze(app):
    #draw border of maze
    drawRect(app.width/2,app.height/2,app.mazeHeight,app.mazeWidth,
             align='center',border='black',fill=None)
    # draw all walls of the maze
    for lineCoordinates in app.drawSet:
        drawLine(lineCoordinates[0][0],lineCoordinates[0][1],
                 lineCoordinates[1][0],lineCoordinates[1][1])


# I got all maze algorithms from https://www.youtube.com/watch?v=sVcB8vUFlmU
# generating maze using DFS
# input number of rows and colums in 2-D list (maze)
def generateMaze(app):
    visited=set()
    generateMazeHelper(app,app.startLocation,visited)

#Helper function for maze generation
def generateMazeHelper(app,location,visited):
    visited.add(location)
    if  len(visited)==app.rows*app.cols:
        return None
    neighbors=neighborCells(location,app.rows,app.cols)
    for neighbor in neighbors:
        if neighbor not in visited:
            addPath(app,location,neighbor)
            generateMazeHelper(app,neighbor,visited)

 # function to find neighboring cells       
def neighborCells(location,rows,cols):
    neighbors=set()
    for row in range(location[0]-1,location[0]+2,2):
        if 0<=row<rows:
            neighbors.add((row,location[1]))
    for col in range(location[1]-1,location[1]+2,2):
        if 0<=col<cols:
            neighbors.add((location[0],col))
    return neighbors

# function to add path (carve walls in maze)
def addPath(app,location,neighbor):
    cell=app.maze[location[0]][location[1]]
    if neighbor[0]>location[0]:
        cell=(cell*10)+2 # south wall
    elif neighbor[0]<location[0]:
        cell=(cell*10)+1 # north wall
    elif neighbor[1]>location[1]:
        cell=(cell*10)+4 # east wall
    elif neighbor[1]<location[1]:
        cell=(cell*10)+3  # west wall
    app.maze[location[0]][location[1]]=cell


def mazeWalls(app):
    # loop over and add every wall (start-end coordinates) for each cell in maze
    # to a set.
    #  We only need to add the right wall and the bottom wall for each
    # cell as the upper wall and left wall of each cell is either shared with 
    # the border drawn earlier or an adjacent cell to right or cell above.
    # draw all lines left in list/set to finally draw the maze
    lineSet=set()
    mazeLeft= app.width/2-app.mazeWidth/2 # left border of maze
    mazeTop= app.height/2-app.mazeHeight/2 # top border of maze
    cellHeight=app.mazeHeight/app.rows
    cellWidth=app.mazeWidth/app.cols
    for row in range(app.rows):
        for col in range(app.cols):
            # if row is not last row, add bottom wall
            if row!=app.rows-1:
                lineSet.add(((col*cellWidth+mazeLeft,(row+1)*cellHeight+mazeTop),
                            ((col+1)*cellWidth+mazeLeft,(row+1)*cellHeight+mazeTop)))
            # if col is not last col, add right wall
            if col!=app.cols-1:
                lineSet.add((((col+1)*cellWidth+mazeLeft,row*cellHeight+mazeTop),
                            ((col+1)*cellWidth+mazeLeft,(row+1)*cellHeight+mazeTop)))
    # find walls to delete by looping over 2-D list maze and add to a set
    deleteLines=set()
    for row in range(app.rows):
        for col in range(app.cols):
            value=app.maze[row][col]
            while value>0:
                wall=value%10
                value=value//10
                if wall==1:
                    #add north wall to delete
                    deleteLines.add(((col*cellWidth+mazeLeft,
                                  row*cellHeight+mazeTop),
                                  ((col+1)*cellWidth+mazeLeft,
                                   row*cellHeight+mazeTop)))
                elif wall==2:
                    #add south wall to delete
                    deleteLines.add(((col*cellWidth+mazeLeft,
                                  (row+1)*cellHeight+mazeTop),
                                  ((col+1)*cellWidth+mazeLeft,
                                   (row+1)*cellHeight+mazeTop)))
                elif wall==3:
                    #add west wall to delete
                    deleteLines.add(((col*cellWidth+mazeLeft,
                                  row*cellHeight+mazeTop),
                                  (col*cellWidth+mazeLeft,
                                  (row+1)*cellHeight+mazeTop)))
                else:
                    #add east wall to delete
                    deleteLines.add((((col+1)*cellWidth+mazeLeft,
                                  row*cellHeight+mazeTop),
                                  ((col+1)*cellWidth+mazeLeft,
                                  (row+1)*cellHeight+mazeTop)))
    # take difference of the two sets to have all walls that should be drawn
    drawSet=lineSet-deleteLines
    return drawSet

def onKeyPress(app,key):
    if key=='r':
        resetApp(app)
    elif key=='R':
        gameReset(app) 

# class for storing tank (player) information
class tank:
    counter=0
    def __init__(self,x,y,color):
        tank.counter+=1
        self.x=x # x-coordinate of tank 
        self.y=y # y-coordinate of tank
        self.color=color #color of tank
        self.player=tank.counter # player number
        self.rotation=0 # roatation of tank's gun
        # at any given time only 5 bullets shot by the player must be active
        # bullets dissipate after some time (TBD)
        self.bullets={1:None,2:None,3:None,4:None,5:None} 
    
    def rotateTank(self): # rotating the tank
        self.rotation+=36
        if self.rotation==360:
            self.rotation=0
    
    def moveTank(self,dx,dy): # movement direction of tank
        self.x+=5*dx #moving tank left/right
        self.y+=5*dy #moving tank up/down

    def shootBullet (self):
        for key in self.bullets:
            # if bullets shot do not exceed 5, store the info of shot bullet
            if self.bullets[key]==None:
                self.bullets[key]=(self.x,self.y,self.rotation,0)

def onStep(app):
    if not app.pause:
        takeStep(app)

def takeStep(app):
    pass

runApp()