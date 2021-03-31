import math
import time
from collections import deque

class Puzzle:
    
    StateRepresentation = []
    size = None
    heuristic = 0
    parent = None
    child = None
    action = ""
    pathcost = 0
    statepath = ""

    def __init__(self,path):
        self.action = ""
        self.parent = None
        self.pathcost = 0
        self.StateRepresentation = []
        self.InitializePathToState(path)
        self.heuristic = self.h3()
    
    def getRoot(self):

        # print(self.statepath)  
        # if self.action != None:
        #     print("--> ", end='')
        #     print(self.action, end = '')
        #     print(" | f(n) = " + str(self.h3() + self.g(self.h3())))
        # if self.parent != None:
        #     self.parent.getRoot()

        if self.parent == None:
            return self 

        parentroot = self.parent.getRoot

        return parentroot
    
    def printPath(self):
        
        if self.child == None:
            return ""
        
        return self.statepath + " \n" + self.action + " \n" + self.child.printPath()

    def flatten(self):
        flattened = []

        for row in range(self.size):
            for column in range(self.size):
                flattened.append(self.StateRepresentation[row][column])

        return flattened

    def InitializePathToState(self,path):
        text = path.replace("(","").replace(")","")
        values = text.split(";")
        # "((4;3;2);(1;5;6);(7;8;9))"


        self.size = int(math.sqrt(len(values)))
        rownum = 0
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(values[rownum + j])
            self.StateRepresentation.append(row)
            rownum += self.size
        self.SetState()
        return
        #do stuff

    def SetState(self):
        path = "("
        for row in range(self.size):
            path += "("
            for column in range(self.size):
                path += str(self.StateRepresentation[row][column])
                if column != self.size - 1:
                    path += ";"
            path += ")"
            if row != self.size - 1:
                path += ";"
        path += ")"
        self.statepath = path
       # print("STATE SET TO: " + path)
        return path
         

    def SwapTile(self,row,column,direction):
        # print("attempting to swap tile at Position " + str(row*3+column + 1) + " in Direction " + direction)
        if direction == "up":
            if row == 0:
                # print("cannot swap up on top row")
                self.SetState()
                return False
            temp = self.StateRepresentation[row -1 ][column]
            self.StateRepresentation[row - 1][column] = self.StateRepresentation[row][column]
            self.StateRepresentation[row][column] = temp
        if direction == "down":
            if row == self.size - 1:
                # print("cannot swap down on bottom row")
                self.SetState()
                return False
            temp = self.StateRepresentation[row + 1][column]
            self.StateRepresentation[row + 1][column] = self.StateRepresentation[row][column]
            self.StateRepresentation[row][column]= temp
        if direction == "left":
            if column == 0:
                # print("cannot swap left on leftmost column")
                self.SetState()
                return False
            temp = self.StateRepresentation[row][column - 1]
            self.StateRepresentation[row][column - 1] = self.StateRepresentation[row][column]
            self.StateRepresentation[row][column] = temp
        if direction == "right":
            if column == (self.size - 1):
                # print("cannot swap right on rightmost column")
                self.SetState()
                return False
            temp = self.StateRepresentation[row][column + 1]
            self.StateRepresentation[row][column + 1] = self.StateRepresentation[row][column]
            self.StateRepresentation[row][column] = temp
        
        self.SetState()
        return True
            

    def PrintPuzzle(self):
        spacer = ""
        for i in range(self.size):
            spacer += "----"
        print(spacer)
        for row in self.StateRepresentation:
            for column in row:
               column.PrintTile()
            print()
        print(spacer)


    def TestGoalState(self):
        #print()
        # print("Testing State: " + str(self.statepath) + "...")
        for row in range(self.size):
            for column in range(self.size):
                if not self.TestTilePosition(row,column):
                    return False
        return True
        
      
        
    
    def TestTilePosition(self,row,column):
        # print()
       
        Puzzleindex = ((row * self.size) + column + 1)
        if int(self.StateRepresentation[row][column]) == Puzzleindex:
            # print("Position " + str(Puzzleindex) + " has the correct Tile: " + str(self.StateRepresentation[row][column]))
            return True
        else: 
            # print("Position " + str(Puzzleindex) + " has the wrong Tile: " + str(self.StateRepresentation[row][column]))
            return False

    def h1(self):
        # Hamming Distance
        hDistance = 0
        for row in range(self.size):
            for column in range(self.size):
                if not self.TestTilePosition(row,column):
                    hDistance += 1

        return hDistance

    def h2(self):
        # Manhattan Distance
        mDistance = 0
        for row in range(self.size):
            for column in range(self.size):
                if not self.TestTilePosition(row,column):
                    mDistance += 1
        return mDistance
    
    def h3(self):
        sum = 0
        flattened = self.flatten()
        
        for i in range(len(flattened)):
            for j in range(i,len(flattened)):
                if flattened[j] < flattened[i]:
                    #print(str(flattened[j] + 'is greater than ' + str(flattened[i])))
                    sum += 1
        
        return sum
    
    
    def g(self,h):
        if self.parent is not None:
            self.pathcost = self.parent.pathcost + h
        return self.pathcost
        
