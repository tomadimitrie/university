import itertools

import sympy

for file_index in range(0, 5):
    with open(f"input{file_index}.txt", 'r') as input_file, open(f"output{file_index}.txt", 'w') as output_file:
        # read m, n
        m, n = [int(number) for number in input_file.read().split(' ')]
        # generate all possible combinations of 0 and 1 of size n
        lists = list(itertools.product('01', repeat=n))
        # generate all possible combinations of the previously generated lists of size m
        matrices = list(itertools.product(lists, repeat=m))
        # apply rref for each matrix
        rrefs = [sympy.Matrix(matrix).rref()[0] for matrix in matrices]
        # apply % 2 for every element of every matrix because we are working in base 2
        for i in range(len(rrefs)):
            for j in range(len(rrefs[i])):
                rrefs[i][j] %= 2
        # only keep the unique matrices
        filtered_rrefs = []
        for rref in rrefs:
            if rref not in filtered_rrefs:
                filtered_rrefs.append(rref)
        # print the number of matrices
        print(
            f"there are {len(filtered_rrefs)} matrices A ∈ M_({m}, {n})(Z_2) in reduced echelon form\n",
            file=output_file
        )
        # print the matrices if 2 <= m, n <= 5
        if 2 <= m <= 5 and 2 <= n <= 5:
            # get the list representation from sympy's Matrix
            matrices = [matrix.tolist() for matrix in filtered_rrefs]
            for matrix in matrices:
                for i in range(len(matrix)):
                    flag = True
                    for j in range(len(matrix[i])):
                        # mark the leading 1s
                        if matrix[i][j] == 1 and flag:
                            matrix[i][j] = "[1]"
                            flag = False
                        else:
                            matrix[i][j] = f" {matrix[i][j]} "
                        output_file.write(matrix[i][j])
                    output_file.write('\n')
                output_file.write('\n')
