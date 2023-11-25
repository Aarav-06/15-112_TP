import random as rand
import math
from cmu_graphics import *

def onAppStart(app):
    app.width=800
    app.height=800
    app.mazeHeight=600
    app.mazeWidth=600
    resetApp(app)

def resetApp(app):
    app.rows=rand.randint(3,8)
    app.cols=rand.randint(5,12)
    app.maze,app.carveDirection=generateMaze(app.rows,app.cols)
    

def redrawAll(app):
    drawMaze(app) #function to draw maze


def drawMaze(app):
    #draw border of maze
    drawRect(app.width/2,app.height/2,app.mazeHeight,app.mazeWidth,
             align='center',border='black',fill=None)
    # loop over and add every wall (start-end coordinates) for each cell in maze
    # to a set.
    #  We only need to add the right wall and the bottom wall for each
    # cell as the upper wall and left wall of each cell is either shared with 
    # the border drawn earlier or an adjacent cell to right or cell above.
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
            if app.maze[row][col]==app.carveDirection[0]:
                # add top/bottom wall to set of walls to be removed
                deleteLines.add(((col*cellWidth+mazeLeft,
                                  (row+app.carveDirection[0]//2)*cellHeight+mazeTop),
                                  ((col+1)*cellWidth+mazeLeft,
                                   (row+app.carveDirection[0]//2)*cellHeight+mazeTop)))
            elif app.maze[row][col]==app.carveDirection[1]:
                # add left/right wall to set of walls to be removed
                deleteLines.add((((col+app.carveDirection[1]//2-1)*cellWidth+mazeLeft,
                                  row*cellHeight+mazeTop),
                                 ((col+app.carveDirection[1]//2-1)*cellWidth+mazeLeft,
                                  (row+1)*cellHeight+mazeTop)))
    # take difference of the two sets to have all walls that should be drawn
    drawSet=lineSet-deleteLines
    # draw all lines left in list/set to finally draw the maze
    for lineCoordinates in drawSet:
        drawLine(lineCoordinates[0][0],lineCoordinates[0][1],
                 lineCoordinates[1][0],lineCoordinates[1][1])


# I got all maze algorithms from https://www.youtube.com/watch?v=sVcB8vUFlmU
# generating maze using binary tree algorithm
# input number of rows and colums in 2-D list (maze)
def generateMaze(rows=5,cols=5):
    # make 2-D list of given dimension,
    maze=[[0]*cols for _ in range (rows)]
    # Randomly choose  tuple direction to carve wall in
    # tuple index 0 contains either 1 or 2
    # 1 refers to North, 2 refers to South
    # tuple index 1 contains either 3 or 4
    # 3 refers to West, 4 refers to East
    carveDirection= (rand.randint(1,2),rand.randint(3,4))
    # randomly "carve a wall" in each cell of maze by assigning an element from
    # carveDirection to the cell
    for row in range (rows):
        for col in range(cols):
            maze[row][col]=carveDirection[rand.randint(0,1)]
    if carveDirection[0]==1:
        # can't carve the walls of first row in north direction
        #carve in either east or west direction
        maze[0]=[carveDirection[1]]*cols
    elif carveDirection[0]==2:
        # can't carve the walls of last row in south direction
        #carve in either east or west direction
        maze[rows-1]=[carveDirection[1]]*cols
    if carveDirection[1]==3:
        # can't carve the walls of first column in west direction
        #carve in either north or south direction
        for row in range (rows):
            maze[row][0]=carveDirection[0]
    elif carveDirection[1]==4:
        # can't carve the walls of last column in east direction
        #carve in either north or south direction
        for row in range (rows):
            maze[row][cols-1]=carveDirection[0]
    if carveDirection==(1,3):
        #can't carve the top-left cell in either direction
        # set it back to 0
        maze[0][0]=0
    elif carveDirection==(1,4):
        #can't carve the top-right cell in either direction
        # set it back to 0
        maze[0][cols-1]=0
    elif carveDirection==(2,3):
        # can't carve the bottom-left cell in either direction
        #set it back to 0
        maze[rows-1][0]=0
    elif carveDirection==(2,4):
        #can't carve the bottom-right cell in either direction
        # set it back to 0
        maze[rows-1][cols-1]=0
    # return the final maze
    return maze,carveDirection

runApp()