# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

import queue
import math
import itertools
import copy

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    myq = queue.Queue()
    myq.put(start)
    explored = []
    tree = {}
    tree[start] = None
    objective = maze.getObjectives()[0]
    while (not myq.empty()):
        top = myq.get()
        explored.append(top)
        neighbors = maze.getNeighbors(top[0], top[1])
        if objective in neighbors:
            tree[objective] = top
            break
        for neighbor in neighbors:
            if neighbor not in explored and maze.isValidMove(neighbor[0], neighbor[1]):
                tree[neighbor] = top
                explored.append(neighbor)
                myq.put(neighbor)
    #print(tree)
    path = [objective]
    temp = objective
    while (temp != start):
        path.append(tree[temp])
        temp = tree[temp]
    path.reverse()
    #print("Path is ", path)
    return path
    
def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    objective = maze.getObjectives()[0]
    start = maze.getStart()
    myq = queue.PriorityQueue()
    myq.put((abs(objective[0]-start[0]) + abs(objective[1]-start[1]), start))
    explored = []
    tree = {}
    length = 0
    while(not myq.empty()):
        top = myq.get()
        step = top[1]
        explored.append(step)
        neighbors = maze.getNeighbors(step[0],step[1])
        if objective in neighbors:
            tree[objective] = step
            break
        length = top[0] - abs(objective[0]-step[0]) - abs(objective[1]-step[1])
        length+=1
        for neighbor in neighbors:
            if neighbor not in explored:
                tree[neighbor] = step
                explored.append(neighbor)
                myq.put((length + abs(objective[0]-neighbor[0]) + abs(objective[1]-neighbor[1]), neighbor))
                #length+=1

        #print(list(myq.queue))
    path = [objective]
    temp = objective
    while (temp != start):
        path.append(tree[temp])
        temp = tree[temp]
    path.reverse()
    #print("Path is ", path)
    return path

def astar_2_point(maze, points):
    objective = points[1]
    start = points[0]
    myq = queue.PriorityQueue()
    myq.put((abs(objective[0]-start[0]) + abs(objective[1]-start[1]), start))
    explored = []
    tree = {}
    length = 0
    while(not myq.empty()):
        top = myq.get()
        step = top[1]
        explored.append(step)
        neighbors = maze.getNeighbors(step[0],step[1])
        if objective in neighbors:
            tree[objective] = step
            break
        length = top[0] - abs(objective[0]-step[0]) - abs(objective[1]-step[1])
        length+=1
        for neighbor in neighbors:
            if neighbor not in explored:
                tree[neighbor] = step
                explored.append(neighbor)
                myq.put((length + abs(objective[0]-neighbor[0]) + abs(objective[1]-neighbor[1]), neighbor))

    path = [objective]
    temp = objective
    while (temp != start):
        path.append(tree[temp])
        temp = tree[temp]
    path.reverse()
    length = len(path)
    return length, path

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
        
    @param maze: The maze to execute the search on.
        
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    start = maze.getStart()
    objective = maze.getObjectives()
    all_point = objective + [start]
    all_path = itertools.combinations(all_point, 2)
    combos = itertools.permutations(objective, 4)
    pathandlen = {}
    myq = queue.PriorityQueue()

    for each_path in all_path:
        length, path = astar_2_point(maze, (each_path[0], each_path[1]))
        pathandlen[(each_path[0], each_path[1])] = (length, path)
        newpath = copy.copy(path)
        newpath.reverse()
        pathandlen[(each_path[1], each_path[0])] = (length, newpath)

    for combo in combos:
        length2 = int(pathandlen[(start, combo[0])][0])
        temp = list(pathandlen[(start, combo[0])][1])
        for i in range(3):
            temp_length2 = int(pathandlen[(combo[i], combo[i+1])][0])
            temp_path2 = list(pathandlen[(combo[i], combo[i+1])][1])
            length2 += temp_length2
            temp.pop()
            temp += temp_path2
        myq.put((length2, temp))
    res = myq.get()[1]
    #print(res)
    #print("len is", len(res))
    return res


