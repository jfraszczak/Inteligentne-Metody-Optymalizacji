from greedy_algorithms import NearestNeighbour, GreedyCycle, RegretHeuristics
import math
from matplotlib import pyplot as plt
import random
from copy import deepcopy
from time import perf_counter
import numpy as np
import csv


# Klasa instancji, przechowuje macierz odległości, listę wierzchołków, liczbę wierzchołków (teraz całość jest osobno zamaist tak jak poprrzednio jako część klasy algorytm żeby troche bardziej zmodularyzować)
class Instance:
    def __init__(self):
        self.distance_matrix = None
        self.vertices = []
        self.size = 0

    def read(self, file_name):
        file = open(file_name, 'r', encoding='utf-8')

        reading = False
        for line in file:
            if line == 'EOF':
                break
            elif not reading and line[0] == '1':
                reading = True

            if reading:
                data = line.split()

                identifier = int(data[0])
                x = int(data[1])
                y = int(data[2])

                vertex = self.Vertex(identifier, x, y)
                self.vertices.append(vertex)

        n = len(self.vertices)
        self.size = n

        self.distance_matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                distance = round(math.sqrt(
                    (self.vertices[i].x - self.vertices[j].x) ** 2 + (self.vertices[i].y - self.vertices[j].y) ** 2))
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance

    class Vertex:
        def __init__(self, identifier, x, y):
            self.identifier = identifier
            self.x = x
            self.y = y


# Klasa rozwiązanie, przechowuje obiekt instancji oraz oba cykle, już zaimplementowałem losową inizjalizację i inicjalizację rozwiązania przez użycie algorytmow zachłannych
# z poprzedniego zadania i wszystkie te elementarne operacje jak wymiana wierzchołkami i krawędziami
class Solution:
    def __init__(self, file_name):
        self.instance = Instance()
        self.instance.read(file_name)

        self.path1 = []
        self.path2 = []

    def random_initialization(self):
        vertices = list(range(self.instance.size))
        self.path1 = random.sample(vertices, int(self.instance.size / 2))
        for vertex in self.path1:
            vertices.remove(vertex)
        self.path2 = vertices[:]

    def greedy_algorithm_initialization(self):
        alg = GreedyCycle()
        alg.read_instance_object(self.instance)
        alg.find_solution()
        self.path1 = alg.path1[:]
        self.path2 = alg.path2[:]

    def exchange_vertices(self, vertex1, vertex2):
        self.path1[vertex1], self.path2[vertex2] = self.path2[vertex2], self.path1[vertex1]

    def swap_vertices_path1(self, vertex1, vertex2):
        self.path1[vertex1], self.path1[vertex2] = self.path1[vertex2], self.path1[vertex1]

    def swap_vertices_path2(self, vertex1, vertex2):
        self.path2[vertex1], self.path2[vertex2] = self.path2[vertex2], self.path2[vertex1]

    def swap_edges_path1(self, edge1, edge2):
        new_path = []
        edge1, edge2 = min(edge1, edge2), max(edge1, edge2)

        for i in range(edge1 + 1):
            new_path.append(self.path1[i])

        for i in range(edge2, edge1, -1):
            new_path.append(self.path1[i])

        for i in range(edge2 + 1, len(self.path1)):
            new_path.append(self.path1[i])

        self.path1 = new_path[:]

    def swap_edges_path2(self, edge1, edge2):
        new_path = []
        edge1, edge2 = min(edge1, edge2), max(edge1, edge2)

        for i in range(edge1 + 1):
            new_path.append(self.path2[i])

        for i in range(edge2, edge1, -1):
            new_path.append(self.path2[i])

        for i in range(edge2 + 1, len(self.path2)):
            new_path.append(self.path2[i])

        self.path2 = new_path[:]

    def cumulative_length_after_move(self, move, *args):
        path1 = self.path1[:]
        path2 = self.path2[:]
        move(*args)
        length = self.cumulative_length()
        self.path1 = path1[:]
        self.path2 = path2[:]

        return length

    def calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += self.instance.distance_matrix[path[i]][path[i + 1]]
        length += self.instance.distance_matrix[path[0]][path[-1]]

        return length

    def cumulative_length(self):
        return self.calculate_path_length(self.path1) + self.calculate_path_length(self.path2)

    def path1_size(self):
        return len(self.path1)

    def path2_size(self):
        return len(self.path2)

    def visualise(self, title=None, save=False):
        x = []
        y = []

        for vertex in self.instance.vertices:
            x.append(vertex.x)
            y.append(vertex.y)
        plt.scatter(x, y, color='k')

        for vertex in self.instance.vertices:
            plt.annotate(vertex.identifier, (vertex.x, vertex.y))

        path1_x = []
        path1_y = []

        for vertex in self.path1:
            path1_x.append(self.instance.vertices[vertex].x)
            path1_y.append(self.instance.vertices[vertex].y)
        path1_x.append(self.instance.vertices[self.path1[0]].x)
        path1_y.append(self.instance.vertices[self.path1[0]].y)
        plt.plot(path1_x, path1_y, 'c-')

        path2_x = []
        path2_y = []

        for vertex in self.path2:
            path2_x.append(self.instance.vertices[vertex].x)
            path2_y.append(self.instance.vertices[vertex].y)
        path2_x.append(self.instance.vertices[self.path2[0]].x)
        path2_y.append(self.instance.vertices[self.path2[0]].y)
        plt.xlabel(type(self).__name__)
        plt.plot(path2_x, path2_y, 'm-')

        if title is not None:
            plt.title(title)

        if not save:
            plt.show()
        else:
            plt.savefig('visualisations/' + title + '.png')
            plt.clf()


