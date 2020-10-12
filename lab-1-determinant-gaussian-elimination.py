#                                                                 #
#   Calculate the matrix determinant using Gaussian elimination   #
#              with the main matrix element selection             #
#                                                                 #


def main(A=None):
    if A is None:
        A = []
        n = int(input('Please enter the matrix dimension: '))
        for i in range(0, n):
            A.append([])

        for i in range(0, n):
            for j in range(0, n):
                row_element = float(input("A[{}][{}] = ".format(i + 1, j + 1)))
                A[i].append(row_element)
    else:
        n = len(A)

    print('Your matrix: ')
    for i in range(0, n):
        print(A[i])

    det = 1
    V = []
    C = []
    for column in range(0, n):
        V.append([])
        C.append([])

    for i in range(0, n):
        for j in range(0, n):
            V[i].append(A[i][j])

    for i in range(0, n):
        for j in range(0, n):
            if j > i:
                C[i].append(0)
            else:
                C[i].append(A[i][j])

    for k in range(0, n):
        max = abs(V[k][k])
        h = k
        w = k
        for l in range(k, n):
            for f in range(k, n):
                if max < V[l][f]:
                    max = abs(V[l][f])
                    h = l
                    w = f
        for d in range(0, n):
            value = V[k][d]
            V[k][d] = V[h][d]
            V[h][d] = value
        for d in range(0, n):
            if d < k:
                value = C[d][k]
                C[d][k] = C[d][w]
                C[d][w] = value
            else:
                value = V[d][k]
                V[d][k] = V[d][w]
                V[d][w] = value
        det = det * pow((-1), w + h) * V[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                C[k][j] = V[k][j] / V[k][k]
                V[i][j] = V[i][j] - V[i][k] * C[k][j]

    print('Determinant = ' + str(det))


if __name__ == '__main__':
    A = [
        [8.30, 2.78, 4.10, 1.90],
        [3.92, 8.45, 7.62, 2.46],
        [3.77, 7.37, 8.04, 2.28],
        [2.21, 3.49, 1.69, 6.69]
    ]
    main(A)
