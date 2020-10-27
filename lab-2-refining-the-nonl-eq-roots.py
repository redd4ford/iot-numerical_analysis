#                                                                 #
#           Clarify the roots of the nonlinear equation           #
#         using the combined method of chords and tangents        #
#                                                                 #

from math import exp


def f(x):
    return exp(-x) - x


def df(x):
    return -1 - exp(-x)


def main():
    a = float(input('enter a: '))
    b = float(input('enter b: '))
    err = float(input('enter err(%): '))

    is_fulfilled = False
    while not is_fulfilled:
        fa = f(a)  # calculate the function value
        fb = f(b)  # at the ends of the interval

        x1 = a - fa * ((b - a) / (fb - fa))  # get x1 by the chord formula
        fx1 = f(x1)

        if fx1 * fa > 0:  # narrow the interval at one end
            a = x1
            x2 = b  # and define a preliminary approximation
        else:
            b = x1
            x2 = a

        fx2 = f(x2)
        dfx2 = df(x2)

        x2 -= fx2 / dfx2

        if a == x1:
            b = x2
        else:
            a = x2

        if abs((x1 - x2) / x1) < err:
            is_fulfilled = True

    print('x1: ' + str(x1))
    print('x2: ' + str(x2))
    print('the condition of convergence is fulfilled')
    print('the interval has been narrowed to [' + str(a) + ', ' + str(b) + ']')

    x = (x1 + x2) / 2
    print('x: ' + str(x))
    print('f(' + str(x) + '): ' + str(f(x)))


if __name__ == '__main__':
    main()
