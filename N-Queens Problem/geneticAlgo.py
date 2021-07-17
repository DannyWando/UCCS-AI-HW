# This function is the genetic algorithm to be used in CS4820 HW2.
#
# Code reused from midterm project where I used a GA to suggest best search query results

import random
import nQueens

MAX_GENERATIONS = 1000
# Population size per generation
POPULATION_SIZE = 100
GENES = '01234567'

# Chromosome class
class Individual(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculateFitness()

    @classmethod
    # Randomly mutates a genes
    def mutated_genes(self):
        global GENES
        gene = random.randint(0,7)
        return gene

    @classmethod
    # Creates the chromosome out of randomly generated genes
    def createChromosome(self):
        chromosomeLen = 8
        newChromosome = []
        for i in range(chromosomeLen):
            newChromosome.append(self.mutated_genes())

        return newChromosome

    # Uses random probability to choose which parent passes on their gene
    # 10 percent of the time, a gene will be randomly created instead of taken from parents
    def mating(self, parent2):
        # Child chromosome
        newChromosome = []

        for geneP1, geneP2 in zip(self.chromosome, parent2.chromosome):
            prob = random.random()

            # If the probability is less than 0.45
            # Pass gene from parent 1
            if prob < 0.45:
                newChromosome.append(geneP1)

            # If the probability is between 0.45-0.90
            # Pass gene from parent 2
            elif prob < 0.9:
                newChromosome.append(geneP2)

            # If the probability is over 0.90
            # Randomly generate a new gene
            else:
                newChromosome.append(self.mutated_genes())

        return Individual(newChromosome)

    def calculateFitness(self):
        return nQueens.checkSolution(self.chromosome)


# Genetic algorithm implementation
def geneticAlgo():
    global POPULATION_SIZE

    currentGen = 1
    found = False
    population = []

    # create initial population
    for i in range(POPULATION_SIZE):
        genePool = Individual.createChromosome()
        population.append(Individual(genePool))

    while not found:

        # Sorting the population starting from the lowest fitness score and increasing
        # Lower fitness means less collisions, which means "better" solution
        population = sorted(population, key=lambda x: x.fitness)

        new_generation = []

        # Perform Elitism, that mean 10% of fittest population
        # goes to the next generation
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        # Better half of generation gets pooled into mating
        s = int((90 * POPULATION_SIZE) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = parent1.mating(parent2)
            new_generation.append(child)

        population = new_generation

        print("Generation: {}\tString: {}\tFitness: {}". \
              format(currentGen,
                     "".join(str(population[0].chromosome)),
                     str(population[0].fitness)))

        if population[0].fitness == 0:
            found = True
        currentGen += 1

    print("Generation: {}\tString: {}\tFitness: {}". \
          format(currentGen-1,
                 "".join(str(population[0].chromosome)),
                 str(population[0].fitness)))

    nQueens.printBoardFromState(len(population[0].chromosome), population[0].chromosome)

