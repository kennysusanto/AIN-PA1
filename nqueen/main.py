import random
import time


def initial_population(n):
    # function to generate random population
    # a population contains n inidividual populations
    # an individual population contains n digits (melambangkan posisi row dari tiap queen)
    # sedangkan posisi column dilambangkan dengan index digit tersebut
    # ex: an individual population [2, 3, 1, 4] has 4 queens
    # the first is at (1, 2)
    # the second is at (2, 3)
    # the third is at (3, 1)
    # the fourth is at (4, 4)

    # initialize empty list (outer list)
    pop = []
    i = 0
    # generate list inside list as much as n
    # so that a population contains n individual populations
    # and each individual population contains n digits
    while i < n:
        # generate the inner list
        inner_pop = []
        j = 0
        while j < n:
            # generate digits as much as n
            # append generated digits into the inner list
            inner_pop.append(random.randint(1, n))
            j += 1
        # append the inner list into the outer list
        pop.append(inner_pop)
        i += 1
    # return generated population to caller
    return pop


def calc_best_fit(n):
    # function to calculate max fitness / best fitness (means the solution)
    # this calculates the maximum number of non-attacking queen pairs in the board

    # initialize subtractor variable x as 0
    x = 0
    # initialize total variable as 0
    total = 0
    # as long as subtractor variable is less than n
    # add the total as much as (n - 1) - x
    while x < n:
        # the formula is: sigma total from i=0 to n = (n - 1) - x
        total += (n-1)-x
        x += 1
    # return the total to caller
    return total


def cal_fitness(pop):
    # function to calculate the fitness of each individual population
    # fitness = number of non-attacking queens
    # initialize empty list (outer list)
    fitnesses = []
    for indv_pop in pop:
        # for every individual population in population
        # initialize result / fitness value
        res = 0
        # n = how many digits in an individual population
        n = len(indv_pop)
        i = 0
        # initialize list of queens positions (col, row)
        queens = []
        while i < n:
            # for every queen in an individual population
            # column is the index of the digit
            col = i + 1
            # row is the digit
            row = indv_pop[i]
            # apppend queen (col, row) into list of queens
            queens.append([col, row])
            i += 1

        l = 0
        while l < len(queens):
            # for every queen in an individual population
            j = l
            while j < len(queens):
                # get each queen from the same individual population
                # so that a queen is paired with every queen in the same individual population
                
                # check if the queen from the outer loop is the same as the queen in the inner loop
                if queens[l] == queens[j]:
                    # same queen, do nothing
                    pass
                else:
                    # different queen
                    # check if this pair of queens are attacking each other
                    if check_attacking(queens[l], queens[j], n):
                        # attacking pair, don't add fitness
                        pass
                    else:
                        # non-attacking pair, add fitness for this individual population by 1
                        res += 1

                j += 1
            l += 1
        # append the fitness value of each individual population to the outer list
        fitnesses.append(res)
    # return the list of fitnesses to caller
    return fitnesses


def check_attacking(q1, q2, n):
    # function to check whether a pair of queens attack each other or not
    # attacking = same row, same col, same diagonal

    # IMPORTANT!!!
    # position (0, 0) is on bottom left
    # queen[col, row]

    # generate diagonal boxes
    col = q1[0]
    row = q1[1]
    # initialize empty list to hold the possible diagonals of a queen
    diagonals = []
    #print('kanan atas')
    # generate diagonals for top-right
    diagonals.append(gen_diagonals(col, row, n, n, 1, 1))  # NE
    #print('kanan bawah')
    # generate diagonals for bottom-right
    diagonals.append(gen_diagonals(col, row, n, 1, 1, -1))  # SE
    #print('kiri atas')
    # generate diagonals for top-left
    diagonals.append(gen_diagonals(col, row, 1, n, -1, 1))  # NW
    #print('kiri bawah')
    # generate diagonals for bottom-left
    diagonals.append(gen_diagonals(col, row, 1, 1, -1, -1))  # SW

    # initialize empty list to normalize the list of diagonals
    # ex: [[[1, 2]], [1, 2]] --> [[1,2], [1, 2]]
    diagonals2 = []
    for d in diagonals:
        for dd in d:
            diagonals2.append(dd)

    # checking conditions
    if q1[0] == q2[0] or q1[1] == q2[1]:
        # the pair of queens have the same col or same row
        return True
    elif q2 in diagonals2:
        # the pair of queens have the same diagonal for any directions
        return True
    else:
        # the pair of queens are non-attacking pair
        return False


def gen_diagonals(col, row, col_limit, row_limit, col_diff, row_diff):
    # function to generate diagonal positions of a queen
    # col --> queen column position
    # row --> queen row position
    # col_limit --> the max or min of the column value
    # row_limit --> the max or min of the row value
    # col_diff --> add by how much for every column iteration
    # row_diff --> add by how much for every row iteration

    # initialize empty list to hold possible diagonal positions
    poss = []
    # c is the column position of the queen, r is the row position of the queen
    c = col
    r = row

    while (1 <= c and c <= col_limit) or (1 <= r and r <= row_limit):
        # while the value of c or r is in the limits
        # add c and r by their diffs
        c += col_diff
        r += row_diff
        # append the value of each iteration to the diagonal positions list
        poss.append([c, r])
    # return the possible diagonal positions list to caller
    return poss


