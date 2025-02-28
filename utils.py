import random
import pygame
import utils
import heapq

### maze generation related
def return_unvisited_neibhors(coords, visited, M, N):
  i, j = coords
  res = []
  if i + 1 < M and (i + 1, j) not in visited:
    res.append((i + 1, j))

  if i - 1 >= 0 and (i - 1, j) not in visited:
    res.append((i - 1, j))


  if j + 1 < N and (i, j + 1) not in visited:
    res.append((i, j + 1))

  if j - 1 >= 0 and (i, j - 1) not in visited:
    res.append((i, j - 1))

  return res


def fill_maze(maze, visited, unvisited, wall_cell, M, N):
  # repeatedly choose a rand starting point, run a full DFS from it, and do it until
  # all nodes are visited
  while unvisited:

    # choose a random starting point
    start = random.sample(list(unvisited), 1)[0]

    # do DFS on the maze from a given starting point, until all options are exhausted
    stack = [start]
    while stack:
      current = stack[-1]

      if current not in visited:
        if random.random() < 0.3:
          maze[current[0]][current[1]] = wall_cell
        
        visited.add(current)
        unvisited.remove(current)


      neibhors = utils.return_unvisited_neibhors(current, visited, M, N)
      if neibhors:
        next = random.sample(neibhors, 1)[0]
        stack.append(next)

      else:
        stack.pop()
  return maze

def generate_agent_goal_coords(maze, empty_cell):
  empty_cells = []
  for i, row in enumerate(maze):
    for j, cell in enumerate(row):
      if cell == empty_cell:
        empty_cells.append((i, j))
  return random.sample(empty_cells, 2)


def generate_maze_and_maze_map(empty_cell, wall_cell, agent_cell, goal_cell, M, N):
  # generate an empty maze, a filled unvisited set, and an empty visited set
  maze = [[empty_cell for _ in range(N)] for _ in range(M)]
  maze_map = [[empty_cell for _ in range(N)] for _ in range(M)] 
  unvisited = {(a, b) for a in range(M) for b in range(N)}
  visited = set()

  # populate the maze with walls
  maze = utils.fill_maze(maze, visited, unvisited, wall_cell, M, N)

  # choose random goal and agent coords
  agent_coords, goal_coords = utils.generate_agent_goal_coords(maze, empty_cell)
  maze[agent_coords[0]][agent_coords[1]] = agent_cell
  maze[goal_coords[0]][goal_coords[1]] = goal_cell

  # add coords for self and the goal
  maze_map[agent_coords[0]][agent_coords[1]] = agent_cell
  maze_map[goal_coords[0]][goal_coords[1]] = goal_cell

  return [maze, maze_map, agent_coords, goal_coords]



### visualization

def visualize_maze(maze, M, N, symbols):
  empty_cell, wall_cell, agent_cell, goal_cell, path_cell = symbols

  UI_WIDTH = 200
  SCREEN_WIDTH = 600 + UI_WIDTH
  SCREEN_HEIGHT = 600

  CELL_SIZE = min((SCREEN_WIDTH - UI_WIDTH) // N, SCREEN_HEIGHT // M)
  matrix = maze

  pygame.init()
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Matrix Visualization")

  BACKGROUND = (215, 210, 195)  # Muted Sand (#D7D2C3)
  WALLS = (40, 45, 50)          # Deep Charcoal (#282D32)
  AGENT = (0, 120, 210)         # Electric Blue (#0078D2)
  PATH = (202, 220, 235)        # light blue
  GOAL = (220, 80, 10)          # Deep Orange (#DC500A)



  TEXT_COLOR = (0, 0, 0)
  FONT = pygame.font.SysFont(None, 24)

  def draw_grid():
    for row in range(M):
      for col in range(N):
        x = col * CELL_SIZE + UI_WIDTH
        y = row * CELL_SIZE
        
        if matrix[row][col] == wall_cell:
          color = WALLS
        elif matrix[row][col] == empty_cell:
          color = BACKGROUND
        elif matrix[row][col] == agent_cell:
          color = AGENT
        elif matrix[row][col] == goal_cell:
          color = GOAL
        elif matrix[row][col] == path_cell:
          color = PATH
        
        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

  def draw_ui():
    screen.fill((220, 220, 220), (0, 0, UI_WIDTH, SCREEN_HEIGHT))
    labels = [
      ("Wall", WALLS),
      ("Empty", BACKGROUND),
      ("Agent", AGENT),
      ("Path", PATH),
      ("Goal", GOAL)
    ]
    y_offset = 50
    for text, color in labels:
      pygame.draw.rect(screen, color, (20, y_offset, 20, 20))
      label = FONT.render(text, True, TEXT_COLOR)
      screen.blit(label, (50, y_offset))
      y_offset += 40
    
    exit_label = FONT.render("Press ESC to Exit", True, TEXT_COLOR)
    screen.blit(exit_label, (20, y_offset + 20))

  running = True
  while running:
    screen.fill(BACKGROUND)
    draw_grid()
    draw_ui()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = False
    
    pygame.display.flip()

  pygame.quit()



### A* related

def manhattan_distance(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])


