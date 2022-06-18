import tsplib95


class EulerianPath:

    def __init__(self, path):
        self._matrix = tsplib95.load(path)

    def _get_nodes(self):
        return list(self._matrix.get_nodes())

    def _get_nodes_quantity(self):
        return len(self._get_nodes())

    @staticmethod
    def _get_weight(matrix, origin, end):
        return matrix.get_weight(origin, end)

    def get_eulerian_path(self):
        # matrix = self._matrix.as_name_dict().edge_weights
        matrix = self._matrix.as_name_dict()['edge_weights']
        stack = []
        path = []
        origin = 0 # random
        while len(stack) > 0 or self._get_number_of_ady_nodes(matrix, origin) != 0:
            if self._get_number_of_ady_nodes(matrix, origin) == 0:
                path.append(origin)
                origin = stack[-1]
                del stack[-1]
            else:
                for node in range(self._get_nodes_quantity()):
                    if self._is_ady(matrix, origin, node):
                        stack.append(origin)
                        matrix[origin][node] = 0
                        matrix[node][origin] = 0
                        origin = node
                        break

        for ele in path:
            print(ele, end= " -> ")

    @staticmethod
    def _is_ady(matrix, origin, end):
        return matrix[origin][end] != 0 and matrix[origin][end] != 9999

    @staticmethod
    def _get_ady_nodes(matrix, node):
        nodes = matrix[node]
        ady = list()
        for ady_node in range(len(nodes)):
            weight = matrix[node][ady_node]
            if weight != 0 and weight != 9999:
                ady.append(ady_node)
        return ady

    def _get_number_of_ady_nodes(self, matrix, node):
        return len(self._get_ady_nodes(matrix, node))


path = './Resources/Instancias-TSP/br17.atsp'
TSP = EulerianPath(path)
TSP.get_eulerian_path()