# class node
class edge_node:
    def __init__(self, x, y, g):
        self.x = x
        self.y = y
        self.walk = g
        self.weight = 0
        self.waitlist = []
        self.explored = []
    def __lt__(self, other):
        return self.weight < other.weight

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objective = maze.getObjectives()
    all_point = objective + [start]
    #table of all paths between objective with lenth ((1,1), (2,2)) : [3, [(1,1), (1,2), (2,2)]]
    combos = itertools.combinations(all_point, 2)
    frontier = queue.PriorityQueue()

    path = {}
    length = {}
    for combo in combos:
        edge_len, edge = astar_2_point(maze, combo)
        path[combo] = edge
        revese_edge = copy.copy(edge)
        revese_edge.reverse()
        path[(combo[1], combo[0])] = revese_edge
        length[combo] = edge_len 
        length[(combo[1], combo[0])] = edge_len 
    
    # s = mst_length(length, objective)
    #print(s)
    start_point = edge_node(start[0], start[1], 0)
    start_point.waitlist = objective.copy()
    start_point.explored.append((start[0], start[1]))
    frontier.put((start_point.weight, start_point))
    end_node = edge_node(0, 0, 0)

    while not frontier.empty():
        top = frontier.get()[1]
        if len(top.waitlist) == 0:
            end_node = top
            break
        for obj in top.waitlist:
            next_node = edge_node(obj[0], obj[1], 0)
            next_node.waitlist = top.waitlist.copy()
            next_node.waitlist.remove(obj)
            next_node.explored = top.explored.copy()
            next_node.explored.append(obj)
            mst = mst_length(length, next_node.waitlist)
            next_node.walk = top.walk + (length[((top.x, top.y), obj)] - 1)
            next_node.weight = mst + next_node.walk + len(next_node.waitlist)
            frontier.put((next_node.weight, next_node))

    res = [start]
    for i in range(len(end_node.explored) - 1):
        subpath = path[(end_node.explored[i], end_node.explored[i + 1])]
        subpath.pop(0)
        res += subpath
    return res
 

def mst_length(length, objective):
    if not objective:
        return 0
    objective = objective.copy()
    mst = 0
    done = []
    done.append(objective[0])
    while len(done) < len(objective):
        shortest = 100000
        for visit_edge in done:
            for novisit_edge in objective:
                if novisit_edge not in done:
                    temp_len = length[(visit_edge, novisit_edge)] - 2
                    if shortest == 100000 or shortest > temp_len:
                        shortest = temp_len
                        nearest = novisit_edge
        mst += shortest
        done.append(nearest)
    return mst
def sortfirst(val): 
    return val[0]  

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start = maze.getStart()
    objective = maze.getObjectives()
    myq = []
    for goal in objective:
        distance = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        myq.append((distance, goal))
    myq.sort(key = sortfirst)
    # print(myq)
    length, path = astar_2_extra(maze,(start, myq[0][1]))
    temp = start
    for i in range(len(objective) - 1):
        myq = []
        for goal in objective:
            distance = abs(temp[0] - goal[0]) + abs(temp[1] - goal[1])
            myq.append((distance, goal))
        myq.sort(key = sortfirst)
        nextpoint = myq[i][1]
        nextnext = myq[i+1][1]
        leng, subpath = astar_2_extra(maze, (nextpoint, nextnext))
        temp = subpath.pop(0)
        # print("subpath is", subpath)
        path += subpath

    return path
    # return astar_multi(maze)


def astar_2_extra(maze, points):
    objective = points[1]
    start = points[0]
    myq = queue.PriorityQueue()
    myq.put((abs(objective[0]-start[0]) + abs(objective[1]-start[1]), start))
    explored = []
    tree = {}
    while(not myq.empty()):
        top = myq.get()
        step = top[1]
        explored.append(step)
        neighbors = maze.getNeighbors(step[0],step[1])
        if objective in neighbors:
            tree[objective] = step
            break
        for neighbor in neighbors:
            if neighbor not in explored:
                tree[neighbor] = step
                explored.append(neighbor)
                myq.put((abs(objective[0]-neighbor[0]) + abs(objective[1]-neighbor[1]), neighbor))

    path = [objective]
    temp = objective
    while (temp != start):
        path.append(tree[temp])
        temp = tree[temp]
    path.reverse()
    length = len(path)
    return length, path


# def astar_2_extra(maze, points):
#     objective = points[1]
#     start = points[0]
#     myq = queue.PriorityQueue()
#     myq.put((abs(objective[0]-start[0]) + abs(objective[1]-start[1]), start))
#     explored = []
#     tree = {}
#     while(not myq.empty()):
#         top = myq.get()
#         step = top[1]
#         explored.append(step)
#         neighbors = maze.getNeighbors(step[0],step[1])
#         if objective in neighbors:
#             tree[objective] = step
#             break
#         for neighbor in neighbors:
#             if neighbor not in explored:
#                 tree[neighbor] = step
#                 explored.append(neighbor)
#                 myq.put((abs(objective[0]-neighbor[0]) + abs(objective[1]-neighbor[1]), neighbor))

#     path = [objective]
#     temp = objective
#     while (temp != start):
#         path.append(tree[temp])
#         temp = tree[temp]
#     path.reverse()
#     length = len(path)
#     return length, path