import copy
import math
import random
import time
import datetime
import tsplib95
from hamiltonianPath import HamiltonianPath
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class TSPProblem:

    def __init__(self, path):
        self._matrix = tsplib95.load(path)
        self._hamiltonian_path = HamiltonianPath(self)
        self._population_size = None
        self._c_factor = None

    # region initialize population
    def generate_population(self):
        # print('Inicializando poblacion de manera random')
        nodes = self.get_nodes()
        solutions = dict()
        for solution_num in range(0, self._population_size):
            initial_node = self._get_initial_node(nodes)
            solutions[solution_num] = self._generate_solution(initial_node)
            nodes = self._delete_initial_node(nodes, initial_node)
        return solutions

    @staticmethod
    def _get_initial_node(nodes):
        return random.choice(nodes)

    def _delete_initial_node(self, nodes, initial_node):
        nodes.remove(initial_node)
        if not len(nodes):
            nodes = self.get_nodes()
        return nodes

    def _generate_solution(self, initial_node):
        return self._hamiltonian_path.get_hamiltonian_cycle(initial_node)

    def _decode_solution(self, solutions, solution_num):
        solution = solutions[solution_num]
        weight = 0
        for origin in solution.keys():
            destination = solution[origin]
            weight += self.get_weight(origin, destination)
        return weight

    def decode_solutions(self, solutions):
        for solution in range(0, self._population_size):
            self._decode_solution(solutions, solution)

    def decode_solution(self, solution):
        weight = 0
        for origin in solution.keys():
            destination = solution[origin]
            weight += self.get_weight(origin, destination)
        return weight
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

    def calculate_solutions_fitness(self, solutions):
        fitness = dict()
        for solution in range(0, self._population_size):
            fitness[solution] = self._calculate_fitness(self._decode_solution(solutions, solution))
        return fitness
    # endregion

    # region parents selection

    # region mating pool definition
    # method can be 'rueda de ruleta' or 'torneo'
    def define_mating_pool(self, solutions, solutions_fitness, method='rueda de ruleta'):
        method = method.lower()
        if method == 'rueda de ruleta':
            # print('Generando mating pool con seleccion de padres por rueda de ruleta ...')
            return self.generate_mating_pool_by_roulette_wheel(solutions, solutions_fitness)
        elif method == 'torneo':
            # print('Generando mating pool con seleccion de padres por torneo ...')
            return self.generate_mating_pool_by_tournament(solutions, solutions_fitness)
        else:
            return None

    def generate_mating_pool_by_roulette_wheel(self, solutions, solutions_fitness):
        roulette_parents = self.parent_selection_by_roulette_wheel(solutions, solutions_fitness, self._population_size)
        return roulette_parents

    # estandarizar el k ?
    def generate_mating_pool_by_tournament(self, solutions, solutions_fitness):
        mating_pool = list()
        for i in range(0, self._population_size):
            parent = self.parent_selection_by_tournament(solutions, solutions_fitness, 2)
            mating_pool.append(parent)
        return mating_pool

    # endregion

    # region parent selection ranking (exponential)
    def parent_selection_ranking(self, solutions):
        sorted_solutions = self._sort_solutions_list(self.calculate_solutions_fitness(solutions))
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
    def parent_selection_by_tournament(self, solutions, solutions_fitness, k):
        parent_key_1 = self.get_best_solution_by_fitness(self.get_couple(k, solutions_fitness))
        return [parent_key_1, solutions[parent_key_1]]

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
    def parent_selection_by_roulette_wheel(self, solutions, solutions_fitness, n):
        sorted_solutions = self._sort_solutions_list(solutions_fitness)
        roulette = self._get_exponential_ranking_sum(self._get_exponential_ranking(sorted_solutions))
        parents = list()
        for i in range(0, n):
            parent = self.spin_roulette(roulette)
            parents.append([parent, solutions[parent]])
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

    # region child generation

    def generate_child_population(self, mating_pool, method='cruce basado en arcos'):
        if method.lower() == 'cruce basado en arcos':
            # print('Generado poblacion de hijos con el metodo de cruce basado en arcos ... ')
            return self.edge_based_crossing(mating_pool)
        elif method.lower() == 'cruce basado en un punto':
            # print('Generando poblacion de hijos con el metodo de cruce de un punto ...')
            return self.point_crossing(mating_pool)
        else:
            return None
    # endregion

    # region edge-based crossing
    def edge_based_crossing(self, mating_pool):
        childs = dict()
        i = 0
        while len(childs) < self._population_size:
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            table = self._get_table(parent1[1], parent2[1])
            child = self._generate_child_from_table(table)
            childs[i] = child
            i += 1
        return childs

    def _get_table(self, parent1, parent2):
        table = dict()
        nodes = self.get_nodes()
        for node in nodes:
            table[node] = []
            table[node] += self._get_ady_nodes_from_parent(node, parent1)
            table[node] += self._get_ady_nodes_from_parent(node, parent2)
            table[node] = list(dict.fromkeys(table[node]))
        return table

    def _generate_child_from_table(self, table):
        nodes = self.get_nodes()
        initial_node = random.choice(nodes)
        return self._hamiltonian_path.get_hamiltonian_cycle_child(initial_node, table)

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
            return []
    # endregion

    # region point crossing
    def point_crossing(self, mating_pool):
        childs = dict()
        i = 0
        while len(childs) < self._population_size:
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            child1, child2 = self._generate_child_from_point_crossing(parent1[1], parent2[1])
            if child1 is None or child2 is None:
                continue
            child1.append(child1[0])
            child2.append(child2[0])
            childs[i] = self._hamiltonian_path.generate_dict_solution(child1)
            childs[i + 1] = self._hamiltonian_path.generate_dict_solution(child2)
            i += 2
        return childs

    def _generate_child_from_point_crossing(self, parent1, parent2):
        parent11 = copy.deepcopy(self.to_list(parent1))
        parent22 = copy.deepcopy(self.to_list(parent2))
        del parent11[-1]
        del parent22[-1]
        n = len(parent11)
        c = random.randint(1, n - 2)

        child1 = parent11[0:c]
        child1_ordered = self._get_ordered_list(parent11[c:n], parent22)
        if not self._condition_is_satisfied(child1, child1_ordered):
            return None, None

        child1.extend(child1_ordered)

        if not self.is_ady(child1[0], child1[-1]):
            return None, None

        child2 = parent22[0:c]
        child2_ordered = self._get_ordered_list(parent22[c:n], parent11)
        if not self._condition_is_satisfied(child2, child2_ordered):
            return None, None
        child2.extend(child2_ordered)

        if not self.is_ady(child2[0], child2[-1]):
            return None, None

        return child1, child2

    @staticmethod
    def _get_ordered_list(parent_c_n, opposite_parent):
        new_list = list()
        for i in range(0, len(opposite_parent)):
            if opposite_parent[i] in parent_c_n:
                new_list.append(opposite_parent[i])
        return new_list

    @staticmethod
    def to_list(dictionary):
        new_list = list(dictionary)
        new_list.append(new_list[0])
        return new_list

    def _condition_is_satisfied(self, first_list, second_list):
        valid = True
        if not self.is_ady(first_list[-1], second_list[0]):
            valid = False

        if not self.is_ady(first_list[0], second_list[-1]):
            valid = False

        for i in range(len(second_list) - 1):
            if not self.is_ady(second_list[i], second_list[i + 1]):
                valid = False

        return valid

    # endregion

    # endregion

    # region mutation

    # region define mutations
    def apply_mutation(self, child_population, method):
        key = random.choice(list(child_population.keys()))
        if method.lower() == 'intercambio':
            print('Aplicando mutancion por intercambio ...')
            return key, self.exchange_mutation(child_population[key])
        elif method.lower() == 'inversion':
            print('Aplicando mutacion por inversion ...')
            return key, self.inversion_mutation(child_population[key])
        else:
            return None

    # endregion

    # region exchange mutation
    def exchange_mutation(self, solution):
        solution_list = self.get_solution_exchange_mutation(solution)
        return self._hamiltonian_path.generate_dict_solution(solution_list)

    def get_solution_exchange_mutation(self, solution):
        valid = False
        solution_list = self.to_list(copy.deepcopy(solution))
        while not valid:
            n = len(solution_list)
            x = random.randint(0, n - 2)
            y = random.randint(0, n - 2)
            while x == y:
                y = random.randint(0, n - 2)
            if self._exchange_is_valid(solution_list, x, y):
                solution_list[x], solution_list[y] = solution_list[y], solution_list[x]
                valid = True
        return solution_list

    def _exchange_is_valid(self, s, x, y):
        if x == 0:
            valid = self.is_ady(s[y], s[1]) and self.is_ady(s[y], s[-2]) and self.is_ady(s[x], s[y - 1]) and \
                    self.is_ady(s[x], s[y + 1])
        elif y == 0:
            valid = self.is_ady(s[x], s[1]) and self.is_ady(s[x], s[-2]) and self.is_ady(s[y], s[x - 1]) and \
                    self.is_ady(s[y], s[x + 1])
        else:
            valid = self.is_ady(s[y], s[x - 1]) and self.is_ady(s[y], s[x + 1]) and self.is_ady(s[x], s[y - 1]) and \
                    self.is_ady(s[x], s[y + 1])
        return valid

    # endregion

    # region inversion mutation
    def inversion_mutation(self, solution):
        solution_list = self.get_solution_inversion_mutation(solution)
        return self._hamiltonian_path.generate_dict_solution(solution_list)

    def get_solution_inversion_mutation(self, solution):
        valid = False
        solution_list = self.to_list(copy.deepcopy(solution))
        new_solution = list()
        while not valid:
            n = len(solution_list)
            x = random.randint(0, n - 2)
            y = random.randint(0, n - 2)
            while x == y:
                y = random.randint(0, n - 2)
            if self._inversion_is_valid(solution_list, x, y):
                new_solution = self._invert_positions(solution_list, x, y)
                valid = True
        return new_solution

    def _inversion_is_valid(self, s, x, y):
        if x < y:
            if x == 0:
                valid = self.is_ady(s[y], s[-2]) and self.is_ady(s[x], s[y + 1])
            else:
                valid = self.is_ady(s[y], s[x - 1]) and self.is_ady(s[x], s[y + 1])
        else:
            if y == 0:
                valid = self.is_ady(s[x], s[-2]) and self.is_ady(s[y], s[x + 1])
            else:
                valid = self.is_ady(s[x], s[y - 1]) and self.is_ady(s[y], s[x + 1])
        return valid

    @staticmethod
    def _invert_positions(s, x, y):
        if x < y:
            while x < y:
                temp = s[x]
                s[x] = s[y]
                s[y] = temp
                x += 1
                y -= 1
        else:
            while y < x:
                temp = s[y]
                s[y] = s[x]
                s[x] = temp
                y += 1
                x -= 1
        return s

    # endregion

    # endregion

    # region survivors selection

    # region select survivors
    def define_new_population(self, actual_population, child_population, actual_fitness, new_fitness, n=None,
                              method='steady-state'):
        if method.lower() == 'steady-state':
            # print('Generando nueva poblacion mediante el metodo de steady-state ...')
            return self.steady_state(actual_population, child_population, actual_fitness, new_fitness, n)
        elif method.lower() == 'elitismo':
            # print('Generando nueva poblacion mediante el metodo de elitismo ...')
            return self.elitism(actual_population, child_population, actual_fitness, new_fitness)
        else:
            return None

    # endregion

    # region steady-state
    def steady_state(self, actual_population, child_population, actual_fitness, new_fitness, n):
        sort_actual_population = self._sort_solutions_list(actual_fitness)
        sort_child_population = self._sort_solutions_list(new_fitness)
        size = len(sort_child_population)
        best_actual_population = sort_actual_population[n:size]
        best_child_population = sort_child_population[n:size]
        best_actual_population.extend(best_child_population)
        return self._get_new_population_steady_state(actual_population, child_population, best_actual_population, n)

    @staticmethod
    def _get_new_population_steady_state(actual_population, child_population, bests_fitness, n):
        new_population = dict()
        i = 0
        while i < n:
            solution_num = bests_fitness[i][0]
            new_population[i] = actual_population[solution_num]
            i += 1
        while i < len(bests_fitness):
            solution_num = bests_fitness[i][0]
            new_population[i] = child_population[solution_num]
            i += 1
        return new_population

    # endregion

    # region elitism

    def elitism(self, actual_population, child_population, actual_fitness, new_fitness):
        sort_actual_population = self._sort_solutions_list(actual_fitness)
        sort_child_population = self._sort_solutions_list(new_fitness)
        return self._get_new_population_elitism(actual_population, child_population, sort_actual_population, sort_child_population)

    @staticmethod
    def _get_new_population_elitism(actual_population, child_population, actual_fitness, new_fitness):
        new_population = dict()
        if actual_fitness[-1][1] > new_fitness[-1][1]:
            new_population[0] = actual_population[actual_fitness[-1][0]]
        else:
            new_population[0] = child_population[new_fitness[-1][0]]

        for i in range(1, len(new_fitness)):
            new_population[i] = child_population[new_fitness[i][0]]
        return new_population

    # endregion

    # endregion

    # region evolutional algorithm
    def evolutional_algorithm(self, population_size=100, cross_p=1, mutation_p=0.05, generation_numbers=500,
                              parent_selection_type='torneo', crossing_type='cruce basado en arcos',
                              mutation_type='mutacion por intercambio', survivors_type='elitismo', n=None,
                              stagnant_generations_limit=100, config_n=None):
        values_txt = dict()
        values_txt['parametros'] = 'tamaño poblacion: {}, numero de generaciones: {}\nmetodo de seleccion de padres: {}, ' \
                                   'metodo de cruzamiento: {}\nmetodo de mutacion: {}, seleccion de sobrevivientes: {}\n' \
                                   'probabilidad de cruce: {}, probabilidad de mutacion: {}\n' \
                                   'estancamiento de generaciones: {}'.format(population_size, generation_numbers,
                                                                             parent_selection_type, crossing_type,
                                                                             mutation_type, survivors_type, cross_p,
                                                                             mutation_p, stagnant_generations_limit)
        self._standar_init(population_size)
        start = time.time()
        actual_population = self.generate_population()
        stagnant_generations = 0
        i = 0
        initial_cost = self._decode_solution(actual_population, 0)
        while not self.is_finished(i, stagnant_generations, stagnant_generations_limit, generation_numbers):

            fitness = self.calculate_solutions_fitness(actual_population)

            mating_pool = self.define_mating_pool(actual_population, fitness, parent_selection_type)

            child_population = actual_population

            if self.apply_transformation(cross_p):
                child_population = self.generate_child_population(mating_pool, crossing_type)

            if self.apply_transformation(mutation_p):
                key, mutation = self.apply_mutation(child_population, mutation_type)
                child_population[key] = mutation

            new_fitness = self.calculate_solutions_fitness(child_population)

            best_actual_fitness, best_child_fitness = self._get_best_fitness(fitness), self._get_best_fitness(new_fitness)
            values_txt['mejor fitness generacion {}'.format(i)] = str(best_actual_fitness)

            if best_actual_fitness == best_child_fitness:
                stagnant_generations += 1
            else:
                stagnant_generations = 0

            actual_population = self.define_new_population(actual_population, child_population, fitness, new_fitness,
                                                           n=n, method=survivors_type)
            i += 1
        end = time.time()
        best_solution, best_fitness = self._get_best_solution(actual_population)
        values_txt['mejor solucion'] = str(list(best_solution))
        values_txt['fitness de la mejor solucion'] = str(best_fitness)
        values_txt['tiempo de ejecucion'] = str(end - start)
        values_txt['costo_viaje'] = str(1 / best_fitness)

        return best_solution, initial_cost, end - start, values_txt

    def _get_best_solution(self, population):
        sorted_solutions = self._sort_solutions_list(self.calculate_solutions_fitness(population))
        solution_num = sorted_solutions[-1][0]
        best_fitness = sorted_solutions[-1][1]
        return population[solution_num], best_fitness

    def generate_txt_file(self, info, config):
        name = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        with open('{}_{}.txt'.format(name, config), 'w') as f:
            f.write(self.get_string_format(info))

    def get_string_format(self, info):
        s = ''
        for key in info.keys():
            s += key + ': '
            s += str(info[key])
            s += '\n'
        return s

    def get_display_data(self, data):
        display_data = dict()
        display_data['mejor solucion'] = data['mejor solucion']
        display_data['fitness de la mejor solucion'] = data['fitness de la mejor solucion']
        display_data['tiempo de ejecucion'] = data['tiempo de ejecucion']
        return display_data

    # region evolutional algorithm utils
    @staticmethod
    def apply_transformation(parameter):
        rand = random.random()
        return rand < parameter

    def _standar_init(self, population_size):
        self._population_size = population_size
        self._c_factor = self._get_c_factor()

    @staticmethod
    def is_finished(i, stagnant_generations, stagnant_generations_limit, generation_number):
        finished = False
        if i >= generation_number:
            finished = True

        if stagnant_generations >= stagnant_generations_limit:
            finished = True

        return finished

    def _get_best_fitness(self, population_fitness):
        return self._sort_solutions_list(population_fitness)[-1][1]

    def get_solution_graph(self, best_solution, initial_cost, time_ex, config=None):
        G = nx.Graph()
        for key in best_solution.keys():
            G.add_node(key)
            G.add_edge(key, best_solution[key])
        pos = nx.spring_layout(G)
        bs_cost = self.decode_solution(best_solution)
        nx.draw(G, pos=pos, cmap=plt.get_cmap('jet'), node_color='red', with_labels=True)
        nx.draw_networkx_edge_labels(G, pos, font_color='red', edge_labels=self._get_edge_labels(G))
        plt.plot([], [], ' ', label='costo viaje inicial: {}'.format(initial_cost))
        plt.plot([], [], ' ', label='costo mejor viaje: {}'.format(bs_cost))
        plt.plot([], [], ' ', label='mejora: {}%'.format(math.floor((initial_cost / bs_cost)*100)))
        plt.plot([], [], ' ', label='tiempo de ejecucion: {} secs'.format(math.floor(time_ex)))
        plt.legend(loc='upper left')
        plt.savefig("../Web/static/image/best_solution.png")
        plt.clf()

    def _get_edge_labels(self, G):
        return dict([((n1, n2), f'{self.get_weight(n1, n2)}')
              for n1, n2 in G.edges])

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

option = 0
if option == 1:
    path2 = './Resources/Instancias-TSP/br17.atsp'
    TSPProblem = TSPProblem(path2)
    TSPProblem.evolutional_algorithm(population_size=10, cross_p=1, mutation_p=0.01, generation_numbers=50,
                                     parent_selection_type='torneo', crossing_type='cruce basado en un punto',
                                     mutation_type='intercambio', survivors_type='elitismo', n=5,
                                     stagnant_generations_limit=100)






