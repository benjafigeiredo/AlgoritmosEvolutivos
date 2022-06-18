import math

import tsplib95
from hamiltonianPath import HamiltonianPath


class TSPProblem:

    def __init__(self, path, population_size=100):
        self._matrix = tsplib95.load(path)
        self._hamiltonian_path = HamiltonianPath(self)
        self._population_size = population_size
        self._solutions = dict()

    def generate_population(self):
        print('Inicializando poblacion de manera random')
        for solution_num in range(0, self._population_size):
            self._generate_solution(solution_num)

    def _generate_solution(self, solution_num):
        self._solutions[solution_num] = self._hamiltonian_path.get_hamiltonian_cycle()

    def _decode_solution(self, solution_num):
        solution = self._solutions[solution_num]
        weight = 0
        for origin in solution.keys():
            destination = solution[origin]
            weight += self.get_weight(origin, destination)
        return weight

    def decode_solutions(self):
        for solution in range(0, self._population_size):
            self._decode_solution(solution)

    @staticmethod
    def _calculate_fitness(value):
        return 1 / value

    def _get_exponential_value(self, value):
        return (1 - math.exp(value * (-1))) / self._population_size

    def calculate_solutions_fitness(self):
        for solution in range(0, self._population_size):
            fitness = self._calculate_fitness(self._decode_solution(solution))
            print(fitness)

    def get_nodes(self):
        return list(self._matrix.get_nodes())

    def get_nodes_quantity(self):
        return len(self.get_nodes())

    def get_weight(self, origin, end):
        return self._matrix.get_weight(origin, end)

    def get_graph(self):
        return self._matrix.as_name_dict()['edge_weights']

    def is_ady(self, origin, end):
        return self.get_weight(origin, end) != 0 and self.get_weight(origin, end) != 9999

    def get_ady_nodes(self, node):
        nodes = list(self.get_graph()[node])
        ady = list()
        for ady_node in range(len(nodes)):
            weight = self.get_graph()[node][ady_node]
            if weight != 0 and weight != 9999:
                ady.append(ady_node)
        return ady

    def _get_number_of_ady_nodes(self, node):
        return len(self.get_ady_nodes(node))


path2 = './Resources/Instancias-TSP/br17.atsp'
TSPProblem = TSPProblem(path2, population_size=100)
TSPProblem.generate_population()
TSPProblem.decode_solutions()
TSPProblem.calculate_solutions_fitness()
