# -*- coding: utf-8 -*-
# Python 3.4*

'''
INPUT:
To run an nQueens problem with n queens:
import nQueens.py
nQueens.nQueens(8, 'realPop')

or this at the command line:
python nQueens 8 realPop


OUTPUT:
Returns the sequence of y positions from left to right which are a solution as a list, and your student ID # as an int:
e.g., return [7, 3, 0, 2, 5, 1, 6, 4]

'''

# %%
from random import choice, random, uniform
import sys


# %%
def fitness(trial):
    fitn = 1
    for pos in (range(len(trial) -1)):
        if trial.count(trial[pos]) > 1:
            fitn -= 1/len(trial)
        else:
            for i in range(len(trial)):
                diff = i - pos
                if diff != 0 and (trial[i] == (trial[pos] + diff) or trial[i] == (trial[pos] - diff)):
                    fitn -= 1/len(trial)
    return fitn
def mutaterate(bestParent):
    '''
    Less mutation the closer the fit of the parent.
    This is not the most biologically realistic,
    but is decent to mimick T of simulated annealing.
    Performance is actually sensitive to below schedule
    '''
    fit = fitness(bestParent)
    ret = 0
    
    ret =  ((1- (perfectfitness - (fit ** 2)) / (target /2))) #simulated annealing with exponential curve
    return ret
def mutate(sequence, rate):
    return [(ch if random() <= rate else choice(charset)) for ch in sequence]


def que(iterations, bestParent, rate):
    'prints progress'
    print ("Run %-4i had fitness=%4.1f%%, sequence= '%s', and mutation rate p=%-4f/char" %
           (iterations, fitness(bestParent)*100, ', '.join(map(str, bestParent)), 1-rate))

def mate(a, b):
    '''
    Mates two parents via sexual reproduction (crossing over).
    Crossing over happens with ~p=0.7
    '''
    place = 0
    if choice(range(10)) < 7:
        place = choice(range(target))
    else:
        return a, b
    return a[:place] + b[place:], b[:place] + a[place:]


def get_lucky(items):
    '''
    Chooses a random element from items,
    where items is a list of tuples in the form (item, weight).
    weight determines the probability of choosing its respective item.
    '''
    weight_total = sum((item[1] for item in items))
    n = uniform(0, weight_total)
    for item, weight in items:
        if n < weight:
            return item
        n = n - weight
    return item


def nQueens(targInput= 8, pop_version='realPop'):
    '''
    Inputs:
    targInput as string, pop_version (realPop or pseudoPop)
    realPop is default

    Outputs:
    The goal string, your student ID number (hard coded)

    Example:
    weasel_the_answer_out(targInput='text string', pop_version = 'realPop' or 'pseudoPop')
    '''

    global target
    global charset
    global perfectfitness

    target = targInput
    charset = range(targInput)
    perfectfitness = 1

    POP_SIZE = 400
    bestParent = [choice(charset) for _ in range(target)]
    center = int(POP_SIZE/2)

    iterations = 0
    while fitness(bestParent) != perfectfitness:
        rate = mutaterate(bestParent)
        iterations += 1
        if iterations % 100 == 0:
            que(iterations, bestParent, rate)
        if pop_version == 'pseudoPop':
            # Pseudo-population section is a bit of a hack,is not really bio-realistic,
            # and not really a good population for many problems with local minima,
            # since a single parents produces an entire generation,
            # after which, only two single best individuals are breeding
            # to produce 1 offspring.
            children = [mutate(bestParent, rate) for _ in range(POP_SIZE)] + [bestParent]
            twentysomething1 = max(children[:center], key=fitness)
            twentysomething2 = max(children[center:], key=fitness)
            bestParent = max(mate(twentysomething1, twentysomething2), key=fitness)
        else:
            # Population version works via larger random pool of "sexual" crossing over
            if iterations == 1:
                population = [mutate(bestParent, rate) for _ in range(POP_SIZE)] + [bestParent]

            sexy_breeders = []
            for individual in population:
                fitness_val = fitness(individual)
                pair = (individual, fitness_val/(perfectfitness))
                sexy_breeders.append(pair)

            population = []
            for _ in range(int(POP_SIZE/2)):
                parent1 = get_lucky(sexy_breeders)
                parent2 = get_lucky(sexy_breeders)
                child1, child2 = mate(parent1, parent2)
                population.append(mutate(child1, rate))
                population.append(mutate(child2, rate))

            bestParent = max(population, key=fitness)

    que(iterations, bestParent, rate)
    return bestParent

# %%
if __name__ == "__main__":
    total = len(sys.argv)
    if total == 1:
       nQueens()
    elif total == 2:
        nQueens(str(sys.argv[1]))
    elif total == 3:
        nQueens(str(sys.argv[1]), str(sys.argv[2]))
    else:
        print('You supplied too many inputs and should read the docstring first!')
