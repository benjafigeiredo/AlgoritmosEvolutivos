import math

from flask import Blueprint, request, render_template, Response
from Final.tspFinal import TSPProblem
from datetime import datetime
from time import sleep

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/TSP", methods=["GET", "POST"])
def get_parameters():
    display_data = dict()
    if request.method == "POST":
        psize = int(request.form.get("population_size"))
        gsize = int(request.form.get("generation_size"))
        parent_method = request.form.get("parent_method")
        cross_method = request.form.get("cross_method")
        mutation_method = request.form.get("mutation_method")
        survivors_method = request.form.get("survivors_method")
        cross_p = float(request.form.get("cross_p"))
        mutation_p = float(request.form.get("mutation_p"))
        file_name = request.form.get("graph_file")
        path2 = '../Final/Resources/Instancias-TSP/{}'.format(file_name)
        tsp = TSPProblem(path2)
        best_solution, initial_cost, time_ex, data = tsp.evolutional_algorithm(population_size=psize, cross_p=cross_p, mutation_p=mutation_p,
                                                  generation_numbers=gsize, parent_selection_type=parent_method,
                                                  crossing_type=cross_method, mutation_type=mutation_method,
                                                  survivors_type=survivors_method, n=math.floor(psize / 2),
                                                  stagnant_generations_limit=100)
        tsp.get_solution_graph(best_solution, initial_cost, time_ex)
        tsp.generate_txt_file(data)
        display_data = tsp.get_display_data(data)
    return render_template("tsp_page.html", data=display_data)


def streamer():
    while True:
        print('in while true')
        yield "<p>{}</p>".format(datetime.now())
        sleep(1)

@views.route("/about")
def about():
    return render_template("about.html")