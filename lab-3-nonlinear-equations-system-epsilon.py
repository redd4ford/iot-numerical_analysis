def g1(x1, x2):
    return float(pow(x1, 2) + 0.8 * x2 ** 2 + 0.1)


def g2(x1, x2):
    return float(2 * x1 * x2 - 0.1)


def generate_matrix(function_count, arguments_count):
    matrix = []
    for function in range(2 * function_count):
        arguments = []
        for argument in range(arguments_count):
            argument_values = [0, 0]
            arguments.append(argument_values)
        matrix.append(arguments)
    return matrix


def main():
    epsilon_matrix = generate_matrix(2, 2)
    # 0.5 0.5
    x1 = float(input('enter x1: '))
    x2 = float(input('enter x2: '))
    function_count, arguments_count = 2, 2
    error = 0.0000001

    exit_marker = False
    while not exit_marker:
        x = []
        for iteration_count in range(p):
            x1 = g1(x1, x2)
            x2 = g2(x1, x2)

        if len(epsilon_matrix[0][0]) > 1:
            epsilon_matrix[0][0][1] = x1
            epsilon_matrix[0][1][1] = x2
        else:
            epsilon_matrix[0][0].append(x1)
            epsilon_matrix[0][1].append(x2)

        # генерація послідовності S
        for function in range(2 * function_count):
            if len(epsilon_matrix[function][0]) > 1:
                epsilon_matrix[function][0][1] = g1(x1, x2)
                epsilon_matrix[function][1][1] = g2(x1, x2)
            else:
                epsilon_matrix[function][0].append(g1(x1, x2))
                epsilon_matrix[function][1].append(g2(x1, x2))
            if function == 0:
                exit_marker = True
                for i in range(arguments_count):
                    try:
                        exit_marker = exit_marker and abs(float((epsilon_matrix[1][i][1] - epsilon_matrix[0][i][1])) /
                                                          float(epsilon_matrix[1][i][1])) < error
                    except ZeroDivisionError:
                        exit_marker = False
                        continue
        # метод екстраполяції
        if not exit_marker:
            for subraw_index in range(1, function_count * 2):
                for subcolumn_index in range(0, function_count * 2 - subraw_index):
                    V = []
                    try:
                        # обертання Самельсона
                        for i in range(function_count):
                            V.append(epsilon_matrix[subcolumn_index + 1][i][subraw_index] -
                                     epsilon_matrix[subcolumn_index][i][subraw_index])
                    except IndexError:
                        break
                    sum_of_V = sum([pow(Vi, 2) for Vi in V])

                    try:
                        for q in range(len(V)):
                            V[q] /= sum_of_V
                    except ZeroDivisionError:
                        break

                    try:
                        # кожен елемент - сума наступних нормалізованих
                        for i in range(function_count):
                            if len(epsilon_matrix[subcolumn_index][i]) > subraw_index + 1:
                                epsilon_matrix[subcolumn_index][i][subraw_index + 1] = \
                                    epsilon_matrix[subcolumn_index + 1][i][subraw_index - 1] + V[i]
                            else:
                                epsilon_matrix[subcolumn_index][i].append(
                                    epsilon_matrix[subcolumn_index + 1][i][subraw_index - 1] + V[i])
                    except IndexError:
                        continue
                x1 = epsilon_matrix[0][0][-1]
                x2 = epsilon_matrix[0][1][-1]
    print(x1)
    print(x2)
    print(g1(x1, x2))
    print(g2(x1, x2))
    print("g1(x1, x2) - x1 = " + str("{:.3f}".format(g1(x1, x2) - x1)))
    print("g2(x1, x2) - x2 = " + str("{:.3f}".format(g2(x1, x2) - x2)))


if __name__ == '__main__':
    main()
