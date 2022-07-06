from Final.tspFinal import TSPProblem
import math


path_br17 = './Resources/Instancias-TSP/br17.atsp'
tsp_br17 = TSPProblem(path_br17)

path_p43 = './Resources/Instancias-TSP/p43.atsp'
tsp_p43 = TSPProblem(path_p43)

ruleta = 'rueda de ruleta'
torneo = 'torneo'
punto = 'cruce basado en un punto'
arcos = 'cruce basado en arcos'
inversion = 'inversion'
intercambio = 'intercambio'
steady_state = 'steady-state'
elitismo = 'elitismo'

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, intercambio, steady_state, math.floor(100/2), 100, 'config1')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, intercambio, steady_state, math.floor(100/2), 100, 'config2')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, intercambio, steady_state, math.floor(200/2), 100, 'config3')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, intercambio, steady_state, math.floor(200/2), 100, 'config4')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, intercambio, elitismo, math.floor(100/2), 100, 'config5')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, intercambio, elitismo, math.floor(100/2), 100, 'config6')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, intercambio, elitismo, math.floor(200/2), 100, 'config7')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, intercambio, elitismo, math.floor(200/2), 100, 'config8')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, inversion, steady_state, math.floor(100/2), 100, 'config9')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, inversion, steady_state, math.floor(100/2), 100, 'config10')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, inversion, steady_state, math.floor(200/2), 100, 'config11')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, inversion, steady_state, math.floor(200/2), 100, 'config12')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, inversion, elitismo, math.floor(100/2), 100, 'config13')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, arcos, inversion, elitismo, math.floor(100/2), 100, 'config14')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, inversion, elitismo, math.floor(200/2), 100, 'config15')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, arcos, inversion, elitismo, math.floor(200/2), 100, 'config16')


# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, intercambio, steady_state, math.floor(100/2), 100, 'config17')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, intercambio, steady_state, math.floor(100/2), 100, 'config18')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, intercambio, steady_state, math.floor(200/2), 100,'config19')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, intercambio, steady_state, math.floor(200/2), 100, 'config20')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, intercambio, elitismo, math.floor(100/2), 100, 'config21')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, intercambio, elitismo, math.floor(100/2), 100, 'config22')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, intercambio, elitismo, math.floor(200/2), 100, 'config23')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, intercambio, elitismo, math.floor(200/2), 100, 'config24')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, inversion, steady_state, math.floor(100/2), 100, 'config25')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, inversion, steady_state, math.floor(100/2), 100, 'config26')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, inversion, steady_state, math.floor(200/2), 100, 'config27')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, inversion, steady_state, math.floor(200/2), 100, 'config28')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, inversion, elitismo, math.floor(100/2), 100, 'config29')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, torneo, punto, inversion, elitismo, math.floor(100/2), 100, 'config30')

# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, inversion, elitismo, math.floor(200/2), 100, 'config31')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, torneo, punto, inversion, elitismo, math.floor(200/2), 100, 'config32')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, intercambio, steady_state, math.floor(100/2), 100, 'config33')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, intercambio, steady_state, math.floor(100/2), 100, 'config34')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, intercambio, steady_state, math.floor(200/2), 100, 'config35')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, intercambio, steady_state, math.floor(200/2), 100, 'config36')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, intercambio, elitismo, math.floor(100/2), 100, 'config37')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, intercambio, elitismo, math.floor(100/2), 100, 'config38')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, intercambio, elitismo, math.floor(200/2), 100, 'config39')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, intercambio, elitismo, math.floor(200/2), 100, 'config40')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, inversion, steady_state, math.floor(100/2), 100, 'config41')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, inversion, steady_state, math.floor(100/2), 100, 'config42')
# tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, inversion, steady_state, math.floor(200/2), 100, 'config43')
# tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, inversion, steady_state, math.floor(200/2), 100, 'config44')

# tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, inversion, elitismo, math.floor(100/2), 100, 'config45')
# tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, arcos, inversion, elitismo, math.floor(100/2), 100, 'config46')
tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, inversion, elitismo, math.floor(200/2), 100, 'config47')
tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, arcos, inversion, elitismo, math.floor(200/2), 100, 'config48')

"""
tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, intercambio, steady_state, math.floor(100/2), 100, 'config49')
tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, intercambio, steady_state, math.floor(100/2), 100, 'config50')
tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, intercambio, steady_state, math.floor(200/2), 100, 'config51')
tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, intercambio, steady_state, math.floor(200/2), 100, 'config52')

tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, intercambio, elitismo, math.floor(100/2), 100, 'config53')
tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, intercambio, elitismo, math.floor(100/2), 100, 'config54')
tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, intercambio, elitismo, math.floor(200/2), 100, 'config55')
tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, intercambio, elitismo, math.floor(200/2), 100, 'config56')

tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, inversion, steady_state, math.floor(100/2), 100, 'config57')
tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, inversion, steady_state, math.floor(100/2), 100, 'config58')
tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, inversion, steady_state, math.floor(200/2), 100, 'config59')
tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, inversion, steady_state, math.floor(200/2), 100, 'config60')

tsp_br17.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, inversion, elitismo, math.floor(100/2), 100, 'config61')
tsp_p43.evolutional_algorithm(100, 1, 0.1, 500, ruleta, punto, inversion, elitismo, math.floor(100/2), 100, 'config62')
tsp_br17.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, inversion, elitismo, math.floor(200/2), 100, 'config63')
tsp_p43.evolutional_algorithm(200, 1, 0.2, 1000, ruleta, punto, inversion, elitismo, math.floor(200/2), 100, 'config64')
"""




