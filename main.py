import numpy as np

GRID_WIDTH = 10
GRID_HEIGHT = 10

def init_grid():
    grid = np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

    # Obstacles
    grid[1, 7] = 1
    grid[8, 3] = 1

    # Person
    grid[0, 0] = 3
    grid[9, 9] = 3

    # Obejctive
    grid[5, 4] = 2

    return grid

def minkowski_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def move_person(grid, person_pos, objective_pos):
    # Get the possible moves
    possible_moves = []
    # Move up
    if person_pos[0] > 0:
        possible_moves.append((person_pos[0] - 1, person_pos[1]))
    # Move down
    if person_pos[0] < GRID_HEIGHT - 1:
        possible_moves.append((person_pos[0] + 1, person_pos[1]))
    # Move left
    if person_pos[1] > 0:
        possible_moves.append((person_pos[0], person_pos[1] - 1))
    # Move right
    if person_pos[1] < GRID_WIDTH - 1:
        possible_moves.append((person_pos[0], person_pos[1] + 1))

    # Get the best move
    best_move = possible_moves[0]
    best_move_distance = minkowski_distance(possible_moves[0], objective_pos)
    for move in possible_moves:
        move_distance = minkowski_distance(move, objective_pos)
        if move_distance < best_move_distance:
            best_move = move
            best_move_distance = move_distance

    # Move the person
    grid[person_pos[0], person_pos[1]] = 0
    grid[best_move[0], best_move[1]] = 3

    return grid, best_move


def main():

    grid = init_grid()
    #Init person
    person1_pos = (0, 0)
    person2_pos = (9, 9)
    #Init objective
    objective_pos = (5, 4)
    #Init obstacles
    obstacles_pos = [(1, 7), (8, 3)]

    print(grid)

    print(minkowski_distance(person1_pos, objective_pos))
    print(minkowski_distance(person2_pos, objective_pos))

if __name__ == "__main__":
    main()