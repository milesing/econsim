'''
Created on Jan 22, 2014

@author: Peter Norvig
'''

#import matplotlib
import matplotlib.pyplot as plt

import populations
import transactions
import interactions


def simulate(population, transaction_fn, interaction_fn, T, percentiles, record_every):
    "Run simulation for T steps; collect percentiles every 'record_every' time steps."
    results = []
    for t in range(T):
        i, j = interaction_fn(population)
        #population[i], population[j] = transaction_fn(population[i], population[j]) 
        population[i].allocation, population[j].allocation = transaction_fn(population[i], population[j]) 
        if t % record_every == 0:
            results.append(record_percentiles(population, percentiles))
    return results


def report(distribution=populations.gauss, 
           transaction_fn=transactions.random_split, 
           interaction_fn=interactions.anyone, 
           N=populations.N, mu=populations.mu, T=5*populations.N, 
           percentiles=(1, 10, 25, 33.3, 50, -33.3, -25, -10, -1), record_every=25):
    "Print and plot the results of the simulation running T steps." 
    # Run simulation
    population = populations.sample(distribution, N, mu)
    results = simulate(population, transaction_fn, interaction_fn, T, percentiles, record_every)
    # Print summary
    print('Simulation: {} * {}(mu={}) for T={} steps with {} doing {}:\n'.format(
          N, name(distribution), mu, T, name(interaction_fn), name(transaction_fn)))
    fmt = '{:6}' + '{:10.2f} ' * len(percentiles)
    print(('{:6}' + '{:>10} ' * len(percentiles)).format('', *map(percentile_name, percentiles)))
    for (label, nums) in [('start', results[0]), ('mid', results[len(results)//2]), ('final', results[-1])]:
        print fmt.format(label, *nums)
    # Plot results
    col = 0.75
    for line in zip(*results):
        normaline = [x/line[0] for x in line]
        plt.plot(normaline, color=str(col))
        col *= 0.75
        # lighter is richer
    plt.show()


def record_percentiles(population, percentiles):
    "Pick out the percentiles from population."
    population = sorted(population, reverse=True)
    N = len(population)
    #return [population[int(p*N/100.)] for p in percentiles] 
    return [population[int(p*N/100.)].utility for p in percentiles]


def percentile_name(p):
    return ('median' if p == 50 else 
            '{} {}%'.format(('top' if p > 0 else 'bot'), abs(p)))

    
def name(obj):
    return getattr(obj, '__name__', str(obj))