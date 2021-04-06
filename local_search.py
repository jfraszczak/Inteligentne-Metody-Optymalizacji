from greedy_algorithms import NearestNeighbour, GreedyCycle, RegretHeuristics
import math
from matplotlib import pyplot as plt
import random


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
                distance = round(math.sqrt((self.vertices[i].x - self.vertices[j].x) ** 2 + (self.vertices[i].y - self.vertices[j].y) ** 2))
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

    def greedy_algorithm_initialization(self, algorithm):
        alg = algorithm()
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

    def visualise(self, title=None):
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
        plt.show()


# Pierwszy z 2 algorytmów, jeszcze nie wiem które ruchy mamy wykonywać w jakiej kombinacji więc wrzuciłem wszystkie 5.
# Też nie wiedziałem jak te metody ładnie wrzucić do tablicy i po nich iterować więc użyłem introspekcji ale chyba jest nadal dosyć czytelne
def steepest_search(solution):
    moves = ['swap_vertices_path1',
             'swap_vertices_path2',
             'swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices']

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

# Inicjalizacja rozwiązania
s = Solution('kroA100.tsp')
#s.random_initialization()
s.greedy_algorithm_initialization(GreedyCycle)
print(s.cumulative_length())
s.visualise()

# Zastosowanie tego steepest searcha
sol = steepest_search(s)
print(sol.cumulative_length())
sol.visualise()

