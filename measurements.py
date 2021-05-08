from previous_iterations_steepest_search import PreviousIterationsSteepestSearch
from candidate_moves_steepest_search import CandidateMovesSteepestSearch
import local_search
from solution import Solution
from greedy_algorithms import RegretHeuristics

import time
import concurrent.futures


def runner(moves, i, instance):
    solution = Solution(instance)
    solution.randomized_heuristic_initialization()
    solution = local_search.steepest_search(solution, moves)
    print(i)
    return solution


def multiple_start_local_search(instance):
    moves = ['swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices'
             ]

    res = []

    with concurrent.futures.ProcessPoolExecutor(8) as executor:
        futures = [executor.submit(runner, moves, i, instance) for i in range(10)]
        for future in concurrent.futures.as_completed(futures):
                res.append(future.result())

    best_solution = res[0]
    best_length = res[0].cumulative_length()
    for i in range(1, len(res)):
        solution = res[i]
        length = solution.cumulative_length()
        if length < best_length:
            best_solution = solution
            best_length = length

    return best_solution, best_length


def iterated_local_search1(instance, time_of_execution):
    moves = ['swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices'
             ]

    solution = Solution(instance)
    solution.randomized_heuristic_initialization()

    best_solution = solution
    best_length = solution.cumulative_length()

    t0 = time.perf_counter()
    while time.perf_counter() - t0 < time_of_execution:
        solution.perturbation1()
        solution = local_search.steepest_search(solution, moves)

        length = solution.cumulative_length()
        if length < best_length:
            best_solution = solution
            best_length = length

    return best_solution, best_length


def iterated_local_search2(instance, time_of_execution):
    moves = ['swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices'
             ]

    solution = Solution(instance)
    solution.randomized_heuristic_initialization()

    best_solution = solution
    best_length = solution.cumulative_length()

    t0 = time.perf_counter()
    while time.perf_counter() - t0 < time_of_execution:
        solution.perturbation2()
        solution = local_search.steepest_search(solution, moves)

        length = solution.cumulative_length()
        if length < best_length:
            best_solution = solution
            best_length = length

    return best_solution, best_length


def iterated_local_search2a(instance, time_of_execution):
    solution = Solution(instance)
    solution.randomized_heuristic_initialization()

    best_solution = solution
    best_length = solution.cumulative_length()

    t0 = time.perf_counter()
    while time.perf_counter() - t0 < time_of_execution:
        solution.perturbation2()

        length = solution.cumulative_length()
        if length < best_length:
            best_solution = solution
            best_length = length

    return best_solution, best_length


if __name__ == '__main__':
    instance = 'kroA100.tsp'

    solution, length = multiple_start_local_search(instance)
    solution.visualise()
    print(length)

    solution, length = iterated_local_search1(instance, 20)
    solution.visualise()
    print(length)

    solution, length = iterated_local_search2(instance, 20)
    solution.visualise()
    print(length)

    solution, length = iterated_local_search2a(instance, 20)
    solution.visualise()
    print(length)
