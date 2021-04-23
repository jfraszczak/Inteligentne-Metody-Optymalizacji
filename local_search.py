import random
from copy import deepcopy
from time import perf_counter
import numpy as np
import csv
from solution import Solution


# Pierwszy z 2 algorytmów, jeszcze nie wiem które ruchy mamy wykonywać w jakiej kombinacji więc wrzuciłem wszystkie 5.
# Też nie wiedziałem jak te metody ładnie wrzucić do tablicy i po nich iterować więc użyłem introspekcji ale chyba jest nadal dosyć czytelne
def steepest_search(solution: Solution, moves):
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
                    length = solution.cumulative_length_after_move(move, arg1, arg2)
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
                    length = solution.cumulative_length_after_move(move, arg1, arg2)
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

    while perf_counter() - time_start < max_time:
        random.shuffle(moves)
        for move in moves:
            arg1_list = list(range(solution.path1_size()))
            random.shuffle(arg1_list)
            for arg1 in arg1_list:
                arg2_list = deepcopy(arg1_list)
                arg2_list.remove(arg1)
                random.shuffle(arg2_list)
                for arg2 in arg2_list:
                    length = solution.cumulative_length_after_move(move, arg1, arg2)
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
