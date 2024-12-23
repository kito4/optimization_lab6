import random

def calculate_fitness(route, distances):
    """Вычисляет длину маршрута."""
    total_distance = 0
    for i in range(len(route)):
        total_distance += distances[route[i]][route[(i + 1) % len(route)]]
    return total_distance

def generate_population(cities, population_size):
    """Создает начальную популяцию."""
    population = []
    for _ in range(population_size):
        route = cities[:]
        random.shuffle(route)
        population.append(route)
    return population

def select_parents(population, distances):
    """Выбирает родителей на основе турнирной селекции."""
    tournament_size = 3
    selected = random.sample(population, tournament_size)
    selected.sort(key=lambda route: calculate_fitness(route, distances))
    return selected[0], selected[1]

def crossover(parent1, parent2):
    """Однородный кроссовер."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    pointer = 0
    for city in parent2:
        if city not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = city
    return child

def mutate(route, mutation_rate):
    """Мутирует маршрут с заданной вероятностью."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

def genetic_algorithm(distances, population_size, generations, mutation_rate):
    """Основной цикл генетического алгоритма."""
    cities = list(distances.keys())
    population = generate_population(cities, population_size)

    for generation in range(generations):
        # Вычисляем приспособленность для текущей популяции
        population.sort(key=lambda route: calculate_fitness(route, distances))
        next_generation = population[:2]  # Элитизм (сохранение лучших решений)

        while len(next_generation) < population_size:
            parent1, parent2 = select_parents(population, distances)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            next_generation.append(child)

        population = next_generation

    # Возвращаем лучшее решение
    best_route = min(population, key=lambda route: calculate_fitness(route, distances))
    return best_route, calculate_fitness(best_route, distances)

# Данные задачи
DISTANCES_BETWEEN_CITIES = {
    1: {2: 1, 3: 7, 4: 2, 5: 8},
    2: {1: 2, 3: 10, 4: 3, 5: 1},
    3: {1: 7, 2: 10, 4: 2, 5: 6},
    4: {1: 2, 2: 3, 3: 2, 5: 4},
    5: {1: 8, 2: 1, 3: 6, 4: 4}
}

# Параметры алгоритма
POPULATION_SIZE = 4
GENERATIONS = 100
MUTATION_RATE = 0.01

# Запуск алгоритма
best_route, best_distance = genetic_algorithm(DISTANCES_BETWEEN_CITIES, POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
print("Лучший маршрут:", best_route)
print("Расстояние:", best_distance)
