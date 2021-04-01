import math
import time
import random
from collections import deque
from queue import PriorityQueue

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
        
        path = ""

        if self.parent == None:
            print(self.statepath)
            path += self.statepath + "\n"
        else:
            path += self.parent.printPath()
            print(self.action, end = '')
            path += self.action
            print(" --> ", end = "")
            path += " --> "
            print(self.statepath) 
            path += self.statepath + '\n'
        return path

        

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

    Frontier = PriorityQueue()
    OpenList = deque()
    ClosedList = deque()
    Marked = deque()

    def __init__(self,path):
        self.initialState = Node(str(path))
        self.OpenList = deque()
        self.ClosedList = deque()
        self.Marked = deque()
        self.Frontier = PriorityQueue()
    
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

        print()
        print("Implementing DFS on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")
        search = "Implementing DFS on " + str(self.initialState.statepath) + "\n" + "---------------------------------------\n"
        self.OpenList.clear()
        self.ClosedList.clear()
        self.Marked.clear()
        
        self.OpenList.append(self.initialState)
        startTime = time.time()

        elapsedtime = 0
        solutionFound = False
        cost = 0
        pathLength = 0

        while self.OpenList:
            if time.time() - startTime > 60:
                print("Search timed out after 60 seconds...")
                search += "Search timed out after 60 seconds...\n"
                break
            
            x = self.OpenList.pop()
            
            if x.TestGoalState():

                cost = x.depth
                pathLength = x.depth
                elapsedtime = time.time() - startTime
                solutionFound = True

                print("Solved")
                print("time elapsed = " + str(elapsedtime))
                search += "time elapsed = " + str(elapsedtime) + "\n"
                return search,elapsedtime,solutionFound,cost,pathLength
                break
            else:
                children = self.Successor(x)
                self.ClosedList.append(x)
                for state in children:
                    if state.statepath not in self.Marked:
                        self.Marked.append(state.statepath)
                    self.OpenList.append(state)     
        
        cost = x.depth
        pathLength = x.depth
        elapsedtime = 60

        return search,elapsedtime,solutionFound,cost,pathLength
        
    def DepthLimitedSearch(self,limit,node,startTime):
            result = False
            search = ''
            self.OpenList.clear()
            self.Marked.clear()

            self.OpenList.append(self.initialState)

            while self.OpenList:
                if time.time() - startTime > 60: break
                x = self.OpenList.pop()
                
                if x.TestGoalState(): 
                    search += x.printPath()
                    result = True
                    return result, search
                if  x.depth > limit: continue
                
                else:
                    children = self.Successor(x)
                    for state in children:
                        if state.statepath not in self.Marked:
                            self.Marked.append(state.statepath)
                        self.OpenList.append(state)
        
            return result, search
            
    def IterativeDeepeningSearch(self):
        print()
        print("Implementing IDS on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")
        search = "Implementing IDS on " + str(self.initialState.statepath) + "\n" + "---------------------------------------\n"
        startTime = time.time()
        depthlimit = 0

        elapsedtime = 60
        solutionFound = False
        cost = 0
        pathLength = 0

        while time.time() - startTime < 60:
            
            boolean,path = self.DepthLimitedSearch(depthlimit,self.initialState,startTime)
            if boolean:
                
                solutionFound = True
                elapsedtime = time.time() - startTime
                cost = depthlimit + 1
                pathLength = cost

                print("Success at depth: " + str(cost))
                print("time elapsed = " + str(elapsedtime))
                search += path
                return search,elapsedtime,solutionFound,cost,pathLength
                break
            
            depthlimit += 1
        print("Search timed out after 60 seconds...")
        print("No solution found up to depth " + str(depthlimit))
        search += "Search timed out after 60 seconds...\n"
        search += "No solution found up to depth " + str(depthlimit) + "\n"

        cost = depthlimit + 1
        pathLength = cost
        elapsedtime = 60

        return search,elapsedtime,solutionFound,cost,pathLength


    def AstarSearch(self):

        self.Frontier = PriorityQueue()
        self.Marked.clear()
        self.Frontier.put((0,self.initialState.statepath,self.initialState))
        startTime = time.time()
        search = "Implementing A* (h1) on " + str(self.initialState.statepath) + "\n" + "---------------------------------------\n"
        
        #Metrics
        elapsedtime = 0
        solutionFound = False
        cost = 0
        pathLength = 0

        print()
        print("Implementing A* (h1) on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")

        while not self.Frontier.empty():

            if time.time() - startTime > 60:
                print("Search timed out after 60 seconds ...")
                print("No solution found")
                search += "Search timed out after 60 seconds ...\n"
                search += "No solution found\n"
                break

            y = self.Frontier.get()
            x = y[2]
            pathLength = x.depth

            if x.TestGoalState():
    
                search += x.printPath()
                elapsedtime = time.time() - startTime
                cost = x.g(x.h1())
                solutionFound = True

                print("time elapsed = " + str(elapsedtime))
                search += "time elapsed = " + str(elapsedtime) + "\n"

                return search,elapsedtime,solutionFound,cost,pathLength
                break
            else:
                children = self.Successor(x)
                
                self.ClosedList.append(x)
                
                
                
                for state in children:
                    
                    score = state.h1() + state.g(state.h1())
                    self.Frontier.put((score, state.statepath,state))
    
        
        return search,elapsedtime,solutionFound,cost,pathLength

    def AstarSearch2(self):

        self.Frontier = PriorityQueue()
        self.Marked.clear()
        self.Frontier.put((0,self.initialState.statepath,self.initialState))
        startTime = time.time()
        search = "Implementing A* (h2) on " + str(self.initialState.statepath) + "\n" + "---------------------------------------\n"
        
        #Metrics
        elapsedtime = 0
        solutionFound = False
        cost = 0
        pathLength = 0

        print()
        print("Implementing A* (h2) on ", end = '')
        print(self.initialState.statepath)
        print("---------------------------------------")

        while not self.Frontier.empty():

            if time.time() - startTime > 60:
                print("Search timed out after 60 seconds ...")
                print("No solution found")
                search += "Search timed out after 60 seconds ...\n"
                search += "No solution found\n"
                break

            y = self.Frontier.get()
            x = y[2]
            pathLength = x.depth
            if x.TestGoalState():
    
                search += x.printPath()
                elapsedtime = time.time() - startTime
                cost = x.g(x.h2())
                solutionFound = True

                print("time elapsed = " + str(elapsedtime))
                search += "time elapsed = " + str(elapsedtime) + "\n"

                return search,elapsedtime,solutionFound,cost,pathLength
                break
            else:
                children = self.Successor(x)
                
                self.ClosedList.append(x)
                
                
                
                for state in children:
                    
                    score = state.h2() + state.g(state.h2())
                    self.Frontier.put((score, state.statepath,state))
    
        
        return search,elapsedtime,solutionFound,cost,pathLength


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

