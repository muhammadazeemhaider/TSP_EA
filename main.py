import sys
from EA import EA

def main():
    problem = "TSP"
    filename = "qa194.tsp"
    parent_selection = "random"
    survivor_selection = "truncation"
    pop_size = 20
    offspring_size = 4
    generations_no = 10000
    mutation_rate = 0.35
    iterations = 5
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, problem, parent_selection, survivor_selection, filename).run()

def selection_scheme(scheme):
    if scheme=="fps":
        return "fitness_prop_selection"
    elif scheme=="rbs":
        return "rank_based_selection"
    elif scheme=="tr":
        return "truncation"
    elif scheme=="rn":
        return "random"
    elif "ts" in scheme:
        size = scheme.split("_")[-1]
        return "tournament_selection_" + size

main()