import random
import time


def initial_population(n):
    # function to create random population
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


def calc_best_fit(n):
    # function to calculate max fitness / best fitness (means the solution)
    x = 0
    total = 0
    while x < n:
        total += (n-1)-x
        x += 1
    return total


def cal_fitness(pop):
    # function to calculate the fitness of each individual population
    # fitness = number of non-attacking queens
    fitnesses = []
    for board in pop:
        #print(f"board {board}")
        res = 0
        n = len(board)
        i = 0
        queens = []
        while i < n:
            col = i + 1
            row = board[i]
            queens.append([col, row])
            #print(f'board {board} q{i+1}({col},{row})')
            i += 1

        l = 0
        while l < len(queens):
            j = l
            while j < len(queens):
                #print(f'q1->{queens[l]}, q2->{queens[j]}, attacking pair->{check_attacking(queens[l], queens[j], n)}')
                if queens[l] == queens[j]:
                    pass
                else:

                    if check_attacking(queens[l], queens[j], n):
                        # attacking pair, don't add fitness
                        pass
                    else:
                        # non-attacking pair, add fitness for this board by 1
                        res += 1

                    #print(f'{queens[l]} {queens[j]} = {check_attacking(queens[l], queens[j], n)}, {res}')

                j += 1
            # print('----\r')
            l += 1

        fitnesses.append(res)
    return fitnesses


def check_attacking(q1, q2, n):
    # function to check whether queens attack each other or not
    # attacking = same row, same col, same diag

    # IMPORTANT!!!
    # board (0, 0) on bottom left
    # queen[col, row]

    # generate diagonal boxes
    col = q1[0]
    row = q1[1]
    diagonals = []
    #print('kanan atas')
    diagonals.append(gen_diagonals(col, row, n, n, 1, 1))  # NE
    #print('kanan bawah')
    diagonals.append(gen_diagonals(col, row, n, 1, 1, -1))  # SE
    #print('kiri atas')
    diagonals.append(gen_diagonals(col, row, 1, n, -1, 1))  # NW
    #print('kiri bawah')
    diagonals.append(gen_diagonals(col, row, 1, 1, -1, -1))  # SW
    diagonals2 = []
    for d in diagonals:
        for dd in d:
            diagonals2.append(dd)

    # checking conditions
    if q1[0] == q2[0] or q1[1] == q2[1]:
        # same col or same row
        return True
    elif q2 in diagonals2:
        # same diagonal all directions
        return True
    else:
        # non-attacking pair
        return False


def gen_diagonals(col, row, col_limit, row_limit, col_diff, row_diff):
    # function to generate diagonal boxes
    cols = []
    c = col
    r = row

    while (1 <= c and c <= col_limit) or (1 <= r and r <= row_limit):
        c += col_diff
        r += row_diff
        cols.append([c, r])

    return cols


def cal_probs(fits):
    # function to calculate probabilities of each individual population
    total = 0
    for fitness in fits:
        total += fitness

    probs = []
    for fitness in fits:
        if fitness == 0:
            probs.append(0)
        else:
            val = (fitness/total)*100
            probs.append(val)

    return probs


def cross_over(population, probabilities):
    # function to cross two individual populations
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


def mutation(population):
    # function to mutate individual populations
    res = []
    for pop in population:
        tmp_pop = pop[:]
        n = len(tmp_pop)
        random_index = random.randint(0, n-1)
        random_val = random.randint(1, n)
        tmp_pop[random_index] = random_val
        res.append(tmp_pop)

    return res


def check_best_solution(result_pop, fitness, best_fitness):
    # functoin to check if the best solution is present at current generation
    for f in fitness:
        if f == best_fitness:
            x = fitness.index(f)
            print(f'found best solution {result_pop[x]} at index {x}')
            return result_pop[x]


# main
n = int(input("Enter n: "))
g = int(input("Enter g: "))

# initialize time counter
start_time = time.time()

population = initial_population(n)
print(f'initial population->{population}')
best_fitness = calc_best_fit(n)
fitness = cal_fitness(population)
probabilities = cal_probs(fitness)
population_after_crossover = cross_over(population, probabilities)
result_pop = mutation(population_after_crossover)

# variable to store the best solution is found
solution = None

i = 1
while i <= g:
    if i == g:
        print('reached final generation')
        print(f"--- {(time.time() - start_time)} seconds ---")
        break

    fitness = cal_fitness(result_pop)
    print(
        f'gen {i} -> {result_pop} -> fitness: {fitness} -> probs: {probabilities}')

    # check for best solution
    solution = check_best_solution(result_pop, fitness, best_fitness)
    if solution:
        print(f"--- {(time.time() - start_time)} seconds ---")
        break

    probabilities = cal_probs(fitness)
    population_after_crossover = cross_over(result_pop, probabilities)
    result_pop = mutation(population_after_crossover)

    i += 1
