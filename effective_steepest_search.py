from solution import Solution
import abc


class EffectiveSteepestSearch:
    __metaclass__ = abc.ABCMeta

    def __init__(self, instance_name):
        self.moves_list = []
        self.solution = Solution(instance_name)
        self.solution.random_initialization()
        self.previous_move = None

    class Edge:
        def __init__(self, vertex_a, vertex_b):
            self.vertex_a = vertex_a
            self.vertex_b = vertex_b

        def string(self):
            return '(' + str(self.vertex_a + 1) + ', ' + str(self.vertex_b + 1) + ')'

        def show(self):
            print('(' + str(self.vertex_a + 1) + ', ' + str(self.vertex_b + 1) + ')')

    class Move:
        def __init__(self, move_type, vertex_a=None, vertex_b=None, edge_a=None, edge_b=None, improvement=None):
            self.type = move_type
            self.vertex_a = vertex_a
            self.vertex_b = vertex_b
            self.edge_a = edge_a
            self.edge_b = edge_b
            self.improvement = improvement

        def applicable(self, solution):
            if self.type == 'exchange_vertices':
                return self.vertex_a in solution.path1 and self.vertex_b in solution.path2
            else:
                if self.type == 'swap_edges_path1':
                    path = 'path1'
                elif self.type == 'swap_edges_path2':
                    path = 'path2'
                return (solution.edge_in_path(self.edge_a, path) and solution.edge_in_path(self.edge_b, path)) or \
                       (solution.reversed_edge_in_path(self.edge_a, path) and solution.reversed_edge_in_path(
                           self.edge_b, path))

        def edges_exist_but_different_directions(self, solution):
            if self.type == 'exchange_vertices':
                return False
            if self.type == 'swap_edges_path1':
                path = 'path1'
            elif self.type == 'swap_edges_path2':
                path = 'path2'

            return (solution.reversed_edge_in_path(self.edge_a, path) and solution.edge_in_path(self.edge_b, path)) or \
                   (solution.edge_in_path(self.edge_a, path) and solution.reversed_edge_in_path(self.edge_b, path))

        def show(self):
            print(self.type, self.vertex_a + 1 if self.vertex_a is not None else None,
                  self.vertex_b + 1 if self.vertex_a is not None else None,
                  self.edge_a.string() if self.edge_a is not None else None,
                  self.edge_b.string() if self.edge_b is not None else None, self.improvement)

    def index_to_edge(self, index, path, path_size=None):
        if path_size is None:
            path_size = getattr(self.solution, path + '_size')()
        vertex_a = self.solution.index_to_vertex(index, path)
        vertex_b = self.solution.index_to_vertex(index + 1 if index + 1 < path_size else 0, path)
        edge = self.Edge(vertex_a, vertex_b)

        return edge

    def perform_move(self, move):
        if move.type == 'exchange_vertices':
            self.solution.exchange_vertices(move.vertex_a, move.vertex_b, index=False)
        elif move.type == 'swap_edges_path1' or move.type == 'swap_edges_path2':
            getattr(self.solution, move.type)(move.edge_a, move.edge_b, index=False)

    def show_moves(self):
        for move in self.moves_list:
            move.show()

    @abc.abstractmethod
    def local_search(self):
        return
