import argparse
import numpy as np
import itertools
import copy

parser = argparse.ArgumentParser()
parser.add_argument("--infile")
parser.add_argument("--outfile")
args = parser.parse_args()
try:
    with open(args.infile, 'r') as infile:
        equations = [list(map(float, i.rstrip('\n').split())) for i in infile.readlines()]
        num_v = equations[0][0]
        equations.pop(0)
except ValueError:
    with open(args.infile, 'r') as infile:
        equations = [i.rstrip('\n').split() for i in infile.readlines()]
        num_v = int(equations[0][0])
        equations.pop(0)
        equations = [[complex(x) for x in equations[i]] for i in range(len(equations))]
eq_matrix = np.array(equations)
a = [x for x in range(len(equations))]
r, c = eq_matrix.shape


def check_identity(data):
    matrix = np.delete(data, -1, axis=1)
    rows = matrix.shape[0]
    id_matrix = np.identity(rows, dtype=float)
    id_matrix = id_matrix[::-1]
    return matrix.tolist() == id_matrix.tolist()


def leading_entry(item):
    for entry in item:
        if entry != 0:
            yield entry
    yield None


def check_arrangement(data):
    for i in range(len(data)):
        if data[i][i] == 0:
            for j in range(i + 1, len(data)):
                if data[j][i] != 0:
                    temp_copy = copy.copy(data[i])
                    data[i] = data[j]
                    data[j] = temp_copy
                    print(f'R{i + 1} <-> R{j + 1}')


def no_solutions(data):
    x = False
    for eq in data:
        if eq[-1] != 0 and set(eq[:-1]) == {0}:
            with open(args.outfile, 'w') as outfile:
                outfile.writelines('No solutions\n')
                x = True
    return x


def solver(data):
    solved = 0
    for i in itertools.cycle(a):
        try:
            for k in range(len(data)):
                if set(data[k]) == {0}:
                    data.pop(k)
                if no_solutions(data):
                    solved = 1
            le = next(leading_entry(data[i]))
            pos = np.where(np.array(data)[i] == le)[0][0]
            if le != 1:
                data[i] = [x / le for x in data[i]]
                print(f'{(1 / le, 2)} * R{i + 1} -> R{i + 1}')
            for j in range(i + 1, len(data)):
                if data[j][pos] != 0:
                    x = [-data[j][pos] * item for item in data[i]]
                    print(f'{(-data[j][pos], 2)} * R{i + 1} + R{j + 1} -> R{j + 1}')
                    data[j] = np.add(x, data[j])
                    print(np.array(data))
            d = set(x for x in np.diag(data))
            if d == {1}:
                data = list(reversed(data))
            if check_identity(np.array(data)):
                data = list(reversed(data))
                answers = [row[-1] for row in data]
                with open(args.outfile, 'w') as outfile:
                    for ans in answers:
                        outfile.writelines(f'{str(ans)}\n')
                        solved = 1
                print(f'Your solution is - {tuple(answers)}.')
            if (data[-1][len(data) - 1] == 0) and num_v > len(data):
                if no_solutions(data):
                    solved = 1
                elif d == {0, 1} and len(data) == 2:  # special case
                    with open(args.outfile, 'w') as outfile:
                        outfile.writelines('No solutions\n')
                        solved = 1
                elif num_v > len(data):
                    with open(args.outfile, 'w') as outfile:
                        outfile.writelines('Infinitely many solutions\n')
                        solved = 1
            if type(data[0][0]) == complex and num_v > len(data):
                with open(args.outfile, 'w') as outfile:
                    outfile.writelines('Infinitely many solutions\n')
                    solved = 1
            if solved == 1:
                break
        except IndexError:
            pass


check_arrangement(equations)
solver(equations)
