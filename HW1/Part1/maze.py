# maze.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This file contains the Maze class, which reads in a maze file and creates
a representation of the maze that is exposed through a simple interface.
"""

from operator import pos
import re
import copy
from collections import Counter

class Maze:
    # Initializes the Maze object by reading the maze from a file
    def __init__(self, filename):
        self.__filename = filename
        self.__wallChar = '%'
        self.__startChar = 'P'
        self.__objectiveChar = '.'
        self.__start = None
        self.__objective = []
        self.__states_explored = 0

        with open(filename) as f:
            lines = f.readlines()

        lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
        lines = [list(line.strip('\n')) for line in lines]
#看到這兒而兒兒而兒而兒而兒而
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.mazeRaw = lines

        # 檢查所有行是否長度一致
        for row in lines:
            if len(row) != self.cols:
                print("Maze dimensions incorrect")
                raise SystemExit

        for row in range(len(self.mazeRaw)):
            for col in range(len(self.mazeRaw[0])):
                if self.mazeRaw[row][col] == self.__startChar:
                    self.__start = (row, col)
                elif self.mazeRaw[row][col] == self.__objectiveChar:
                    self.__objective.append((row, col))

    # Returns True if the given position is the location of a wall
    # 是否為牆壁
    def isWall(self, row, col):
        return self.mazeRaw[row][col] == self.__wallChar

    # Rturns True if the given position is the location of an objective
    # 檢查該位置是否為目標
    def isObjective(self, row, col):
        return (row, col) in self.__objective

    # Returns the start position as a tuple of (row, column)
    # 返回起點座標
    def getStart(self):
        return self.__start

    #設定新的起點
    def setStart(self, start):
        self.__start = start

    # Returns the dimensions of the maze as a (row, column) tuple
    #返回起點座標
    def getDimensions(self):
        return (self.rows, self.cols)

    # Returns the list of objective positions of the maze
    #回去目標座標的列表，deepcopy是為了避免外部修改目標列表，造成迷宮物件內部狀態不一致
    def getObjectives(self):
        return copy.deepcopy(self.__objective)

    #就是設定下一棵要去吃的點點
    def setObjectives(self, objectives):
        self.__objective = objectives

    #返回探索的狀態數量，作為評估演算法效率的指標
    ##有點不懂
    def getStatesExplored(self):
        return self.__states_explored

    # Check if the agent can move into a specific row and column
    #檢查移動是否合法（在邊界內且不是牆）
    def isValidMove(self, row, col):
        return row >= 0 and row < self.rows and col >= 0 and col < self.cols and not self.isWall(row, col)

    # Returns list of neighboing squares that can be moved to from the given row,col
    #返回鄰近可移動的方格列表
    def getNeighbors(self, row, col):
        possibleNeighbors = [
            (row + 1, col),
            (row - 1, col),
            (row, col + 1),
            (row, col - 1)
        ]
        neighbors = [] ##建立一個空的鄰居列表
        for r, c in possibleNeighbors:
            if self.isValidMove(r,c):
                neighbors.append((r,c)) ##append是把符合條件的鄰居加入列表
        self.__states_explored += 1 ##每檢查一個鄰居就把探索狀態數量加一，作為前面說的評估演算法效率的指標
        #阿這個在part1很重要，因為要去看最後兩個演算法的效率
        return neighbors

    def isValidPath(self, path):
        
        #檢查path的格式是否正確（類型，非空）
        #不合格的例子：
        #path = ((1, 2), (1, 3), (2, 3))  # 用元組而不是列表 ❌
        #path = {(1, 2), (1, 3), (2, 3)}  # 用集合 ❌
        #path = "(1,2),(1,3)"              # 用字串 ❌
        #合格的例子：
        #path = [(1, 2), (1, 3), (2, 3)]  # 用列表 ✅
        if not isinstance(path, list):
            return "path must be list"

        if len(path) == 0:#路徑不能是0
            return "path must not be empty"

        #tuple就是(1,2)這種東西
        #這就只是在說位置必須是(x, y)這種格式，二維移動就是一X和Y
        #原本是檢查path[0]，但這樣不夠全面，應該檢查整個path裡面的每一個位置，所以改成下面這個寫法
        #檢查每個位置(pos)是否為tuple且長度為2
        for pos in path:
            if not isinstance(pos, tuple) or len(pos) != 2:
                return "Invalid position format"

        # check single hop
        #曼哈頓距離必須是1
        #range從1開始是因為要和前一個位置比較，len(path)是路徑長度
        #所以她就是在說從路徑的第二個位置開始，一直到最後一個位置
        #不從第一個位置開始是因為第一個位置沒有前一個位置可以比較
        for i in range(1, len(path)): 
            prev = path[i-1] #previous position
            cur = path[i] #current position
            dist = abs((prev[1]-cur[1])+(prev[0]-cur[0])) #[1]是X座標，[0]是Y座標
            if dist > 1:
                return "Not single hop" #一次只能移動一格

        # check whether it is valid move
        for pos in path:
            if not self.isValidMove(pos[0], pos[1]):
                return "Not valid move"

        # check whether it passes all goals
        if not set(self.__objective).issubset(set(path)):
            return "Not all goals passed"

        # check whether it ends up at one of goals
        if not path[-1] in self.__objective:
            return "Last position is not goal"

        # check for duplication
        if len(set(path)) != len(path):
            c = Counter(path)
            dup_dots = [p for p in set(c.elements()) if c[p] >= 2]
            for p in dup_dots:
                indices = [i for i, dot in enumerate(path) if dot == p]
                is_dup = True
                for i in range(len(indices) - 1):
                    for dot in path[indices[i]+1: indices[i + 1]]:
                        if self.isObjective(dot[0], dot[1]):
                            is_dup = False
                            break
                if is_dup:
                    return "Unnecessary path detected"
        return "Valid"
