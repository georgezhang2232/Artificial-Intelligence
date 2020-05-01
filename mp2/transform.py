
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    arm_limit = arm.getArmLimit()
    min_a, max_a = arm_limit[0]
    min_b, max_b = arm_limit[1]
    row = int( ((abs(max_a - min_a) / granularity)) + 1)
    col = int(((abs(max_b - min_b) / granularity)) + 1)

    maze_2d = [[SPACE_CHAR for i in range(col)] for j in range(row)]

    a_start_angle, b_start_angle = arm.getArmAngle()

    for i in range(min_a, max_a + 1):
        for j in range(min_b, max_b + 1):
            index = angleToIdx([i,j],[min_a,min_b],granularity)
            x = index[0]
            y = index[1]
            
            new_angle = idxToAngle([x,y], [min_a,min_b], granularity)
            arm.setArmAngle(new_angle)

            if x == angleToIdx([a_start_angle], [min_a], granularity)[0] and y == angleToIdx([b_start_angle], [min_b], granularity)[0]:
                maze_2d[x][y] = START_CHAR
            elif doesArmTipTouchGoals(arm.getEnd(), goals):
                maze_2d[x][y] = OBJECTIVE_CHAR
            elif doesArmTouchObjects(arm.getArmPosDist(), obstacles, False):
                maze_2d[x][y] = WALL_CHAR
            elif doesArmTouchObjects(arm.getArmPosDist(), goals, isGoal = True):
                maze_2d[x][y] = WALL_CHAR
            elif not isArmWithinWindow(arm.getArmPosDist(), window):
                maze_2d[x][y]= WALL_CHAR
            else:
                maze_2d[x][y] = SPACE_CHAR

    return Maze(maze_2d,[min_a,min_b],granularity)