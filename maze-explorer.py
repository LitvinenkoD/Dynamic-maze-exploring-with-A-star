import random
import utils
import heapq

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

def astar(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: utils.manhattan_distance(start, goal)}

    while open_set:
        fscore, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            print ("Found a path!")
            return path[::-1]

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < M and 0 <= neighbor[1] < N and maze[neighbor[0]][neighbor[1]] != wall_cell:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + utils.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    print ("No path found ):")
    return None
path = astar(maze, agent_coords, goal_coords)

if path:
    for step in path[1:-1]:
        maze[step[0]][step[1]] = path_cell


for row in maze:
    print(" ".join(row))
# once we'll be done with actually solving the maze, I can add a visualization for that,
# showing how the agent moved
