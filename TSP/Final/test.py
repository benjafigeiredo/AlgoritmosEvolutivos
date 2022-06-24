from hamiltonianPath import HamiltonianPath


def inicializar_matriz():
    return [[9999, 1, 0, 0, 1, 0, 0, 1],
            [1, 9999, 1, 0, 0, 0, 0, 1],
            [0, 1, 9999, 1, 0, 1, 1, 0],
            [0, 0, 1, 9999, 1, 0, 1, 0],
            [1, 0, 0, 1, 9999, 0, 0, 0],
            [0, 0, 1, 0, 0, 9999, 1, 1],
            [0, 0, 1, 1, 0, 1, 9999, 0],
            [1, 1, 0, 0, 0, 1, 0, 9999]]


class Test:

    def __init__(self, matriz):
        print('init ...')
        self.matriz = matriz
        self._hamiltonian_path = HamiltonianPath(self)

    def get_hamiltonian_path_child(self, initial_node, table):
        return self._hamiltonian_path.get_hamiltonian_cycle_child(initial_node, table)

    def get_parent(self, initial_node):
        return self._hamiltonian_path.get_hamiltonian_cycle(initial_node)

    def get_graph(self):
        return self.matriz

    @staticmethod
    def get_nodes():
        return [0, 1, 2, 3, 4, 5, 6, 7]

    def get_nodes_quantity(self):
        return len(self.matriz[0])

    def recursion(self, v, tabla):
        if v == 10:
            return True
        else:
            before_tabla = tabla.copy()
            tabla[v] = 'hola{}'.format(v)
            self.recursion(v + 1, tabla)
            tabla = before_tabla
            print('salio {}'.format(v))
            print('tabla {}: {}'.format(v, tabla))

    def get_table(self, parent1, parent2):
        table = dict()
        nodes = self.get_nodes()
        for node in nodes:
            table[node] = list()
            table[node] += self._get_ady_nodes_from_parent(node, parent1)
            table[node] += self._get_ady_nodes_from_parent(node, parent2)
            table[node] = list(dict.fromkeys(table[node]))
        return table

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


# continuar test para ver si el circuito hamiltoniano con condiciones
matriz2 = inicializar_matriz()
test = Test(matriz2)
parent11 = test.get_parent(2)
parent21 = test.get_parent(6)
table = test.get_table(parent11, parent21)
print(str(parent11))
print(str(parent21))
print(str(test.get_hamiltonian_path_child(0, table)))