# Pierwszy z 2 algorytmów, jeszcze nie wiem które ruchy mamy wykonywać w jakiej kombinacji więc wrzuciłem wszystkie 5.
# Też nie wiedziałem jak te metody ładnie wrzucić do tablicy i po nich iterować więc użyłem introspekcji ale chyba jest nadal dosyć czytelne
def steepest_search(solution: Solution, moves):
    # moves = ['swap_vertices_path1',
    #          'swap_vertices_path2',
    #          'swap_edges_path1',
    #          'swap_edges_path2',
    #          'exchange_vertices']

    found_better = True
    while found_better:
        best_length = solution.cumulative_length()
        best_move = None
        best_arg1 = None
        best_arg2 = None
        found_better = False

        for move in moves:
            for arg1 in range(solution.path1_size()):
                arg2_start = 0
                if move != 'exchange_vertices':
                    arg2_start = arg1 + 1

                for arg2 in range(arg2_start, solution.path1_size()):
                    length = solution.cumulative_length_after_move(getattr(solution, move), arg1, arg2)
                    if length < best_length:
                        found_better = True
                        best_length = length
                        best_move = move
                        best_arg1 = arg1
                        best_arg2 = arg2
        if found_better:
            getattr(solution, best_move)(best_arg1, best_arg2)

    return solution


def greedy_search(solution: Solution, moves):
    # moves = ['swap_vertices_path1',
    #          'swap_vertices_path2',
    #          'swap_edges_path1',
    #          'swap_edges_path2',
    #          'exchange_vertices']

    found_better = True

    while found_better:
        best_length = solution.cumulative_length()
        random.shuffle(moves)
        found_better = False

        random.shuffle(moves)
        for move in moves:
            arg1_list = list(range(solution.path1_size()))
            random.shuffle(arg1_list)
            for arg1 in arg1_list:
                arg2_list = deepcopy(arg1_list)
                arg2_list.remove(arg1)
                random.shuffle(arg2_list)
                for arg2 in arg2_list:
                    length = solution.cumulative_length_after_move(getattr(solution, move), arg1, arg2)
                    if length < best_length:
                        found_better = True
                        best_length = length
                        getattr(solution, move)(arg1, arg2)

    return solution


def random_walk(solution: Solution, max_time: float):
    moves = ['swap_vertices_path1',
             'swap_vertices_path2',
             'swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices']

    best_length = solution.cumulative_length()
    best_solution = deepcopy(solution)

    time_start = perf_counter()

    while (perf_counter() - time_start < max_time):
        random.shuffle(moves)
        for move in moves:
            arg1_list = list(range(solution.path1_size()))
            random.shuffle(arg1_list)
            for arg1 in arg1_list:
                arg2_list = deepcopy(arg1_list)
                arg2_list.remove(arg1)
                random.shuffle(arg2_list)
                for arg2 in arg2_list:
                    length = solution.cumulative_length_after_move(getattr(solution, move), arg1, arg2)
                    if length < best_length:
                        best_length = length
                        best_solution = deepcopy(solution)
                    getattr(solution, move)(arg1, arg2)

    return best_solution


def measurements(num_of_measurements=10):
    instances = ['kroA100.tsp', 'kroB100.tsp']
    initializations = ['random_initialization', 'greedy_algorithm_initialization']
    algorithms = [steepest_search, greedy_search]

    movesets = [
        ['swap_vertices_path1',
         'swap_vertices_path2',
         'swap_edges_path1',
         'swap_edges_path2'],

        ['swap_vertices_path1',
         'swap_vertices_path2',
         'exchange_vertices']
    ]

    max_time = 0
    results = []
    times = []

    best_solutions = dict()

    for _ in range(num_of_measurements):
        line = []
        line_times = []
        for instance in instances:
            s = Solution(instance)
            for initialization in initializations:
                initial_solution = deepcopy(s)
                getattr(initial_solution, initialization)()

                line.append(initial_solution.cumulative_length())

                for fun in algorithms:
                    for i_move, moves in enumerate(movesets):
                        time_start = perf_counter()

                        solution = fun(deepcopy(initial_solution), moves)

                        time = perf_counter() - time_start
                        if time > max_time:
                            max_time = time

                        line_times.append(time)
                        line.append(solution.cumulative_length())

                        key = instance + ' ' + initialization + ' ' + fun.__name__ + ' ' + str(i_move)
                        if key not in best_solutions:
                            best_solutions[key] = deepcopy(solution)
                        else:
                            if best_solutions[key].cumulative_length() > solution.cumulative_length():
                                best_solutions[key] = deepcopy(solution)

                solution = random_walk(deepcopy(initial_solution), max_time)
                line.append(solution.cumulative_length())

        results.append(line)
        times.append(line_times)

    results = np.array(results)
    minimum = np.amin(results, 0)
    maximum = np.amax(results, 0)
    std = np.std(results, 0)
    mean = np.mean(results, 0)
    results = [minimum, maximum, std, mean]
    results = np.transpose(np.array(results))

    times = np.array(times)
    minimum_time = np.amin(times, 0)
    maximum_time = np.amax(times, 0)
    std_time = np.std(times, 0)
    mean_time = np.mean(times, 0)
    times = [minimum_time, maximum_time, std_time, mean_time]
    times = np.transpose(np.array(times))

    with open('results.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['min', 'max', 'std', 'mean'])
        for line in results:
            line = [str(a) for a in list(line)]
            writer.writerow(line)

    with open('times.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['min', 'max', 'std', 'mean'])
        for line in times:
            line = [str(a) for a in list(line)]
            writer.writerow(line)

    for key in best_solutions:
        solution = best_solutions[key]
        print(solution.cumulative_length())
        solution.visualise(title=key, save=True)

measurements(10)
