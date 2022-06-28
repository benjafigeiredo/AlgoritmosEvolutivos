from flask import Blueprint, request, render_template
from Final.tspFinal import TSPProblem

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/TSP", methods=["GET", "POST"])
def get_parameters():
    if request.method == "POST":
        psize = int(request.form.get("population_size"))
        gsize = int(request.form.get("generation_size"))
        parent_method = request.form.get("parent_method")
        cross_method = request.form.get("cross_method")
        mutation_method = request.form.get("mutation_method")
        survivors_method = request.form.get("survivors_method")
        cross_p = float(request.form.get("cross_p"))
        mutation_p = float(request.form.get("mutation_p"))
        path2 = '../Final/Resources/Instancias-TSP/br17.atsp'
        tsp = TSPProblem(path2)
        best_solution = tsp.evolutional_algorithm(population_size=psize, cross_p=cross_p, mutation_p=mutation_p,
                                  generation_numbers=gsize, parent_selection_type=parent_method,
                                  crossing_type=cross_method, mutation_type=mutation_method,
                                  survivors_type=survivors_method, n=50, stagnant_generations_limit=100)
        tsp.get_solution_graph(best_solution)
    return render_template("tsp_page.html")
def tsp():
    return render_template("tsp_page.html")

@views.route("/about")
def about():
    return render_template("about.html")