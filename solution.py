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

        self.total_length = None

    def vertices_distance(self, vertex1, vertex2):
        return self.instance.distance_matrix[vertex1][vertex2]

    def set_paths(self, path1, path2):
        self.path1 = path1
        self.path2 = path2

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

    def randomized_heuristic_initialization(self):
        alg = GreedyCycle()
        alg.read_instance_object(self.instance)
        alg.find_solution_randomized()
        self.path1 = alg.path1[:]
        self.path2 = alg.path2[:]

    def perturbation1(self):
        num_of_vertices_exchanges = 5
        num_of_vertices_swaps = 3

        central_vertices = []
        for vertex in self.instance.vertices:
            if 1000 < vertex.x < 3000:
                central_vertices.append(vertex.identifier - 1)

        #print(central_vertices)

        central_vertices1 = []
        for i in range(self.path1_size()):
            if self.path1[i] in central_vertices:
                central_vertices1.append(i)

        central_vertices2 = []
        for i in range(self.path2_size()):
            if self.path2[i] in central_vertices:
                central_vertices2.append(i)

        # print(central_vertices1)
        # print(central_vertices2)

        for i in range(num_of_vertices_exchanges):
            if len(central_vertices1) > 0 and len(central_vertices2) > 0:
                vertex1 = random.randint(0, len(central_vertices1) - 1)
                vertex2 = random.randint(0, len(central_vertices2) - 1)
                self.exchange_vertices(vertex1, vertex2)
        #
        # for i in range(num_of_vertices_swaps):
        #     vertex1 = random.randint(0, self.path1_size() - 1)
        #     vertex2 = random.randint(0, self.path1_size() - 1)
        #     self.swap_vertices_path1(vertex1, vertex2)
        #
        # for i in range(num_of_vertices_swaps):
        #     vertex1 = random.randint(0, self.path2_size() - 1)
        #     vertex2 = random.randint(0, self.path2_size() - 1)
        #     self.swap_vertices_path2(vertex1, vertex2)

        for i in range(num_of_vertices_swaps):
            edge1 = random.randint(0, self.path1_size())
            edge2 = random.randint(0, self.path1_size())
            self.swap_edges_path1(edge1, edge2)

        for i in range(num_of_vertices_swaps):
            edge1 = random.randint(0, self.path2_size())
            edge2 = random.randint(0, self.path2_size())
            self.swap_edges_path2(edge1, edge2)

    def destroy(self, percentage):
        removed_vertices = []
        for i in range(int(percentage * self.path1_size())):
            vertex_to_remove = random.choice(self.path1)
            self.path1.remove(vertex_to_remove)
            removed_vertices.append(vertex_to_remove)

        for i in range(int(percentage * self.path2_size())):
            vertex_to_remove = random.choice(self.path2)
            self.path2.remove(vertex_to_remove)
            removed_vertices.append(vertex_to_remove)

        return removed_vertices

    def perturbation2(self):
        percentage = 0.3
        used_vertices = []
        removed_vertices = self.destroy(percentage)
        for i in range(self.instance.size):
            if i not in removed_vertices:
                used_vertices.append(i)

        greedy = GreedyCycleRepair(self)
        self = greedy.repair2(used_vertices, int(self.instance.size * percentage / 2))

    def genetic_algorithm_repair(self, used_vertices):
        greedy = GreedyCycleRepair(self)
        self = greedy.repair2(used_vertices, int(self.instance.size / 2))

    def exchange_vertices(self, vertex1, vertex2, index=True):
        if not index:
            vertex1 = self.vertex_to_index(vertex1, 'path1')
            vertex2 = self.vertex_to_index(vertex2, 'path2')

        self.path1[vertex1], self.path2[vertex2] = self.path2[vertex2], self.path1[vertex1]

    def swap_vertices_path1(self, vertex1, vertex2, index=True):
        if not index:
            vertex1 = self.vertex_to_index(vertex1, 'path1')
            vertex2 = self.vertex_to_index(vertex2, 'path1')

        self.path1[vertex1], self.path1[vertex2] = self.path1[vertex2], self.path1[vertex1]

    def swap_vertices_path2(self, vertex1, vertex2, index=True):
        if not index:
            vertex1 = self.vertex_to_index(vertex1, 'path1')
            vertex2 = self.vertex_to_index(vertex2, 'path1')

        self.path2[vertex1], self.path2[vertex2] = self.path2[vertex2], self.path2[vertex1]

    def swap_edges_path1(self, edge1, edge2, index=True):
        new_path = []
        if not index:
            path = 'path1'
            edge1, edge2 = self.edge_to_index(edge1, path), self.edge_to_index(edge2, path)

        edge1, edge2 = min(edge1, edge2), max(edge1, edge2)

        new_path = new_path + self.path1[:edge1 + 1]
        new_path.extend(reversed(self.path1[edge1 + 1: edge2 + 1]))
        new_path = new_path + self.path1[edge2 + 1: len(self.path1)]

        self.path1 = new_path[:]

    def swap_edges_path2(self, edge1, edge2, index=True):
        new_path = []
        if not index:
            path = 'path2'
            edge1, edge2 = self.edge_to_index(edge1, path), self.edge_to_index(edge2, path)

        edge1, edge2 = min(edge1, edge2), max(edge1, edge2)

        new_path = new_path + self.path2[:edge1 + 1]
        new_path.extend(reversed(self.path2[edge1 + 1: edge2 + 1]))
        new_path = new_path + self.path2[edge2 + 1: len(self.path2)]

        self.path2 = new_path[:]

    def cumulative_length_after_move(self, move, *args, index=True):
        path1 = self.path1[:]
        path2 = self.path2[:]
        getattr(self, move)(*args, index=index)
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

    def set_total_length(self):
        self.total_length = self.cumulative_length()

    def path1_size(self):
        return len(set(self.path1))

    def path2_size(self):
        return len(set(self.path2))

    def previous_and_next_vertex(self, vertex, path):
        path_size = getattr(self, path + '_size')()
        index = self.vertex_to_index(vertex, path)
        previous_index = index - 1 if index - 1 >= 0 else path_size - 1
        next_index = index + 1 if index + 1 < path_size else 0

        return getattr(self, path)[previous_index], getattr(self, path)[next_index]

    def index_to_vertex(self, index, path):
        if index < getattr(self, path + '_size')():
            return getattr(self, path)[index]
        return -1

    def vertex_to_index(self, vertex, path):
        path_size = getattr(self, path + '_size')()
        for index in range(path_size):
            if vertex == getattr(self, path)[index]:
                return index
        return -1

    def edge_to_index(self, edge, path):
        path_size = getattr(self, path + '_size')()
        for index1 in range(path_size):
            index2 = index1 + 1
            if index1 + 1 == path_size:
                index2 = 0
            if edge.vertex_a == getattr(self, path)[index1] and edge.vertex_b == getattr(self, path)[index2]:
                return index1
        return -1

    def edge_in_path(self, edge, path):
        path_size = getattr(self, path + '_size')()
        for index1 in range(path_size):
            index2 = index1 + 1
            if index1 + 1 == path_size:
                index2 = 0
            if edge.vertex_a == getattr(self, path)[index1] and edge.vertex_b == getattr(self, path)[index2]:
                return True
        return False

    def reversed_edge_in_path(self, edge, path):
        path_size = getattr(self, path + '_size')()
        for index1 in range(path_size):
            index2 = index1 + 1
            if index1 + 1 == path_size:
                index2 = 0
            if edge.vertex_a == getattr(self, path)[index2] and edge.vertex_b == getattr(self, path)[index1]:
                return True
        return False

    def show(self):
        print('PATH1', self.path1)
        print('PATH2', self.path2)

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


