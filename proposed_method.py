import math
import matplotlib.pyplot as plt
import random
from time import time
from solution import Solution


def reading(File):
    vertexes = []
    file = open(File, "r")
    i = 0
    for line in file:
        if i == 1:
            pom = line.split()
            x = float(pom[1])
            y = float(pom[2])
            vertexes.append([x, y])
        else:
            global number_of_vertexes
            number_of_vertexes = int(line)
            i = 1
    return vertexes


def triangle(vertexes):
    x1 = vertexes[0][0]
    x2 = vertexes[0][0]
    y1 = vertexes[0][1]
    y2 = vertexes[0][1]
    for V in vertexes:
        if V[0] < x1:
            x1 = V[0]
        if V[0] > x2:
            x2 = V[0]
        if V[1] < y1:
            y1 = V[1]
        if V[1] > y2:
            y2 = V[1]
    N = 5
    W = 100
    max = 0
    sector = []
    for y in range(W + 1):
        y_bottom = ((y2 - y1) * (N - 1 / N)) * y / W + y1
        y_top = ((y2 - y1) * (N - 1 / N)) * y / W + y1 + (y2 - y1) / N
        for x in range(W + 1):
            x_left = ((x2 - x1) * (N - 1 / N)) * x / W + x1
            x_right = ((x2 - x1) * (N - 1 / N)) * x / W + x1 + (x2 - x1) / N
            count = 0
            array = []
            for i in range(len(vertexes)):
                if vertexes[i][0] >= x_left and vertexes[i][0] <= x_right and vertexes[i][1] >= y_bottom and vertexes[i][1] <= y_top:
                    count += 1
                    array.append(i)
            if count > max:
                max = count
                sector = array[:]
    sequence = random.sample(sector, 3)
    indexes = []
    for i in range(len(vertexes)):
        indexes.append(i)
    sequence_pom = sequence[:]
    sequence.append(sequence[0])
    sequence_pom.sort()
    for i in range(2, -1, -1):
        indexes.pop(sequence_pom[i])
    path = []
    for index in sequence:
        path.append(vertexes[index])
    return [sequence, path, indexes]


def add_Vertex(vertexes, indexes, Vertex, Index):
    vertexes_pom = vertexes[:]
    indexes_pom = indexes[:]
    min = 1000000000000
    for i in range(len(vertexes) - 1):
        pom1 = math.sqrt((vertexes[i][0] - vertexes[i + 1][0]) ** 2 + (vertexes[i][1] - vertexes[i + 1][1]) ** 2)
        pom2 = math.sqrt((vertexes[i][0] - Vertex[0]) ** 2 + (vertexes[i][1] - Vertex[1]) ** 2)
        pom3 = math.sqrt((Vertex[0] - vertexes[i + 1][0]) ** 2 + (Vertex[1] - vertexes[i + 1][1]) ** 2)
        if (pom3 + pom2 - pom1) < min:
            min = pom3 + pom2 - pom1
            m = i + 1
    vertexes_pom.insert(m, Vertex)
    indexes_pom.insert(m, Index)
    return [indexes_pom, vertexes_pom]


def distance(vertexes):
    total = 0
    for i in range(len(vertexes) - 1):
        pom = math.sqrt((vertexes[i][0] - vertexes[i + 1][0]) ** 2 + (vertexes[i][1] - vertexes[i + 1][1]) ** 2)
        total += pom
    return total


def Create_path(vertexes_of_path, indexes_of_path, permutation, vertexes, flag):
    vertexes_pom = vertexes_of_path[:]
    indexes_pom = indexes_of_path[:]
    p = permutation[:]
    if flag == 1:
        x = vertexes_of_path[0][0]
        y = vertexes_of_path[0][1]
        ind = []
        for i in range(int(0.2 * len(permutation))):
            max = 0
            for j in range(len(p)):
                if math.sqrt( (vertexes[p[j]][0] - x) ** 2 + (vertexes[p[j]][1] - y) ** 2 ) > max:
                    max = math.sqrt( (vertexes[p[j]][0] - x) ** 2 + (vertexes[p[j]][1] - y) ** 2 )
                    index = j
            ind.append(p[index])
            p.pop(index)
        p = ind + p
    for index in p:
        pom = add_Vertex(vertexes_pom, indexes_pom, vertexes[index], index)
        indexes_pom = pom[0]
        vertexes_pom = pom[1]
    return [indexes_pom, vertexes_pom]


def create_population(file_name, Count):
    vertexes = reading(file_name + '.txt')

    pom = triangle(vertexes)
    indexes_of_path = pom[0]
    vertexes_of_path = pom[1]
    indexes_to_be_added = pom[2]
    parents = []
    distances = []

    population = []
    for i in range(Count):
        rate = random.random()
        if rate <= 0.1:
            flag = 1
        else:
            flag = 0
        random.shuffle(indexes_to_be_added)
        pom = indexes_to_be_added[:]
        parents.append(pom)
        pom = Create_path(vertexes_of_path, indexes_of_path, pom, vertexes, flag)
        d = distance(pom[1])
        distances.append(d)

        path1, path2 = find_best_cut(pom[1])
        path1 = map_to_indexes(path1, vertexes)
        path2 = map_to_indexes(path2, vertexes)

        solution = Solution(file_name + '.tsp')
        solution.set_paths(path1, path2)
        solution.set_total_length()

        population.append(solution)

    return population


def distance1(vertexes):
    total = 0
    for i in range(len(vertexes) - 1):
        pom = math.sqrt((vertexes[i][0] - vertexes[i + 1][0]) ** 2 + (vertexes[i][1] - vertexes[i + 1][1]) ** 2)
        total += pom

    pom = math.sqrt((vertexes[-1][0] - vertexes[0][0]) ** 2 + (vertexes[-1][1] - vertexes[0][1]) ** 2)
    total += pom

    return total


def make_cut(path, cut_index):
    path1 = []
    path2 = []

    length = len(path)
    for i in range(int(length / 2)):
        vertex = path[(cut_index + i) % length]
        path1.append(vertex)

    for i in range(int(length / 2)):
        vertex = path[(cut_index + int(length / 2) + i) % length]
        path2.append(vertex)

    return path1, path2


def find_best_cut(path):
    path = path[:-1]
    best_distance = 100000000
    best_paths = ()
    for i in range(len(path)):
        path1, path2 = make_cut(path, i)
        d1 = distance1(path1)
        d2 = distance1(path2)

        if d1 + d2 < best_distance:
            best_distance = d1 + d2
            best_paths = (path1, path2)

    path1, path2 = best_paths
    print(best_distance)
    path1.append(path1[0])
    path2.append(path2[0])
    print(distance(path1) + distance(path2))

    return path1, path2


def map_to_indexes(path, vertexes):
    path_indexes = []
    for vertex in path:
        for j in range(len(vertexes)):
            if vertex == vertexes[j]:
                path_indexes.append(j)
                break

    return path_indexes
