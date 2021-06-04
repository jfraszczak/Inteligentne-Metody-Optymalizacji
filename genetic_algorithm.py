import math
import matplotlib.pyplot as plt
import random
from statistics import median
from time import time

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

def graph_generation(N):
    file = open("Wierzchołki.txt", "w")
    file.write(str(N))
    for i in range(100):
        x = random.randint(4000,7000)
        y = random.randint(4000,7000)
        file.write('\n')
        file.write(str(i + 1) + ' ' + str(x) + ' ' + str(y))
    for i in range(N - 50):
        x = random.randint(0, 10000)
        y = random.randint(0, 10000)
        file.write('\n')
        file.write(str(i + 1)+ ' ' + str(x) + ' ' + str(y))
    file.close()

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

def average(list):
    sum = 0
    for el in list:
        sum += el
    return sum / len(list)

def sec2min(seconds):
    min = int(seconds / 60)
    sec = int(seconds % 60)
    return (str(min) + 'min' + str(sec) + 'sec')

def graph(vertexes):
    x_coords = []
    y_coords = []
    for i in range(len(vertexes)):
        x_coords.append(vertexes[i][0])
        y_coords.append(vertexes[i][1])
    plt.plot(x_coords, y_coords, marker='o', color='blue')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

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

def crossing_over_order1(parentA, parentB, section):
    parent1 = parentA[:]
    parent2 = parentB[:]
    gene = []
    part1 = []
    part2 = []
    pom = []
    for i in range(section[0], section[1] + 1):
        gene.append(parent1[i])
    for i in range(len(parent2)):
        for e in gene:
            if e == parent2[i]:
                pom.append(i)
    pom.sort()
    k = 0
    for i in pom:
        parent2.pop(i - k)
        k += 1
    for i in range(section[0]):
        part1.append(parent2[i])
    for i in range(len(parent1) - section[1] - 1):
        part2.append(parent2[i + section[0]])
    child = part1 + gene + part2
    return child

def contains(array, element):
    k = 0
    i = 0
    while i < len(array) and k == 0:
        if array[i] == element:
            k = 1
        i += 1
    if k == 1:
        return True
    else:
        return False

def position(array, element):
    i = 0
    while i < len(array):
        if array[i] == element:
            return i
        i += 1

def crossing_over_PMX(parentA, parentB, section):
    parent1 = parentA[:]
    parent2 = parentB[:]
    gene = []
    gene2 = []
    indexes = []
    for i in range(section[0], section[1] + 1):
        gene.append(parent1[i])
        gene2.append(parent2[i])
    for i in range(len(gene2)):
        if not contains(gene, gene2[i]):
            flag = 0
            value = gene[i]
            while flag == 0:
                index = position(parent2, value)
                if index < section[0] or index > section[1]:
                    indexes.append([gene2[i], index])
                    flag = 1
                else:
                    value = parent1[index]
    child = []
    for i in range(len(parent2)):
        if i < section[0] or i > section[1]:
            e = 0
            k = 0
            while e < len(indexes) and k == 0:
                if indexes[e][1] == i:
                    child.append(indexes[e][0])
                    k = 1
                e += 1
            if k == 0:
                child.append(parent2[i])

        else:
            child.append(parent1[i])
    return child

def Nietzsche_algorithm(generation, distances, Count):
    list1 = []
    list2 = []
    mini = min(distances)
    maxi = max(distances)
    mediani = median(distances)
    for i in range(len(distances)):
        x = 0
        y = 0
        if mediani == mini:
            x = 1
        if mediani == maxi:
            y = 1
        if distances[i] < mediani:
            r = (mediani - distances[i]) / (mediani - mini + x)
        else:
            r = (-1) * (distances[i] - mediani) / (maxi - mediani + y)
        f = Count / len(generation) + (1 - Count / len(generation)) * r
        probability = random.random()
        if f >= probability:
            list1.append(generation[i])
            list2.append(distances[i])
    return (list1, list2)

def tournament(generation, distances, Count):
    new_generation = []
    new_distances = []
    for i in range(Count):
        t = random.sample(range(0, len(generation)), 2)
        rate = random.random()
        if distances[t[0]] < distances[t[1]]:
            if rate <= 0.8:
                min_index = t[0]
            else:
                min_index = t[1]
        else:
            if rate <= 0.8:
                min_index = t[1]
            else:
                min_index = t[0]
        new_generation.append(generation[min_index])
        new_distances.append(distances[min_index])
    mini = distances[0]
    min_index = 0
    for i in range(1, len(generation)):
        if distances[i] < mini:
            mini = distances[i]
            min_index = i
    new_generation.append(generation[min_index])
    new_distances.append(distances[min_index])
    return (new_generation, new_distances)

def fitness(distances, index):
    f = 1 / distances[index]
    s = 0
    for i in range(len(distances)):
        s += (1 / distances[i])
    p = f / s
    return p

def roulette(generation, distances, Count):
    sum = 0;
    distribution = []
    new_generation = []
    new_distances = []
    mini = distances[0]
    min_index = 0
    for i in range(len(generation)):
        sum += fitness(distances, i)
        distribution.append(sum)
        if distances[i] < mini:
            mini = distances[i]
            min_index = i
    new_generation.append(generation[min_index])
    new_distances.append(distances[min_index])
    for i in range(Count):
        r = random.random()
        j = 0
        while r > distribution[j]:
            j += 1
        new_generation.append(generation[j])
        new_distances.append(distances[j])
    return (new_generation, new_distances)

