import math
import time
from collections import deque

class Node:
    
    State = []
    size = None
    heuristic = 0
    parent = None
    child = None
    action = ""
    pathcost = 0
    statepath = ""
    depth = 0

    def __init__(self,path):
        self.depth = 0
        self.action = ""
        self.parent = None
        self.pathcost = 0
        self.State = []
        self.InitializePathToState(path)
        self.heuristic = self.h3()
    
    
    def printPath(self):
        
        
        if self.parent == None:
            print(self.statepath)
        else:
            self.parent.printPath()
            print(self.action, end = '')
            print(" --> ", end = "")
            print(self.statepath) 

        

    def flatten(self):
        flattened = []

        for row in range(self.size):
            for column in range(self.size):
                flattened.append(self.State[row][column])

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
            self.State.append(row)
            rownum += self.size
        self.SetState()
        return
        #do stuff

    def SetState(self):
        path = "("
        for row in range(self.size):
            path += "("
            for column in range(self.size):
                path += str(self.State[row][column])
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
        self.action = "Tile " + str(self.State[row][column]) + " at postion [" + str(row) + "][" + str(column) + "] moved " + direction + "\n"
        if direction == "up":
            if row == 0:
                # print("cannot swap up on top row")
                self.SetState()
                return False
            temp = self.State[row -1 ][column]
            self.State[row - 1][column] = self.State[row][column]
            self.State[row][column] = temp
        if direction == "down":
            if row == self.size - 1:
                # print("cannot swap down on bottom row")
                self.SetState()
                return False
            temp = self.State[row + 1][column]
            self.State[row + 1][column] = self.State[row][column]
            self.State[row][column]= temp
        if direction == "left":
            if column == 0:
                # print("cannot swap left on leftmost column")
                self.SetState()
                return False
            temp = self.State[row][column - 1]
            self.State[row][column - 1] = self.State[row][column]
            self.State[row][column] = temp
        if direction == "right":
            if column == (self.size - 1):
                # print("cannot swap right on rightmost column")
                self.SetState()
                return False
            temp = self.State[row][column + 1]
            self.State[row][column + 1] = self.State[row][column]
            self.State[row][column] = temp
        
        self.SetState()
        return True
            

    def PrintPuzzle(self):
        spacer = ""
        for i in range(self.size):
            spacer += "----"
        print(spacer)
        for row in self.State:
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
        print("Solved")
        self.printPath()
        return True
        
      
        
    
    def TestTilePosition(self,row,column):
        # print()
       
        Puzzleindex = ((row * self.size) + column + 1)
        if int(self.State[row][column]) == Puzzleindex:
            # print("Position " + str(Puzzleindex) + " has the correct Tile: " + str(self.State[row][column]))
            return True
        else: 
            # print("Position " + str(Puzzleindex) + " has the wrong Tile: " + str(self.State[row][column]))
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
        self.initialState = Node(str(path))
        self.OpenList = deque()
        self.ClosedList = deque()
        self.Marked = deque()
    
    def Successor(self,node):
        directions = ["up","down","left","right"]
        successors = []
        for row in range(node.size):
            for column in range(node.size):
                for direction in directions:
                
                    successor = Node(node.statepath)
                    successor.SwapTile(row,column,direction)
                    node.child = successor
                    successor.parent = node
                    successor.depth = successor.parent.depth + 1

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

        while self.OpenList:
            if time.time() - startTime < 60:
                print("Search timed out after 60 seconds...")
                break
            
            x = self.OpenList.pop()
            
            if x.TestGoalState():
                print("Solved")
                print("time elapsed = " + str(time.time() - startTime))
                return True
                break
            else:
                children = self.Successor(x)
                self.ClosedList.append(x)
                for state in children:
                    if state.statepath not in self.Marked:
                        self.Marked.append(state.statepath)
                    self.OpenList.append(state)     
        return False
        
    def DepthLimitedSearch(self,limit,node):
            result = False

            self.OpenList.clear()
            self.Marked.clear()

            self.OpenList.append(self.initialState)

            while self.OpenList:
                x = self.OpenList.pop()
                # print("ids state: " + str(x.statepath))
                if x.TestGoalState(): 
                    result = True
                    return result
                if  x.depth > limit: continue
                
                else:
                    children = self.Successor(x)
                    for state in children:
                        if state.statepath not in self.Marked:
                            self.Marked.append(state.statepath)
                        self.OpenList.append(state)
        
            return result
            
    def IterativeDeepeningSearch(self):
        

        print()
        print("Implementing IDS on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")
        startTime = time.time()
        depthlimit = 0
        while time.time() - startTime < 60:
            
            if self.DepthLimitedSearch(depthlimit,self.initialState):
                print("Success at depth: " + str(depthlimit + 1))
                print("time elapsed = " + str(time.time() - startTime))
                return True
            
            depthlimit += 1
        print("Search timed out after 60 seconds...")
        print("No solution found up to depth " + str(depthlimit))
        return False


    def AstarSearch(self):
        self.OpenList.clear()
        self.ClosedList.clear()
        self.Marked.clear()
        
        self.OpenList.append(self.initialState)

        startTime = time.time()

        print()
        print("Implementing A* on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")
        while self.OpenList:
            search = False
            
            if time.time() - startTime > 60:
                print("Search timed out after 60 seconds ...")
                print("No solution found")
                break
            
            x = self.OpenList.pop()

            #print("current state : " + str(x.statepath))
            if x.TestGoalState():
                print("time elapsed = " + str(time.time() - startTime))
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
        path = Node(path)
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

searchArr[0] = Search("((2;5;3);"
                        "(4;6;9);"
                        "(7;8;1))")

searchArr[1] = Search("((1;2;3);"
                        "(4;5;9);"
                        "(7;8;6)")

for i in range(len(searchArr)):
    searchArr[i].AstarSearch()
    searchArr[i].IterativeDeepeningSearch()

