from solution import Solution
import random
from time import time
from copy import deepcopy
import local_search
import math

from proposed_method import create_population

class HybridGeneticAlgorithm:
    def __init__(self, instance_name, population_size, time_limit):
        self.population = []
        self.population_size = population_size
        self.instance_name = instance_name
        self.time_limit = time_limit

    def initialize_population(self):
        for i in range(self.population_size):
            solution = Solution(self.instance_name)
            solution.randomized_heuristic_initialization()

            # moves = ['swap_edges_path1',
            #          'swap_edges_path2',
            #          'exchange_vertices'
            #          ]
            # solution = local_search.steepest_search(solution, moves)

            solution.set_total_length()
            self.population.append(solution)
            print(i)
        self.population = sorted(self.population, key=lambda sol: sol.total_length)

    def initialize_population_improved(self):
        population = create_population(self.instance_name, 500)
        self.population = sorted(population, key=lambda sol: sol.total_length)
        self.population = self.population[:self.population_size]

    def create_list_of_edges(self, solution):
        edges1 = []
        edges2 = []

        path_size = solution.path1_size()
        for i in range(path_size):
            vertex1, vertex2 = solution.path1[i], solution.path1[(i + 1) % path_size]
            edge = self.Edge(vertex1, vertex2)
            edges1.append(edge)

        path_size = solution.path2_size()
        for i in range(path_size):
            vertex1, vertex2 = solution.path2[i], solution.path2[(i + 1) % path_size]
            edge = self.Edge(vertex1, vertex2)
            edges2.append(edge)

        return [edges1, edges2]

    @staticmethod
    def edges_the_same(edge1, edge2):
        return (edge1.vertex1 == edge2.vertex1 and edge1.vertex2 == edge2.vertex2) or \
               (edge1.vertex1 == edge2.vertex2 and edge1.vertex2 == edge2.vertex1)

    def edge_in_list(self, edge, edges):
        for e in edges:
            if self.edges_the_same(edge, e):
                return True
        return False

    def edges_to_vertices(self, edges):
        vertices = []
        for i, edge in enumerate(edges):
            if i == 0 or edge.vertex1 != vertices[-1]:
                vertices.append(edge.vertex1)
            vertices.append(edge.vertex2)

        if vertices[0] == vertices[-1]:
            vertices = vertices[:-1]

        return vertices

    def remove_common_edges(self, parent1, parent2):
        parent1_edges = self.create_list_of_edges(parent1)
        parent2_edges = self.create_list_of_edges(parent2)

        if parent2.total_length < parent1.total_length:
            tmp = deepcopy(parent2)
            parent2 = deepcopy(parent1)
            parent1 = deepcopy(tmp)

        if random.random() < max(math.log(self.iteration / 30 + 1), 0.5):
            perturbated_parent2 = deepcopy(parent2)
            perturbated_parent2.perturbation2()
            parent2 = deepcopy(perturbated_parent2)

        edges_to_delete = []
        for cycle in range(2):
            for i in range(len(parent2_edges[cycle])):
                edge = parent2_edges[cycle][i]

                if not (self.edge_in_list(edge, parent1_edges[0]) or self.edge_in_list(edge, parent1_edges[1])):
                    edges_to_delete.append((edge, cycle))

        for edge, cycle in edges_to_delete:
            parent2_edges[cycle].remove(edge)

        new_paths = []
        used_vertices = []
        for cycle in range(2):
            edges = parent2_edges[cycle]
            vertices = self.edges_to_vertices(edges)
            new_paths.append(vertices)
            used_vertices.extend(vertices)

        child = Solution(self.instance_name + '.tsp')
        child.set_paths(new_paths[0], new_paths[1])

        return child, used_vertices

    def crossover(self, parent1, parent2, perform_local_search=True):
        child, used_vertices = self.remove_common_edges(parent1, parent2)
        child.genetic_algorithm_repair(used_vertices)

        if perform_local_search:
            moves = ['swap_edges_path1',
                     'swap_edges_path2',
                     'exchange_vertices'
                     ]
            child = local_search.steepest_search(child, moves)

        child.set_total_length()

        return child

    def different(self, solution):
        for s in self.population:
            if s.total_length == solution.total_length:
                return False
        return True

    def run(self, perform_local_search=True):
        self.initialize_population_improved()

        start_time = time()
        self.iteration = 0
        while time() - start_time < self.time_limit:
            parent1, parent2 = tuple(random.sample(self.population, 2))
            child = self.crossover(parent1, parent2, perform_local_search=perform_local_search)
            print('New child', child.total_length)
            #child.visualise()

            if child.total_length < self.population[-1].total_length and self.different(child):
                self.population[-1] = child
                self.population = sorted(self.population, key=lambda sol: sol.total_length)


                moves = ['swap_edges_path1',
                         'swap_edges_path2',
                         'exchange_vertices'
                         ]

                self.population[0] = local_search.steepest_search(self.population[0], moves)
                self.population[0].set_total_length()

                print('BEST', self.population[0].cumulative_length())
                #self.population[0].visualise()

            self.iteration += 1

        print(self.population[0].total_length)
        print(self.population[1].total_length)
        print(self.population[0].path1_size(), self.population[0].path2_size())
        #self.population[0].visualise()
        return self.population[0]

    class Edge:
        def __init__(self, vertex1, vertex2):
            self.vertex1 = vertex1
            self.vertex2 = vertex2

        def show(self):
            print('({}, {})'.format(self.vertex1 + 1, self.vertex2 + 1))


def measurements(instance_name, time, num_of_measurements=5, perform_local_search=True):
    if perform_local_search:
        title = instance_name + '-ILS2'
    else:
        title = instance_name + '-ILS2a'

    best_solution = None
    scores = []

    for i in range(num_of_measurements):
        alg = HybridGeneticAlgorithm(instance_name, 100, time)
        solution = alg.run(perform_local_search=perform_local_search)

        scores.append(solution.total_length)

        if best_solution is None:
            best_solution = solution
        else:
            if solution.total_length < best_solution.total_length:
                best_solution = solution

    minimum = min(scores)
    maximum = max(scores)
    avg = sum(scores) / len(scores)

    file = open(title + '.txt', 'w')
    file.write(str(minimum) + ' ' + str(maximum) + ' ' + str(avg))

    best_solution.visualise(title=title + '.png', save=True)


measurements('kroA200', 600, perform_local_search=True)
measurements('kroB200', 600, perform_local_search=True)