def mutation(vertexes_of_path, indexes_of_path, vertexes, generation, distances, rate):
    mini = min(distances)
    N = len(generation)
    for i in range(N):
        if distances[i] != mini and random.random() <= rate:
            pom = []
            for j in range(number_of_vertexes - 3):
                pom.append(j)
            a = random.sample(pom, int((number_of_vertexes - 3) * 0.1))
            b = []
            for j in range(len(a)):
                b.append(j)
            random.shuffle(b)
            pom = generation[i][:]
            for j in range(len(b)):
                generation[i][a[j]] = pom[a[b[j]]]
            pom = Create_path(vertexes_of_path, indexes_of_path, generation[i], vertexes, 0)
            distances[i] = distance(pom[1])

def RSM(vertexes_of_path, indexes_of_path, vertexes, generation, distances, rate):
    mini = min(distances)
    N = len(generation)
    S = int((number_of_vertexes - 3) * 0.1)
    for i in range(N):
        if distances[i] != mini and random.random() <= rate:
            p = random.randint(0, number_of_vertexes - 3 - S)
            pom_g = generation[i][:]
            for j in range(p + S - 1, p - 1, -1):
                pom_g[j] = generation[i][p + S - 1 - j + p]
            generation[i][:] = pom_g
            pom = Create_path(vertexes_of_path, indexes_of_path, generation[i], vertexes, 0)
            distances[i] = distance(pom[1])

def two_opt(path, dist, N):
    mini = dist
    p = path[:]
    for e in range(N):
        for i in range(1, len(path) - 1):
            for j in range(i + 1, len(path) - 1):
                pom = p[i]
                p[i] = p[j]
                p[j] = pom
                d = distance(p)
                if d < mini:
                    mini = d
                else:
                    pom = p[i]
                    p[i] = p[j]
                    p[j] = pom
    print("2-OPT", int(round(mini, 0)))
    return p


def Genetic_algorithm(File, Count, M, P, S, R):
    vertexes = reading(File)
    t = time()
    pom = triangle(vertexes)
    indexes_of_path = pom[0]
    vertexes_of_path = pom[1]
    indexes_to_be_added = pom[2]
    parents = []
    distances = []
    for i in range(Count):
        rate = random.random()
        if rate <= R:
            flag = 1
        else:
            flag = 0
        random.shuffle(indexes_to_be_added)
        pom = indexes_to_be_added[:]
        parents.append(pom)
        pom = Create_path(vertexes_of_path, indexes_of_path, pom, vertexes, flag)
        d = distance(pom[1])
        distances.append(d)
    e = 0
    print('XDDDDD', int(round(min(distances), 0)))

    mini = distances[0]
    best = parents[0]
    for i in range(len(parents)):
        if distances[i] < mini:
            mini = distances[i]
            best = parents[i]

    best = Create_path(vertexes_of_path, indexes_of_path, best, vertexes, 0)
    best = best[1]

    return best


    while (time() - t) < 15:
        length = random.randint(3, max([int(number_of_vertexes * S), 3]))
        generation = parents[:]
        for i in range(int(len(parents) / 2)):
            section = random.randint(0, number_of_vertexes - 3 - length - 1)
            if random.random() <= P:
                if distances[i] > distances[i + 1]:
                    child = crossing_over_PMX(parents[i], parents[i + 1], [section, section + length])
                else:
                    child = crossing_over_PMX(parents[i + 1], parents[i], [section, section + length])
            else:
                if distances[i] < distances[i + 1]:
                    child = crossing_over_PMX(parents[i], parents[i + 1], [section, section + length])
                else:
                    child = crossing_over_PMX(parents[i + 1], parents[i], [section, section + length])
            generation.append(child)
        for i in range(len(parents), len(generation)):
            pom = Create_path(vertexes_of_path, indexes_of_path, generation[i], vertexes, 0)
            d = distance(pom[1])
            distances.append(d)
        pom = Nietzsche_algorithm(generation, distances, Count)
        parents = pom[0]
        distances = pom[1]
        mutation(vertexes_of_path, indexes_of_path, vertexes, parents, distances, M)
        x = list(zip(parents, distances))
        random.shuffle(x)
        parents, distances = zip(*x)
        parents = list(parents)
        distances = list(distances)
        print(int(round(min(distances), 0)))
        e += 1
    mini = distances[0]
    best = parents[0]
    for i in range(len(parents)):
        if distances[i] < mini:
            mini = distances[i]
            best = parents[i]
    best = Create_path(vertexes_of_path, indexes_of_path, best, vertexes, 0)
    best = best[1]
    print("Minimal distance",int(round(mini, 0)), len(best))
    #best = two_opt(best, mini, 5)
    print(best)
    sec2min(time() - t)
    return best


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

    x_coords = []
    y_coords = []
    for i in range(len(path1)):
        x_coords.append(path1[i][0])
        y_coords.append(path1[i][1])
    plt.plot(x_coords, y_coords, marker='o', color='blue')
    plt.xlabel('X')
    plt.ylabel('Y')

    x_coords = []
    y_coords = []
    for i in range(len(path2)):
        x_coords.append(path2[i][0])
        y_coords.append(path2[i][1])
    plt.plot(x_coords, y_coords, marker='o', color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()


best = Genetic_algorithm("kroA200.txt", 100, 0.15, 0.9, 0.15, 0.1)
graph(best)

find_best_cut(best)