import random


investments = {
    "Stock A": 0.12,
    "Stock B": 0.10,
    "Stock C": 0.15,
    "Bond A": 0.06,
    "Gold": 0.08
}

investment_names = list(investments.keys())



def portfolio_return(portfolio):
    total = 0

    for i in range(len(portfolio)):
        total += portfolio[i] * investments[investment_names[i]]

    return total



def portfolio_risk(portfolio):
    risk = 0

    for weight in portfolio:
        risk += weight ** 2

    return risk



def fitness(portfolio):
    return portfolio_return(portfolio) - 0.05 * portfolio_risk(portfolio)



def create_population(size):
    population = []

    for _ in range(size):

        weights = [random.random() for _ in investment_names]

        total = sum(weights)

        # Convert weights so total = 1
        portfolio = [w / total for w in weights]

        population.append(portfolio)

    return population



def selection(population):
    population.sort(
        key=fitness,
        reverse=True
    )

    return population[:len(population) // 2]



def crossover(parent1, parent2):

    point = random.randint(
        1,
        len(parent1) - 1
    )

    child = (
        parent1[:point] +
        parent2[point:]
    )

    # Normalize weights
    total = sum(child)

    child = [
        weight / total
        for weight in child
    ]

    return child



def mutation(portfolio, mutation_rate=0.1):

    portfolio = portfolio.copy()

    if random.random() < mutation_rate:

        index = random.randint(
            0,
            len(portfolio) - 1
        )

        portfolio[index] += random.uniform(
            -0.1,
            0.1
        )

        # Prevent negative investment
        portfolio[index] = max(
            0,
            portfolio[index]
        )

        # Normalize
        total = sum(portfolio)

        portfolio = [
            weight / total
            for weight in portfolio
        ]

    return portfolio



def genetic_algorithm(
    population_size=100,
    generations=500,
    mutation_rate=0.1
):

    population = create_population(
        population_size
    )

    for generation in range(generations):

        selected = selection(population)

        new_population = selected.copy()

        while len(new_population) < population_size:

            parent1 = random.choice(selected)
            parent2 = random.choice(selected)

            child = crossover(
                parent1,
                parent2
            )

            child = mutation(
                child,
                mutation_rate
            )

            new_population.append(child)

        population = new_population

        if generation % 50 == 0:

            best = max(
                population,
                key=fitness
            )

            print(
                f"Generation {generation}: "
                f"Return = "
                f"{portfolio_return(best) * 100:.2f}%"
            )

    return max(
        population,
        key=fitness
    )



best_portfolio = genetic_algorithm()



print("\nOPTIMIZED INVESTMENT PORTFOLIO")

for i in range(len(investment_names)):

    print(
        f"{investment_names[i]}: "
        f"{best_portfolio[i] * 100:.2f}%"
    )

print(
    f"\nExpected Return: "
    f"{portfolio_return(best_portfolio) * 100:.2f}%"
)

print(
    f"Risk Score: "
    f"{portfolio_risk(best_portfolio):.4f}"
)