import utils
import sys
import random

M = N = 101
empty_cell = " "
wall_cell = "X"
agent_cell = "A"
goal_cell = "G"
path_cell = "-"


# Configurable settings for the algorithm run
# Choose any tie breaking technique, any orientation (backward / forward),
# Choose if you want to visualize the maze
# Choose if you want to run large scale tests


# Two tie-breaking options
TIE_BREAK = "higher g"
#TIE_BREAK = "lower g"

# Forward vs Backward A*
orientation = 'normal'
# orientation = 'reverse'

visualize = False
# visualize = True

# after a demonstrative run of the algorithm, perform computation heavy tests such as:
# generate 50 mazes, try to solve them, do Forward vs Backward on them, do Adaptive vs Repeated,
# collect and print stats.
# performAllTests = False
performAllTests = True







## Initializing the maze and populating the maze with walls,
## creating an empty maze map which the agent uses, and 
## randomly placing an agent and the goal in some 2 empty cells
###############################################################

maze, maze_map, agent_coords, goal_coords = utils.generate_maze_and_maze_map(empty_cell, wall_cell, agent_cell, goal_cell, M, N)
agent_initial_coords = agent_coords




## Solving the maze. We're running A* on our maze_map and finding
## the best path relying on our knowledge of the maze
## A* returns the best path, and then we attempt to follow this
## path in the real maze. As we walk along the path, we take note
## of the walls we encounter as we walk, adding them to the map.
## if the alleged shortest path doesn't work (we hit a wall at some point)
## we run A* again, relying on the new wall knowledge we obtained as we walked
## along the initial path, and continue from where we stopped
###############################################################


# plot initial state neighbor walls
neighbor_walls = list(filter(lambda coords: maze[coords[0]][coords[1]] == wall_cell, utils.return_neibhors(agent_coords, M, N)))
maze_map = utils.update_map_with_walls(neighbor_walls, maze_map, wall_cell)


class MazeSolutionResult():
  def __init__(self, success, path_taken, numberOfExpandedCells):
    self.success = success
    self.path_taken = path_taken
    self.numberOfExpandedCells = numberOfExpandedCells

print(f"agent coords are {agent_coords}, goal coords are {goal_coords}")

def solveMaze(orientation, agent_coords, maze_map, overall_path_taken, visualize = False, expanded_cells = 0, heuristics_table = {}):
  path, local_expanded_cells = utils.find_shortest_path_with_AStar(orientation, agent_coords, goal_coords, heuristics_table, maze_map, wall_cell, TIE_BREAK, M, N)

  if path:
    # plot the path on the maze_map
    for index, coord in enumerate(path):
      if index != len(path) - 1:
        maze_map[coord[0]][coord[1]] = path_cell
    

    # show the projected path
    if visualize:
      utils.visualize_maze(maze_map, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))
    

    # move through the path, updating our map as we go
    for step in path:
      if maze_map[step[0]][step[1]] == wall_cell: # if the next step leads to a wall, stop
        #print("agent hit a wall and had to stop")
        #print(f"agent traveled {utils.manhattan_distance(path[0], agent_coords) + 1} cells")
        break

      # move agent to the new cell on the path
      maze_map[agent_coords[0]][agent_coords[1]] = empty_cell
      agent_coords = step
      overall_path_taken.append(agent_coords)
      maze_map[agent_coords[0]][agent_coords[1]] = agent_cell

      # look around, see if there are any walls. If there are, draw them on our map
      neighbor_walls = list(filter(lambda coords: maze[coords[0]][coords[1]] == wall_cell, utils.return_neibhors(agent_coords, M, N)))
      maze_map = utils.update_map_with_walls(neighbor_walls, maze_map, wall_cell)


    # show the result of moving along the path
    if visualize:
      utils.visualize_maze(maze_map, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))


    if agent_coords == goal_coords:
      #print('goal reached!')
      return MazeSolutionResult(True, overall_path_taken, expanded_cells)
    else:
      # clear the path!
      for i, row in enumerate(maze_map):
        for k, _ in enumerate(row):
          if maze_map[i][k] == path_cell:
            maze_map[i][k] = empty_cell

      return solveMaze(orientation, agent_coords, maze_map, overall_path_taken, visualize, expanded_cells + local_expanded_cells)


  # if no valid path found (goal not reachable)
  else:
    #print(f'path not found, goal coords are {goal_coords}')
    return MazeSolutionResult(False, overall_path_taken, expanded_cells)


res = solveMaze(orientation, agent_coords, maze_map, [], visualize)


## results visualization
########################

# draw out the overall path taken
for index, coords in enumerate(res.path_taken):
  if index != len(res.path_taken) - 1:
    maze_map[coords[0]][coords[1]] = path_cell

# reset goal and agent coords for demonstration
maze_map[goal_coords[0]][goal_coords[1]] = goal_cell
maze_map[agent_initial_coords[0]][agent_initial_coords[1]] = agent_cell

if visualize:
  # show overall path taken
  utils.visualize_maze(maze_map, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))

  # show true maze
  utils.visualize_maze(maze, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))







