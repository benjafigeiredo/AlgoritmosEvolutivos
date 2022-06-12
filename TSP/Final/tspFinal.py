import tsplib95
from tsplib95 import *


class TSPProblem:

    path = './Resources/Instancias-TSP/br17.atsp'

    def __init__(self, path):
        self.problem = tsplib95.load(path)
