import random
import pygame
import utils
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




def generate_maze(maze, visited, unvisited, wall_cell, M, N):
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
  PATH = (80, 140, 190)         # Muted Steel Blue (#508CBE)
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
