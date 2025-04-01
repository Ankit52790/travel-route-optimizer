import numpy as np
from geopy.distance import geodesic

# Example locations (latitude, longitude)
locations = [(28.7041, 77.1025), (19.0760, 72.8777), (13.0827, 80.2707), (22.5726, 88.3639)]  # Delhi, Mumbai, Chennai, Kolkata

# Calculate total travel distance for a route
def fitness(route):
    distance = sum(geodesic(route[i], route[i+1]).km for i in range(len(route) - 1))
    return distance

# Generate Initial Population
def create_population(size):
    return [np.random.permutation(locations).tolist() for _ in range(size)]

# Select best routes
def select_best(population):
    return sorted(population, key=fitness)[:5]  # Top 5 routes

# Crossover: Swap parts of two parents
def crossover(parent1, parent2):
    cut = np.random.randint(1, len(parent1) - 1)
    child = list(parent1[:cut]) + [gene for gene in parent2 if gene not in parent1[:cut]]
    return child

# Mutation: Swap two random locations
def mutate(route):
    idx1, idx2 = np.random.randint(0, len(route), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

# Main Genetic Algorithm Loop
def genetic_algorithm(iterations=100, pop_size=10):
    population = create_population(pop_size)
    for _ in range(iterations):
        population = select_best(population)
        new_population = []
        for i in range(len(population) - 1):
            new_population.append(mutate(crossover(population[i], population[i+1])))
        population = new_population
    return population[0]  # Best optimized route

