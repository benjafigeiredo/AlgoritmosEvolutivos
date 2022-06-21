import copy
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

    # region initialize population
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
    # endregion

    # region fitness
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
    # endregion

    # region parents selection

    # region mating pool definition
    # method can be 'rueda de ruleta' or 'torneo'
    def define_mating_pool(self, method='rueda de ruleta'):
        method = method.lower()
        if method == 'rueda de ruleta':
            print('Generando mating pool con seleccion de padres por rueda de ruleta ...')
            return self.generate_mating_pool_by_roulette_wheel()
        elif method == 'torneo':
            return self.generate_mating_pool_by_tournament()

    def generate_mating_pool_by_roulette_wheel(self):
        roulette_parents = self.parent_selection_by_roulette_wheel(2 * self._population_size)
        mating_pool = dict()
        for i in range(0, self._population_size):
            parents = [roulette_parents[2*i], roulette_parents[2*i+1]]
            mating_pool[i] = parents
        return mating_pool

    # estandarizar el k ?
    def generate_mating_pool_by_tournament(self):
        mating_pool = dict()
        for i in range(0, self._population_size):
            parents = self.parent_selection_by_tournament(2)
            mating_pool[i] = parents
        return mating_pool

    # endregion

    # region parent selection ranking (exponential)
    def parent_selection_ranking(self):
        sorted_solutions = self._sort_solutions_list(self.calculate_solutions_fitness())
        return self._get_exponential_ranking(sorted_solutions)

    def _get_exponential_ranking(self, sorted_solutions):
        exponential_ranking = dict()
        # the position is + 1 because the list index starts in 0
        for i in range(0, len(sorted_solutions)):
            exponential_ranking[sorted_solutions[i][0]] = self._get_exponential_value(i + 1)
        return exponential_ranking

    @staticmethod
    def _sort_solutions_list(solutions):
        return sorted(solutions.items(), key=lambda x: x[1])

    # endregion

    # region parent selection by tournament
    def parent_selection_by_tournament(self, k):
        solutions = self.calculate_solutions_fitness()
        parent_key_1 = self.get_best_solution_by_fitness(self.get_couple(k, solutions))
        parent_key_2 = self.get_best_solution_by_fitness(self.get_couple(k, solutions))

        return [[parent_key_1, self._solutions[parent_key_1]], [parent_key_2, self._solutions[parent_key_2]]]

    @staticmethod
    def get_couple(k, solutions):
        solutions_selected = list()
        i = 0
        while i < k:
            solution = random.choice(list(solutions.items()))
            if solution not in solutions_selected:
                solutions_selected.append(solution)
                i += 1
        return solutions_selected

    @staticmethod
    def get_best_solution_by_fitness(couple):
        best = couple[0]
        for value in couple:
            if value[1] > best[1]:
                best = value
        return best[0]
    # endregion

    # region parent selection by roulette wheel
    def parent_selection_by_roulette_wheel(self, n):
        sorted_solutions = self._sort_solutions_list(self.calculate_solutions_fitness())
        roulette = self._get_exponential_ranking_sum(self._get_exponential_ranking(sorted_solutions))
        parents = list()
        for i in range(0, n):
            parent = self.spin_roulette(roulette)
            parents.append([parent, self._solutions[parent]])
        return parents

    @staticmethod
    def _get_exponential_ranking_sum(exponential_ranking):
        sum_prob = exponential_ranking.copy()
        first_duple = list(sum_prob.items())[0]
        first_key = first_duple[0]
        last_value = first_duple[1]
        for key in sum_prob.keys():
            if key != first_key:
                sum_prob[key] += last_value
                last_value = sum_prob[key]
        return sum_prob

    @staticmethod
    def spin_roulette(roulette):
        random_value = random.random()
        for key in roulette.keys():
            if random_value < roulette[key]:
                return key
    # endregion

    # endregion

    # region genetic crossing

    # region edge-based crossing
    def arc_based_crossing(self, mating_pool):
        for parents in mating_pool.values():
            table = self._get_table(parents[0][1], parents[1][1])
            child = self._generate_child_from_table(table)

    def _get_table(self, parent1, parent2):
        table = dict()
        nodes = self.get_nodes()
        for node in nodes:
            table[node] = list()
            table[node] += self._get_ady_nodes_from_parent(node, parent1)
            table[node] += self._get_ady_nodes_from_parent(node, parent2)
            table[node] = list(dict.fromkeys(table[node]))
        return table

    def _generate_child_from_table(self, table):
        child = dict()
        nodes = self.get_nodes()
        last_node = random.choice(nodes)
        self._remove_references(last_node, nodes, table)
        while len(nodes):
            next_node = self._select_next_node(last_node, table, nodes)
            self._remove_references(next_node, nodes, table)
            child[last_node] = next_node
            last_node = next_node
        return child

    @staticmethod
    def _remove_references(node, nodes, table):
        if node in nodes:
            nodes.remove(node)
        for ady in table.values():
            if node in ady:
                ady.remove(node)
                if not len(ady):
                    print('cuando se elimino el nodo: {}, se vacio la tabla de adyacencias')

    def _select_next_node(self, last_node, table, nodes):
        ady_nodes = table[last_node]

        if not len(ady_nodes):
            return None

        print(last_node, len(ady_nodes))
        if len(nodes) <= 1:
            return nodes[0]

        if len(ady_nodes) == 1:
            return ady_nodes[0]
        elif self._len_equals(ady_nodes, table):
            return random.choice(ady_nodes)
        else:
            return self._get_node_min(ady_nodes, table)


    @staticmethod
    def _len_equals(ady_nodes, table):
        lenghts = list()
        for ady in ady_nodes:
            lenghts.append(len(table[ady]))
        return lenghts.count(lenghts[0]) == len(lenghts)

    @staticmethod
    def _get_node_min(ady_nodes, table):
        ref_size = len(table[ady_nodes[0]])
        ref_node = ady_nodes[0]
        for ady in ady_nodes:
            if len(table[ady]) < ref_size:
                ref_node, ref_size = ady, len(table[ady])
        return ref_node

    @staticmethod
    def _get_key_by_value(d, v):
        for key, value in d.items():
            if value == v:
                return key
        return None

    def _get_ady_nodes_from_parent(self, node, parent):
        key_by_value = self._get_key_by_value(parent, node)
        if key_by_value is not None:
            return [parent[node], key_by_value]
        else:
            return None, None
    # endregion

    # endregion

    # region graph utils
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
    # endregion


path2 = './Resources/Instancias-TSP/br17.atsp'
TSPProblem = TSPProblem(path2, population_size=100)
TSPProblem.generate_population()
TSPProblem.decode_solutions()
TSPProblem.arc_based_crossing(TSPProblem.define_mating_pool(method='torneo'))
