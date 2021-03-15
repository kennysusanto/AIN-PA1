import random

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

# fitness = number of non-attacking queens
def fitness(pop):
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
    
        fitnesses.append(res)
    return fitnesses

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

def gen_diagonals(col, row, col_limit, row_limit, col_diff, row_diff):
    while 1 < col < col_limit and 1 < row < row_limit:
        col += col_diff
        row += row_diff
        return [col, row]

def cross_over():
    pass

def mutation():
    pass


# main
n = int(input("Enter n: "))
population = initial_population(n)
fitness = fitness(population)
print(population)
print(fitness)