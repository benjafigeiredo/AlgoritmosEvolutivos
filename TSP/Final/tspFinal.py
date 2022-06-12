import tsplib95


class TSPProblem:

    def __init__(self, path):
        self.problem = tsplib95.load(path)


path = './Resources/Instancias-TSP/br17.atsp'
TSPProblem = TSPProblem(path)
