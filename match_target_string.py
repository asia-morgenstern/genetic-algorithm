""" match_target_string - genetic algorithm that matches to a target string

Asia Morgenstern
21 November 2023
"""

import random

# define global constants

POPULATION_SIZE = 100

GENES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-=" \
    "!@#$%^&*()_+,./;'[]\<>?:{}| "

TARGET = "I love Geeks for Geeks!"

class Individual(list):
    def __init__(self, chromosome):
        """ __ init__ - initializes an Individual
                      - contains two properties:  chromosome and fitness score
        """
        
        self.chromosome = chromosome
        self.fitness = self.calc_fitness()
    
    def gen_chromosome():
        """ gen_chromosome - generates a chromosome
                           - returns a list of randomly chosen characters
        """
        
        global GENES
        global TARGET
        
        chromosome = []
        for i in range(len(TARGET)):
            gene = random.choice(GENES)
            chromosome.append(gene)
    
        return chromosome
    
    def calc_fitness(self):
        """ calc_fitness - calculates and returns the fitness score
                         - determines fitness based on number of differing characters
        """
        
        global TARGET
    
        fitness = 0
        for s_gene, t_gene in zip(self.chromosome, TARGET):
            if s_gene != t_gene:
                fitness += 1
    
        return fitness
    
    def mate(self, parent2):
        """ mate - returns a child chromosome by crossing 2 parents and adding mutations
        
        - parent2 - one of 2 parents 
        """
        
        # chances of mutations or using genes from parent 1 or 2
        
        mutation_percent = 0.1
        p2_percent = 1 - mutation_percent
        p1_percent = p2_percent/2
        
        # create a child chromosome
        
        child_chromosome = []    
        for p1_gene, p2_gene in zip(self.chromosome, parent2.chromosome):
            r = random.random()
            
            # choose gene
            
            if r < p1_percent:
                child_chromosome.append(p1_gene)
            elif r < p2_percent:
                child_chromosome.append(p2_gene)
            else:
                child_chromosome.append(self.mutated_gene())
    
        return Individual(child_chromosome)
    
    def mutated_gene(self):
        """ mutated_gene - mutates a gene
                         - returns a randomly selected gene
        """
        
        global GENES
    
        gene = random.choice(GENES)
        return gene

def print_individual(indiv, gen):
    """ print_individual - prints generation, Individual with lowest fitness, and fitness
    """
    
    curr_str = "".join(indiv.chromosome)
    curr_fitness = indiv.fitness
    print(f"Generation {gen}  String:  {curr_str}  Fitness:  {curr_fitness}")

def genetic_algorithm():
    global POPULATION_SIZE
    
    # initial population
    
    population = []
    for _ in range(POPULATION_SIZE):
        gnome = Individual.gen_chromosome()
        population.append(Individual(gnome))
    
    # perform genetic algorithm until convergence
    
    curr_gen = 1                    # current generation
    converge = False    
    while not converge:
        # sort population on fitness score in ascending order
        
        population = sorted(population, key=lambda x : x.fitness)
        #print_individual(population[0], curr_gen)
        
        # algorithm converges if lowest fitness is 0
        
        if population[0].fitness == 0:
            converge = True
            break
        
        # create new generation
        
        new_generation = []
        
        # add top 10% to new generation (elitism)
        
        elite_percent = 0.1
        n_elite = int(elite_percent*POPULATION_SIZE)
        new_generation.extend(population[:n_elite])
        
        # generate remaining children using top 50% of old generation
        
        top_percent = 0.5
        n_top = int(top_percent*POPULATION_SIZE)
        
        for _ in range(POPULATION_SIZE - n_elite):
            parent1 = random.choice(population[:n_top])
            parent2 = random.choice(population[:n_top])
            child = parent1.mate(parent2)
            new_generation.append(child)
        
        # set current population to new generation and update curr_gen
        
        population = new_generation
        curr_gen += 1
    
    return curr_gen

def main():
    N_runs = 1000
    
    # statistical quantities
    
    gen = genetic_algorithm()
    
    tot_gen = gen
    min_gen = gen
    max_gen = gen
    
    for i in range(1, N_runs):
        gen = genetic_algorithm()
        
        tot_gen += gen
        
        min_gen = gen if gen < min_gen else min_gen
        max_gen = gen if gen > max_gen else max_gen
    
    # output statistics
    
    avg_gen = tot_gen/N_runs
    
    print(f"Number of Runs:  {N_runs}")
    print(f"Total Number of Generations:  {tot_gen}")
    print(f"Average Number of Generations:  {avg_gen:.3F}")
    print(f"Minimum Number of Generations:  {min_gen}")
    print(f"Maximum Number of Generations:  {max_gen}")

if __name__ == "__main__": 
    main()
