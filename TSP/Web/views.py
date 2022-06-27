from flask import Blueprint, request, render_template

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/TSP", methods=["GET", "POST"])
def get_parameters():
    psize = 0
    gsize = 0
    if request.method == "POST":
        psize = request.form.get("population_size")
        gsize = request.form.get("generation_size")
        parent_method = request.form.get("parent_method")
        cross_method = request.form.get("cross_method")
        mutation_method = request.form.get("mutation_method")
        survivors_method = request.form.get("survivors_method")
        cross_p = request.form.get("cross_p")
        mutation_p = request.form.get("mutation_p")
        print(psize)
        print(gsize)
        print(parent_method)
        print(cross_method)
        print(mutation_method)
        print(survivors_method)
        print(cross_p)
        print(mutation_p)
    return render_template("tsp_page.html")
def tsp():
    return render_template("tsp_page.html")

@views.route("/about")
def about():
    return render_template("about.html")