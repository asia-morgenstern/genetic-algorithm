""" root_finder - genetic algorithm that find roots of polynomial like equations

Asia Morgenstern
22 November 2023
"""

import random
import math

# define global constants

POPULATION_SIZE = 100

MAX_VAL = 21                                        # function dependent min and max val
MIN_VAL = 11

PRECISION = 10

def f(x):
    """ f - polynomial like equation
          - assumes function has at least 1 real root
    
    x - x value
    """
    
    #return (x - 10)**3 - 1
    #return (x - 10)**3 - math.cos(x) - 1
    #return (x - 10)**3 - math.cos(x) + 4*x
    return (x - 10)**3 - math.cos(x) + math.sin(x)

class Individual(object):    
    def __init__(self, chromosome):
        """ __ init__ - initializes an Individual
                      - contains two properties:  chromosome and fitness score
        """
        
        self.chromosome = chromosome
        self.fitness = self.calc_fitness()
    
    def gen_chromosome():
        """ gen_chromosome - generates a chromosome
                           - returns a list of bits based on randomly chosen floats
        """
        
        global MAX_VAL
        global MIN_VAL
        global PRECISION
        
        n = random.random()*(MAX_VAL - MIN_VAL) + MIN_VAL   # random float [MIN_VAL, MAX_VAL)
        n = float_to_bin(n, PRECISION)              # convert float to binary string
        
        chromosome = list(n)                        # convert string to list
    
        return chromosome
    
    def calc_fitness(self):
        """ calc_fitness - calculates and returns the fitness score
                         - determines fitness based on calculating f(x)
        """
        
        x = "".join(self.chromosome)                # convert list to string
        x = bin_to_float(x)                         # convert binary string to float
        
        fitness = abs(f(x))                         # calculate fitness
        
        return fitness
    
    def mate(self, parent2):
        """ mate - returns a child chromosome by crossing 2 parents and adding mutations
        
        - parent2 - one of 2 parents 
        """
        
        global MAX_VAL
        global MIN_VAL
        global PRECISION
        
        # chances of mutations or using genes from parent 1 or 2
        
        mutation_percent = 0.1
        p2_percent = 1 - mutation_percent
        p1_percent = p2_percent/2
        
        # ensure all child chromosomes are within range [MIN_VAL, MAX_VAL)
        
        max_str = float_to_bin(MAX_VAL, PRECISION)
        min_str = float_to_bin(MIN_VAL, PRECISION)
            
        i = 0
        check_max = True
        check_min = True
        
        # create a child chromosome
        
        child_chromosome = []        
        for p1_gene, p2_gene in zip(self.chromosome, parent2.chromosome):
            r = random.random()
            
            # choose gene
            
            if p1_gene == ".":                      # add decimal point
                child_chromosome.append(p1_gene)
                i += 1                
                continue
            
            if r < p1_percent:
                gene = p1_gene
            elif r < p2_percent:
                gene = p2_gene
            else:
                gene = self.mutated_gene()
            
            # check if gene is in range
            
            if check_max:
                if gene < max_str[i]:               # gene within max range
                    check_max = not check_max       # max no longer needs checked
                if gene > max_str[i]:               # gene out of range
                    gene = max_str[i]               # set gene to max_str bit
            
            if check_min:
                if gene > min_str[i]:               # gene within min range
                    check_min = not check_min       # min no longer needs checked
                if gene < min_str[i]:               # gene out of range
                    gene = min_str[i]               # set gene to min_str bit
            
            i += 1
            
            child_chromosome.append(gene)
    
        return Individual(child_chromosome)
    
    def mutated_gene(self):
        """ mutated_gene - mutates a gene
                         - returns either 0 or 1
        """
        
        r = random.randint(0, 1)
        
        gene = str(r)
        
        return gene

def print_individual(indiv, gen):
    """ print_individual - prints generation, Individual with lowest fitness, float val, and fitness
    """
    
    curr_str = "".join(indiv.chromosome)
    curr_val = bin_to_float(curr_str)
    curr_fit = indiv.fitness
    print(f"Generation {gen}  String:  {curr_str}  ", end="")
    print(f"Val:  {curr_val}  Fitness:  {curr_fit}")

def float_to_bin(n, precision):
    """ float_to_bin - converts ints and floats to binary strings
    
    n - int or float to convert to binary
      - assumes valid input
    precision - number of decimal places in binary representation
    """
    
    global MAX_VAL
    
    # convert int to float
    
    if type(n) is not float:
        n = float(n)
        
    # split float into whole number and decimal strings
    
    n = str(n)
    whole, decimal = n.split(".")
    
    # convert whole number to binary

    whole = int(whole)                              # convert string to int
    whole = str(bin(whole))                         # convert int to binary string
    bin_rep = whole[2:]                             # strip off "0x"
    
    # ensure int portion of bin_rep is same length as int portion of MAX_VAL
    
    max_val_int = int(MAX_VAL)                      # find int val of MAX_VAL
    max_val_bin = str(bin(max_val_int))             # convert to binary string
    max_val_bin = max_val_bin[2:]                   # strip off "0x"
    max_val_len = len(max_val_bin)                  # determine length of string
    
    while len(bin_rep) < max_val_len:               # pad front with 0
        bin_rep = "0" + bin_rep
    
    # convert decimal portion to binary
    
    decimal = "0." + decimal                        # convert decimal portion to decimal
    decimal = float(decimal)                        # convert string to float
    
    bin_rep += "."    
    for i in range(precision):                      # calculate bin_rep to set precision
        decimal = 2*decimal                         # double decimal
        bin_rep += str(int(decimal))                # add int portion to bin_rep
        
        if decimal >= 1:                            # subtract if decimal >= 1
            decimal -= 1

    return bin_rep

def bin_to_float(bin_rep):
    """ bin_to_float - convert binary string to float
    
    bin_rep - string or list to convert to float
            - assumes valid input
    """
    
    # convert list to string
    
    if type(bin_rep) is list:
        bin_rep = "".join(bin_rep)
    
    # split string into whole number and decimal strings
    
    whole, decimal = bin_rep.split(".")
    
    # calculate float equivalent from binary whole
    
    ft_num = 0.0
    exponent = 0
    for i in range(len(whole) - 1, -1, -1):         # iterate backwards through string
        multiplier = int(whole[i])                  # determine multiplier, 0 or 1
        ft_num += multiplier*2**exponent            # multiply by 2^n, n = exponent
        
        exponent += 1
    
    # calculate float equivalent from binary decimal portion
    
    exponent = -1
    for i in range(0, len(decimal), 1):             # iterate forwards through string
        multiplier = int(decimal[i])                # determine multiplier, 0 or 1
        ft_num += multiplier*2**exponent            # multiply by 2^n, n = exponent
        
        exponent -= 1
    
    return ft_num

def genetic_algorithm():
    global POPULATION_SIZE
    
    # initial population
    
    population = []
    for _ in range(POPULATION_SIZE):
        gnome = Individual.gen_chromosome()
        population.append(Individual(gnome))
        
    # perform genetic algorithm until convergence
        
    curr_gen = 1                                    # current generation    
    epsilon = 2e-3
    converge = False    
    while not converge:
        # sort population on fitness score in ascending order
        
        population = sorted(population, key=lambda x : x.fitness)
        #print_individual(population[0], curr_gen)
        
        # algorithm converges if lowest fitness is less than epsilon
        
        if population[0].fitness < epsilon:
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
        
        for i in range(POPULATION_SIZE - n_elite):
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
