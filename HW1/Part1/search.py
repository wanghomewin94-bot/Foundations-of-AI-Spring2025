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

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)


def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def reconstruct_path(parent, start, goal):
    """Reconstruct path from start to goal using parent dictionary."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path


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
