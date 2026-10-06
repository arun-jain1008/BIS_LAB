import random
def fitness(water, fertilizer):
   
    yield_value = 100 - (water - 80)**2 - (fertilizer - 50)**2
    return yield_value
num_particles = 10
iterations = 20
particles = []

for i in range(num_particles):
    water = random.uniform(0, 100)
    fertilizer = random.uniform(0, 100)

    particles.append({
        "water": water,
        "fertilizer": fertilizer,
        "best_water": water,
        "best_fertilizer": fertilizer,
        "best_fitness": fitness(water, fertilizer)
    })
global_best = max(particles, key=lambda p: p["best_fitness"])

gbest_water = global_best["best_water"]
gbest_fertilizer = global_best["best_fertilizer"]
gbest_fitness = global_best["best_fitness"]

for iteration in range(iterations):

    for p in particles:

        
        r1 = random.random()
        r2 = random.random()


        p["water"] += 0.5 * r1 * (p["best_water"] - p["water"]) \
                      + 0.5 * r2 * (gbest_water - p["water"])

        p["fertilizer"] += 0.5 * r1 * (p["best_fertilizer"] - p["fertilizer"]) \
                           + 0.5 * r2 * (gbest_fertilizer - p["fertilizer"])

        p["water"] = max(0, min(100, p["water"]))
        p["fertilizer"] = max(0, min(100, p["fertilizer"]))

        current_fitness = fitness(p["water"], p["fertilizer"])

        if current_fitness > p["best_fitness"]:
            p["best_water"] = p["water"]
            p["best_fertilizer"] = p["fertilizer"]
            p["best_fitness"] = current_fitness

        if current_fitness > gbest_fitness:
            gbest_water = p["water"]
            gbest_fertilizer = p["fertilizer"]
            gbest_fitness = current_fitness

print("Best Water Amount:", round(gbest_water, 2))
print("Best Fertilizer Amount:", round(gbest_fertilizer, 2))
print("Maximum Crop Yield:", round(gbest_fitness, 2))
