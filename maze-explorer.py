import random
import utils

M = N = 40
empty_cell = " "
wall_cell = "X"
agent_cell = "A"
goal_cell = "G"
path_cell = "-"


# generate an empty maze, a filled unvisited set, and an empty visited set
maze = [[empty_cell for _ in range(N)] for _ in range(M)]
unvisited = {(a, b) for a in range(M) for b in range(N)}
visited = set()

# populate the maze with walls
maze = utils.generate_maze(maze, visited, unvisited, wall_cell, M, N)


# choose random goal and agent coords
agent_coords, goal_coords = utils.generate_agent_goal_coords(maze, empty_cell)
maze[agent_coords[0]][agent_coords[1]] = agent_cell
maze[goal_coords[0]][goal_coords[1]] = goal_cell


utils.visualize_maze(maze, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))

# at this point you have a generated maze, and coords of agent and goal.
# while developing the algorithm, you can comment out the visualizer call
# so that it doesn't open every time you test the code

# once we'll be done with actually solving the maze, I can add a visualization for that,
# showing how the agent moved