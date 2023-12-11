
import numpy as np
import random
import time
import multiprocessing
import threading
import logging

GRID_WIDTH = 512
GRID_HEIGHT = 128

grid = [['| |' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
lock = threading.Lock()

def process_section(section, x_objectif, y_objectif, personnes, isArrived):
    while not all(isArrived):
        for i, (x, y) in enumerate(personnes):
            if not isArrived[i]:
                best_x, best_y = best_path(x, y, x_objectif, y_objectif)
                if best_x == x_objectif and best_y == y_objectif:
                    section[y][x] = '| |'
                    isArrived[i] = True
                else:
                    section[y][x] = '| |'
                    section[best_y][best_x] = f'|{i + 1}|'
                    personnes[i] = (best_x, best_y)

def print_grid(grid):
    for line in grid:
        print(' '.join(line))


def minkowski_distance(point1, point2):
    distance = 0
    for i in range(len(point1)):
        distance += abs(point1[i] - point2[i]) ** 1

    distance = distance ** 1

    return distance


def best_path(x_personne, y_personne, x_objectif, y_objectif):
    best_x = 0
    best_y = 0
    best_distance = 10000000
    if x_personne + 1 < GRID_WIDTH and grid[y_personne][x_personne + 1] != '|X|':
        distance = minkowski_distance([x_personne + 1, y_personne], [x_objectif, y_objectif])
        if distance < best_distance:
            best_distance = distance
            best_x = x_personne + 1
            best_y = y_personne
    if x_personne - 1 >= 0 and grid[y_personne][x_personne - 1] != '|X|':
        distance = minkowski_distance([x_personne - 1, y_personne], [x_objectif, y_objectif])
        if distance < best_distance:
            best_distance = distance
            best_x = x_personne - 1
            best_y = y_personne
    if y_personne + 1 < GRID_HEIGHT and grid[y_personne + 1][x_personne] != '|X|':
        distance = minkowski_distance([x_personne, y_personne + 1], [x_objectif, y_objectif])
        if distance < best_distance:
            best_distance = distance
            best_x = x_personne
            best_y = y_personne + 1
    if y_personne - 1 >= 0 and grid[y_personne - 1][x_personne] != '|X|':
        distance = minkowski_distance([x_personne, y_personne - 1], [x_objectif, y_objectif])
        if distance < best_distance:
            best_distance = distance
            best_x = x_personne
            best_y = y_personne - 1

    return best_x, best_y


def move_person(person_index, x_objectif, y_objectif, isArrived, personnes):
    while not isArrived[person_index]:
        x, y = personnes[person_index]
        with lock:
            best_x, best_y = best_path(x, y, x_objectif, y_objectif)
            if best_x == x_objectif and best_y == y_objectif and not isArrived[person_index]:
                grid[y][x] = '| |'
                isArrived[person_index] = True
            elif not isArrived[person_index]:
                grid[y][x] = '| |'
                grid[best_y][best_x] = f'|{person_index + 1}|'
                personnes[person_index] = (best_x, best_y)



def main(nb_personnes):
    middle_width = GRID_WIDTH // 2
    middle_height = GRID_HEIGHT // 2

    section_1 = [row[:middle_width] for row in grid[:middle_height]]
    section_2 = [row[middle_width:] for row in grid[:middle_height]]
    section_3 = [row[:middle_width] for row in grid[middle_height:]]
    section_4 = [row[middle_width:] for row in grid[middle_height:]]

    sections = [section_1, section_2, section_3, section_4]

    personnes = []
    isArrived = []
    threads = []

    for i in range(nb_personnes):
        x_personne = np.random.randint(0, GRID_WIDTH - 1)
        y_personne = np.random.randint(0, GRID_HEIGHT - 1)
        personnes.append((x_personne, y_personne))
        isArrived.append(False)
        grid[y_personne][x_personne] = f'|{i + 1}|'

    x_objectif = np.random.randint(0, GRID_WIDTH - 1)
    y_objectif = np.random.randint(0, GRID_HEIGHT - 1)
    grid[y_objectif][x_objectif] = '|T|'

    threads = []
    for i in range(nb_personnes):
        thread = threading.Thread(target=move_person, args=(i, x_objectif, y_objectif, isArrived, personnes))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    #print_grid(grid)


    #print("Nombre personnes:", len(personnes))
    lap = 1



    while True:
        #print("Tour : ", lap)
        for i in range(nb_personnes):
            x, y = personnes[i]
            best_x, best_y = best_path(x, y, x_objectif, y_objectif)
            if best_x == x_objectif and best_y == y_objectif and not isArrived[i]:
                #print(f"Personne {i + 1} a atteint l'objectif et disparaît !")
                grid[y][x] = '| |'
                isArrived[i] = True
            elif not isArrived[i]:
                grid[y][x] = '| |'
                grid[best_y][best_x] = f'|{i + 1}|'
                personnes[i] = (best_x, best_y)

        if all(isArrived):
            #print("Toutes les personnes ont atteint l'objectif !")
            break
        lap += 1


def measure_execution_time(num_personnes):
    start_time = time.time()
    main(num_personnes)
    end_time = time.time()
    return end_time - start_time


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    num_personnes = [2**1, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10]
    execution_times = []

    for n in num_personnes:
        execution_time = measure_execution_time(n)
        execution_times.append(execution_time)

    speedup = execution_times[0] / np.array(execution_times)

    efficiency = speedup / np.array(num_personnes)

    logging.info("Nombre de personnes: %s", num_personnes)
    logging.info("Temps d'exécution (secondes): %s", execution_times)
    logging.info("Speedup: %s", speedup)
    logging.info("Efficacité: %s", efficiency)
