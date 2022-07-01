import copy
import random


class HamiltonianPath:

    def __init__(self, TSPProblem):
        self.TSPProblem = TSPProblem
        self.graph = TSPProblem.get_graph()
        self.nodes = TSPProblem.get_nodes_quantity()

    # check if this vertex is and adjacent vertex of the previously added and is not part of the path
    def is_valid_vertex(self, v, pos, path):
        # Check if current vertex and last vertex in path are adjacent
        if self.graph[path[pos - 1]][v] == 0 or self.graph[path[pos - 1]][v] == 9999:
            return False

        # Check if current vertex not already in path
        for vertex in path:
            if vertex == v:
                return False

        return True

    # stablish the hamiltonian path recursively
    def generate_hamiltonian_cycle(self, path, pos):

        if pos == self.nodes:
            # Last vertex must be adjacent to the first vertex
            if self.graph[path[pos - 1]][path[0]] != 0 and self.graph[path[pos - 1]][path[0]] != 9999:
                return True
            else:
                return False

        # Try different vertices as a next candidate
        for v in range(0, self.nodes):

            if self.is_valid_vertex(v, pos, path):

                path[pos] = v

                if self.generate_hamiltonian_cycle(path, pos + 1):
                    return True

                # Remove current vertex if it doesn't lead to a solution
                path[pos] = -1

        return False

    def get_hamiltonian_cycle(self, initial_node):
        path = [-1] * (self.nodes + 1)

        # initialize from a random vertex
        path[0] = initial_node

        if not self.generate_hamiltonian_cycle(path, 1):
            print("No existe solucion para este grafo")
            return None
        path[self.nodes] = path[0]

        return self.generate_dict_solution(path)

    @staticmethod
    def generate_dict_solution(path):
        solution = dict()
        for i in range(0, len(path) - 1):
            origin = path[i]
            end = path[i + 1]
            solution[origin] = end
        return solution

    @staticmethod
    def printsolution(path):
        print("circuito hamiltoniano encontrado: ")
        for vertex in path:
            print(vertex, end=" ")
        print("\n")

    # stablish the hamiltonian path recursively
    def generate_hamiltonian_cycle_child(self, path, pos, table):

        if pos == self.nodes:
            # Last vertex must be adjacent to the first vertex
            if self.graph[path[pos - 1]][path[0]] != 0 and self.graph[path[pos - 1]][path[0]] != 9999:
                return True
            else:
                return False

        # Try different vertices as a next candidate
        candidates = copy.deepcopy(table[path[pos - 1]])
        if candidates is not None and len(candidates):
            self.order_by_min(candidates, table)
            for v in range(0, len(candidates)):

                if self.is_valid_vertex(candidates[v], pos, path):
                    reference_table = copy.deepcopy(table)
                    path[pos] = candidates[v]
                    self._remove_references(candidates[v], table)

                    if self.generate_hamiltonian_cycle_child(path, pos + 1, table):
                        return True

                    # Remove current vertex if it doesn't lead to a solution
                    path[pos] = -1
                    table = reference_table

        return False

    def get_hamiltonian_cycle_child(self, initial_node, table):
        path = [-1] * (self.nodes + 1)

        # initialize from a random vertex
        path[0] = initial_node
        self._remove_references(path[0], table)

        if not self.generate_hamiltonian_cycle_child(path, 1, table):
            print("No existe solucion para este grafo")
            return None
        path[self.nodes] = path[0]

        return self.generate_dict_solution(path)

    @staticmethod
    def _remove_references(node, table):
        for ady in table.values():
            if node in ady:
                ady.remove(node)

    def _order_candidates(self, candidates, table):
        if len(candidates) == 1:
            return
        elif self._len_equals(candidates, table):
            return
        else:
            self.order_by_min(candidates, table)


    @staticmethod
    def _len_equals(ady_nodes, table):
        lenghts = list()
        for ady in ady_nodes:
            lenghts.append(len(table[ady]))
        return lenghts.count(lenghts[0]) == len(lenghts)

    @staticmethod
    def order_by_min(ady_nodes, table):
        ady_table = dict()
        for ady in ady_nodes:
            ady_table[ady] = table.get(ady)
        res = sorted(ady_table, key=lambda key: len(ady_table[key]))
        ady_nodes.clear()
        for value in res:
            ady_nodes.append(int(value))