executionTimesDFS = []
executionTimesIDS = []
executionTimesA1 = []
executionTimesA2 = []

noSolutionDFS = []
noSolutionIDS = []
noSolutionA1 = []
noSolutionA2 = []

costDFS = []
costIDS = []
costA1 = []
costA2 = []

pathLengthDFS = []
pathLengthIDS = []
pathLengthA1 = []
pathLengthA2 = []



sn = generateValidPuzzle(3,20)

searchArr = []

for puzzlepaths in sn:
    search = Search(puzzlepaths)
    searchArr.append(search)

# searchArr[0] = Search("((1;6;3;4);"
#                         "(5;2;10;8);"
#                         "(9;16;7;11);"
#                         "(13;14;15;12);")

searchArr[1] = Search("((1;2;3);"
                        "(4;5;9);"
                        "(7;8;6)")

# Compute each path using four different algorithms
for i in range(len(searchArr)):
    filename = str(i) + "_" + sn[i] + ".txt"
    f = open(filename, "a")

    search,elapsedtime,solutionFound,cost,pathLength = searchArr[i].AstarSearch()
    executionTimesA1.append(elapsedtime)
    noSolutionA1.append(solutionFound)
    costA1.append(cost)
    pathLengthA1.append(pathLength)
    f.write(search)
    f.write("\n")

    search,elapsedtime,solutionFound,cost,pathLength = searchArr[i].IterativeDeepeningSearch()
    executionTimesIDS.append(elapsedtime)
    noSolutionIDS.append(solutionFound)
    costIDS.append(cost)
    pathLengthIDS.append(pathLength)
    f.write(search)
    f.write("\n")

    search,elapsedtime,solutionFound,cost,pathLength = searchArr[i].AstarSearch2()
    executionTimesA2.append(elapsedtime)
    noSolutionA2.append(solutionFound)
    costA2.append(cost)
    pathLengthA2.append(pathLength)
    f.write(search)
    f.write("\n")

    search,elapsedtime,solutionFound,cost,pathLength = searchArr[i].DFS()
    executionTimesDFS.append(elapsedtime)
    noSolutionDFS.append(solutionFound)
    costDFS.append(cost)
    pathLengthDFS.append(pathLength)
    f.write(search)
    
    f.close()


def calAverage(nums):
    total = 0
    for i in range(len(nums)):
        total += nums[i]
    average = total/len(nums)
    return average,total

def calNoSol(arr):
    total = len(arr)
    noSols = 0
    for i in arr:
        if i == False:
            noSols += 1
    percent = (noSols/total) * 100
    
    return percent, noSols


f = open("Report.txt", "a")
    f.write("A* 1\n")
    f.write("________________________________________________________________________________\n")
    average,total = calAverage(executionTimesA1)
    f.write("AVERAGE EXECUTION TIME: " + str(average) + "\n"))
    f.write("TOTAL EXECUTION TIME: " + str(total) + "\n"))
    average,total = calAverage(costA1)
    f.write("AVERAGE COST: " + str(average) + "\n"))
    f.write("TOTAL COST: " + str(total) + "\n"))
    average,total = calAverage(pathLengthA1)
    f.write("AVERAGE PATH LENGTH: " + str(average) + "\n"))
    f.write("TOTAL PATH LENGTH: " + str(total) + "\n"))
    average,total = calNoSol(noSolutionA1)
    f.write("AVERAGE NO SOLUTION: " + str(average) + "\n"))
    f.write("TOTAL NO SOLUTION: " + str(total) + "\n"))
    


    f.write("________________________________________________________________________________\n")
    f.write('\n')

    f.write("A* 2\n")
    f.write("________________________________________________________________________________\n")
    f.write("EXECUTION TIMES: ")
    f.write(str(executionTimesA2))
    f.write("________________________________________________________________________________\n")
    f.write('\n')

    f.write("IDS\n")
    f.write("________________________________________________________________________________\n")
    f.write("EXECUTION TIMES: ")
    f.write(str(executionTimesIDS))
    f.write("________________________________________________________________________________\n")
    f.write('\n')

    f.write("DFS\n")
    f.write("________________________________________________________________________________\n")
    f.write("EXECUTION TIMES: ")
    f.write(str(executionTimesDFS))
    f.write("________________________________________________________________________________\n")
    