class GreedyCycleRepair():

    def __init__(self, solution):
        self.solution = solution

    def calculate_path_length(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += self.solution.instance.distance_matrix[path[i]][path[i + 1]]
        length += self.solution.instance.distance_matrix[path[0]][path[-1]]

        return length

    def make_best_insertion(self, path_id, vertex):
        if path_id == 1:
            path = self.solution.path1[:]
        elif path_id == 2:
            path = self.solution.path2[:]

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
            self.solution.path1.insert(best_insertion, vertex)
        elif path_id == 2:
            self.solution.path2.insert(best_insertion, vertex)

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
        for i in range(self.solution.instance.size):
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

    def repair(self, used_vertices, num_of_iterations):

        previously_added1 = self.solution.path1[0]
        previously_added2 = self.solution.path2[0]

        for i in range(num_of_iterations):
            closest_vertex1 = self.find_best_vertex(previously_added1, used_vertices, self.solution.path1)
            used_vertices.append(closest_vertex1)

            closest_vertex2 = self.find_best_vertex(previously_added2, used_vertices, self.solution.path2)
            used_vertices.append(closest_vertex2)

            previously_added1 = closest_vertex1
            previously_added2 = closest_vertex2

        return self.solution

    def repair2(self, used_vertices, final_path_size):
        previously_added1 = self.solution.path1[0]
        previously_added2 = self.solution.path2[0]

        path1_size = len(self.solution.path1)
        path2_size = len(self.solution.path2)

        num_of_iterations = final_path_size - max(path1_size, path2_size)

        for i in range(num_of_iterations):
            closest_vertex1 = self.find_best_vertex(previously_added1, used_vertices, self.solution.path1)
            used_vertices.append(closest_vertex1)

            closest_vertex2 = self.find_best_vertex(previously_added2, used_vertices, self.solution.path2)
            used_vertices.append(closest_vertex2)

            previously_added1 = closest_vertex1
            previously_added2 = closest_vertex2

        while len(self.solution.path1) < final_path_size:
            closest_vertex1 = self.find_best_vertex(previously_added1, used_vertices, self.solution.path1)
            used_vertices.append(closest_vertex1)
            previously_added1 = closest_vertex1

        while len(self.solution.path2) < final_path_size:
            closest_vertex2 = self.find_best_vertex(previously_added2, used_vertices, self.solution.path2)
            used_vertices.append(closest_vertex2)
            previously_added2 = closest_vertex2

        return self.solution