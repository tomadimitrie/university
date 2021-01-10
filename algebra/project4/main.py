import functools
import itertools


def check(matrix):
    # check if every element appears only once on the each column
    # we don't have to check the rows since they are permutations of the elements and the elements are unique
    transpose = tuple(zip(*matrix))
    for row in transpose:
        if tuple(dict.fromkeys(row).keys()) != row:
            return False
    # get a square matrix out of the matrix
    # check if that matrix is symmetric with respect to the main diagonal,
    # which means that it is equal to its transpose
    # by doing this at every step we get a final valid matrix
    chunk = [row[0:len(matrix)] for row in matrix]
    return tuple(zip(*chunk)) == tuple(chunk)


def pretty_print_matrix(matrix):
    # print a matrix in a readable form
    return '\n'.join(
        [' '.join(
            [f"a{element}" for element in row]
        ) for row in matrix]
    )


def backtrack(current, permutations, step, size, valid_matrices):
    # perform backtracking to generate the solutions
    for permutation in permutations:
        current.append(permutation)
        if check(current):
            # if we got to the desired size append the matrix to the solutions of its identity element
            if step == size:
                valid_matrices[current[0][0] - 1].append(current.copy())
            else:
                backtrack(current, permutations, step + 1, size, valid_matrices)
        current.pop()


for i in range(2, 7):
    with open(f"input{i}.txt", 'r') as input_file, open(f"output{i}.txt", 'w') as output_file:
        n = int(input_file.read())
        elements = [*range(1, n + 1)]
        # create all permutations of the elements
        permutations = list(itertools.permutations(elements, n))
        valid_matrices = [[] for _ in range(n)]
        # make sure that the first row has the sorted elements with the identity element in the first position
        for identity in range(1, n + 1):
            first = [*range(1, n + 1)]
            first.insert(0, first.pop(first.index(identity)))
            first = tuple(first)
            backtrack([first], permutations, 2, n, valid_matrices)
        # compute the number of valid matrices
        number_of_matrices = functools.reduce(
            lambda accumulator, current: accumulator + len(current),
            valid_matrices,
            0
        )
        # print the number
        output_file.write(f"there are {number_of_matrices} abelian group structures on a set with {n} elements\n\n")
        # if n <= 7 also write the matrices
        if n <= 7:
            for identity, solutions in enumerate(valid_matrices):
                output_file.write(f"for identity element a_{identity + 1}:\n")
                for matrix in solutions:
                    print(pretty_print_matrix(matrix), sep='\n', file=output_file)
                    output_file.write('\n')