def return_neibhors(coords, M, N):
  i, j = coords
  res = []
  if i + 1 < M:
    res.append((i + 1, j))

  if i - 1 >= 0:
    res.append((i - 1, j))


  if j + 1 < N:
    res.append((i, j + 1))

  if j - 1 >= 0:
    res.append((i, j - 1))

  return res


def update_map_with_walls(walls_list, maze_map, wall_cell):
  for coords in walls_list:
    maze_map[coords[0]][coords[1]] = wall_cell
  return maze_map


# add neibhors of a cell to the open list (and the closed list too)
def expand_cell(coords, maze_map, heuristics_table, open_list, closed_list, parents, agent_coords, goal_coords, wall_cell, TIE_BREAK, M, N):
  nonwall_neighbors = list(filter(lambda coords: maze_map[coords[0]][coords[1]] != wall_cell, utils.return_neibhors(coords, M, N)))

  for neighbor in nonwall_neighbors:
    if neighbor not in closed_list:
      g_value = utils.manhattan_distance(agent_coords, neighbor)
      if neighbor in heuristics_table:
        h_value = heuristics_table[neighbor]
      else:
        h_value = utils.manhattan_distance(goal_coords, neighbor)
      f_value = g_value + h_value

      parents[neighbor] = coords

      # heap format: (f_cost, g or -g cost, coordinates of cell)
      if TIE_BREAK == "higher g":
        heapq.heappush(open_list, (f_value, -g_value, neighbor))

      elif TIE_BREAK == "lower g":
        heapq.heappush(open_list, (f_value, g_value, neighbor))

      closed_list.add(neighbor)


def find_shortest_path_with_AStar(orientation, agent_coords, goal_coords, heuristics_table, maze_map, wall_cell, TIE_BREAK, M, N):
  # initialize variables needed for the A*

  if orientation == 'reverse':
    agent_coords, goal_coords = goal_coords, agent_coords

  open_list = [(0, 0, agent_coords)]
  heapq.heapify(open_list)
  closed_list = {agent_coords}
  parents = {agent_coords: None} # lists the parent of every expanded cell
  expanded_cells = 0

  # print(f"agent coords are {agent_coords}, goal coords are {goal_coords}")


  path = []
  while open_list:
    next_cell_coords = heapq.heappop(open_list)[2]
    if next_cell_coords == goal_coords:
      path.append(next_cell_coords)
      while parents[next_cell_coords]:
        if parents[next_cell_coords] != agent_coords:
          path.append(parents[next_cell_coords])
        next_cell_coords = parents[next_cell_coords]
      
      if orientation == 'normal':
        return (path[::-1], expanded_cells)
      
      return (path[1:] + [agent_coords], expanded_cells) # needed to format the reverse path
    
    utils.expand_cell(next_cell_coords, maze_map, heuristics_table, open_list, closed_list, parents, agent_coords, goal_coords, wall_cell, TIE_BREAK, M, N)
    expanded_cells += 1
  if orientation == 'normal':
    return (path[::-1], expanded_cells)
  return (path[1:], expanded_cells)