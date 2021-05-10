from previous_iterations_steepest_search import PreviousIterationsSteepestSearch
from candidate_moves_steepest_search import CandidateMovesSteepestSearch
import local_search
from solution import Solution
from greedy_algorithms import RegretHeuristics
import numpy as np
import time
import concurrent.futures


def runner(moves, instance):
    solution = Solution(instance)
    solution.randomized_heuristic_initialization()
    solution = local_search.steepest_search(solution, moves)
    return solution


def multiple_start_local_search(instance):
    moves = ['swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices'
             ]

    res = []

    time_start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(16) as executor:
        futures = [executor.submit(runner, moves, instance) for _ in range(32)]
        for future in concurrent.futures.as_completed(futures):
            res.append(future.result())
    time_end = time.perf_counter() - time_start

    best_solution = res[0]
    best_length = res[0].cumulative_length()
    for i in range(1, len(res)):
        solution = res[i]
        length = solution.cumulative_length()
        if length < best_length:
            best_solution = solution
            best_length = length

    return best_solution, best_length, time_end


def iterated_local_search1(instance, time_of_execution):
    moves = ['swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices'
             ]

    solution = Solution(instance)
    solution.randomized_heuristic_initialization()

    best_solution = solution
    best_length = solution.cumulative_length()
    print(best_length)

    t0 = time.perf_counter()
    while time.perf_counter() - t0 < time_of_execution:
        solution.perturbation1()
        solution = local_search.steepest_search(solution, moves)

        length = solution.cumulative_length()
        if length < best_length:
            best_solution = solution
            best_length = length
            print(best_length)

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
    instance = 'kroA200.tsp'
    #
    # msls = []
    # msls_l = np.empty(6)
    # msls_t = np.empty(6)
    # for i in range(1):
    #     sol, msls_l[i], msls_t[i] = multiple_start_local_search(instance)
    #     msls.append(sol)
    #
    # t_avg = msls_t.mean()
    # print(f"msls average time: {t_avg}")
    # print(f"msls average len: {msls_l.mean()}")
    # print(f"msls longest: {msls_l.max()}")
    # print(f"msls shortest: {msls_l.min()}")
    # msls_best = msls_l.argmin()

    t_avg = 637.8583766700001

    ils1 = []
    ils1_l = np.empty(6)
    for i in range(6):
        sol, ils1_l[i] = iterated_local_search1(instance, t_avg)
        ils1.append(sol)

    print(f"ils1 average len: {ils1_l.mean()}")
    print(f"ils1 longest: {ils1_l.max()}")
    print(f"ils1 shortest: {ils1_l.min()}")
    ils1_best = ils1_l.argmin()

    # ils2 = []
    # ils2_l = np.empty(6)
    # for i in range(6):
    #     sol, ils2_l[i] = iterated_local_search2(instance, t_avg)
    #     ils2.append(sol)
    #
    # print(f"ils2 average len: {ils2_l.mean()}")
    # print(f"ils2 longest: {ils2_l.max()}")
    # print(f"ils2 shortest: {ils2_l.min()}")
    # ils2_best = ils2_l.argmin()
    #
    # ils2a = []
    # ils2a_l = np.empty(6)
    # for i in range(6):
    #     sol, ils2a_l[i] = iterated_local_search2a(instance, t_avg)
    #     ils2a.append(sol)
    #
    # print(f"ils2 average len: {ils2a_l.mean()}")
    # print(f"ils2 longest: {ils2a_l.max()}")
    # print(f"ils2 shortest: {ils2a_l.min()}")
    # ils2_best = ils2a_l.argmin()

    #msls[msls_best].visualise()
    ils1[ils1_best].visualise()
    # ils2[ils2_best].visualise()
    # ils2a[ils2_best].visualise()
