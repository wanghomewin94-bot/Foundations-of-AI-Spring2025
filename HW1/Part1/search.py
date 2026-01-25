# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022

"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

from collections import deque
import heapq

#search是一個總調度函數，根據searchMethod選擇對應的搜尋演算法
def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze) #.get()會回傳對應的函數，並執行該函數，傳入maze參數，maze參數是一個迷宮物件


def manhattan_distance(pos1, pos2): #回傳兩個位置的曼哈頓距離，作為A*的啟發式函數
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) #pos1和pos2是(row, col)的tuple形式


#parent是一個字典，紀錄每個節點的父節點，用來回溯路徑，定義一個函數reconstruct_path來回溯路徑
#start是起點，goal是終點，parent就是中間的連結
def reconstruct_path(parent, start, goal):
    """Reconstruct path from start to goal using parent dictionary."""
    path = [] #建立一個空的路徑列表
    current = goal #從終點開始回溯
    while current is not None: #當前節點不為None時，表示還沒回到起點
        path.append(current) #將當前節點加入路徑列表，append可以將元素加入列表的末尾
        current = parent.get(current) #取得當前節點的父節點，繼續回溯，.get()是字典的方法，可以取得對應鍵的值
    path.reverse() #將路徑列表反轉，因為是從終點回溯到起點，reverse()是python列表的方法，可以將列表反轉
    return path #回傳完整的路徑列表
#所以簡單來說它就是從goal開始，一直往parent字典中找它的父節點，直到找到start為止，然後把這些節點反轉回來，就得到從start到goal的路徑
#欸不是阿大哥，AI直接幫我打好我想要打的總結，是有點太牛逼，真棒


#恭喜你看了56行了，繼續加油，喔對，記得餵狗！

def bfs(maze): #廣度優先搜尋 (Breadth-First Search)
    """
    Runs BFS for part 1 of the assignment.
    
    State representation: (row, col) for position
    Goal test: reached a dot position
    
    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    #getStart()定義在maze.py中的第71行
    #maze物件有getStart()和getObjectives()方法，分別用來取得起點和目標點
    start = maze.getStart() #getStart()會回傳迷宮的起點位置，形式是(row, col)的tuple
    objectives = maze.getObjectives() #getObjectives()會回傳迷宮中所有目標點的位置，形式是list of (row, col)的tuple
    
    #在part 1，只有一個目標點（單一的點）
    #objectives的型態是list，所以可以用if not objectives來檢查是否為空
    if not objectives: #如果目標列表是空的，表示沒有目標點
        return [start] #直接回傳起點作為路徑，表示不需要移動
    
    goal = objectives[0] #就是去找下一個目標點，因為part1只有一個目標點，所以直接取list的第一個元素
    
    # BFS
    #使用deque作為隊列來實現BFS，定義在collections模組中，可參考 https://docs.python.org/zh-tw/3/library/collections.html#collections.deque
    #collection模組定義在python標準庫中，提供了許多有用的資料結構，是python內建的功能
    queue = deque([start]) #deque是雙端佇列，可以高效地從兩端添加和刪除元素，初始化時將起點加入隊列
    visited = {start} #使用集合來記錄已訪問的節點，初始化時將起點加入已訪問集合
    parent = {start: None} #使用字典來記錄每個節點的父節點，初始化時將起點的父節點設為None
    #從第58行道地87行這邊都是在做初始化，下面才會開始真正的BFS搜尋
    ##############################################################################
    #############          在下面開始實作BFS演算法          ##################
    ##############################################################################
    
    while queue: #當queue不為0時，表示還有節點要探索，繼續執行BFS；是0的話就表示所有節點都探索完了
        current = queue.popleft() #從隊列的左端取出當前節點，popleft()是deque的方法，可以高效地從左端刪除並回傳元素
        
        if current == goal: #如果當前節點是目標點，表示找到了路徑
            return reconstruct_path(parent, start, goal) #reconstruct_path()會回傳從起點到目標點的完整路徑，定義在46行到55行
        
        # Explore neighbors in the exact order returned by getNeighbors()
        #getNeighbors()定義在maze.py中的第100行，是我們自己定義的函式
        neighbors = maze.getNeighbors(current[0], current[1]) #回傳當前節點的鄰居列表，形式是list of (row, col)的tuple
        for neighbor in neighbors: #neighbors是鄰居列表，對每個鄰居進行迭代；neighbor是當前鄰居的(row, col)tuple
            if neighbor not in visited: #visited是已訪問集合，檢查當前鄰居是否已被訪問過，沒有的話就進行以下操作
                visited.add(neighbor) #把這個鄰居加入已訪問集合，表示已經訪問過了
                parent[neighbor] = current 
                queue.append(neighbor)
    
    # No path found
    return []


def astar(maze):
    """
    Runs A star for part 1 of the assignment.
    
    Uses Manhattan distance as heuristic.
    
    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    start = maze.getStart()
    objectives = maze.getObjectives()
    
    # For part 1, we have only one objective (single dot)
    if not objectives:
        return [start]
    
    goal = objectives[0]
    
    # A* search
    # Priority queue: (f_value, counter, position)
    counter = 0  # To break ties consistently
    heap = [(0, counter, start)]
    counter += 1
    
    visited = set()
    g_cost = {start: 0}  # Cost from start
    parent = {start: None}
    
    while heap:
        f_value, _, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == goal:
            return reconstruct_path(parent, start, goal)
        
        # Explore neighbors
        neighbors = maze.getNeighbors(current[0], current[1])
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            new_g_cost = g_cost[current] + 1
            
            if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_g_cost
                h_cost = manhattan_distance(neighbor, goal)
                f_cost = new_g_cost + h_cost
                parent[neighbor] = current
                heapq.heappush(heap, (f_cost, counter, neighbor))
                counter += 1
    
    # No path found
    return []

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
