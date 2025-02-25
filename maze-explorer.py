import random
import utils
import heapq

M = N = 20
empty_cell = " "
wall_cell = "X"
agent_cell = "A"
goal_cell = "G"
path_cell = "-"

TIE_BREAK = "higher g"

## Initializing the maze and populating the maze with walls,
## creating an empty maze map which the agent uses, and 
## randomly placing an agent and the goal in some 2 empty cells
###############################################################

# generate an empty maze, a filled unvisited set, and an empty visited set
maze = [[empty_cell for _ in range(N)] for _ in range(M)]
maze_map = [[empty_cell for _ in range(N)] for _ in range(M)] 
unvisited = {(a, b) for a in range(M) for b in range(N)}
visited = set()

# populate the maze with walls
maze = utils.generate_maze(maze, visited, unvisited, wall_cell, M, N)

# choose random goal and agent coords
agent_coords, goal_coords = utils.generate_agent_goal_coords(maze, empty_cell)
maze[agent_coords[0]][agent_coords[1]] = agent_cell
maze[goal_coords[0]][goal_coords[1]] = goal_cell

# add coords for self and the goal
maze_map[agent_coords[0]][agent_coords[1]] = agent_cell
maze_map[goal_coords[0]][goal_coords[1]] = goal_cell






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





def solveMaze(agent_coords, maze_map, visualize = False):
  path = utils.find_shortest_path_with_AStar(agent_coords, goal_coords, maze_map, wall_cell, TIE_BREAK, M, N)
  path = path[::-1]

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
        print("agent hit a wall and had to stop")
        print(f"agent traveled {utils.manhattan_distance(path[0], agent_coords) + 1} cells")
        break

      # move agent to the new cell on the path
      maze_map[agent_coords[0]][agent_coords[1]] = empty_cell
      agent_coords = step
      maze_map[agent_coords[0]][agent_coords[1]] = agent_cell

      # look around, see if there are any walls. If there are, draw them on our map
      neighbor_walls = list(filter(lambda coords: maze[coords[0]][coords[1]] == wall_cell, utils.return_neibhors(agent_coords, M, N)))
      maze_map = utils.update_map_with_walls(neighbor_walls, maze_map, wall_cell)


    # show the result of moving along the path
    if visualize:
      utils.visualize_maze(maze_map, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))


    if agent_coords == goal_coords:
      print('goal reached!')
      return True
    else:
      # clear the path!
      for i, row in enumerate(maze_map):
        for k, _ in enumerate(row):
          if maze_map[i][k] == path_cell:
            maze_map[i][k] = empty_cell

      return solveMaze(agent_coords, maze_map, visualize)


  # if no valid path found (goal not reachable)
  else:
    print(f'path not found, goal coords are {goal_coords}')
    return False


res = solveMaze(agent_coords, maze_map, visualize = True)


utils.visualize_maze(maze, M, N, (empty_cell, wall_cell, agent_cell, goal_cell, path_cell))