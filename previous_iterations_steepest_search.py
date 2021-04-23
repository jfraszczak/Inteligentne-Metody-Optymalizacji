from effective_steepest_search import EffectiveSteepestSearch
from copy import deepcopy


class PreviousIterationsSteepestSearch(EffectiveSteepestSearch):

    def initialize_moves_list(self):
        move_type = 'exchange_vertices'
        for vertex_a_index, vertex_a in enumerate(self.solution.path1):
            for vertex_b_index, vertex_b in enumerate(self.solution.path2):
                solution_length = self.solution.cumulative_length_after_move(move_type, vertex_a_index, vertex_b_index)
                improvement = self.solution.cumulative_length() - solution_length
                if improvement > 0:
                    move = self.Move(move_type, vertex_a=vertex_a, vertex_b=vertex_b, improvement=improvement)
                    self.moves_list.append(move)

        for path in ['path1', 'path2']:
            path_size = getattr(self.solution, path + '_size')()
            move_type = 'swap_edges_' + path
            for edge_a_index in range(path_size):
                for edge_b_index in range(edge_a_index + 2, path_size):
                    if (edge_a_index - 1) % path_size != edge_b_index:
                        edge_b_index = edge_b_index % path_size
                        solution_length = self.solution.cumulative_length_after_move(move_type, edge_a_index,
                                                                                     edge_b_index)
                        improvement = self.solution.cumulative_length() - solution_length
                        if improvement > 0:
                            edge_a = self.index_to_edge(edge_a_index, path, path_size=path_size)
                            edge_b = self.index_to_edge(edge_b_index, path, path_size=path_size)
                            move = self.Move(move_type, edge_a=edge_a, edge_b=edge_b, improvement=improvement)
                            self.moves_list.append(move)

        self.moves_list.sort(key=lambda move: move.improvement, reverse=True)

    def add_move(self, move):  # przerobić na dzielenie przez połowienie
        if move.improvement > 0:
            for i in range(len(self.moves_list)):
                if self.moves_list[i].improvement <= move.improvement:
                    self.moves_list.insert(i, move)
                    return
            self.moves_list.append(move)

    def add_new_edges_swaps(self, edge, path):
        path_size = getattr(self.solution, path + '_size')()
        move_type = 'swap_edges_' + path
        edge_index = self.solution.edge_to_index(edge, path)

        for new_edge_index in range(path_size):
            if new_edge_index != edge_index and new_edge_index != (edge_index - 1) % path_size and new_edge_index != (
                    edge_index + 1) % path_size:
                solution_length = self.solution.cumulative_length_after_move(move_type, edge_index, new_edge_index)
                improvement = self.solution.cumulative_length() - solution_length
                new_edge = self.index_to_edge(new_edge_index, path, path_size=path_size)
                move = self.Move(move_type, edge_a=edge, edge_b=new_edge, improvement=improvement)
                self.add_move(move)

    def add_new_moves_after_edges_swap(self, path):
        self.add_new_edges_swaps(self.previous_move.edge_a, path)
        self.add_new_edges_swaps(self.previous_move.edge_b, path)

    def add_new_edges_after_vertices_exchange(self):
        vertex_a = self.previous_move.vertex_a
        vertex_b = self.previous_move.vertex_b

        previous_vertex_a, next_vertex_a = self.solution.previous_and_next_vertex(vertex_a, 'path2')
        previous_vertex_b, next_vertex_b = self.solution.previous_and_next_vertex(vertex_b, 'path1')

        edge_a_path1 = self.Edge(previous_vertex_b, vertex_b)
        edge_b_path1 = self.Edge(vertex_b, next_vertex_b)
        self.add_new_edges_swaps(edge_a_path1, 'path1')
        self.add_new_edges_swaps(edge_b_path1, 'path1')

        edge_a_path2 = self.Edge(previous_vertex_a, vertex_a)
        edge_b_path2 = self.Edge(vertex_a, next_vertex_a)
        self.add_new_edges_swaps(edge_a_path2, 'path2')
        self.add_new_edges_swaps(edge_b_path2, 'path2')

    def add_new_vertices_exchanges(self, exchanged_vertex, path):
        move_type = 'exchange_vertices'
        for i in range(len(getattr(self.solution, path))):
            vertex = getattr(self.solution, path)[i]
            solution_length = self.solution.cumulative_length_after_move(move_type, vertex, exchanged_vertex, index=False)
            improvement = self.solution.cumulative_length() - solution_length
            if path == 'path1':
                move = self.Move(move_type, vertex_a=vertex, vertex_b=exchanged_vertex, improvement=improvement)
            elif path == 'path2':
                move = self.Move(move_type, vertex_a=exchanged_vertex, vertex_b=vertex, improvement=improvement)
            self.add_move(move)

    def add_new_moves_after_vertices_exchange(self):
        self.add_new_vertices_exchanges(self.previous_move.vertex_a, 'path1')
        self.add_new_vertices_exchanges(self.previous_move.vertex_b, 'path2')
        self.add_new_edges_after_vertices_exchange()

    def perform_first_applicable_move(self):
        for move in self.moves_list:
            perform = False
            if move.applicable(self.solution):
                if move.type == 'exchange_vertices':
                    if self.solution.cumulative_length_after_move(move.type, move.vertex_a, move.vertex_b, index=False) < self.solution.cumulative_length():
                        perform = True
                else:
                    if self.solution.cumulative_length_after_move(move.type, move.edge_a, move.edge_b, index=False) < self.solution.cumulative_length():
                        perform = True
                if perform:
                    self.perform_move(move)
                    self.previous_move = deepcopy(move)
                    self.moves_list.remove(move)
                    return True
            elif not move.edges_exist_but_different_directions(self.solution):
                self.moves_list.remove(move)
        return False

    def update_moves_list(self):
        if self.previous_move is None:
            self.initialize_moves_list()
        else:
            if self.previous_move.type == 'swap_edges_path1' or self.previous_move.type == 'swap_edges_path2':
                if self.previous_move.type == 'swap_edges_path1':
                    path = 'path1'
                else:
                    path = 'path2'

                self.add_new_moves_after_edges_swap(path)

            elif self.previous_move.type == 'exchange_vertices':
                self.add_new_moves_after_vertices_exchange()

    def local_search(self):
        self.update_moves_list()
        move_performed = True
        while move_performed:
            move_performed = self.perform_first_applicable_move()
            self.update_moves_list()

        return self.solution