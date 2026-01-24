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

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.
    
    State representation: (row, col) for position
    Goal test: reached a dot position
    
    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    start = maze.getStart()
    objectives = maze.getObjectives()
    
    # For part 1, we have only one objective (single dot)
    if not objectives:
        return [start]
    
    goal = objectives[0]
    
    # BFS
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            return reconstruct_path(parent, start, goal)
        
        # Explore neighbors in the exact order returned by getNeighbors()
        neighbors = maze.getNeighbors(current[0], current[1])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
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
