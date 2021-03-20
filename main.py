import math
import random
from matplotlib import pyplot as plt
from copy import copy


# Klasa przechowująca współrzędne wierzchołka
class Vertex:
    def __init__(self, identifier, x, y):
        self.identifier = identifier
        self.x = x
        self.y = y


# Klasa, z której dziedziczą algorytmy zachłanne (implementuje odczyt instancji z pliku, obliczenie długości ścieżek, wizualizację rozwiązania)
class GreedyAlgorithm:
    def __init__(self):
        self.distance_matrix = None  #macierz odległości
        self.vertices = []  # lista wierzchołków - używana tylko do wizualizacji, algorytm bazuje tylko na macierzy odległości!!
        self.size = 0       # rozmiar instancji
        self.path1 = []     # wierzchołki należące do pierwszego cyklu
        self.path2 = []     # wierzchołki należące do drugiego cyklu

    def read_instance(self, file_name):
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

                vertex = Vertex(identifier, x, y)
                self.vertices.append(vertex)

        n = len(self.vertices)
        self.size = n

        self.distance_matrix = [[0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                distance = round(math.sqrt((self.vertices[i].x - self.vertices[j].x) ** 2 + (self.vertices[i].y - self.vertices[j].y) ** 2))
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance

    def calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += self.distance_matrix[path[i]][path[i + 1]]
        length += self.distance_matrix[path[0]][path[-1]]

        return length

    # zwraca łączną długość obu cykli
    def cumulative_length(self):
        return self.calculate_path_length(self.path1) + self.calculate_path_length(self.path2)

    def show_distance_matrix(self):
        for row in self.distance_matrix:
            print(row)

    def visualise(self, title=None):
        x = []
        y = []

        for vertex in self.vertices:
            x.append(vertex.x)
            y.append(vertex.y)
        plt.scatter(x, y, color='k')

        for vertex in self.vertices:
            plt.annotate(vertex.identifier, (vertex.x, vertex.y))

        path1_x = []
        path1_y = []

        for vertex in self.path1:
            path1_x.append(self.vertices[vertex].x)
            path1_y.append(self.vertices[vertex].y)
        path1_x.append(self.vertices[self.path1[0]].x)
        path1_y.append(self.vertices[self.path1[0]].y)
        plt.plot(path1_x, path1_y, 'c-')

        path2_x = []
        path2_y = []

        for vertex in self.path2:
            path2_x.append(self.vertices[vertex].x)
            path2_y.append(self.vertices[vertex].y)
        path2_x.append(self.vertices[self.path2[0]].x)
        path2_y.append(self.vertices[self.path2[0]].y)
        plt.xlabel(type(self).__name__)
        plt.plot(path2_x, path2_y, 'm-')

        if title is not None:
            plt.title(title)
        plt.show()


class NearestNeighbour(GreedyAlgorithm):

    def initialize_starting_vertices(self, vertex1=None, vertex2=None):
        if vertex1 is None or vertex2 is None:
            vertex1 = random.randint(0, self.size - 1)
            max_distance = 0
            vertex2 = None
            for vertex in range(self.size):
                if vertex1 != vertex:
                    distance = self.distance_matrix[vertex1][vertex]
                    if distance > max_distance:
                        max_distance = distance
                        vertex2 = vertex
        self.path1 = [vertex1]
        self.path2 = [vertex2]

    def find_closest_vertex(self, vertex, used_vertices):
        closest_vertex = None
        first = True
        for i in range(self.size):
            if i not in used_vertices and i != vertex:
                if first:
                    min_distance = self.distance_matrix[vertex][i]
                    closest_vertex = i
                    first = False
                else:
                    distance = self.distance_matrix[vertex][i]
                    if distance < min_distance:
                        min_distance = distance
                        closest_vertex = i

        return closest_vertex

    def make_best_insertion(self, path_id, vertex):
        if path_id == 1:
            path = self.path1[:]
        elif path_id == 2:
            path = self.path2[:]

        for i in range(1, len(path) + 1):
            new_path = path[:]
            new_path.insert(i, vertex)
            length = self.calculate_path_length(new_path)

            if i == 1:
                shortest_length = length
                best_insertion = i
            else:
                if length < shortest_length:
                    shortest_length = length
                    best_insertion = i

        if path_id == 1:
            self.path1.insert(best_insertion, vertex)
        elif path_id == 2:
            self.path2.insert(best_insertion, vertex)

    def find_solution(self, vertex1=None, vertex2=None):
        self.initialize_starting_vertices(vertex1, vertex2)

        num_of_iterations = int(self.size / 2) - 1
        previously_added1 = self.path1[0]
        previously_added2 = self.path2[0]

        used_vertices = [previously_added1, previously_added2]

        for i in range(num_of_iterations):
            closest_vertex1 = self.find_closest_vertex(previously_added1, used_vertices)
            used_vertices.append(closest_vertex1)
            self.make_best_insertion(1, closest_vertex1)

            closest_vertex2 = self.find_closest_vertex(previously_added2, used_vertices)
            used_vertices.append(closest_vertex2)
            self.make_best_insertion(2, closest_vertex2)

            previously_added1 = closest_vertex1
            previously_added2 = closest_vertex2

        if self.size % 2 == 1:
            closest_vertex1 = self.find_closest_vertex(previously_added1, used_vertices)
            used_vertices.append(closest_vertex1)
            self.make_best_insertion(1, closest_vertex1)


class GreedyCycle(NearestNeighbour):
    def get_k_insertions(self, path, vertex, k):
        lengths = []

        for i in range(1, len(path) + 1):
            new_path = path[:]
            new_path.insert(i, vertex)
            length = self.calculate_path_length(new_path)
            lengths.append(length)

            if i == 1:
                shortest_length = length
                best_insertion = i
            else:
                if length < shortest_length:
                    shortest_length = length
                    best_insertion = i

        return sorted(lengths)[:k], best_insertion

    def find_best_vertex(self, vertex, used_vertices, path):
        best_vertex = None
        first = True
        for i in range(self.size):
            if i not in used_vertices and i != vertex:
                if first:
                    cost, insertion = self.get_k_insertions(path, i, 1)
                    min_cost = cost[0]
                    best_insertion = insertion
                    best_vertex = i
                    first = False
                else:
                    cost, insertion = self.get_k_insertions(path, i, 1)
                    if cost[0] < min_cost:
                        min_cost = cost[0]
                        best_vertex = i
                        best_insertion = insertion

        path.insert(best_insertion, best_vertex)

        return best_vertex

    def find_solution(self, vertex1=None, vertex2=None):
        self.initialize_starting_vertices(vertex1, vertex2)

        num_of_iterations = int(self.size / 2) - 1
        previously_added1 = self.path1[0]
        previously_added2 = self.path2[0]

        used_vertices = [previously_added1, previously_added2]

        for i in range(num_of_iterations):
            closest_vertex1 = self.find_best_vertex(previously_added1, used_vertices, self.path1)
            used_vertices.append(closest_vertex1)

            closest_vertex2 = self.find_best_vertex(previously_added2, used_vertices, self.path2)
            used_vertices.append(closest_vertex2)

            previously_added1 = closest_vertex1
            previously_added2 = closest_vertex2

        if self.size % 2 == 1:
            closest_vertex1 = self.find_closest_vertex(previously_added1, used_vertices)
            used_vertices.append(closest_vertex1)
            self.make_best_insertion(1, closest_vertex1)


class RegretHeuristics(GreedyCycle):
    def find_best_vertex(self, vertex, used_vertices, path):
        best_vertex = None
        first = True
        for i in range(self.size):
            if i not in used_vertices and i != vertex:
                if first:
                    cost, insertion = self.get_k_insertions(path, i, 2)
                    min_cost = (cost[0] - 0.4*cost[1]) if len(path) > 1 else cost[0]
                    best_insertion = insertion
                    best_vertex = i
                    first = False
                else:
                    cost, insertion = self.get_k_insertions(path, i, 2)
                    cost = (cost[0] - 0.4*cost[1]) if len(path) > 1 else cost[0]
                    if cost < min_cost:
                        min_cost = cost
                        best_vertex = i
                        best_insertion = insertion

        path.insert(best_insertion, best_vertex)

        return best_vertex


# funkcja do wykonania pomiarów
def measurements(num_of_measurements=100):
    instances = ['kroA100.tsp', 'kroB100.tsp']
    results = {}
    best_algorithms = {}
    for instance in instances:
        for algorithm in [NearestNeighbour, GreedyCycle, RegretHeuristics]:
            lengths = []
            min_length = 100000000
            for _ in range(num_of_measurements):
                alg = algorithm()
                alg.read_instance(instance)
                alg.find_solution()
                length = alg.cumulative_length()
                lengths.append(length)
                if min_length > length:
                    min_length = length
                    best_algorithms[instance + ' ' + type(alg).__name__] = copy(alg)
            min_length = min(lengths)
            max_length = max(lengths)
            avg_length = sum(lengths) / num_of_measurements
            results[instance + ' ' + type(alg).__name__] = [min_length, max_length, avg_length]

    for key in best_algorithms:
        alg = best_algorithms[key]
        alg.visualise(key)

    print(results)


alg = NearestNeighbour()
alg.read_instance('kroA100.tsp')
alg.find_solution(11, 26)
print('Laczna dlugosc cykli:', alg.cumulative_length())
alg.visualise()

alg = GreedyCycle()
alg.read_instance('kroA100.tsp')
alg.find_solution(11, 26)
print('Laczna dlugosc cykli:', alg.cumulative_length())
alg.visualise()

alg = RegretHeuristics()
alg.read_instance('kroA100.tsp')
alg.find_solution(11, 26)
print('Laczna dlugosc cykli:', alg.cumulative_length())
alg.visualise()

measurements()