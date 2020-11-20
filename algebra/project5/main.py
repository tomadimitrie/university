import itertools
from mod import Mod

Mod.__repr__ = lambda self: f"{int(self)}"
Mod.__str__ = Mod.__repr__


def minor(m, i, j):
    return [row[:j] + row[(j + 1):] for row in (m[:i] + m[(i + 1):])]


def determinant(matrix):
    # credits: https://stackoverflow.com/a/39881309/6603599

    # base case for 2x2 matrix
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c in range(len(matrix)):
        det += ((-1) ** c) * matrix[0][c] * determinant(minor(matrix, 0, c))
    return det


# read each input file
for file_index in range(2, 7):
    with open(f"input{file_index}.txt", 'r') as input_file, open(f"output{file_index}.txt", 'w') as output_file:
        n = int(input_file.read())
        # credits to https://math.stackexchange.com/a/362320
        # to count the number of bases of the vector space Z^n_2 over Z_2 we apply the following formula:
        # (2^n - 1)(2^n - 2^1)...(2^n - 2^(n - 1))
        # because there are 2^n - 1 ways to choose the first element (we can't choose zero),
        # the generated subspace has 2 elements => there are 2^n - 2 ways to choose the second element
        # by repeating this, we obtain the formula
        bases_count = 1
        for current in range(n):
            bases_count *= 2 ** n - 2 ** current
        print(f"the number of bases of the vector space Z^{n}_2 over Z_2 is {bases_count} \n", file=output_file)

        # if n <= 4 we also print the bases
        if n <= 4:
            # generate each vector in the vector space Z^n_2 over Z_2 without zero
            vectors = [permutation for permutation in itertools.product([Mod(0, 2), Mod(1, 2)], repeat=n) if
                       permutation != (0,) * n]
            bases = []
            # for each way to take a group of n vectors
            for permutation in itertools.permutations(vectors, n):
                # check if the vectors are linearly independent <=> the determinant is non-zero
                if determinant(permutation) != 0:
                    bases.append(permutation)
            print('the vectors of each such basis are:', file=output_file)
            print(*bases, sep='\n', file=output_file)
