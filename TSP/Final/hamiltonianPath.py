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

    def get_hamiltonian_cycle(self):
        path = [-1] * self.nodes

        # initialize from a random vertex
        path[0] = random.randrange(0, self.nodes)

        if not self.generate_hamiltonian_cycle(path, 1):
            print("No existe solucion para este grafo")
            return None
        path[self.nodes - 1] = path[0]

        self.printsolution(path)
        return path

    @staticmethod
    def printsolution(path):
        print("circuito hamiltoniano encontrado: ")
        for vertex in path:
            print(vertex, end=" ")
        print("\n")