def cal_probs(fits):
    # function to calculate probabilities of each individual population
    # initialize total as 0
    total = 0
    for fitness in fits:
        # for every fitness value in the fitnesses list
        # the total is added by that value
        total += fitness

    # initialize the list of probabilities
    probs = []
    for fitness in fits:
        # for every fitness value in the fitnesses list
        # check if the fitness value is zero or not
        if fitness == 0:
            # fitness is 0, just add 0 so no calculations will happen (prevent error)
            probs.append(0)
        else:
            # fitness is not 0
            # calculate probability
            # probability of each individual population = 
            # (the fitness value of each individual population / total of fitness values in the population) * 100
            val = (fitness/total)*100
            # append the calculated probability to list of probabilities
            probs.append(val)
    # return the list of probabilities to caller
    return probs


def cross_over(population, probabilities):
    # function to cross two individual populations
    # choose n pop from population based on probability

    # initialize n as the number of individual populations
    n = len(population)
    # choose n random individual populations based on their probabilities
    # the higher the probability of an individual population,
    # the higher it's chance to get choosen
    # that is why we use weights here
    # store the choosen individual populations to the choosen variable
    choosen = random.choices(population, weights=probabilities, k=n)

    # cross over
    # initialize empty list to store the
    # individual populations after the cross over (outer list)
    crossed = []
    i = 0
    while i < n:
        # for every individual population in the choosen population
        # initialize the split point of the individual population
        split_point = random.randint(1, n-1)
        # take a pair of individual populations to do cross over
        pop1 = choosen[i]
        pop2 = choosen[i+1]
        # cross over the pair of individual populations by splitting
        # each of them on the split point and then swap their first half and second half
        combined1 = pop1[:split_point] + pop2[split_point:]
        combined2 = pop2[:split_point] + pop1[split_point:]
        # append the resulting individual populations after cross over to the outer list
        crossed.append(combined1)
        crossed.append(combined2)
        # add by 2 because we are calculating a pair every iteration
        i += 2
    # return the population after cross over
    return crossed


def mutation(population):
    # function to mutate individual populations
    # initialize an empty list to hold the result of mutation
    # of every individual populations (outer list)
    res = []
    for pop in population:
        # for every individual population in the population
        # copy the individual population into tmp_pop
        tmp_pop = pop[:]
        # initialize n as the number of digits in an individual population
        n = len(tmp_pop)
        # initialize a random index to pick where to mutate the digit
        random_index = random.randint(0, n-1)
        # initialize a random value to mutate the digit into
        random_val = random.randint(1, n)
        # update the digit from the individual population to the mutated value
        tmp_pop[random_index] = random_val
        # append the mutated individual population to the result list (outer list)
        res.append(tmp_pop)
    # return the population after mutation to caller
    return res


def check_best_solution(result_pop, fitness, best_fitness):
    # function to check if the best solution is present at current generation
    for f in fitness:
        # for every fitness value in the fitnesses list
        # check if the fitness value is equal to the best fitness / max fitness value
        if f == best_fitness:
            # the fitness value is the best fitness value
            # initialize x as the index of the fitness value in the fitnesses list
            x = fitness.index(f)
            # use x (index of the best fitness value in the fitnesses list)
            # to get the individual population from the population list
            print(f'found best solution {result_pop[x]} at index {x}')
            # return the individual population that has the best fitness to caller
            return result_pop[x]


# main
# get input n (used in the number of queens, size of the board, and the number of digits)
n = int(input("Enter n: "))
# get the input g (limit of how many times to do the loop or how many generations to generate)
g = int(input("Enter g: "))

# initialize time counter to count how long to find the solution or reach the limit generation
start_time = time.time()

# generate the initial population
population = initial_population(n)
# display it
print(f'initial population->{population}')
# calculate the best fitness of n-queens problem
best_fitness = calc_best_fit(n)
# calculate the fitnesses of the population
fitness = cal_fitness(population)
# calculate the probabilities of the population
probabilities = cal_probs(fitness)
# do cross over on the population and store the new population after cross over
population_after_crossover = cross_over(population, probabilities)
# do mutation on the new population and store the new population after mutation
result_pop = mutation(population_after_crossover)

# variable to store the individual population that has the best fitness if it is found
solution = None

i = 1
while i <= g:
    # while the limit generation is not met
    # check if the limit generation is met
    if i == g:
        # reached the limit generation
        # display time spent and stop loop
        print('reached final generation')
        print(f"--- {(time.time() - start_time)} seconds ---")
        break
    
    # calculate fitness of the current population
    fitness = cal_fitness(result_pop)
    # display the current generation's population, fitness, and probabilities
    print(
        f'gen {i} -> {result_pop} -> fitness: {fitness} -> probs: {probabilities}')

    # check if the current generation has the best fitness
    solution = check_best_solution(result_pop, fitness, best_fitness)
    if solution:
        # current generation has the best fitness
        # display time spent and stop loop
        print(f"--- {(time.time() - start_time)} seconds ---")
        break
    
    # calculate the probabilites of the current population
    probabilities = cal_probs(fitness)
    # do cross over on the current population and store the new population after cross over
    population_after_crossover = cross_over(result_pop, probabilities)
    # do mutation on the new population and store the new population after mutation
    result_pop = mutation(population_after_crossover)

    i += 1