class Search:

    OpenList = deque()
    ClosedList = deque()
    Marked = deque()

    def __init__(self,path):
        self.initialState = Puzzle(str(path))
        self.OpenList = deque()
        self.ClosedList = deque()
        self.Marked = deque()
    
    def Successor(self,node):
        directions = ["up","down","left","right"]
        successors = []
        for row in range(node.size):
            for column in range(node.size):
                for direction in directions:
                
                    successor = Puzzle(node.statepath)
                    successor.SwapTile(row,column,direction)
                    node.child = successor
                    successor.parent = node
                    successor.action = "Tile " + str(successor.StateRepresentation[row][column]) + " at position +[" + str(row) + "][" + str(column) + "] moved " + direction
                        
                    if successor.statepath not in self.Marked:
                        self.Marked.append(successor.statepath)
                        successors.append(successor)
        return successors

    def DFS(self):
        self.OpenList.clear()
        self.ClosedList.clear()
        self.Marked.clear()
        
        self.OpenList.append(self.initialState)
        startTime = time.time()
        statesvisited = 0
        while self.OpenList:
            statesvisited += 1
            if statesvisited % 1000 == 0:
                print("states visited : " + str(statesvisited))
                print("time elapsed = " + str(time.time() - startTime))
            
            x = self.OpenList.pop()
            
            if x.TestGoalState():
                print("Solved")
                break
                return True
            else:
                children = self.Successor(x)
                self.ClosedList.append(x)
                for state in children:
                    if state.statepath not in self.Marked:
                        self.Marked.append(state.statepath)
                    self.OpenList.append(state)     
        return x.getRoot()
        
    def DepthLimitedSearch(self,limit,node):
            maxdepth = limit

            if node.TestGoalState(): 
                node.getRoot()
                return True
            
            if limit <= 0: return False
            
            children = self.Successor(node)

            for child in children:
                if self.DepthLimitedSearch((maxdepth - 1), child):
                    return True
        
            return False
            
    def IterativeDeepeningSearch(self, node):
        print()
        print("Implementing IDS on ", end = '')
        print(node.statepath)
        print("---------------------------------------")
        startTime = time.time()
        depth = 0
        while time.time() - startTime < 60:
            
            if depth % 10000 == 0:
                print("time elapsed = " + str(time.time() - startTime))
            if self.DepthLimitedSearch(depth,node):
                print("Success at depth: " + str(depth + 1))
                return True
            depth += 1
        print("No solution found up to depth " + str(depth))
        return False


    def AstarSearch(self):
        self.OpenList.clear()
        self.ClosedList.clear()
        self.Marked.clear()
        
        self.OpenList.append(self.initialState)

        startTime = time.time()
        statesvisited = 0
        print()
        print("Implementing A* on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")
        while self.OpenList:
            search = False
            statesvisited += 1
            if statesvisited % 5000 == 0:
                print("time elapsed = " + str(time.time() - startTime))
            
            if time.time() - startTime > 60:
                print("Search timed out after 60 seconds ...")
                print("No solution found")
                break
            
            x = self.OpenList.pop()

            #print("current state : " + str(x.statepath))
            if x.TestGoalState():
                print("Solved")
                root = x.getRoot()
                print(x.printPath())
                search = True
                return search
                break
            else:
                children = self.Successor(x)
                
                self.ClosedList.append(x)
                
                
                minchild = x
                for state in children:
                    if (state.h2() + state.g(state.h2())) <= (minchild.h2() + state.g(minchild.h2())):
                         minchild = state

                self.OpenList.append(minchild)     
        return search

import random
def generateRandomPuzzle(size,outnum):
    statenums = []
    numbers = []
    
    for i in range(size*size):
        numbers.append(i+1)

    for i in range(outnum):
        state = []
        for row in range(size):
            rows = []
            for column in range(size):
                rows.append(numbers[(row*size) + column])
            state.append(rows)
        random.shuffle(numbers)
        statenums.append(state)

    paths = []

    for i in statenums:
        path = "("
        for row in range(size):
            path += "("
            for column in range(size):
                path += str(i[row][column])
                if column != size - 1:
                    path += ";"
            path += ")"
            if row != size - 1:
                path += ";"
        path += ")"
        paths.append(path)

    return paths

def generateValidPuzzle(size,outnum):
    
    statenums = []
    numbers = []
    
    
    #fill numbers array with ordered numbers
    for i in range(size*size):
        numbers.append(i+1)


    for i in range(outnum):
        state = []
        for row in range(size):
            rows = []
            for column in range(size):
                rows.append(numbers[(row*size) + column])
            state.append(rows)
        statenums.append(state)

    direction = ["up","down","left","right"]
    paths = []

    for i in statenums:
        path = "("
        for row in range(size):
            path += "("
            for column in range(size):
                path += str(i[row][column])
                if column != size - 1:
                    path += ";"
            path += ")"
            if row != size - 1:
                path += ";"
        path += ")"
        paths.append(path)

    newpaths = []
    for path in paths:
        path = Puzzle(path)
        for i in range(random.randint(1,10)):
            path.SwapTile(random.randint(0,2),random.randint(0,2),random.choice(direction))
        path.SetState()
        path = path.statepath
        newpaths.append(path)

    return newpaths

# MAIN ___________________________________________________________________________________________________________________________________________________________
  
sn = generateValidPuzzle(3,20)

searchArr = []

for puzzlepaths in sn:
    search = Search(puzzlepaths)
    searchArr.append(search)

searchArr[1] = Search("((2;5;3);"
                        "(4;6;9);"
                        "(7;8;1))")

# searchArr[2] = Search("((2;3;6);"
#                         "(8;4;9);"
#                         "(7;1;5)")

for i in range(len(searchArr)):
    searchArr[i].AstarSearch()
    initialNode = searchArr[i].initialState
    searchArr[i].IterativeDeepeningSearch(initialNode)

