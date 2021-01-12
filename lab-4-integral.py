import math


def f(x):
    return math.sqrt((1+x)/(1-x))


def F(x):
    return -math.sqrt(1 - pow(x, 2)) + math.asin(x)


def simpson(a, b, m=10):
    integral = 0
    n = 2 * m
    h = (b - a) / n
    fa = f(a)
    fb = f(b)
    for i in range(1, m):
        x = a + (2 * i - 1) * h
        integral = integral + 4 * f(x)
    for i in range(1, m - 1):
        x = a + 2 * i * h
        integral = integral + 2 * f(x)
    integral = (h / 3) * (fa + fb + integral)

    return integral


def left_rectangle(a, b, n=30):
    integral = 0
    h = (b - a) / n
    x = a

    for i in range(0, n - 1):
        integral += f(x)
        x += h
    return integral * h


def newton_leibniz(a, b):
    return F(a) - F(b)


def main():
    # 0 0.5
    a = float(input('enter a: '))
    b = float(input('enter b: '))

    print('left rectangle: ' + str(left_rectangle(a, b)))
    print('simpson: ' + str(simpson(a, b)))
    print('newton-leibniz formula: ' + str(newton_leibniz(a, b)))


if __name__ == '__main__':
    main()
