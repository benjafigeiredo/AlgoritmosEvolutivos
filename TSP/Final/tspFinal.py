import math
import random

import tsplib95
from hamiltonianPath import HamiltonianPath


class TSPProblem:

    def __init__(self, path, population_size=10):
        self._matrix = tsplib95.load(path)
        self._hamiltonian_path = HamiltonianPath(self)
        self._population_size = population_size
        self._c_factor = self._get_c_factor()
        self._solutions = dict()

    def generate_population(self):
        print('Inicializando poblacion de manera random')
        nodes = self.get_nodes()
        for solution_num in range(0, self._population_size):
            initial_node = self._get_initial_node(nodes)
            self._generate_solution(solution_num, initial_node)
            nodes = self._delete_initial_node(nodes, initial_node)

    @staticmethod
    def _get_initial_node(nodes):
        return random.choice(nodes)

    def _delete_initial_node(self, nodes, initial_node):
        nodes.remove(initial_node)
        if not len(nodes):
            nodes = self.get_nodes()
        return nodes

    def _generate_solution(self, solution_num, initial_node):
        self._solutions[solution_num] = self._hamiltonian_path.get_hamiltonian_cycle(initial_node)

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

    def _get_exponential_value(self, position):
        return (1 - math.exp(position * (-1))) / self._c_factor

    def _get_c_factor(self):
        exponential = 0
        for i in range(0, self._population_size):
            exponential += math.exp((i + 1) * (-1))
        return self._population_size - exponential

    def calculate_solutions_fitness(self):
        fitness = dict()
        for solution in range(0, self._population_size):
            fitness[solution] = self._calculate_fitness(self._decode_solution(solution))
        return fitness

    def parent_selection_ranking(self):
        sorted_solutions = self._sort_solutions(self.calculate_solutions_fitness())
        return self._get_exponential_ranking(sorted_solutions)

    def parent_selection_by_tournament(self, k):
        print()

    def get_couple(self, k):
        print()

    def _get_exponential_ranking(self, sorted_solutions):
        exponential_ranking = dict()
        # the position is + 1 because the list index starts in 0
        for i in range(0, len(sorted_solutions)):
            exponential_ranking[sorted_solutions[i][0]] = self._get_exponential_value(i + 1)
        return exponential_ranking

    @staticmethod
    def _sort_solutions(solutions):
        return sorted(solutions.items(), key=lambda x: x[1])

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
TSPProblem.parent_selection_ranking()
