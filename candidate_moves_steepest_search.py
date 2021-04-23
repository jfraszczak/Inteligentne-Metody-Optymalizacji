from effective_steepest_search import EffectiveSteepestSearch

class CandidateMovesSteepestSearch(EffectiveSteepestSearch):

    @staticmethod
    def add_to_closest(closest, vertex_to_add, num_of_neighbours):
        if len(closest) == 0:
            closest.append(vertex_to_add)
        else:
            if len(closest) < num_of_neighbours or closest[-1][1] > vertex_to_add[1]:
                added = False
                for i in range(len(closest)):
                    vertex = closest[i]
                    if vertex[1] > vertex_to_add[1]:
                        closest.insert(i, vertex_to_add)
                        added = True
                        break
                if not added and len(closest) < num_of_neighbours:
                    closest.append(vertex_to_add)
        closest = closest[:num_of_neighbours]
        return closest

    def find_neighbours(self, vertex, num_of_neighbours):
        closest = []
        for potential_neighbour in range(self.solution.instance.size):
            if potential_neighbour != vertex:
                distance = self.solution.vertices_distance(vertex, potential_neighbour)
                closest = self.add_to_closest(closest, (potential_neighbour, distance), num_of_neighbours)
        return [vertex[0] for vertex in closest]

    def vertices_in_the_same_path(self, vertex1, vertex2):
        for path in ['path1', 'path2']:
            if vertex1 in getattr(self.solution, path) and vertex2 in getattr(self.solution, path):
                return True
        return False

    @staticmethod
    def complementary_path(path):
        if path == 'path1':
            return 'path2'
        return 'path1'

    def update_moves_list(self, num_of_neighbours):
        self.moves_list = []
        for path in ['path1', 'path2']:
            for vertex in getattr(self.solution, path):
                closest_vertices = self.find_neighbours(vertex, num_of_neighbours)
                for neighbour in closest_vertices:
                    if not self.vertices_in_the_same_path(vertex, neighbour):
                        move_type = 'exchange_vertices'
                        previous_vertex, next_vertex = self.solution.previous_and_next_vertex(neighbour, self.complementary_path(path))

                        solution_length = self.solution.cumulative_length_after_move(move_type, vertex, previous_vertex, index=False)
                        improvement1 = self.solution.cumulative_length() - solution_length

                        solution_length = self.solution.cumulative_length_after_move(move_type, vertex, next_vertex, index=False)
                        improvement2 = self.solution.cumulative_length() - solution_length

                        if path == 'path1':
                            move1 = self.Move(move_type, vertex_a=vertex, vertex_b=previous_vertex, improvement=improvement1)
                            move2 = self.Move(move_type, vertex_a=vertex, vertex_b=next_vertex, improvement=improvement2)
                        elif path == 'path2':
                            move1 = self.Move(move_type, vertex_a=previous_vertex, vertex_b=vertex, improvement=improvement1)
                            move2 = self.Move(move_type, vertex_a=next_vertex, vertex_b=vertex, improvement=improvement2)

                        previous_vertex, next_vertex = self.solution.previous_and_next_vertex(vertex, path)

                        solution_length = self.solution.cumulative_length_after_move(move_type, neighbour, previous_vertex, index=False)
                        improvement1 = self.solution.cumulative_length() - solution_length

                        solution_length = self.solution.cumulative_length_after_move(move_type, neighbour, next_vertex, index=False)
                        improvement2 = self.solution.cumulative_length() - solution_length

                        if self.complementary_path(path) == 'path1':
                            move3 = self.Move(move_type, vertex_a=neighbour, vertex_b=previous_vertex, improvement=improvement1)
                            move4 = self.Move(move_type, vertex_a=neighbour, vertex_b=next_vertex, improvement=improvement2)
                        elif self.complementary_path(path) == 'path2':
                            move3 = self.Move(move_type, vertex_a=previous_vertex, vertex_b=neighbour, improvement=improvement1)
                            move4 = self.Move(move_type, vertex_a=next_vertex, vertex_b=neighbour, improvement=improvement2)

                        moves = [move1, move2, move3, move4]
                        for move in moves:
                            if move.improvement > 0:
                                self.moves_list.append(move)
                    else:
                        move_type = 'swap_edges_' + path
                        previous_vertex, next_vertex = self.solution.previous_and_next_vertex(vertex, path)
                        previous_vertex_neighbour, next_vertex_neighbour = self.solution.previous_and_next_vertex(neighbour, self.complementary_path(path))

                        edge_vertex_first = self.Edge(vertex, next_vertex)
                        edge_neighbour_first = self.Edge(neighbour, next_vertex_neighbour)

                        edge_vertex_second = self.Edge(previous_vertex, vertex)
                        edge_neighbour_second = self.Edge(previous_vertex_neighbour, neighbour)

                        solution_length = self.solution.cumulative_length_after_move(move_type, edge_vertex_first, edge_neighbour_first, index=False)
                        improvement1 = self.solution.cumulative_length() - solution_length

                        solution_length = self.solution.cumulative_length_after_move(move_type, edge_vertex_second, edge_neighbour_second, index=False)
                        improvement2 = self.solution.cumulative_length() - solution_length

                        move1 = self.Move(move_type, edge_a=edge_vertex_first, edge_b=edge_neighbour_first, improvement=improvement1)
                        move2 = self.Move(move_type, edge_a=edge_vertex_second, edge_b=edge_neighbour_second, improvement=improvement2)

                        moves = [move1, move2]
                        for move in moves:
                            if move.improvement > 0:
                                self.moves_list.append(move)
                                #move.show()

        self.moves_list.sort(key=lambda move: move.improvement, reverse=True)

    def best_move(self):
        return self.moves_list[0]

    def stop_condition(self):
        return len(self.moves_list) == 0

    def local_search(self):
        num_of_neighbours = 10
        self.update_moves_list(num_of_neighbours)
        while not self.stop_condition():
            move = self.best_move()
            self.perform_move(move)
            self.update_moves_list(num_of_neighbours)

        return self.solution