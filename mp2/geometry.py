# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """
    x = start[0]
    y = start[1]
    rangle = math.radians(angle)
    cos = math.cos(rangle) 
    sin = math.sin(rangle)
    newx = x + int(length*cos)
    newy = y - int(length*sin)
    return (newx, newy)

#line point intersection distance calculation algorithm cite from stackoverflow
# https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment

def line_seg(start, end, object):
    temp = ( start[0] - end[0]) * ( start[0] - end[0]) + ( start[1] - end[1]) * ( start[1] - end[1])
    if temp == 0:
        return math.sqrt((object[0] - start[0])**2 + (object[1] - start[1])**2 )
    dot = (object[0] - start[0]) * (end[0] - start[0]) +  (object[1] - start[1]) * (end[1] - start[1])
    min_L = min( 1, dot/temp)
    max_L = max(0, min_L)
    result = (start[0] + max_L * (end[0] - start[0]), start[1] + max_L * (end[1] - start[1]))
    res = math.sqrt((result[0] - object[0])**2 + (result[1] - object[1])**2 )
    return res

def armTouchGoal(arm, goal):
    start, end, padding = arm
    distance = line_seg(start, end, goal)
    if distance <= goal[2]:
        return True
    return False


def armTouchObstacle(arm, obstacle):
    start, end, padding = arm
    # obstacle_x, obstacle_y, obstacle_r = obstacle
    distance = line_seg(start, end, obstacle)
    if distance <= obstacle[2] + padding:
        return True
    return False

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """
    # touch goal
    if isGoal is True:
        for arm in armPosDist:
            for goal in objects:
                if armTouchGoal(arm, goal) is True:
                    return True
    else:            
        for arm in armPosDist:
            for obstacle in objects:
                if armTouchObstacle(arm, obstacle) is True:
                    return True
    return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tip touch goals

        Args:
            armEnd (tuple): the arm tip position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tick touches any goal. False if not.
    """
    for goal in goals:
        arm_x, arm_y = armEnd
        goal_x, goal_y, goal_r = goal
        distance = math.sqrt((goal_x - arm_x)**2 + (goal_y - arm_y)**2 )
        if distance <= goal_r:
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    for arm in armPos:
        width, height = window
        start = arm[0]
        end = arm[1]
        x1, y1 = start
        x2, y2 = end
        if (x1 > width or x1 < 0) or (y1 > height or y1 < 0) or (x2 > width or x2 < 0) or (y2 > height or y2 < 0):
            return False
    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    # print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))

    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
