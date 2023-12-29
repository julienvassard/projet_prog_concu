
import numpy as np
import random
import time
import multiprocessing
import threading
import logging

GRID_WIDTH = 512
GRID_HEIGHT = 128

grid = [['| |' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
#lock = threading.Lock()

def process_section(section, x_objectif, y_objectif, personnes, isArrived):
    while not all(isArrived):
        for i, (x, y) in enumerate(personnes):
            if not isArrived[i] :
                # and 0 <= x < len(section[0]) and 0 <= y < len(section)
                #if section[y][x] != '|X|':
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


def move_person(person_index,  x_objectif, y_objectif, isArrived, personnes):
    while person_index < len(isArrived):  # Vérifiez si person_index est dans la plage valide
        if not isArrived[person_index]:
            # Assurez-vous que person_index ne dépasse pas la taille de la liste personnes
            if person_index < len(personnes):
                x, y = personnes[person_index]
                best_x, best_y = best_path(x, y, x_objectif, y_objectif)
                if best_x == x_objectif and best_y == y_objectif:
                    grid[y][x] = '| |'
                    isArrived[person_index] = True
                else:
                    grid[y][x] = '| |'
                    grid[best_y][best_x] = f'|{person_index + 1}|'
                    personnes[person_index] = (best_x, best_y)
            else:
                break  # Sortir de la boucle si person_index est invalide
        else:
            break  # Sortir de la boucle si la personne est déjà arrivée






def main(nb_personnes):

    # Création de quarts
    mid_width = GRID_WIDTH // 2
    mid_height = GRID_HEIGHT // 2

    quadrant_1 = [row[:mid_width] for row in grid[:mid_height]]
    quadrant_2 = [row[mid_width:] for row in grid[:mid_height]]
    quadrant_3 = [row[:mid_width] for row in grid[mid_height:]]
    quadrant_4 = [row[mid_width:] for row in grid[mid_height:]]



    # Initialisation des quadrants avec obstacles et objectif
    for _ in range(2):
        x_obstacle = random.randint(0, mid_width - 1)
        y_obstacle = random.randint(0, mid_height - 1)
        quadrant_1[y_obstacle][x_obstacle] = '|X|'

        x_obstacle = random.randint(0, mid_width - 1)
        y_obstacle = random.randint(0, mid_height - 1)
        quadrant_2[y_obstacle][x_obstacle] = '|X|'

        x_obstacle = random.randint(0, mid_width - 1)
        y_obstacle = random.randint(0, mid_height - 1)
        quadrant_3[y_obstacle][x_obstacle] = '|X|'

        x_obstacle = random.randint(0, mid_width - 1)
        y_obstacle = random.randint(0, mid_height - 1)
        quadrant_4[y_obstacle][x_obstacle] = '|X|'

    x_objectif = np.random.randint(mid_width, GRID_WIDTH - 1)
    y_objectif = np.random.randint(mid_height , GRID_HEIGHT - 1)

    quadrant_1[y_objectif - mid_height ][x_objectif - mid_width] = '|T|'
    quadrant_2[y_objectif - mid_height ][x_objectif - mid_width - mid_width] = '|T|'
    quadrant_3[y_objectif - mid_height - mid_height ][x_objectif - mid_width] = '|T|'
    quadrant_4[y_objectif - mid_height - mid_height ][x_objectif - mid_width - mid_width] = '|T|'


    personnes = []
    isArrived = []
    threads = []

    # Création des threads pour chaque quadrant
    thread_1 = threading.Thread(target=move_person,
                                args=(0, x_objectif, y_objectif, isArrived, personnes))
    thread_2 = threading.Thread(target=move_person,
                                args=(1, x_objectif, y_objectif, isArrived, personnes))
    thread_3 = threading.Thread(target=move_person,
                                args=(2, x_objectif, y_objectif, isArrived, personnes))
    thread_4 = threading.Thread(target=move_person,
                                args=(3, x_objectif, y_objectif, isArrived, personnes))

    threads.extend([thread_1, thread_2, thread_3, thread_4])



    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()



    #print("Nombre personnes:", len(personnes))
    lap = 1

    while True:
        #print("Tour : ", lap)
        for i in range(nb_personnes):
            if i < len(personnes):
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
            else:
                break

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