# Algorthims / Tie breaking techniques testing
##############################################
if not performAllTests:
  sys.exit(0)


## Forward vs Backward repeated A*, 
## run 50 mazes with both techniques and record the results
############################################################
import copy
forward_expanded_cells = backward_expanded_cells = 0

for i in range(50):
  maze, maze_map, agent_coords, goal_coords = utils.generate_maze_and_maze_map(empty_cell, wall_cell, agent_cell, goal_cell, M, N)
  agent_initial_coords = agent_coords
  maze_map_backward = copy.deepcopy(maze_map)

  resforward = solveMaze('normal', agent_coords, maze_map, [], visualize)
  resbackward = solveMaze('reverse', agent_coords, maze_map_backward, [], visualize)

  forward_expanded_cells += resforward.numberOfExpandedCells
  backward_expanded_cells += resbackward.numberOfExpandedCells

lower_g_expanded_cells = higher_g_expanded_cells = 0



## Higher G vs Lower G tie breaking for repeated A*,
## run 50 mazes with both techniques and record the results
##########################################################
for i in range(50):
  maze, maze_map, agent_coords, goal_coords = utils.generate_maze_and_maze_map(empty_cell, wall_cell, agent_cell, goal_cell, M, N)
  agent_initial_coords = agent_coords
  maze_map_lower_g = copy.deepcopy(maze_map)

  TIE_BREAK = "higher g"
  reshigherg = solveMaze('normal', agent_coords, maze_map, [], visualize)
  TIE_BREAK = "lower g"
  reslowerg = solveMaze('normal', agent_coords, maze_map_lower_g, [], visualize)
  

  higher_g_expanded_cells += reshigherg.numberOfExpandedCells
  lower_g_expanded_cells += reslowerg.numberOfExpandedCells





## Adaptive versus repeated forward A*
## create a single maze, and let both algorithms run on it with different start states
## and the same goal state, then record the results
######################################################################################
maze, maze_map, agent_coords, goal_coords = utils.generate_maze_and_maze_map(empty_cell, wall_cell, agent_cell, goal_cell, M, N)
adaptive_heuristics = {}
repeated_forward_expanded_cells = adaptive_expanded_cells = 0
for i in range(20):
  # generate a random start point
  while not agent_coords:
    candidate_agent_coords = (random.randint(0, M - 1), random.randint(0, N - 1))
    if maze_map[candidate_agent_coords[0]][candidate_agent_coords[1]] == empty_cell:
      maze_map[candidate_agent_coords[0]][candidate_agent_coords[1]] = agent_cell
      agent_coords = candidate_agent_coords
  
  initial_agent_coords = agent_coords
  
  # run repeated A*
  res_repeated = solveMaze(orientation, agent_coords, maze_map, [], visualize)

  # update the heuristics hashmap with the path taken
  for index, coords in enumerate(res_repeated.path_taken):
    if index != len(res_repeated.path_taken) - 1:
      approximate_g = index + 1
      heuristic = len(res_repeated.path_taken) - index - 1 # number of steps to the goal in the overall path

      if coords in adaptive_heuristics:
        adaptive_heuristics[coords] = min(adaptive_heuristics[coords], heuristic)
      else:
        adaptive_heuristics[coords] = heuristic
  


  # reset maze_map 
  if agent_coords == goal_coords:
    maze_map[agent_coords[0]][agent_coords[1]] = goal_cell
  else:
    maze_map[agent_coords[0]][agent_coords[1]] = empty_cell
  
  maze_map[initial_agent_coords[0]][initial_agent_coords[1]] = agent_coords

  # run adaptive A* from the same starting point with the heuristics map
  res_adaptive = solveMaze(orientation, agent_coords, maze_map, [], visualize, heuristics_table=adaptive_heuristics)

  # record results
  repeated_forward_expanded_cells += res_repeated.numberOfExpandedCells
  adaptive_expanded_cells += res_adaptive.numberOfExpandedCells

  # reset maze_map 
  if agent_coords == goal_coords:
    maze_map[agent_coords[0]][agent_coords[1]] = goal_cell
  else:
    maze_map[agent_coords[0]][agent_coords[1]] = empty_cell
  
  # allow agent_coords to be redefined
  agent_coords = None


import pandas as pd
results = {
    "Test Type": ["Forward vs Backward A*", "Higher g vs Lower g", "Repeated A* vs Adaptive A*"],
    "Forward/Repeated Expanded Cells": [forward_expanded_cells, higher_g_expanded_cells, repeated_forward_expanded_cells],
    "Backward/Lower g/Adaptive Expanded Cells": [backward_expanded_cells, lower_g_expanded_cells, adaptive_expanded_cells]
}

df_results = pd.DataFrame(results)
print(df_results)
print('Where Forward vs Backward A* is run on 50 mazes')
print('Higher g vs Lower g  is run on 50 mazes')
print('Repeated A* vs Adaptive A* is run on one maze 10 times')











  

  
