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

##兒兒真棒，已經看超過一半了，真厲害！


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
            if not self.isValidMove(pos[0], pos[1]):#就前面定義的那個(95行)def isValidMove(self, row, col):
                return "Not valid move"

        # check whether it passes all goals
        #self.__objective是目標列表
        #issubset是檢查目標列表的每個目標是否都在路徑中出現過，是python提供的集合操作方法
        #set(path)是把路徑轉換成集合，這樣可以去除重複的點
        #拿來判斷是否全部點點都吃掉了，沒passed代表還沒吃完
        if not set(self.__objective).issubset(set(path)):
            return "Not all goals passed"

        # check whether it ends up at one of goals
        # path[-1]是路徑的最後一個位置，加not就是檢查最後一個位置是否在目標列表中
        # 翻成人話就是最後一個位置必須是目標位置之一才行
        if not path[-1] in self.__objective:
            return "Last position is not goal"

        # check for duplication
        # set(path)是把路徑轉換成集合，這樣可以去除重複的點
        # len(set(path)) != len(path)就是檢查路徑中是否有重複的點，如果有重複的點，就進行以下的檢查
        if len(set(path)) != len(path):
            c = Counter(path) #Counter是collections模組提供的工具，可以計算可迭代對象中每個元素出現的次數
            #下面這句比較難理解喔兒兒
            #dup_dots是找出所有在路徑中出現超過一次的點，不然就會變成同個位置被吃掉好幾次
            #c就是計算每個點出現次數的字典，c.elements()是返回一個包含所有元素的迭代器，set()是把它轉換成集合以去除重複
            #c[p] >= 2是檢查該點在路徑中出現的次數是否大於等於2，>=2的話代表被吃超過一次，打咩喔
            #下面要加中括號是因為要建立一個列表，裡面包含所有出現超過一次的點
            dup_dots = [p for p in set(c.elements()) if c[p] >= 2]
            for p in dup_dots:
                #indices是找出該重複點在路徑中所有出現的位置索引
                #原本寫法是indices = [i for i, dot in enumerate(path) if dot == p]
                #不過太難理解了，換個寫法，應該簡單很多
                indices = []  # 建立空列表存放索引
                for i in range(len(path)):  # 從0遍歷到路徑長度
                    if path[i] == p:  # 如果這個位置等於重複點p
                        indices.append(i)  # 把索引加入列表
                #假設是重複的，除非發現中間有目標點，True代表是重複的，False代表不是重複的
                #何時會變成False呢？就是在中間有目標點的時候
                is_dup = True 
                for i in range(len(indices) - 1):  # 逐對檢查同一點的相鄰兩次出現區間
                    for dot in path[indices[i]+1: indices[i + 1]]: #檢查這兩次出現之間的路徑點
                        if self.isObjective(dot[0], dot[1]): #若中間有目標點
                            is_dup = False #false代表不是重複的
                            break
                if is_dup:
                    return "Unnecessary path detected"
        return "Valid"
