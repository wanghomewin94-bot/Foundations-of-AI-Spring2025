#!/usr/bin/env python3
"""
Simple test script for Part 1 without GUI dependencies
"""

import sys
sys.path.insert(0, '.')

from maze import Maze
from search import bfs, astar

def test_maze(maze_path, method_name):
    print(f"\n{'='*60}")
    print(f"Testing {method_name.upper()} on {maze_path}")
    print(f"{'='*60}")
    
    maze = Maze(maze_path)
    start = maze.getStart()
    objectives = maze.getObjectives()
    
    print(f"Start position: {start}")
    print(f"Objectives: {objectives}")
    
    if method_name == "bfs":
        path = bfs(maze)
    elif method_name == "astar":
        path = astar(maze)
    else:
        print(f"Unknown method: {method_name}")
        return
    
    states_explored = maze.getStatesExplored()
    print(f"\nPath length: {len(path)}")
    print(f"States explored: {states_explored}")
    print(f"Path: {path}")
    
    # Validate path
    validation = maze.isValidPath(path)
    print(f"Validation: {validation}")
    
    return len(path), states_explored

if __name__ == "__main__":
    mazes = [
        "maps/single/tinyMaze.txt",
        "maps/single/mediumMaze.txt",
        "maps/single/bigMaze.txt",
    ]
    
    for maze_path in mazes:
        try:
            print(f"\n\n{'#'*60}")
            print(f"# {maze_path}")
            print(f"{'#'*60}")
            
            bfs_result = test_maze(maze_path, "bfs")
            astar_result = test_maze(maze_path, "astar")
            
            if bfs_result and astar_result:
                bfs_len, bfs_explored = bfs_result
                astar_len, astar_explored = astar_result
                print(f"\nComparison:")
                print(f"  BFS:   path_length={bfs_len}, states_explored={bfs_explored}")
                print(f"  A*:    path_length={astar_len}, states_explored={astar_explored}")
                if bfs_len == astar_len:
                    print(f"  ✓ Path lengths match!")
                if astar_explored <= bfs_explored:
                    print(f"  ✓ A* explores fewer or equal states!")
        except Exception as e:
            print(f"Error testing {maze_path}: {e}")
            import traceback
            traceback.print_exc()
