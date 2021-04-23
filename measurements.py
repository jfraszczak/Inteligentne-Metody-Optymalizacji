from previous_iterations_steepest_search import PreviousIterationsSteepestSearch
from candidate_moves_steepest_search import CandidateMovesSteepestSearch
import local_search
from solution import Solution
from greedy_algorithms import RegretHeuristics


def regret_heuristics(instance):
    regret_heuristics = RegretHeuristics()
    regret_heuristics.read_instance(instance)
    regret_heuristics.find_solution()
    return regret_heuristics.cumulative_length()


def steepest_search(instance):
    moves = ['swap_edges_path1',
             'swap_edges_path2',
             'exchange_vertices']

    solution = Solution(instance)
    solution.random_initialization()
    solution = local_search.steepest_search(solution, moves)
    return solution.cumulative_length()


def previous_iterations_steepest_search(instance):
    steepest_search = PreviousIterationsSteepestSearch(instance)
    solution = steepest_search.local_search()
    return solution.cumulative_length()


def candidate_moves_steepest_search(instance):
    steepest_search = CandidateMovesSteepestSearch(instance)
    solution = steepest_search.local_search()
    return solution.cumulative_length()

instance = 'kroA100.tsp'

print(regret_heuristics(instance))
print(steepest_search(instance))
print(previous_iterations_steepest_search(instance))
print(candidate_moves_steepest_search(instance))