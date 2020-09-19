import numpy as np
import math
import sys
np.set_printoptions(threshold=np.inf, linewidth=300)
import pandas as pd
import time
from PIL import Image


class Map_Obj():

    def __init__(self, task):
        self.start_pos, self.goal_pos, self.end_goal_pos, self.path_to_map = self.fill_critical_positions(task)
        self.int_map, self.str_map = self.read_map(self.path_to_map)
        self.tmp_cell_value = self.get_cell_value(self.goal_pos)
        self.set_cell_value(self.start_pos, ' S ')
        self.set_cell_value(self.goal_pos, ' G ')
        self.tick_counter = 0
        # self.set_start_pos_str_marker(start_pos, self.str_map)
        # self.set_goal_pos_str_marker(goal_pos, self.str_map)

    def read_map(self, path):
        """
        Reads maps specified in path from file, converts them to a numpy array and a string array. Then replaces
        specific values in the string array with predefined values more suitable for printing.
        :param path: Path to .csv maps
        :return: the integer map and string map
        """
        print(path)
        # Read map from provided csv file
        df = pd.read_csv(path, index_col=None, header=None)  # ,error_bad_lines=False)
        # Convert pandas dataframe to numpy array
        data = df.values

        # Convert numpy array to string to make it more human readable
        data_str = data.astype(str)
        # Replace numeric values with more human readable symbols
        data_str[data_str == '-1'] = ' # '
        data_str[data_str == '1'] = ' . '
        data_str[data_str == '2'] = ' , '
        data_str[data_str == '3'] = ' : '
        data_str[data_str == '4'] = ' ; '

        return data, data_str

    def fill_critical_positions(self, task):
        """
        Fills the important positions for the current task. Given the task, the path to the correct map is set, and the
        start, goal and eventual end_goal positions are set.
        :param task: The task we are currently solving
        :return: Start position, Initial goal position, End goal position, path to map for current task.
        """
        global start_pos
        if task == 1:
            start_pos = [27, 18]
            goal_pos = [40, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 2:
            start_pos = [40, 32]
            goal_pos = [8, 5]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_1.csv'
        elif task == 3:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_2.csv'
        elif task == 4:
            start_pos = [28, 32]
            goal_pos = [6, 32]
            end_goal_pos = goal_pos
            path_to_map = 'Samfundet_map_Edgar_full.csv'
        elif task == 5:
            start_pos = [14, 18]
            goal_pos = [6, 36]
            end_goal_pos = [6, 7]
            path_to_map = 'Samfundet_map_2.csv'

        return start_pos, goal_pos, end_goal_pos, path_to_map

    def get_cell_value(self, pos):
        return self.int_map[pos[0], pos[1]]

    def get_goal_pos(self):
        return self.goal_pos

    def get_start_pos(self):
        return self.start_pos

    def get_end_goal_pos(self):
        return self.end_goal_pos

    def get_maps(self):
        # Return the map in both int and string format
        return self.int_map, self.str_map

    def move_goal_pos(self, pos):
        """
        Moves the goal position towards end_goal position. Moves the current goal position and replaces its previous
        position with the previous values for correct printing.
        :param pos: position to move current_goal to
        :return: nothing.
        """
        tmp_val = self.tmp_cell_value
        tmp_pos = self.goal_pos
        self.tmp_cell_value = self.get_cell_value(pos)
        self.goal_pos = [pos[0], pos[1]]
        self.replace_map_values(tmp_pos, tmp_val, self.goal_pos)
        print("move_goal")

    def set_cell_value(self, pos, value, str_map=True):
        if str_map:
            self.str_map[pos[0], pos[1]] = value
        else:
            self.int_map[pos[0], pos[1]] = value
        return self.str_map

    def print_map(self, map_to_print):
        # For every column in provided map, print it

        for column in map_to_print:
            print(column)

    def pick_move(self):
        """
        A function used for moving the goal position. It moves the current goal position towards the end_goal position.
        :return: Next coordinates for the goal position.
        """
        if self.goal_pos[0] < self.end_goal_pos[0]:
            return [self.goal_pos[0] + 1, self.goal_pos[1]]
        elif self.goal_pos[0] > self.end_goal_pos[0]:
            return [self.goal_pos[0] - 1, self.goal_pos[1]]
        elif self.goal_pos[1] < self.end_goal_pos[1]:
            return [self.goal_pos[0], self.goal_pos[1] + 1]
        else:
            return [self.goal_pos[0], self.goal_pos[1] - 1]

    def replace_map_values(self, pos, value, goal_pos):
        """
        Replaces the values in the two maps at the coordinates provided with the values provided.
        :param pos: coordinates for where we want to change the values
        :param value: the value we want to change to
        :param goal_pos: The coordinate of the current goal
        :return: nothing.
        """
        if value == 1:
            str_value = ' . '
        elif value == 2:
            str_value = ' , '
        elif value == 3:
            str_value = ' : '
        elif value == 4:
            str_value = ' ; '
        else:
            str_value = str(value)
        self.int_map[pos[0]][pos[1]] = value
        self.str_map[pos[0]][pos[1]] = str_value
        self.str_map[goal_pos[0], goal_pos[1]] = ' G '

    # def replace_goal_map(self, path):

    def tick(self):
        """
        Moves the current goal position every 4th call if current goal position is not already at the end_goal position.
        :return: current goal position
        """
        # For every 4th call, actually do something
        if self.tick_counter % 4 == 0:
            # The end_goal_pos is not set
            if self.end_goal_pos is None:
                return self.goal_pos
            # The current goal is at the end_goal
            elif self.end_goal_pos == self.goal_pos:
                return self.goal_pos
            else:
                # Move current goal position
                move = self.pick_move()
                self.move_goal_pos(move)
        self.tick_counter += 1

        return self.goal_pos

    def set_start_pos_str_marker(self, start_pos, map):
        # Attempt to set the start position on the map
        if self.int_map[start_pos[0]][start_pos[1]] == -1:
            self.print_map(self.str_map)
            print('The selected start position, ' + str(start_pos) + ' is not a valid position on the current map.')
            exit()
        else:
            map[start_pos[0]][start_pos[1]] = ' S '

    def set_goal_pos_str_marker(self, goal_pos, map):
        # Attempt to set the goal position on the map
        if self.int_map[goal_pos[0]][goal_pos[1]] == -1:
            self.print_map(self.str_map)
            print('The selected goal position, ' + str(goal_pos) + ' is not a valid position on the current map.')
            exit()
        else:
            map[goal_pos[0]][goal_pos[1]] = ' G '

    def show_map(self, path, map=None):
        """
        A function used to draw the map as an image and show it.
        :param map: map to use
        :return: nothing.
        """

        # If a map is provided, set the goal and start positions
        if map is not None:
            print(self.start_pos, self.goal_pos)
            self.set_start_pos_str_marker(self.start_pos, map)
            self.set_goal_pos_str_marker(self.goal_pos, map)
        # If no map is provided, use string_map
        else:
            map = self.str_map

        # Define width and height of image
        width = map.shape[1]
        height = map.shape[0]
        # Define scale of the image
        scale = 20
        # Create an all-yellow image
        image = Image.new('RGB', (width * scale, height * scale), (255, 255, 0))
        # Load image
        pixels = image.load()

        # Define what colors to give to different values of the string map (undefined values will remain yellow, this is
        # how the yellow path is painted)
        colors = {' # ': (255, 0, 0), ' . ': (215, 215, 215), ' , ': (166, 166, 166), ' : ': (96, 96, 96),
                  ' ; ': (36, 36, 36), ' S ': (255, 0, 255), ' G ': (0, 128, 255)}
        # Go through image and set pixel color for every position
        for y in range(height):
            for x in range(width):
                if map[y][x] not in colors: continue
                for i in range(scale):
                    for j in range(scale):
                        pixels[x * scale + i, y * scale + j] = colors[map[y][x]]

        # Show image
        image.show()


# Node Class
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# A* Implementation
def astar(maze, start, goal):
    # Defining start and end node and there g,h,f vaules
    start_node = Node(None, start)
    start_node.g = start_node.f = start_node.h = 0
    goal_node = Node(None, goal)
    goal_node.g = goal_node.f = goal_node.h = 0

    # Setting open and closed lists
    openList = []
    closedList = []

    # Add the start node to the open list
    openList.append(start_node)
    outer_Iterations = 0
    max_iterations = (len(maze) // 2) ** 5

    # loop trough openList
    while len(openList) > 0:

        current_node = openList[0]
        current_index = 0

        outer_Iterations += 1

        # check if the node in first place of openlist is the node with lowest f vaule, if not change it
        for index, item in enumerate(openList):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Max iterations to avoid endless loops
        if outer_Iterations > max_iterations:
            print("reached max iterations")
            return
        # Move current node from open to closed list
        openList.pop(current_index)
        closedList.append(current_node)
        if current_node == goal_node:
            print("Goal reached")
            goal_path = []
            current = current_node

            while current is not None:
                goal_path.append(current.position)

                current = current.parent
            # return reversed array since we go from goal to start
            return goal_path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Check if new position is inside maze
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Check that node position is a walkable position
            maze_position = maze[node_position[0]][node_position[1]]
            if (
                    maze_position != 1 and maze_position != 2 and maze_position != 3 and maze_position != 4
            ):
                continue

            # Adding the new node to the children array
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Checking if the children is in the closed list
        for child in children:
            childTimer1 = time.perf_counter()
            closed = False
            for closed_child in closedList:
                if child == closed_child:
                    closed = True
                    continue
            # Finding g,h and f for children
            if not closed:
                # Calculating g value based on current and the value of the node
                child.g = (current_node.g + maze[child.position[0]][child.position[1]])
                # The Euclidean Distance Heuristic
                #child.h = math.sqrt(((child.position[0] - goal_node.position[0]) ** 2) + (
                #        (child.position[1] - goal_node.position[1]) ** 2))
                child.h = round(math.sqrt(((child.position[0] - goal_node.position[0]) ** 2) + (
                            (child.position[1] - goal_node.position[1]) ** 2)))

                child.f = child.g + child.h

                # Check if child is already discovered and if the already discovered node position has higher g value
                if len(openList) > 0:
                    already = False
                    for open_node in openList:
                        if child == open_node and child.g > open_node.g:
                            already = True
                    if not already:
                        openList.append(child)
                else:
                    openList.append(child)
            childTimer2 = time.perf_counter()
            #print("Child timer in :", childTimer2 - childTimer1, " seconds")




def main(taskInput):
    # Specify which task
    task = taskInput

    # Initialise values with task value
    map = Map_Obj(task)
    # Finds start and goal as well as the path to the map we are using
    start, goal, _, path = map.fill_critical_positions(task)
    print("start node:", tuple(start))
    print("goal node:", tuple(goal))
    maze, str = map.read_map(path)

    # Find shortest path from start to goal and calculate time spend
    tic = time.perf_counter()
    goalPath = astar(maze, tuple(start), tuple(goal))
    toc = time.perf_counter()
    print("Found the goal in :", toc-tic, " seconds")

    # For every pixel in the goal path change the string representation of the map and run show map functions to
    # visualize shortest path
    i = 0
    for pathPixel in goalPath:
        i += 1
        goalMap = map.set_cell_value(pathPixel, ' - ')
        if i == len(goalPath) - 1:
            map.show_map(goalPath, goalMap)


if __name__ == '__main__':
    taskInput = int(sys.argv[1])
    main(taskInput)
