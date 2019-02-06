from anytree import Node, RenderTree
import copy
import sys
import time
import psutil
import os
import operator
import datetime

count = 0
global goal
global stackData
global isGoal
global heuristic
global explored
stackData = []
explored=[]
isGoal = False
goal = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]

#to determine the position of each node to calculate manhattan distance
def position(k):
    for goalIndex in range(4):
        try:
            col = goal[goalIndex].index(k)
            row = goalIndex
        except ValueError:
                continue
    return row,col

#This function calculates the misplaced tiles and manhattan distance.
def NumMisplaced(input):
    if(heuristic=='MisplacedTiles'):
        tiles = 0
        r = 0
        for row in input:
            c = 0
            for i in row:
                if(input[r][c] != '0'):
                    if (input[r][c] != goal[r][c]):
                        tiles = tiles + 1
                c = c + 1
            r = r + 1
        return tiles
    else:
        sum = 0
        r = 0
        for row in input:
            c = 0
            for column in row:
                if (input[r][c] != '0'):
                    if (input[r][c] != goal[r][c]):
                        a, b = position(input[r][c])
                        sum = sum + abs(a - r) + abs(b - c)
                c = c + 1
            r = r + 1
        return sum

#This is the crux of the program. This calculates the movement of the tile
def movement(node):
    global stackData
    global explored


    global count
    for iterator in range(4):
        try:
            column = node.value[iterator].index("0")   #To calculate the position of the tile
            k = iterator
        except ValueError:
            continue
    row = k
    col = column

    if row > 0:   #To move upwards
        nodeBackup = copy.deepcopy(node.value)
        nodeBackup[row][col], nodeBackup[row - 1][col] = nodeBackup[row - 1][col], nodeBackup[row][col]

        if nodeBackup not in explored:
            variance = NumMisplaced(nodeBackup)
            variance = variance + node.depth + 1
            count = count + 1
            conc = "child" + str(count)
            explored.append(nodeBackup)
            nam = Node(conc, parent = node, value = nodeBackup, action = "up",manTile = variance)
            stackData.append(nam)
    if row < 3:     #To move downwards
        nodeBackup = copy.deepcopy(node.value)
        nodeBackup[row][col], nodeBackup[row + 1][col] = nodeBackup[row + 1][col], nodeBackup[row][col]
        if nodeBackup not in explored:
            variance = NumMisplaced(nodeBackup)
            variance = variance + node.depth + 1
            count = count + 1
            conc = "child" + str(count)
            explored.append(nodeBackup)
            nam = Node(conc, parent = node, value = nodeBackup, action = "down", manTile = variance)
            stackData.append(nam)
    if col > 0:     #To move leftwards
        nodeBackup = copy.deepcopy(node.value)
        nodeBackup[row][col], nodeBackup[row][col - 1] = nodeBackup[row][col - 1], nodeBackup[row][col]
        if nodeBackup not in explored:
            variance = NumMisplaced(nodeBackup)
            variance = variance + node.depth + 1
            count = count + 1
            conc = "child" + str(count)
            explored.append(nodeBackup)
            nam = Node(conc, parent = node, value = nodeBackup, action = "left", manTile = variance)
            stackData.append(nam)
    if col < 3:     #To move rights
        nodeBackup = copy.deepcopy(node.value)
        nodeBackup[row][col], nodeBackup[row][col + 1] = nodeBackup[row][col + 1], nodeBackup[row][col]
        if nodeBackup not in explored:
            variance = NumMisplaced(nodeBackup)
            variance = variance + node.depth + 1
            count = count + 1
            conc = "child" + str(count)
            explored.append(nodeBackup)
            nam = Node(conc, parent = node, value = nodeBackup, action = "right", manTile = variance)
            stackData.append(nam)

#This function performs the validations on the input array
def validations(inputArray):
    for index in range(len(inputString)):
        for iterator in range(len(inputString)):
            if (inputString[index] == inputString[iterator]):
                if (index != iterator):
                    print("Values are repeated")
                    return

if __name__ == "__main__":

    delimiter = 0
    inputString = []
    data = []

    print("Please enter the input with four values in a row with space as delimiter")       #To take input from the userr
    for index in range(4):
        inputData = input().strip().split(' ')                                  #removing whitespaces in the input provided
        inputString.append(inputData)

    validations(inputString)                                        #Call to perform validaations

    print("Choose the heuristic - 1: For Misplaced_tiles and 2 : Manhattan:")   #To choose the heuristic
    heuristicChosen = int(input())
    decision = {
        1:'MisplacedTiles',
        2:'ManhattanDistance'
    }
    heuristic = decision[heuristicChosen]
    startTime = datetime.datetime.now()
    discrepancy = NumMisplaced(inputString)
    rootNode = Node("root", parent = None, value = inputString, path = 0, action = "none", manTile = discrepancy)
    if (discrepancy == 0):
        print ("The Goal state is reached")
        print(rootNode.path)
    else:
        stackData.append(rootNode)
        explored.append(rootNode.value)
        while(isGoal == False and len(stackData)!= 0):   #To loop only when there is data
            currentNode = stackData.pop()

            if(currentNode.depth > delimiter):
                delimiter = currentNode.depth
                print("The time taken for execution is %s" % (datetime.datetime.now() - startTime) + " at depth:" + ' ' + str(delimiter))
                space = psutil.Process(os.getpid()).memory_info().rss
                print("The amount of memory consumed is %s" % space + ' ' + "at depth:" + ' ' + str(delimiter))
            if(currentNode.value == goal):
                print("The Goal is found")
                isGoal = True
                print(currentNode.path)
            else:
                movement(currentNode)
                stackData = sorted(stackData, key = lambda x: x.manTile, reverse = True)

    print("The total execution time taken is %s" % (datetime.datetime.now()- startTime))
    space = psutil.Process(os.getpid()).memory_info().rss
    print("The total memory consumed",space)
    print("The total depth of the tree",rootNode.height)
