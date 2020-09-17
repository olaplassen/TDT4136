import numpy as np
np.set_printoptions(threshold=np.inf, linewidth=300)
import pandas as pd
import time
from PIL import Image


class Node():
    def __init__(self, parent=None, position=None):

        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
def astar(maze, start, goal):
    #Setting open and closed lists
    openList = []
    closedList = []

    #Defining start and end node and there g,h,f vaules
    start_node = Node(None, start)
    start_node.g = start_node.f = start_node.h = 0
    goal_node = Node(None, goal)
    goal_node.g = goal_node.f = goal_node.h = 0

    #Add the start node to the open list
    openList.append(start_node)

    # loop trough openList
    while len(openList) > 0:
        current_node = openList[0]
        current_index = 0

        #check if the node in first place of openlist is the node with lowest f vaule, if not change it
        for index, node in enumerate(openList):
            if current_node.f > node.f:
                current_node = node
                current_index = index
        #Move current node from open to closed list
        openList.pop(current_index)
        closedList.append(current_node)

        if current_node == goal_node:
            print("win")
            goal_path = []
            current = current_node
            while current is not None:
                goal_path.append(current.position)
                current = current.parent
            return goal_path[::-1] # return reversed array since we go from goal to start

        children = []
        for new_position in [(0, -1), (-1, 0), (0, 1), (1, 0)]:

            node_position = (current_node.position[0] + new_position[0]), (current_node.position[1] + new_position[1])
            #Sjekker at ny posisjon er innenfor kartet over samfundet
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            #Check that node position is a walkable posistion
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            #adding the new positions to the children array
            children.append(Node(current_node, node_position))
        #checking if the children is in the closed list
        for child in children:
            for closed_child in closedList:
                if child == closed_child:
                    continue
                #Finding g,h and f for children
            child.g = current_node.g + 1
                # Uses pythagoras to get h
            child.h = ((child.position[0] - goal_node.position[0]) ** 2) + ((child.position[1] - goal_node.position[1]) ** 2)
            child.f = child.g + child.h

            #Check if child is already discovered and if the already discoved node position ha higher g value
            for open_node in openList:
                if child == open_node and child.g > open_node.g:
                    continue
            openList.append(child)


def main():

# maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # df = pd.read_csv("Samfundet_map_1.csv", sep=',', index_col=None, header=None)
    # data = df.values
    # path = astar(df,startnode, goalnode)

    start,goal, end_goal_pos,path = map.fill_critical_positions(task)
    print(start,goal, end_goal_pos,path)

if __name__ == '__main__':
    main()
# def main():
#
#     task = 1
#     map = Map_Obj()
#
#     start,goal, _,path = map.fill_critical_positions(task)
#
#
#     maze,str = map.read_map(path)
#     #print(maze)
#
#
#
#     #map.show_map(str)
#
#
#     path = astar(maze, tuple(start), tuple(goal))
#     print(path)
#
# main()
