import random

# function to create random population
def initial_population(n):
    pop = []
    i = 0
    while i < n:
        inner_pop = []
        j = 0
        while j < n:
            inner_pop.append(random.randint(1, n))
            j += 1
        pop.append(inner_pop)
        i += 1
    
    return pop

# function to calculate max fitness / best fitness (means the solution)
def calc_best_fit(n):
    x = 0
    total = 0
    while x < n:
        total += (n-1)-x
        x += 1
    return total

# function to calculate the fitness of each individual population
# fitness = number of non-attacking queens
def cal_fitness(pop):
    fitnesses = []
    for board in pop:
        res = 0
        n = len(board)
        i = 0
        queens = []
        while i < n:
            col = i + 1
            row = board[i]
            queens.append([col, row])
            i += 1
        
        for q in queens:
            j = 0
            while j < len(queens):
                if q == queens[j]:
                    pass
                else:
                    if check_attacking(q, queens[j], n):
                        # attacking pair, don't add fitness
                        pass
                    else:
                        # non-attacking pair, add fitness for this board by 1
                        res += 1
                j += 1
            # remove current queen so it is not calculated
            # in the next iteration
            queens.remove(q)
    
        fitnesses.append(res)
    return fitnesses

# function to check whether queens attack each other or not
# attacking = same row, same col, same diag
def check_attacking(q1, q2, n):
    # IMPORTANT!!!
    # board (0, 0) on bottom left
    # queen[col, row]

    # generate diagonal boxes
    col = q1[0]
    row = q1[1]
    diagonals = []
    diagonals.append(gen_diagonals(col, row, n, n, 1, 1)) # NE
    diagonals.append(gen_diagonals(col, row, n, 1, 1, -1)) # SE
    diagonals.append(gen_diagonals(col, row, 1, n, -1, 1)) # NW
    diagonals.append(gen_diagonals(col, row, 1, 1, -1, -1)) # SW

    # checking conditions
    if q1[0] == q2[0] or q1[1] == q2[1]:
        # same col or same row
        return True
    elif q2 in diagonals:
        # same diagonal all directions
        return True
    else:
        # non-attacking pair
        return False

# function to generate diagonal boxes
def gen_diagonals(col, row, col_limit, row_limit, col_diff, row_diff):
    while 1 < col < col_limit and 1 < row < row_limit:
        col += col_diff
        row += row_diff
        return [col, row]

# function to calculate probabilities of each individual population
def cal_probs(fits):
    total = 0
    for fitness in fits:
        total += fitness
    
    probs = []
    for fitness in fits:
        val = (fitness/total)*100
        probs.append(val)

    return probs

# function to cross two individual populations
def cross_over(population, probabilities):
    # choose n pop from population based on probability
    n = len(population)
    choosen = random.choices(population, weights=probabilities, k=n)
    # cross over
    crossed = []
    i = 0
    while i < n:
        split_point = random.randint(1, n-1)
        pop1 = choosen[i]
        pop2 = choosen[i+1]
        combined1 = pop1[:split_point] + pop2[split_point:]
        combined2 = pop2[:split_point] + pop1[split_point:]
        crossed.append(combined1)
        crossed.append(combined2)

        i += 2

    return crossed

# function to mutate individual populations
def mutation(population):
    res = []
    for pop in population:
        tmp_pop = pop[:]
        n = len(tmp_pop)
        random_index = random.randint(0, n-1)
        random_val = random.randint(1, n)
        tmp_pop[random_index] = random_val
        res.append(tmp_pop)

    return res

# main
n = int(input("Enter n: "))
g = int(input("Enter g: "))
population = initial_population(n)
best_fitness = calc_best_fit(n)
fitness = cal_fitness(population)
probabilities = cal_probs(fitness)
population_after_crossover = cross_over(population, probabilities)
result_pop = mutation(population_after_crossover)
print(f'gen 1 -> {result_pop} -> {fitness}')
i = 1
while i <= g:
    
    if i == g:
        print('reached final generation')
        break
    for f in fitness:
        if f == best_fitness:
            x = fitness.index(f)
            print(f'found best solution {result_pop[x]}')
            break
    
    fitness = cal_fitness(result_pop)
    probabilities = cal_probs(fitness)
    population_after_crossover = cross_over(result_pop, probabilities)
    result_pop = mutation(population_after_crossover)

    i += 1
    print(f'gen {i} -> {result_pop} -> {fitness} -> {probabilities}')

    
    