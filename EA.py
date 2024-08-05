from TSP import TSP
import pandas as pd
import matplotlib.pyplot as plt

class EA:
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, problem_name, parent_selection_scheme, survivor_selection_scheme, filename):
        self.problem_name = globals()[problem_name]
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.instance = self.problem_name(population_size, offspring_size, generations, mutation_rate, iterations, filename)
        self.iterations = iterations  # Store the number of iterations

    def run(self):
        top_solutions = []
        generation_scores = []  # Initialize list to store generation-wise scores

        if "tournament_selection" in self.parent_selection_scheme:
            psf = self.parent_selection_scheme[:20]
            tn_size = self.parent_selection_scheme.split("_")[-1]
            self.instance.tournament_size = int(tn_size)
            self.parent_selection_scheme = psf

        if "tournament_selection" in self.survivor_selection_scheme:
            ssf = self.survivor_selection_scheme[:20]
            tn_size = self.survivor_selection_scheme.split("_")[-1]
            self.instance.tournament_size = int(tn_size)
            self.survivor_selection_scheme = ssf

        parent_selection_function = getattr(self.instance, self.parent_selection_scheme)
        survivor_selection_function = getattr(self.instance, self.survivor_selection_scheme)
        if not callable(parent_selection_function) or not callable(survivor_selection_function):
            print("Invalid selection scheme")
            return

        for i in range(self.instance.iterations):
            top_solution_iteration = float('inf')  # Initialize top solution for current iteration
            generation_scores_iteration = []  # Initialize list for storing generation-wise scores for current iteration
            for j in range(self.instance.generations):
                generation_score = min(self.instance.population, key=lambda x: x[1])[1]  # Get the best fitness for the current generation
                generation_scores_iteration.append(generation_score)  # Append the score to the list
                for k in range(0, self.instance.offspring_size, 2):
                    parents = parent_selection_function(p=True)
                    offsprings = self.instance.crossover(parents[0], parents[1])
                    self.instance.population.append(self.instance.mutate(offsprings[0]))
                    self.instance.population.append(self.instance.mutate(offsprings[1]))
                    self.instance.population.append(offsprings[0])
                    self.instance.population.append(offsprings[1])
                survivors = survivor_selection_function(s=True)
                self.instance.population = survivors
                top_solution_generation = min(self.instance.population, key=lambda x: x[1])
                print("Generation: ", j + 1)
                print("Top solution for this iteration: ", top_solution_generation[1])  # Print the fitness value
                top_solution_iteration = min(top_solution_iteration, top_solution_generation[1])  # Store fitness value only
            generation_scores.append(generation_scores_iteration)  # Append the list of scores for the current iteration
            top_solutions.append((None, top_solution_iteration))  # Append the fitness value only
            self.instance.init_population()  # Reinitialize the population for the next iteration

        self.save_to_csv(top_solutions, generation_scores)
        self.plot_graph(generation_scores)

    def save_to_csv(self, top_solutions, generation_scores):
        generations = []
        for gen in range(1, len(generation_scores[0]) + 1):
            gen_data = [f'Gen {gen}']  # Start with generation label
            for iteration in range(1, self.iterations + 1):
                # Extract the fitness score for the current iteration and generation
                score = generation_scores[iteration - 1][gen - 1]
                gen_data.append(score)
            # Append the list for the current generation to the list of all generations
            generations.append(gen_data)

        # Convert the list of lists into a DataFrame
        new_df = pd.DataFrame(generations, columns=['Generations'] + [f'Iteration {i}' for i in range(1, self.iterations + 1)])

        # Add the Best Fitness Score column
        new_df['Best Fitness Score'] = [min(row[1:]) for _, row in new_df.iterrows()]

        # Save the DataFrame to a CSV file
        new_df.to_csv('top_solutions_TSP.csv', index=False)

    def plot_graph(self, generation_scores):
        for iteration in range(len(generation_scores)):
            plt.plot(range(1, len(generation_scores[iteration]) + 1), generation_scores[iteration], label=f'Iteration {iteration + 1}')

        plt.xlabel('Generations')
        plt.ylabel('Fitness Value')
        plt.title('Fitness Value over Generations for Each Iteration')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()
