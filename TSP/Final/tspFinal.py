import random

import tsplib95
from random import randrange


class TSPProblem:

    def __init__(self, path, population_size=100):
        self._matrix = tsplib95.load(path)
        self._population_size = population_size
        self._solutions = dict()
        self._solutions_decoded = dict()
        self._solutions_fitness = dict()

    def generate_population(self):
        print('Inicializando poblacion de manera random')
        for solution_num in range(0, self._population_size):
            print('generando la solucion: {}'.format(solution_num))
            self._generate_solution(solution_num)

    def _generate_solution(self, solution_num):
        new_solution = dict()
        nodes_quantity = self._get_nodes_quantity()
        remaining_nodes = self._get_nodes()

        initial_node = random.choice(remaining_nodes)
        remaining_nodes.remove(initial_node)

        last_node = initial_node
        while len(new_solution) < nodes_quantity:

            next_node = random.choice(remaining_nodes) if len(remaining_nodes) else None

            if len(new_solution) == nodes_quantity - 2:
                if self._get_weight(next_node, initial_node) == 0:
                    remaining_nodes = self._get_nodes()
                    new_solution.clear()  #
                    continue  # el ultimo nodo debe ser adyacente al inicial, si no lo es planteo una nueva solucion
                else: # de lo contrario, obtengo la solucion
                    new_solution[last_node] = next_node
                    new_solution[next_node] = initial_node
                    break

            if last_node == next_node or self._get_weight(last_node, next_node) == 0:
                continue  # no se puede escoger el mismo nodo como siguiente, y debe ser adyacente al anterior
            new_solution[last_node] = next_node
            last_node = next_node
            remaining_nodes.remove(next_node)
        self._solutions[solution_num] = new_solution

    def _decode_solution(self, solution_num):
        solution = self._solutions[solution_num]
        weight = 0
        for origin in solution.keys():
            destination = solution[origin]
            weight += self._get_weight(origin, destination)
        return weight

    def decode_solutions(self):
        for solution in range(0, self._population_size):
            self._solutions_decoded[solution] = self._decode_solution(solution)
            print(self._solutions_decoded[solution])

    @staticmethod
    def _calculate_fitness(value):
        return 1 / value

    def calculate_solutions_fitness(self):
        for solution in range(0, self._population_size):
            self._solutions_fitness[solution] = self._calculate_fitness(self._solutions_decoded[solution])
            print(self._solutions_fitness[solution])

    def _get_weight(self, origin, end):
        return self._matrix.get_weight(origin, end)

    def _get_nodes(self):
        return list(self._matrix.get_nodes())

    def _get_nodes_quantity(self):
        return len(self._get_nodes())



path = './Resources/Instancias-TSP/br17.atsp'
TSPProblem = TSPProblem(path, population_size=100)
TSPProblem.generate_population()
TSPProblem.decode_solutions()
TSPProblem.calculate_solutions_fitness()

